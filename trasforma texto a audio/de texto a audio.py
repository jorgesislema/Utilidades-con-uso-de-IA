import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from gtts import gTTS
import pygame
from docx import Document
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup

# Inicializar pygame para el reproductor de audio
pygame.init()
pygame.mixer.init()

# Variables globales
audio_en_reproduccion = False
archivo_actual = None

def leer_archivo(ruta_archivo):
    """Lee el contenido de archivos TXT, DOCX, PDF o EPUB."""
    try:
        if ruta_archivo.endswith(".txt"):
            with open(ruta_archivo, "r", encoding="utf-8") as file:
                return file.read()
        elif ruta_archivo.endswith(".docx"):
            doc = Document(ruta_archivo)
            return "\n".join([p.text for p in doc.paragraphs])
        elif ruta_archivo.endswith(".pdf"):
            texto = ""
            with open(ruta_archivo, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    texto += page.extract_text() or ""
            return texto.strip()
        elif ruta_archivo.endswith(".epub"):
            texto = ""
            libro = epub.read_epub(ruta_archivo)
            for item in libro.get_items_of_type(epub.ITEM_DOCUMENT):
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                texto += soup.get_text() + "\n"
            return texto.strip()
        else:
            raise ValueError("Formato de archivo no soportado.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")
        return ""

def seleccionar_archivo():
    """Selecciona un archivo de texto para procesar."""
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un documento para procesar",
        filetypes=[("Documentos", "*.txt *.docx *.pdf *.epub")]
    )
    if ruta_archivo:
        entrada_archivo.delete(0, tk.END)
        entrada_archivo.insert(0, ruta_archivo)

def seleccionar_archivo_salida():
    """Selecciona la ubicación donde se guardará el archivo de audio."""
    archivo_salida = filedialog.asksaveasfilename(
        title="Selecciona el lugar donde guardar el archivo",
        defaultextension=".mp3",
        filetypes=[("Archivos MP3", "*.mp3")]
    )
    if archivo_salida:
        entrada_archivo_salida.delete(0, tk.END)
        entrada_archivo_salida.insert(0, archivo_salida)

def generar_audio():
    """Genera un archivo de audio usando gTTS."""
    ruta_archivo = entrada_archivo.get().strip()
    archivo_salida = entrada_archivo_salida.get().strip()
    idioma_seleccionado = idioma_var.get()

    if not ruta_archivo or not archivo_salida:
        messagebox.showwarning("Información incompleta", "Completa todos los campos.")
        return

    texto = leer_archivo(ruta_archivo)
    if not texto:
        messagebox.showwarning("Archivo vacío", "El documento seleccionado no contiene texto.")
        return

    try:
        barra_progreso["value"] = 0
        barra_progreso["maximum"] = 100

        # Generación del audio
        tts = gTTS(texto, lang=idioma_seleccionado)
        tts.save(archivo_salida)

        # Actualizar progreso al finalizar
        barra_progreso["value"] = 100
        messagebox.showinfo("Éxito", f"Audio generado correctamente: {archivo_salida}")

        global archivo_actual
        archivo_actual = archivo_salida
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el audio: {str(e)}")

def reproducir_audio():
    """Reproduce el archivo de audio generado."""
    global audio_en_reproduccion, archivo_actual

    if not archivo_actual:
        messagebox.showwarning("Advertencia", "No hay un archivo de audio generado para reproducir.")
        return

    try:
        if not audio_en_reproduccion:
            pygame.mixer.music.load(archivo_actual)
            pygame.mixer.music.play(loops=0)
            audio_en_reproduccion = True
            barra_progreso["value"] = 0
            ventana.after(100, actualizar_progreso_reproduccion)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reproducir el audio: {str(e)}")

def actualizar_progreso_reproduccion():
    """Actualiza la barra de progreso mientras se reproduce el audio."""
    global audio_en_reproduccion
    if not pygame.mixer.music.get_busy():
        audio_en_reproduccion = False
        barra_progreso["value"] = 100
    else:
        barra_progreso["value"] += 1  # Simulación de progreso (mejora opcional)
        ventana.after(100, actualizar_progreso_reproduccion)

def pausar_audio():
    """Pausa o reanuda el audio."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def detener_audio():
    """Detiene el audio en reproducción."""
    global audio_en_reproduccion
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        audio_en_reproduccion = False
        barra_progreso["value"] = 0

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Conversor de Documento a Audio con Reproductor")

# Campo para seleccionar archivo de entrada
tk.Label(ventana, text="Selecciona el archivo a procesar:").pack(pady=5)
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack(pady=5)
tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack(pady=5)

# Campo para seleccionar archivo de salida
tk.Label(ventana, text="Selecciona el lugar donde guardar el archivo:").pack(pady=5)
entrada_archivo_salida = tk.Entry(ventana, width=50)
entrada_archivo_salida.pack(pady=5)
tk.Button(ventana, text="Seleccionar archivo de salida", command=seleccionar_archivo_salida).pack(pady=5)

# Selección de idioma
tk.Label(ventana, text="Selecciona el idioma para la conversión:").pack(pady=5)
idioma_var = tk.StringVar(value="es")
idiomas = [("Español", "es"), ("Inglés", "en"), ("Francés", "fr")]
for texto, valor in idiomas:
    tk.Radiobutton(ventana, text=texto, variable=idioma_var, value=valor).pack(anchor="w")

# Botón para generar el audio
tk.Button(ventana, text="Generar audio", command=generar_audio).pack(pady=5)

# Barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate")
barra_progreso.pack(pady=5)

# Botones de control del reproductor
tk.Button(ventana, text="Reproducir", command=reproducir_audio).pack(pady=5)
tk.Button(ventana, text="Pausar/Reanudar", command=pausar_audio).pack(pady=5)
tk.Button(ventana, text="Detener", command=detener_audio).pack(pady=5)

# Ejecutar la aplicación
ventana.mainloop()
