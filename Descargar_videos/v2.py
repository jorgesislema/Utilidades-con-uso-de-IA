import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import yt_dlp
import whisper

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.download_queue = queue.Queue()
        self.running = False
        self.whisper_model = None
        
        self.process_queue()

    def setup_ui(self):
        self.root.title("Descargador Avanzado de Medios")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="URL del video:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, pady=5)

        self.format_var = tk.StringVar(value='video')
        ttk.Radiobutton(main_frame, text="Video", variable=self.format_var, value='video').grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="Audio", variable=self.format_var, value='audio').grid(row=1, column=2, sticky=tk.W)

        self.transcribe_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Transcribir audio", variable=self.transcribe_var).grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)

        ttk.Button(main_frame, text="Seleccionar carpeta", command=self.select_directory).grid(row=3, column=1, pady=10)
        self.download_btn = ttk.Button(main_frame, text="Descargar", command=self.start_download)
        self.download_btn.grid(row=3, column=2, pady=10)
        
        self.progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

        self.status_label = ttk.Label(main_frame, text="Listo")
        self.status_label.grid(row=5, column=0, columnspan=3)

        self.output_path = os.path.expanduser("~/Downloads")
        
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path = directory

    def start_download(self):
        if self.running:
            messagebox.showwarning("Advertencia", "Ya hay una descarga en curso")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida")
            return

        self.running = True
        self.download_btn['state'] = 'disabled'
        self.status_label.config(text="Iniciando descarga...")
        
        options = {
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noplaylist': False  # Permitir listas de reproducción
        }

        if self.format_var.get() == 'audio':
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        threading.Thread(
            target=self.download_video,
            args=(url, options, self.transcribe_var.get()),
            daemon=True
        ).start()

    def download_video(self, url, options, transcribe):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info:
                    filenames = [ydl.prepare_filename(entry) for entry in info['entries']]
                else:
                    filenames = [ydl.prepare_filename(info)]

                if options.get('postprocessors'):
                    filenames = [os.path.splitext(f)[0] + '.mp3' for f in filenames]

            self.download_queue.put(('success', filenames))
            
            if transcribe and self.format_var.get() == 'audio':
                for file in filenames:
                    self.download_queue.put(('transcribe_start', file))
                    self.transcribe_audio(file)
                
        except Exception as e:
            self.download_queue.put(('error', str(e)))
        finally:
            self.download_queue.put(('done', None))

    def transcribe_audio(self, file_path):
        try:
            if not os.path.exists(file_path):
                self.download_queue.put(('error', f"Archivo no encontrado: {file_path}"))
                return

            if not self.whisper_model:
                self.download_queue.put(('status', "Cargando modelo Whisper..."))
                self.whisper_model = whisper.load_model("base")
                
            self.download_queue.put(('status', "Transcribiendo audio..."))
            result = self.whisper_model.transcribe(file_path)
            
            output_file = os.path.splitext(file_path)[0] + '_transcripcion.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            
            self.download_queue.put(('transcribe_done', output_file))
        except Exception as e:
            self.download_queue.put(('error', f"Error en transcripción: {str(e)}"))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            percent_clean = re.sub(r'\x1b\[.*?m', '', percent_str).strip('%')
            try:
                self.download_queue.put(('progress', float(percent_clean)))
            except ValueError:
                self.download_queue.put(('progress', 0))

    def process_queue(self):
        try:
            while True:
                task = self.download_queue.get_nowait()
                action, value = task
                
                if action == 'progress':
                    self.progress_bar['value'] = value
                elif action == 'status':
                    self.status_label.config(text=value)
                elif action == 'success':
                    messagebox.showinfo("Éxito", f"Descarga completada: {', '.join(value)}")
                elif action == 'transcribe_done':
                    messagebox.showinfo("Transcripción lista", f"Transcripción guardada en:{value}")
                elif action == 'error':
                    messagebox.showerror("Error", value)
                elif action == 'done':
                    self.running = False
                    self.download_btn['state'] = 'normal'
                    self.progress_bar['value'] = 0
                    self.status_label.config(text="Listo")
                
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
