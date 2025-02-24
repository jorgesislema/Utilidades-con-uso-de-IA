import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pydub import AudioSegment
import whisper
import torch
from transformers import pipeline

class VideoToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcriptor IA - Video a Texto")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f4f4f4')

        # Configuramos el modelo Whisper con detección automática de hardware
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model("small", device=self.device)  

        # Cargar el modelo de resumen BART de Hugging Face
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        self.setup_ui()

    def setup_ui(self):
        """Interfaz gráfica mejorada"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(main_frame, text="Transcriptor IA - Video a Texto", font=('Arial', 16, 'bold')).pack(pady=10)

        # Selección de archivo local
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Archivo de video:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        self.file_entry = ttk.Entry(file_frame, width=50, font=('Arial', 10))
        self.file_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.browse_button = ttk.Button(file_frame, text="Seleccionar", command=self.select_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # Botón para iniciar la transcripción
        self.process_btn = ttk.Button(main_frame, text="Iniciar Transcripción", command=self.process_local_file, style='Accent.TButton')
        self.process_btn.pack(pady=10)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=600, mode='determinate')
        self.progress_bar.pack(pady=15)

        # Estado
        self.status_label = ttk.Label(main_frame, text="Listo para comenzar", foreground='#2c3e50', font=('Arial', 12))
        self.status_label.pack(pady=10)

    def select_file(self):
        """Seleccionar un archivo de video local"""
        file_path = filedialog.askopenfilename(title="Seleccionar video", filetypes=[("Archivos multimedia", "*.mp4 *.avi *.mkv *.mov")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def process_local_file(self):
        """Procesa un archivo de video local en un hilo separado"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor selecciona un archivo")
            return
        threading.Thread(target=self.process_transcription, args=(file_path,), daemon=True).start()

    def extract_audio(self, video_path):
        """Convierte un video en un archivo de audio WAV"""
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        self.status_label.config(text="Extrayendo audio...")
        self.root.update_idletasks()
        try:
            audio = AudioSegment.from_file(video_path)
            audio.export(audio_path, format="wav")
            return audio_path
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo extraer el audio: {e}")
            return None

    def process_transcription(self, video_path):
        """Realiza la transcripción del video seleccionado con feedback visual"""
        self.process_btn["state"] = "disabled"
        self.progress_bar["value"] = 10
        self.root.update_idletasks()

        audio_path = self.extract_audio(video_path)
        if not audio_path:
            self.process_btn["state"] = "normal"
            return

        self.status_label.config(text="Transcribiendo con Whisper AI...")
        self.progress_bar["value"] = 50
        self.root.update_idletasks()

        result = self.model.transcribe(audio_path)
        transcription_text = result["text"]

        self.progress_bar["value"] = 80
        self.root.update_idletasks()

        # Manejo de errores en la generación de resúmenes
        summary = ""
        if transcription_text.strip():
            try:
                self.status_label.config(text="Resumiendo transcripción...")
                summary = self.summarizer(transcription_text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            except Exception as e:
                summary = "No se pudo generar el resumen. Error: " + str(e)

        text_output = os.path.splitext(video_path)[0] + "_transcrito.txt"
        with open(text_output, "w", encoding="utf-8") as f:
            f.write("TRANSCRIPCIÓN:\n" + transcription_text + "\n\nRESUMEN:\n" + summary)

        self.progress_bar["value"] = 100
        self.status_label.config(text="¡Transcripción y resumen completados!")
        messagebox.showinfo("Éxito", f"Transcripción guardada en {text_output}")
        self.process_btn["state"] = "normal"
        self.progress_bar["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToTextApp(root)
    root.mainloop()
