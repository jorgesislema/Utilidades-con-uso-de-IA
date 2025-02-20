import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import docx2txt
import pdfplumber
from ebooklib import epub
import textwrap
import threading

# Diccionario de idiomas soportados por gTTS y Google Translate
IDIOMAS_DISPONIBLES = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it",
    "Portugués": "pt"
}

# Tamaño máximo de caracteres por fragmento para gTTS
MAX_CHARACTERS = 4000

# --------------- Función para extraer texto de archivos sin cargar todo en memoria ---------------
def extract_text(file_path):
    """Extrae texto de archivos grandes sin sobrecargar la memoria."""
    extension = file_path.lower().split('.')[-1]
    
    try:
        if extension == 'pdf':
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text.append(page.extract_text() or "")
            return "\n".join(text)
        
        elif extension == 'epub':
            text = []
            book = epub.read_epub(file_path)
            for item in book.get_items():
                if item.get_type() == 9:  # Tipo de contenido de texto
                    text.append(item.get_content().decode('utf-8', errors='ignore'))
            return "\n".join(text)
        
        elif extension == 'docx':
            return docx2txt.process(file_path) or ""
        
        elif extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            return f"[Error] Formato no soportado: .{extension}"
    
    except Exception as e:
        return f"[Error] No se pudo procesar el archivo: {str(e)}"

# --------------- Traducción de Texto Mejorada ---------------
def traducir_texto(texto, idioma_destino="es"):
    """Traduce fragmentos grandes en partes pequeñas para evitar errores de mezcla de idiomas."""
    try:
        if idioma_destino == "auto":  # Evita traducción innecesaria
            return texto
        
        traductor = GoogleTranslator(source="auto", target=idioma_destino)
        fragmentos = textwrap.wrap(texto, MAX_CHARACTERS, break_long_words=False, replace_whitespace=False)
        texto_traducido = "\n".join([traductor.translate(frag) for frag in fragmentos])
        return texto_traducido
    except Exception as e:
        print(f"❌ Error en la traducción: {e}")
        return texto  # Devuelve el texto original si hay error

# --------------- Conversión de texto a audio optimizada con hilos ---------------
def text_to_speech(text, language, output_folder, progress_bar):
    """Convierte texto a audio de manera eficiente usando multithreading."""
    def process_audio():
        try:
            os.makedirs(output_folder, exist_ok=True)
            fragments = textwrap.wrap(text, MAX_CHARACTERS, break_long_words=False, replace_whitespace=False)
            num_fragments = len(fragments)
            
            for i, fragment in enumerate(fragments, start=1):
                progress = int((i / num_fragments) * 100)
                progress_bar["value"] = progress  # Actualiza la barra de progreso
                root.update_idletasks()

                tts = gTTS(text=fragment, lang=language, slow=False)
                output_file = os.path.join(output_folder, f"parte_{i}.mp3")
                tts.save(output_file)

            messagebox.showinfo("Éxito", f"Conversión completada. Archivos guardados en:\n{output_folder}")

        except Exception as e:
            messagebox.showerror("Error en la conversión", str(e))

        finally:
            progress_bar["value"] = 0  # Reset progress bar

    # Ejecuta en un hilo separado para no bloquear la interfaz
    threading.Thread(target=process_audio, daemon=True).start()

# --------------- Interfaz gráfica ---------------
class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traductor y Conversor de Audiolibros")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        self.file_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.source_language = tk.StringVar(value="Español")
        self.target_language = tk.StringVar(value="Español")

        # Estilos
        label_font = ("Arial", 10, "bold")

        # Selección de archivo de entrada
        tk.Label(root, text="📂 Archivo de entrada:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.file_path, width=50).pack()
        tk.Button(root, text="Seleccionar", command=self.select_file).pack(pady=2)

        # Selección de idioma de entrada
        tk.Label(root, text="🌍 Idioma del documento:", font=label_font).pack(pady=5)
        tk.OptionMenu(root, self.source_language, *IDIOMAS_DISPONIBLES.keys()).pack()

        # Selección de idioma de salida
        tk.Label(root, text="🔁 Traducir a:", font=label_font).pack(pady=5)
        tk.OptionMenu(root, self.target_language, *IDIOMAS_DISPONIBLES.keys()).pack()

        # Selección de carpeta de salida
        tk.Label(root, text="📁 Carpeta de salida:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.output_folder, width=50).pack()
        tk.Button(root, text="Seleccionar", command=self.select_output_folder).pack(pady=2)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

        # Botón de conversión
        tk.Button(root, text="🔊 Convertir a Audiolibro", command=self.convert).pack(pady=10)

    def select_file(self):
        """Abre el explorador de archivos para seleccionar un documento."""
        file_path = filedialog.askopenfilename(filetypes=[("Documentos", "*.pdf;*.docx;*.epub;*.txt")])
        if file_path:
            self.file_path.set(file_path)

    def select_output_folder(self):
        """Abre el explorador de archivos para seleccionar una carpeta de salida."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder.set(folder_path)

    def convert(self):
        """Inicia la conversión de texto a audiolibro con traducción si es necesario."""
        if not self.file_path.get() or not self.output_folder.get():
            messagebox.showwarning("Advertencia", "Selecciona un archivo de entrada y una carpeta de salida")
            return

        text = extract_text(self.file_path.get())

        if "[Error]" in text:
            messagebox.showerror("Error", text)
            return

        # Traducción solo si es necesario
        if self.source_language.get() != self.target_language.get():
            text = traducir_texto(text, IDIOMAS_DISPONIBLES[self.target_language.get()])
            if "[Error]" in text:
                messagebox.showerror("Error en la traducción", text)
                return

        text_to_speech(text, IDIOMAS_DISPONIBLES[self.target_language.get()], self.output_folder.get(), self.progress_bar)

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
