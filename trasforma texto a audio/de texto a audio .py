# Librerias
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from utils_archivos import extract_text
from utils_traduccion import traducir_texto
from utils_tts import text_to_speech
import os
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

# Interfaz gráfica 
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

        # Selecciona el idioma de entrada
        tk.Label(root, text="📂 Archivo de entrada:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.file_path, width=50).pack()
        tk.Button(root, text="Seleccionar", command=self.select_file).pack(pady=2)

        # Selección de idioma de entrada
        tk.Label(root, text="🌍 Idioma del documento:", font=label_font).pack(pady=5)
        tk.OptionMenu(root, self.source_language, *IDIOMAS_DISPONIBLES.keys()).pack()

        # # Selecciona el  idioma de salida
        tk.Label(root, text="🔁 Traducir a:", font=label_font).pack(pady=5)
        tk.OptionMenu(root, self.target_language, *IDIOMAS_DISPONIBLES.keys()).pack()

        # Selecciona la carpeta de salida
        tk.Label(root, text="📁 Carpeta de salida:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.output_folder, width=50).pack()
        tk.Button(root, text="Seleccionar", command=self.select_output_folder).pack(pady=2)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

        # Botón de conversión
        tk.Button(root, text="🔊 Convertir a Audiolibro", command=self.convert).pack(pady=10)

        # Botón para cancelar la conversión
        self.cancel_btn = tk.Button(root, text="❌ Cancelar conversión", command=self.cancel_conversion, state="disabled")
        self.cancel_btn.pack(pady=2)

    #Función para abrir el explorador de archivos para seleccionar un documento
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Documentos", "*.pdf;*.docx;*.epub;*.txt")])
        if file_path:
            self.file_path.set(file_path)

    #Función para abrir el explorador de archivos para seleccionar una carpeta de salida
    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder.set(folder_path)

    def cancel_conversion(self):
        self.root.cancelar_conversion = True
        self.cancel_btn.config(state="disabled")

    #Función para iniciar la conversión de texto a audiolibro con traducción si es necesario.
    def convert(self):
        if not self.file_path.get() or not self.output_folder.get():
            messagebox.showwarning("Advertencia", "Selecciona un archivo de entrada y una carpeta de salida")
            return

        self.root.cancelar_conversion = False
        self.cancel_btn.config(state="normal")

        text = extract_text(self.file_path.get())
        if text.startswith("[Error]"):
            messagebox.showerror("Error", text)
            self.cancel_btn.config(state="disabled")
            return

        if self.source_language.get() != self.target_language.get():
            text = traducir_texto(text, IDIOMAS_DISPONIBLES[self.target_language.get()])
            if text.startswith("[Error]"):
                messagebox.showerror("Error en la traducción", text)
                self.cancel_btn.config(state="disabled")
                return

        def finalizar_conversion():
            self.cancel_btn.config(state="disabled")
        # Llama a text_to_speech y deshabilita el botón cancelar al finalizar
        threading.Thread(target=lambda: (text_to_speech(text, IDIOMAS_DISPONIBLES[self.target_language.get()], self.output_folder.get(), self.progress_bar, self.root), finalizar_conversion()), daemon=True).start()

# Ejecutamos la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
