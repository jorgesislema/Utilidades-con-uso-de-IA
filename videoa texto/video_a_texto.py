import os
import re
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import yt_dlp
from vosk import Model, KaldiRecognizer
import wave
import json
from googletrans import Translator
from PIL import Image, ImageTk


class VideoDownloaderPro:
    def __init__(self, root):
        self.root = root

        # Definir modelos antes de la UI para evitar el error
        self.modelos = {
            'español': 'vosk-model-small-es-0.42',
            'inglés': 'vosk-model-small-en-us-0.15',
            'francés': 'vosk-model-small-fr-0.22'
        }
        
        self.translator = Translator()
        self.current_model = None
        self.output_path = os.path.expanduser("~/Downloads")
        self.running = False
        self.download_queue = queue.Queue()

        self.setup_ui()
        self.process_queue()

        # Cargar iconos
        self.load_icons()

    def load_icons(self):
        try:
            self.folder_icon = ImageTk.PhotoImage(Image.open("folder_icon.png").resize((20, 20)))
            self.download_icon = ImageTk.PhotoImage(Image.open("download_icon.png").resize((20, 20)))
        except:
            self.folder_icon = "📁"
            self.download_icon = "⏬"

    def setup_ui(self):
        self.root.title("Descargador y Transcriptor de Videos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(main_frame, text="Descargador Multimedia", font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=10, columnspan=3)

        # Configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración")
        config_frame.grid(row=1, column=0, pady=10, columnspan=3, sticky='ew')

        ttk.Label(config_frame, text="URL del video:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.url_entry = ttk.Entry(config_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, sticky='ew')

        # Selector de formato
        self.format_var = tk.StringVar(value='video')
        ttk.Radiobutton(config_frame, text="Video MP4", variable=self.format_var, value='video').grid(row=1, column=1, padx=5, sticky='w')
        ttk.Radiobutton(config_frame, text="Audio MP3", variable=self.format_var, value='audio').grid(row=1, column=2, padx=5, sticky='w')

        # Selector de idioma
        ttk.Label(config_frame, text="Idioma del audio:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.lang_var = tk.StringVar(value='español')
        self.lang_combobox = ttk.Combobox(config_frame, textvariable=self.lang_var, values=list(self.modelos.keys()))
        self.lang_combobox.grid(row=2, column=1, padx=5, sticky='ew')

        # Opciones de traducción
        self.translate_var = tk.BooleanVar()
        self.translate_check = ttk.Checkbutton(config_frame, text="Traducir a español", variable=self.translate_var)
        self.translate_check.grid(row=2, column=2, padx=5, sticky='w')

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=15, columnspan=3)

        ttk.Button(button_frame, text="Seleccionar Carpeta", command=self.select_directory).pack(side=tk.LEFT, padx=5)
        self.download_btn = ttk.Button(button_frame, text="Iniciar Descarga", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=600, mode='determinate')
        self.progress_bar.grid(row=4, column=0, pady=15, columnspan=3)

        # Estado
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, pady=10, columnspan=3, sticky='ew')

        self.status_label = ttk.Label(status_frame, text="Listo para comenzar", foreground='#2c3e50')
        self.status_label.pack(side=tk.LEFT)

        self.time_label = ttk.Label(status_frame, text="Tiempo transcurrido: 00:00:00")
        self.time_label.pack(side=tk.RIGHT)

        self.root.bind('<Return>', lambda event: self.start_download())

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path = directory
            self.status_label.config(text=f"Carpeta seleccionada: {directory}")

    def start_download(self):
        if self.running:
            messagebox.showwarning("Advertencia", "Ya hay una operación en curso")
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida")
            return

        self.running = True
        self.download_btn['state'] = 'disabled'
        self.start_time = time.time()

        options = {
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noplaylist': True
        }

        if self.format_var.get() == 'audio':
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '256'}],
            })

        threading.Thread(target=self.process_download, args=(url, options), daemon=True).start()
        self.update_timer()

    def process_download(self, url, options):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                if options.get('postprocessors'):
                    filename = os.path.splitext(filename)[0] + '.mp3'

            self.download_queue.put(('success', filename))
            self.process_transcription(filename)

        except Exception as e:
            self.download_queue.put(('error', f"Error en descarga: {str(e)}"))
        finally:
            self.download_queue.put(('done', None))

    def process_transcription(self, filename):
        if self.format_var.get() == 'audio':
            self.download_queue.put(('status', "Iniciando transcripción..."))
            transcript = self.transcribe_audio(filename)

            if self.translate_var.get():
                self.download_queue.put(('status', "Traduciendo contenido..."))
                translated = self.translate_text(transcript)
                self.save_file(filename, translated, '_traducido.txt')
            else:
                self.save_file(filename, transcript, '_transcrito.txt')

    def transcribe_audio(self, file_path):
        try:
            wf = wave.open(file_path, 'rb')
            recognizer = KaldiRecognizer(self.current_model, wf.getframerate())

            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    results.append(result.get('text', ''))

            return ' '.join(results)

        except Exception as e:
            self.download_queue.put(('error', f"Error en transcripción: {str(e)}"))
            return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderPro(root)
    root.mainloop()
