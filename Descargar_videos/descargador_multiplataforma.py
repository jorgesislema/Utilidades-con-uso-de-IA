import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from datetime import datetime
import shutil

# Dependencia principal
try:
    import yt_dlp
except ModuleNotFoundError:
    messagebox.showerror("Dependencia faltante", "No se encontró 'yt-dlp'. Instálalo con:\npython -m pip install yt-dlp")
    raise

# Tema moderno opcional (ttkbootstrap)
try:
    import ttkbootstrap as tb  # type: ignore
except Exception:
    tb = None

# Plataformas comunes soportadas por yt-dlp (no exhaustivo)
PLATAFORMAS = [
    ("YouTube", "youtube.com|youtu.be"),
    ("TikTok", "tiktok.com"),
    ("Facebook", "facebook.com|fb.watch"),
    ("Instagram", "instagram.com"),
    ("X (Twitter)", "twitter.com|x.com"),
    ("Reddit", "reddit.com|redd.it"),
    ("Vimeo", "vimeo.com"),
    ("Twitch", "twitch.tv"),
    ("Dailymotion", "dailymotion.com|dai.ly"),
    ("Bilibili", "bilibili.com"),
    ("SoundCloud", "soundcloud.com"),
]

# Perfiles de formato
FORMATOS = {
    "Video 1080p (mp4)": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "Video 720p (mp4)": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best",
    "Video 480p (mp4)": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best",
    "Solo audio (mp3)": "bestaudio/best",
    "Solo audio (m4a)": "bestaudio[ext=m4a]/bestaudio/best",
    "Subtítulos (si hay)": "best",
}

AUDIO_POST = {
    "Solo audio (mp3)": {
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    },
    "Solo audio (m4a)": {
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "192",
        }]
    },
}

