import os
import docx2txt
import pdfplumber
from ebooklib import epub

MAX_CHARACTERS = 4000

# Extrae texto de diferentes tipos de archivos

def extract_text(file_path):
    """
    Extrae texto de archivos PDF, EPUB, DOCX y TXT.
    Devuelve un string con el texto o un mensaje de error si falla.
    """
    if not isinstance(file_path, str) or not file_path:
        return "[Error] Ruta de archivo no válida."
    if not os.path.isfile(file_path):
        return f"[Error] El archivo no existe: {file_path}"
    extension = file_path.lower().split('.')[-1]
    try:
        if extension == 'pdf':
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    if page_text:
                        text.append(page_text.strip())
            return "\n".join(text).strip() if text else "[Error] No se pudo extraer texto del PDF."
        elif extension == 'epub':
            text = []
            book = epub.read_epub(file_path)
            for item in book.get_items():
                if item.get_type() == 9:  # ebooklib.ITEM_DOCUMENT
                    content = item.get_content().decode('utf-8', errors='ignore')
                    if content:
                        text.append(content.strip())
            return "\n".join(text).strip() if text else "[Error] No se pudo extraer texto del EPUB."
        elif extension == 'docx':
            docx_text = docx2txt.process(file_path) or ""
            return docx_text.strip() if docx_text else "[Error] No se pudo extraer texto del DOCX."
        elif extension == 'txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    txt = f.read().strip()
                    return txt if txt else "[Error] El archivo TXT está vacío."
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        txt = f.read().strip()
                        return txt if txt else "[Error] El archivo TXT está vacío."
                except Exception as e:
                    return f"[Error] No se pudo leer el archivo TXT: {str(e)}"
        else:
            return f"[Error] Formato no soportado: .{extension}"
    except Exception as e:
        return f"[Error] No se pudo procesar el archivo: {str(e)}"
