# Instalamos las  dependencias nesesarias
!pip install -q pydub openai torch torchvision torchaudio transformers google-colab ipywidgets ffmpeg fpdf python-docx

# Importamos las librerías
import os
import time
from pydub import AudioSegment
import whisper
import torch
from transformers import pipeline
from google.colab import auth
from googleapiclient.discovery import build
from google.colab import files
from IPython.display import display, clear_output, HTML
import ipywidgets as widgets
from fpdf import FPDF
from docx import Document

# Autenticación en Google Drive
auth.authenticate_user()
from google.colab import drive
drive.mount('/content/drive')

# Configuramos del dispositivo para que pueda trabajar con (CPU/GPU)
dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo en uso: {dispositivo}")

# Cargamos los modelos
print("Cargando modelos...")
inicio = time.time()

# Cargamos el  modelo de Whisper
modelo = whisper.load_model("small", device=dispositivo)

# Cargamos el  modelo de resumen
try:
    resumen_modelo = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error cargando el modelo de resumen: {str(e)}")
    resumen_modelo = None

print(f"Modelos cargados en {time.time() - inicio:.1f} segundos")

# Funcion convierte video a formato WAV
def extract_audio(video_path):
    try:
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        audio = AudioSegment.from_file(video_path)
        audio.export(audio_path, format="wav")
        return audio_path
    except Exception as e:
        print(f"Error extrayendo audio: {str(e)}")
        return None
# Esta funcion guarda el resultado en el formato seleccionado y permite escoger ruta de almacenamiento
def guardar_resultado(texto, nombre_archivo, formato, ruta_guardado):
    ruta_completa = os.path.join(ruta_guardado, nombre_archivo)
    
    if formato == "txt":
        with open(ruta_completa + ".txt", "w", encoding="utf-8") as f:
            f.write(texto)
        display(HTML(f'<a href="/{ruta_completa}.txt" download>{nombre_archivo}.txt</a>'))
    elif formato == "pdf":
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(190, 10, texto)
        pdf.output(ruta_completa + ".pdf")
        display(HTML(f'<a href="/{ruta_completa}.pdf" download>{nombre_archivo}.pdf</a>'))
    elif formato == "docx":
        doc = Document()
        doc.add_paragraph(texto)
        doc.save(ruta_completa + ".docx")
        display(HTML(f'<a href="/{ruta_completa}.docx" download>{nombre_archivo}.docx</a>'))
    print(f"Archivo guardado en formato {formato} en {ruta_guardado}.")

# Esta función procesa los archivos desde Google Drive
def transcribir_desde_drive(ruta_drive, formato_salida, ruta_guardado):
    clear_output()
    print("Procesando archivo...")
    
    if resumen_modelo is None:
        print("Error: Modelo de resumen no disponible")
        return
    
    try:
        print(f"📂 Procesando archivo: {ruta_drive}")
        
        #  Extraemos el audio
        print("🎵 Extrayendo audio...")
        audio_path = extract_audio(ruta_drive)
        if not audio_path:
            return
        
        #  Transcripción del video
        print("📝 Transcribiendo con Whisper...")
        result = modelo.transcribe(audio_path)
        texto_completo = result["text"]
        
        # Generamos el resumen
        print("📄 Generando resumen...")
        texto_resumen = ""
        if len(texto_completo) > 50:
            try:
                resumen = resumen_modelo(
                    texto_completo[:1024], 
                    max_length=150, 
                    min_length=50,
                    do_sample=False
                )[0]['summary_text']
                texto_resumen = f"\nRESUMEN AUTOMÁTICO:\n{resumen}\n"
            except Exception as e:
                texto_resumen = f"\nError generando resumen: {str(e)}\n"
        
        # Formateamos el resultado
        texto_final = f"ARCHIVO PROCESADO: {ruta_drive}\n\n"
        texto_final += f"TRANSCRIPCIÓN COMPLETA:\n{texto_completo}\n\n{texto_resumen}\n"
        texto_final += f"Procesado el: {time.ctime()}"
        
        # Guardamos 
        archivo_salida = os.path.splitext(os.path.basename(ruta_drive))[0] + "_TRANSCRIPCION"
        guardar_resultado(texto_final, archivo_salida, formato_salida, ruta_guardado)
        print("✅ Proceso completado.")
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
    
    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        print("🎯 Tarea finalizada.")

# Solicitamos al usuario el archivo desde Google Drive, el formato de salida y la ruta de guardado
ruta_archivo = input("Introduce la ruta completa del archivo en Google Drive (Ejemplo: /content/drive/My Drive/video.mp4): ")
formato_salida = input("Introduce el formato de salida (txt, pdf, docx): ")
ruta_guardado = input("Introduce la ruta donde deseas guardar el archivo (Ejemplo: /content/drive/My Drive/Resultados): ")
transcribir_desde_drive(ruta_archivo, formato_salida, ruta_guardado)
