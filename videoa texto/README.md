# Video a Texto con IA

Este es un programa que permite la transcripción de videos a texto utilizando **Whisper AI** y la generación de resúmenes automáticos con **Hugging Face Transformers**. Es una aplicación diseñada con **Tkinter**, que permite seleccionar archivos de video locales, extraer su audio y transcribirlo de manera eficiente.

---

## Características Principales

- **Transcripción precisa**: Usa el modelo **Whisper AI (Small)** de OpenAI para convertir el audio en texto.
- **Resúmenes automáticos**: Genera resúmenes utilizando **BART de Facebook** para facilitar la comprensión del contenido.
- **Interfaz gráfica intuitiva**: Desarrollada con **Tkinter**, con botones de selección de archivo, barra de progreso y mensajes de estado.
- **Extracción de audio**: Convierte videos en audio WAV antes de la transcripción utilizando **Pydub**.
- **Optimizado para CPU y GPU**: Detecta automáticamente si hay una GPU disponible y ajusta la carga del modelo en consecuencia.

---

## Tecnologías Usadas

- **Python 3** - Lenguaje principal del programa.
- **Whisper AI** - Para la transcripción del audio.
- **Hugging Face Transformers (BART)** - Para la generación de resúmenes automáticos.
- **Pydub** - Para la extracción y conversión de audio.
- **Tkinter** - Para la interfaz de usuario.

---

## Instalación de Dependencias

Para ejecutar el programa, primero instala las dependencias necesarias:

```bash
pip install torch torchvision torchaudio whisper
pip install transformers
pip install pydub
pip install tkinter
pip install ffmpeg-python
```

Si usas **GPU**, asegúrate de instalar PyTorch con soporte para CUDA. Puedes verificar las instrucciones en [PyTorch](https://pytorch.org/get-started/locally/).

Además, instala **FFmpeg** si no lo tienes:

- **Windows**: [Descargar FFmpeg](https://ffmpeg.org/download.html)
- **Linux/macOS**: Ejecuta `sudo apt install ffmpeg` o `brew install ffmpeg`.

---

## Cómo Usarlo

1. Ejecuta el script **`video_a_texto.py`**:
   ```bash
   python video_a_texto.py
   ```
2. En la interfaz gráfica, selecciona un archivo de video.
3. Presiona **"Iniciar Transcripción"**.
4. Espera a que el programa extraiga el audio, transcriba y resuma el contenido.
5. La transcripción y el resumen se guardarán en un archivo de texto junto al video.

---

## Notas y Recomendaciones

- Para mejorar el rendimiento en CPU, usa el modelo **Whisper Small** o **Tiny** en lugar de "base".
- Los resúmenes pueden fallar si el texto es muy largo; el programa maneja este error dividiendo la transcripción en partes.
- Si experimentas problemas de audio, asegúrate de que FFmpeg esté correctamente instalado y en el PATH.

---

## Contacto y Contribuciones

Si tienes sugerencias, errores o mejoras, ¡házmelas saber! Puedes contribuir con mejoras en el código o sugerencias de optimización.

**Autor:** Jorge Sislema

