import os
import yt_dlp
import whisper
import requests
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tqdm import tqdm
import threading

def download_video(url, output_path='downloads', audio_only=False, progress_callback=None):
    """Descarga un video o audio de múltiples plataformas con barra de progreso."""
    options = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if audio_only else [],
        'progress_hooks': [progress_callback] if progress_callback else []
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    print("Descarga completada!")
    progress_var.set(100)  # Asegurar que la barra de progreso llegue al 100%
    progress_label.config(text="Descarga completada!", fg="green")
    root.update_idletasks()

def enhance_audio(file_path):
    """Mejora la calidad del audio usando Whisper AI."""
    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    print("Transcripción de audio:")
    print(result['text'])

def browse_directory():
    folder_selected = filedialog.askdirectory()
    return folder_selected if folder_selected else 'downloads'

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / max(d.get('total_bytes', 1), 1) * 100
        progress_var.set(percent)
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress_var.set(100)
        progress_label.config(text="Descarga completada!", fg="green")
        root.update_idletasks()

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida.")
        return
    
    output_path = browse_directory()
    choice = audio_var.get()
    audio_only = choice == 1
    
    progress_label.config(text="Descargando...", fg="blue")
    root.update()
    
    threading.Thread(target=download_video, args=(url, output_path, audio_only, progress_hook), daemon=True).start()

def gui():
    global root, url_entry, audio_var, progress_label, progress_var
    root = tk.Tk()
    root.title("Descargador de Videos")
    root.geometry("500x300")
    
    tk.Label(root, text="Ingresa la URL del video:").pack(pady=5)
    url_entry = tk.Entry(root, width=60)
    url_entry.pack(pady=5)
    
    tk.Label(root, text="Selecciona el formato:").pack(pady=5)
    audio_var = tk.IntVar()
    tk.Radiobutton(root, text="Video", variable=audio_var, value=0).pack()
    tk.Radiobutton(root, text="Solo Audio", variable=audio_var, value=1).pack()
    
    tk.Button(root, text="Seleccionar Carpeta", command=browse_directory).pack(pady=5)
    tk.Button(root, text="Descargar", command=start_download).pack(pady=10)
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress_bar.pack(pady=10)
    
    progress_label = tk.Label(root, text="", fg="black")
    progress_label.pack()
    
    root.mainloop()

if __name__ == "__main__":
    gui()
