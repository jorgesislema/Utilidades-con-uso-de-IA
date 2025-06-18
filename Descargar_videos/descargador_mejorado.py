import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

class VideoDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Descargador de Videos Mejorado")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_folder_var = tk.StringVar(value='downloads')
        self.audio_var = tk.IntVar()
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Título
        title_label = tk.Label(self.root, text="🎬 Descargador de Videos", 
                              font=("Arial", 16, "bold"), fg="darkblue")
        title_label.pack(pady=10)
        
        # URL input
        url_frame = tk.Frame(self.root)
        url_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(url_frame, text="URL del video:", font=("Arial", 10, "bold")).pack(anchor='w')
        url_entry_frame = tk.Frame(url_frame)
        url_entry_frame.pack(fill='x', pady=5)
        
        self.url_entry = tk.Entry(url_entry_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side='left', fill='x', expand=True)
        
        paste_btn = tk.Button(url_entry_frame, text="📋 Pegar", command=self.paste_url)
        paste_btn.pack(side='right', padx=(5,0))
        
        # Format selection
        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=10)
        
        tk.Label(format_frame, text="Formato de descarga:", font=("Arial", 10, "bold")).pack()
        tk.Radiobutton(format_frame, text="🎥 Video completo", variable=self.audio_var, value=0).pack()
        tk.Radiobutton(format_frame, text="🎵 Solo audio (MP3)", variable=self.audio_var, value=1).pack()
        
        # Output folder
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(folder_frame, text="Carpeta de salida:", font=("Arial", 10, "bold")).pack(anchor='w')
        folder_entry_frame = tk.Frame(folder_frame)
        folder_entry_frame.pack(fill='x', pady=5)
        
        self.folder_entry = tk.Entry(folder_entry_frame, textvariable=self.output_folder_var, 
                                    state='readonly', width=50)
        self.folder_entry.pack(side='left', fill='x', expand=True)
        
        browse_btn = tk.Button(folder_entry_frame, text="📁 Buscar", command=self.browse_directory)
        browse_btn.pack(side='right', padx=(5,0))
        
        # Download button
        self.download_btn = tk.Button(self.root, text="⬇️ Descargar", command=self.start_download,
                                     font=("Arial", 12, "bold"), bg="green", fg="white",
                                     height=2, width=20)
        self.download_btn.pack(pady=20)
        
        # Progress bar
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(progress_frame, text="Progreso:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(progress_frame, text="Listo para descargar", fg="black")
        self.progress_label.pack()
        
    def paste_url(self):
        """Pega URL desde el portapapeles"""
        try:
            clipboard_content = self.root.clipboard_get()
            if self.validate_url(clipboard_content):
                self.url_var.set(clipboard_content)
            else:
                messagebox.showwarning("URL inválida", "El contenido del portapapeles no es una URL válida")
        except:
            messagebox.showwarning("Error", "No hay contenido en el portapapeles")
            
    def validate_url(self, url):
        """Valida si la URL es válida"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
        
    def browse_directory(self):
        """Selecciona carpeta de salida"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder_var.set(folder_selected)
            
    def progress_hook(self, d):
        """Hook para actualizar progreso"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = d.get('downloaded_bytes', 0) / d['total_bytes'] * 100
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                percent = d.get('downloaded_bytes', 0) / d['total_bytes_estimate'] * 100
            else:
                percent = 0
            self.progress_var.set(percent)
            self.progress_label.config(text=f"Descargando... {percent:.1f}%", fg="blue")
            self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.progress_label.config(text="✅ Descarga completada!", fg="green")
            self.download_btn.config(state="normal")
            self.root.update_idletasks()
            
    def download_video(self, url, output_path, audio_only):
        """Descarga el video o audio"""
        try:
            options = {
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
                'progress_hooks': [self.progress_hook]
            }
            
            if audio_only:
                options['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            os.makedirs(output_path, exist_ok=True)
            
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                
            messagebox.showinfo("Éxito", f"Archivo descargado en: {output_path}")
            
        except Exception as e:
            self.progress_label.config(text=f"❌ Error: {str(e)}", fg="red")
            messagebox.showerror("Error en la descarga", str(e))
            self.progress_var.set(0)
            self.download_btn.config(state="normal")
            
    def start_download(self):
        """Inicia la descarga"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL")
            return
            
        if not self.validate_url(url):
            messagebox.showerror("Error", "URL inválida")
            return
            
        output_path = self.output_folder_var.get()
        if not output_path:
            output_path = 'downloads'
            
        audio_only = self.audio_var.get() == 1
        
        self.download_btn.config(state="disabled")
        self.progress_label.config(text="Iniciando descarga...", fg="blue")
        self.progress_var.set(0)
        
        # Ejecutar descarga en hilo separado
        thread = threading.Thread(target=self.download_video, 
                                 args=(url, output_path, audio_only), 
                                 daemon=True)
        thread.start()
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VideoDownloader()
    app.run()
