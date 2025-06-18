import os
from pydub import AudioSegment
import whisper
from transformers import pipeline
from fpdf import FPDF
from docx import Document

# Extraer audio de video a WAV

def extract_audio(video_path):
    try:
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        audio = AudioSegment.from_file(video_path)
        audio.export(audio_path, format="wav")
        return audio_path
    except Exception as e:
        return f"[Error] Error extrayendo audio: {str(e)}"

# Transcribir audio a texto usando Whisper

def transcribe_audio(audio_path, model=None, device="cpu"):
    try:
        if model is None:
            model = whisper.load_model("small", device=device)
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"[Error] Error en la transcripción: {str(e)}"

# Resumir texto usando transformers

def resumir_texto(texto, resumen_modelo=None):
    if resumen_modelo is None:
        try:
            resumen_modelo = pipeline("summarization", model="facebook/bart-large-cnn")
        except Exception as e:
            return f"[Error] Error cargando el modelo de resumen: {str(e)}"
    try:
        if len(texto) < 50:
            return ""
        resumen = resumen_modelo(
            texto[:1024], max_length=150, min_length=50, do_sample=False
        )[0]["summary_text"]
        return resumen
    except Exception as e:
        return f"[Error] Error generando resumen: {str(e)}"

# Guardar resultado en txt, pdf o docx

def guardar_resultado(texto, nombre_archivo, formato, ruta_guardado):
    ruta_completa = os.path.join(ruta_guardado, nombre_archivo)
    try:
        if formato == "txt":
            with open(ruta_completa + ".txt", "w", encoding="utf-8") as f:
                f.write(texto)
            return ruta_completa + ".txt"
        elif formato == "pdf":
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(190, 10, texto)
            pdf.output(ruta_completa + ".pdf")
            return ruta_completa + ".pdf"
        elif formato == "docx":
            doc = Document()
            doc.add_paragraph(texto)
            doc.save(ruta_completa + ".docx")
            return ruta_completa + ".docx"
        else:
            return f"[Error] Formato de salida no soportado: {formato}"
    except Exception as e:
        return f"[Error] Error guardando archivo: {str(e)}"
