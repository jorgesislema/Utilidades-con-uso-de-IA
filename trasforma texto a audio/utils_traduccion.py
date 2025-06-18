from deep_translator import GoogleTranslator
import textwrap
from .utils_archivos import MAX_CHARACTERS

# Traduce texto en fragmentos para evitar errores

def traducir_texto(texto, idioma_destino="es"):
    """
    Traduce el texto al idioma destino usando GoogleTranslator.
    Devuelve el texto traducido o un mensaje de error si ocurre algún problema.
    """
    if not isinstance(texto, str) or not texto.strip():
        return "[Error] Texto de entrada no válido para traducir."
    if not isinstance(idioma_destino, str) or not idioma_destino:
        return "[Error] Idioma de destino no válido."
    try:
        if idioma_destino == "auto":
            return texto
        traductor = GoogleTranslator(source="auto", target=idioma_destino)
        fragmentos = textwrap.wrap(texto, MAX_CHARACTERS, break_long_words=False, replace_whitespace=False)
        texto_traducido = "\n".join([traductor.translate(frag) for frag in fragmentos])
        if not texto_traducido.strip():
            return "[Error] La traducción resultó vacía."
        return texto_traducido
    except Exception as e:
        print(f"❌ Error en la traducción: {e}")
        return f"[Error] No se pudo traducir el texto: {str(e)}"
