from gtts import gTTS
import os
import textwrap
import threading
from tkinter import messagebox
from .utils_archivos import MAX_CHARACTERS

# Conversión de texto a audio usando gTTS

def text_to_speech(text, language, output_folder, progress_bar, root):
    """
    Convierte texto a audio usando gTTS y guarda los fragmentos en la carpeta de salida.
    Muestra el progreso en la barra y notifica errores o éxito.
    Valida entradas y maneja errores de forma robusta.
    Permite cancelar la conversión si root tiene el atributo 'cancelar_conversion' en True.
    """
    if not isinstance(text, str) or not text.strip():
        messagebox.showerror("Error", "El texto de entrada para convertir a audio no es válido.")
        return
    if not isinstance(language, str) or not language:
        messagebox.showerror("Error", "El idioma de salida no es válido.")
        return
    if not isinstance(output_folder, str) or not output_folder:
        messagebox.showerror("Error", "La carpeta de salida no es válida.")
        return
    def process_audio():
        try:
            os.makedirs(output_folder, exist_ok=True)
            fragments = textwrap.wrap(text, MAX_CHARACTERS, break_long_words=False, replace_whitespace=False)
            num_fragments = len(fragments)
            if num_fragments == 0:
                messagebox.showerror("Error", "No hay texto para convertir a audio.")
                return
            for i, fragment in enumerate(fragments, start=1):
                # Permitir cancelación si root tiene el atributo cancelar_conversion
                if hasattr(root, 'cancelar_conversion') and root.cancelar_conversion:
                    messagebox.showinfo("Cancelado", "La conversión ha sido cancelada por el usuario.")
                    break
                progress = int((i / num_fragments) * 100)
                progress_bar["value"] = progress
                root.update_idletasks()
                try:
                    tts = gTTS(text=fragment, lang=language, slow=False)
                    output_file = os.path.join(output_folder, f"parte_{i}.mp3")
                    tts.save(output_file)
                except Exception as e:
                    messagebox.showerror("Error en la conversión de fragmento", f"Fragmento {i}: {str(e)}")
            else:
                messagebox.showinfo("Éxito", f"Conversión completada. Archivos guardados en:\n{output_folder}")
        except Exception as e:
            messagebox.showerror("Error en la conversión", str(e))
        finally:
            progress_bar["value"] = 0
            if hasattr(root, 'cancelar_conversion'):
                root.cancelar_conversion = False
    threading.Thread(target=process_audio, daemon=True).start()