class DescargadorMultiplataforma:
    def __init__(self):
        # Usar ttkbootstrap si está disponible
        if tb is not None:
            try:
                self.root = tb.Window(themename="darkly")
            except Exception:
                self.root = tk.Tk()
        else:
            self.root = tk.Tk()
        self.root.title("Descargador Multiplataforma")
        self.root.geometry("760x560")
        self.root.resizable(False, False)
        self.url_var = tk.StringVar()
        self.output_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        self.formato_var = tk.StringVar(value=list(FORMATOS.keys())[0])
        self.plataforma_var = tk.StringVar(value=PLATAFORMAS[0][0])
        self.cookies_path = tk.StringVar(value="")
        self.cookies_browser = tk.StringVar(value="Ninguno")
        self.subs_var = tk.BooleanVar(value=False)
        self.embed_subs_var = tk.BooleanVar(value=True)
        self.embed_thumbnail_var = tk.BooleanVar(value=False)
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="Listo")

        self._build_ui()

        # Chequeo rápido de ffmpeg/ffprobe
        self.ffmpeg_path = shutil.which("ffmpeg")
        self.ffprobe_path = shutil.which("ffprobe")
        if not self.ffmpeg_path or not self.ffprobe_path:
            self.status_var.set("⚠️ ffmpeg/ffprobe no detectado. Algunas funciones (mezcla/MP3/M4A/embeds) pueden fallar.")
            try:
                messagebox.showwarning(
                    "ffmpeg no detectado",
                    "No se encontró ffmpeg/ffprobe en PATH.\n\nRecomendado: instalar builds de ffmpeg para yt-dlp (Windows):\nhttps://github.com/yt-dlp/FFmpeg-Builds\n\nPuedes continuar, pero las conversiones y embeddings pueden fallar."
                )
            except Exception:
                pass

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        # Título
        title = tk.Label(self.root, text="🎬 Descargador Multiplataforma", font=("Segoe UI", 18, "bold"), fg="#0b5ed7")
        title.pack(pady=(14, 6))

        # URL + Pegar
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill="x", **pad)
        tk.Label(url_frame, text="URL:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        row = tk.Frame(url_frame)
        row.pack(fill="x")
        self.url_entry = tk.Entry(row, textvariable=self.url_var, font=("Consolas", 10))
        self.url_entry.pack(side="left", fill="x", expand=True)
        tk.Button(row, text="📋 Pegar", command=self._paste).pack(side="left", padx=6)

        # Plataforma + Formato
        pf = tk.Frame(self.root)
        pf.pack(fill="x", **pad)
        left = tk.Frame(pf)
        left.pack(side="left", expand=True, fill="x")
        right = tk.Frame(pf)
        right.pack(side="left", expand=True, fill="x")

        tk.Label(left, text="Plataforma:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.plataforma_combo = ttk.Combobox(left, values=[p[0] for p in PLATAFORMAS], state="readonly", textvariable=self.plataforma_var)
        self.plataforma_combo.pack(fill="x")

        tk.Label(right, text="Formato:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.formato_combo = ttk.Combobox(right, values=list(FORMATOS.keys()), state="readonly", textvariable=self.formato_var)
        self.formato_combo.pack(fill="x")

        # Opciones avanzadas
        adv = tk.LabelFrame(self.root, text="Opciones avanzadas")
        adv.pack(fill="x", **pad)
        row1 = tk.Frame(adv)
        row1.pack(fill="x", pady=4)
        tk.Checkbutton(row1, text="Descargar subtítulos (si disponibles)", variable=self.subs_var).pack(side="left")
        tk.Checkbutton(row1, text="Incrustar subtítulos en video", variable=self.embed_subs_var).pack(side="left", padx=10)
        tk.Checkbutton(row1, text="Incrustar miniatura (audio)", variable=self.embed_thumbnail_var).pack(side="left")

        row2 = tk.Frame(adv)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text="Cookies.txt (opcional):").pack(side="left")
        tk.Entry(row2, textvariable=self.cookies_path, width=40).pack(side="left", padx=6)
        tk.Button(row2, text="📁", command=self._choose_cookies).pack(side="left", padx=(0,8))
        tk.Label(row2, text="o del navegador:").pack(side="left")
        self.browser_combo = ttk.Combobox(row2, values=["Ninguno", "Chrome", "Edge", "Firefox"], state="readonly", width=10, textvariable=self.cookies_browser)
        self.browser_combo.pack(side="left")

        # Carpeta salida
        out = tk.Frame(self.root)
        out.pack(fill="x", **pad)
        tk.Label(out, text="Carpeta de salida:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        rowo = tk.Frame(out)
        rowo.pack(fill="x")
        tk.Entry(rowo, textvariable=self.output_var).pack(side="left", fill="x", expand=True)
        tk.Button(rowo, text="📁 Cambiar", command=self._choose_folder).pack(side="left", padx=6)

        # Acciones
        actions = tk.Frame(self.root)
        actions.pack(pady=8)
        self.download_btn = tk.Button(actions, text="⬇️ Descargar", command=self._start, bg="#198754", fg="white", font=("Segoe UI", 11, "bold"), width=18, height=1)
        self.download_btn.pack(side="left", padx=6)
        tk.Button(actions, text="❌ Cancelar", command=self._cancel, bg="#dc3545", fg="white", font=("Segoe UI", 11), width=12).pack(side="left", padx=6)

        # Progreso
        prog = tk.Frame(self.root)
        prog.pack(fill="x", **pad)
        tk.Label(prog, text="Progreso:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.progress_bar = ttk.Progressbar(prog, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x")
        self.status = tk.Label(prog, textvariable=self.status_var, anchor="w")
        self.status.pack(fill="x", pady=4)

    def _paste(self):
        try:
            s = self.root.clipboard_get()
            self.url_var.set(s)
            # Autodetectar plataforma por URL
            for nombre, patron in PLATAFORMAS:
                if re.search(patron, s, flags=re.IGNORECASE):
                    self.plataforma_var.set(nombre)
                    break
        except Exception:
            messagebox.showwarning("Portapapeles", "No se pudo leer el portapapeles")

    def _choose_cookies(self):
        p = filedialog.askopenfilename(title="Selecciona cookies.txt", filetypes=[("Cookies", "*.txt"), ("Todos", "*.*")])
        if p:
            self.cookies_path.set(p)

    def _choose_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.output_var.set(p)

    def _progress(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total else 0
            self.progress_var.set(percent)
            spd = d.get('speed')
            eta = d.get('eta')
            spd_txt = f" | {spd/1024/1024:.2f} MB/s" if spd else ""
            eta_txt = f" | ETA: {eta}s" if eta else ""
            self.status_var.set(f"Descargando... {percent:.1f}%{spd_txt}{eta_txt}")
            self.root.update_idletasks()
        elif d.get('status') == 'finished':
            self.progress_var.set(100)
            self.status_var.set("Procesando archivo...")
            self.root.update_idletasks()

    def _build_opts(self):
        fmt = FORMATOS[self.formato_var.get()]
        opts = {
            'outtmpl': os.path.join(self.output_var.get(), '%(title)s.%(ext)s'),
            'format': fmt,
            'noprogress': True,
            'progress_hooks': [self._progress],
            'concurrent_fragment_downloads': 5,
            'retries': 5,
            'fragment_retries': 5,
            'ignoreerrors': False,
        }
        if self.subs_var.get():
            opts.update({
                'writesubtitles': True,
                'subtitleslangs': ['es', 'en', 'original'],
                'subtitlesformat': 'srt/best',
            })
        # Incrustar subtítulos (si formato produce contenedor compatible)
        if self.embed_subs_var.get():
            opts.setdefault('postprocessors', [])
            opts['postprocessors'].append({'key': 'FFmpegEmbedSubtitle'})
        # Audio: extraer a mp3/m4a si corresponde
        if self.formato_var.get() in AUDIO_POST:
            opts.setdefault('postprocessors', [])
            opts['postprocessors'] += AUDIO_POST[self.formato_var.get()]['postprocessors']
            if self.embed_thumbnail_var.get():
                opts['postprocessors'].append({'key': 'EmbedThumbnail'})
                opts['writethumbnail'] = True
        # Manejo de cookies
        if self.cookies_path.get():
            # cookies desde archivo
            opts['cookiesfrombrowser'] = None
            opts['cookiefile'] = self.cookies_path.get()
        else:
            # cookies desde navegador si se selecciona
            browser = self.cookies_browser.get().lower()
            if browser in ("chrome", "edge", "firefox"):
                # yt-dlp acepta: (BROWSER[,KEYRING[,PROFILE[,CONTAINER]]])
                # Pasamos simplemente el nombre del navegador
                opts['cookiesfrombrowser'] = (browser, )
        return opts

    def _worker(self, url):
        try:
            os.makedirs(self.output_var.get(), exist_ok=True)
            with yt_dlp.YoutubeDL(self._build_opts()) as ydl:
                ydl.download([url])
            self.status_var.set("✅ Descarga completada")
            messagebox.showinfo("Éxito", f"Archivo descargado en:\n{self.output_var.get()}")
        except Exception as e:
            self.status_var.set(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.download_btn.config(state="normal")
            self.progress_var.set(0)

    def _start(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Validación", "Ingresa una URL")
            return
        if not re.match(r'^https?://', url, flags=re.IGNORECASE):
            messagebox.showerror("Validación", "La URL debe iniciar con http(s)://")
            return
        self.download_btn.config(state="disabled")
        self.status_var.set("Preparando descarga...")
        t = threading.Thread(target=self._worker, args=(url,), daemon=True)
        t.start()

    def _cancel(self):
        messagebox.showinfo("Cancelar", "La cancelación en caliente no está soportada por yt-dlp. Cierra la ventana para abortar.")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = DescargadorMultiplataforma()
    app.run()
