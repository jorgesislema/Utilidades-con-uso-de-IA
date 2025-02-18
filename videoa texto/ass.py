import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import json
import spacy
import language_tool_python
from keybert import KeyBERT
from transformers import pipeline

class TranscriptorApp:
    def __init__(self, master):
        """Inicializa la aplicación y carga los modelos necesarios"""
        self.master = master
        self.master.title("Transcriptor Avanzado de Video a Texto")
        self.master.geometry("600x450")
        
        # Configuración de modelos
        self.MODELO_VOSK = self.cargar_modelo_vosk()
        if not self.MODELO_VOSK:
            messagebox.showerror("Error", "No se encontró el modelo Vosk en la ruta especificada.")
            exit()
        
        self.nlp = spacy.load("es_core_news_sm")  # Carga el modelo de procesamiento de lenguaje en español
        self.kw_model = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')  # Carga el modelo para extraer palabras clave
        
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        except Exception:
            messagebox.showwarning("Advertencia", "No se pudo cargar el modelo de resumen. Se omitirá esta función.")
            self.summarizer = None
        
        self.crear_interfaz()
        self.configurar_ffmpeg()

    def configurar_ffmpeg(self):
        """Configura la ubicación de FFmpeg para la manipulación de audio"""
        ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'  # Ruta del ejecutable FFmpeg
        if os.path.exists(ffmpeg_path):
            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffprobe = ffmpeg_path.replace('ffmpeg', 'ffprobe')

    def cargar_modelo_vosk(self):
        """Carga el modelo de Vosk para el reconocimiento de voz"""
        models_path = r"H:/git/Utilidades diarias/Utilidades_para_el_dia_a_dia/videoa texto/vosk-model-es-0.42"
        if not os.path.exists(models_path):
            return None
        return Model(models_path)

    def crear_interfaz(self):
        """Crea la interfaz gráfica con Tkinter"""
        frame = ttk.Frame(self.master, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Selector de archivo de video
        ttk.Label(frame, text="Archivo de video:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_video = ttk.Entry(frame, width=50)
        self.entrada_video.grid(row=0, column=1)
        ttk.Button(frame, text="Seleccionar", command=self.seleccionar_video).grid(row=0, column=2)

        # Selector de carpeta de salida
        ttk.Label(frame, text="Carpeta de salida:").grid(row=1, column=0, sticky=tk.W)
        self.entrada_carpeta = ttk.Entry(frame, width=50)
        self.entrada_carpeta.grid(row=1, column=1)
        ttk.Button(frame, text="Seleccionar", command=self.seleccionar_carpeta).grid(row=1, column=2)

        # Nombre del archivo de salida
        ttk.Label(frame, text="Nombre del archivo:").grid(row=2, column=0, sticky=tk.W)
        self.entrada_nombre = ttk.Entry(frame)
        self.entrada_nombre.grid(row=2, column=1, sticky=tk.EW)

        # Barra de progreso
        self.progress = ttk.Progressbar(frame, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=tk.EW, pady=10)

        ttk.Button(frame, text="Iniciar Proceso", command=self.iniciar_proceso).grid(row=4, column=0, columnspan=3)

    def seleccionar_video(self):
        """Abre un cuadro de diálogo para seleccionar un archivo de video"""
        archivo = filedialog.askopenfilename(title="Seleccionar video", filetypes=[("Archivos multimedia", "*.mp4 *.avi *.mkv *.mov")])
        if archivo:
            self.entrada_video.delete(0, tk.END)
            self.entrada_video.insert(0, archivo)

    def seleccionar_carpeta(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta de salida"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if carpeta:
            self.entrada_carpeta.delete(0, tk.END)
            self.entrada_carpeta.insert(0, carpeta)

    def actualizar_progreso(self, valor: float):
        """Actualiza la barra de progreso"""
        self.progress['value'] = valor
        self.master.update_idletasks()

    def validar_entradas(self) -> bool:
        """Verifica que todos los campos obligatorios estén llenos"""
        return all([self.entrada_video.get(), self.entrada_carpeta.get(), self.entrada_nombre.get()])

    def iniciar_proceso(self):
        """Inicia el proceso de transcripción en un hilo separado"""
        if not self.validar_entradas():
            messagebox.showwarning("Campos incompletos", "Por favor, rellena todos los campos antes de continuar.")
            return
        
        video_path = self.entrada_video.get()
        carpeta_salida = self.entrada_carpeta.get()
        nombre_archivo = self.entrada_nombre.get()
        
        Thread(target=self.ejecutar_proceso, args=(video_path, carpeta_salida, nombre_archivo), daemon=True).start()

    def ejecutar_proceso(self, video_path: str, carpeta_salida: str, nombre_archivo: str):
        """Ejecuta el proceso de transcripción"""
        audio_path = os.path.join(carpeta_salida, "audio_temp.wav")
        if not self.extraer_audio(video_path, audio_path):
            return
        
        texto = self.procesar_audio(audio_path)
        texto_corregido = self.corregir_texto(texto)
        contenido = self.generar_documento(texto_corregido)
        
        archivo_salida = os.path.join(carpeta_salida, f"{nombre_archivo}.txt")
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        messagebox.showinfo("Éxito", f"Archivo guardado en: {archivo_salida}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        self.actualizar_progreso(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptorApp(root)
    root.mainloop()

