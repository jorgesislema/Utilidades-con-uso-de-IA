import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import torch
from utils_video2text import extract_audio, transcribe_audio, resumir_texto, guardar_resultado

class Video2TextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video a Texto y Resumen")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.output_format = tk.StringVar(value="txt")

        label_font = ("Arial", 10, "bold")

        tk.Label(root, text="🎬 Archivo de video:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.video_path, width=60).pack()
        tk.Button(root, text="Seleccionar", command=self.select_video).pack(pady=2)

        tk.Label(root, text="📁 Carpeta de salida:", font=label_font).pack(pady=5)
        tk.Entry(root, textvariable=self.output_folder, width=60).pack()
        tk.Button(root, text="Seleccionar", command=self.select_output_folder).pack(pady=2)

        tk.Label(root, text="💾 Formato de salida:", font=label_font).pack(pady=5)
        tk.OptionMenu(root, self.output_format, "txt", "pdf", "docx").pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
        self.progress_bar.pack(pady=10)

        tk.Button(root, text="📝 Transcribir y Resumir", command=self.process).pack(pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4;*.mkv;*.avi;*.mov;*.flv;*.wmv")])
        if file_path:
            self.video_path.set(file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder.set(folder_path)

    def process(self):
        if not self.video_path.get() or not self.output_folder.get():
            messagebox.showwarning("Advertencia", "Selecciona un archivo de video y una carpeta de salida")
            return
        self.progress_bar["value"] = 5
        self.root.update_idletasks()
        audio_path = extract_audio(self.video_path.get())
        if isinstance(audio_path, str) and audio_path.startswith("[Error]"):
            messagebox.showerror("Error", audio_path)
            return
        self.progress_bar["value"] = 25
        self.root.update_idletasks()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        texto = transcribe_audio(audio_path, device=device)
        if isinstance(texto, str) and texto.startswith("[Error]"):
            messagebox.showerror("Error", texto)
            return
        self.progress_bar["value"] = 60
        self.root.update_idletasks()
        resumen = resumir_texto(texto)
        if isinstance(resumen, str) and resumen.startswith("[Error]"):
            resumen = "(No se pudo generar resumen)"
        texto_final = f"TRANSCRIPCIÓN COMPLETA:\n{texto}\n\nRESUMEN:\n{resumen}\n"
        nombre_archivo = os.path.splitext(os.path.basename(self.video_path.get()))[0] + "_TRANSCRIPCION"
        resultado = guardar_resultado(texto_final, nombre_archivo, self.output_format.get(), self.output_folder.get())
        self.progress_bar["value"] = 100
        self.root.update_idletasks()
        if isinstance(resultado, str) and resultado.startswith("[Error]"):
            messagebox.showerror("Error", resultado)
        else:
            messagebox.showinfo("Éxito", f"Archivo guardado en: {resultado}")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        self.progress_bar["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = Video2TextApp(root)
    root.mainloop()
