# Video a Texto con IA en Google Colab

Este es un programa que permite la transcripción de videos a texto utilizando **Whisper AI** y la generación de resúmenes automáticos con **Hugging Face Transformers**. Diseñado para ejecutarse en **Google Colab**, permite la selección de archivos de video almacenados en **Google Drive**, extraer su audio y transcribirlo de manera eficiente.

---

## Características Principales

- **Transcripción precisa**: Utiliza el modelo **Whisper AI (Small)** de OpenAI para convertir el audio en texto.
- **Resúmenes automáticos**: Genera resúmenes utilizando **BART de Facebook** para facilitar la comprensión del contenido.
- **Integración con Google Drive**: Accede y procesa archivos directamente desde Google Drive.
- **Extracción de audio**: Convierte videos en audio WAV antes de la transcripción utilizando **Pydub**.
- **Opciones de guardado**: Permite guardar la transcripción en **TXT, PDF o DOCX** y elegir la carpeta de almacenamiento en Google Drive.
- **Optimizado para CPU y GPU**: Detecta automáticamente si hay una GPU disponible y ajusta la carga del modelo en consecuencia.

---

## Tecnologías Usadas

- **Python 3** - Lenguaje principal del programa.
- **Whisper AI** - Para la transcripción del audio.
- **Hugging Face Transformers (BART)** - Para la generación de resúmenes automáticos.
- **Pydub** - Para la extracción y conversión de audio.
- **Google Colab & Google Drive** - Para almacenamiento y procesamiento de archivos.
- **FPDF y python-docx** - Para la generación de archivos PDF y DOCX.

---

## Instalación de Dependencias

Para ejecutar el programa en Google Colab, asegúrate de instalar las siguientes dependencias:

```sh
pip install -q pydub openai torch torchvision torchaudio transformers google-colab ipywidgets ffmpeg fpdf python-docx
```

Además, monta tu **Google Drive** para acceder a los archivos:

```python
from google.colab import drive
drive.mount('/content/drive')
```

---

## Cómo Clonar el Repositorio

Si deseas ejecutar el código desde un repositorio de GitHub en Google Colab, puedes clonarlo con el siguiente comando:

```sh
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

Luego, abre el notebook en Google Colab y sigue las instrucciones.

---

## Cómo Usarlo en Google Colab

1. **Ejecuta todas las celdas** del notebook en Colab.
2. **Proporciona la ruta del archivo de video en Google Drive** cuando se te solicite.
3. **Selecciona el formato de salida** en TXT, PDF o DOCX.
4. **Elige la ruta de almacenamiento** dentro de Google Drive.
5. **Espera a que el proceso finalice**, se generará un enlace para descargar el archivo transcrito.

---

## Notas y Recomendaciones

- Para mejorar el rendimiento en CPU, usa el modelo **Whisper Small** o **Tiny** en lugar de "base".
- Si experimentas problemas de audio, asegúrate de que **FFmpeg** esté correctamente instalado.
- Google Colab puede desconectarse si el proceso es muy largo, guarda periódicamente tu progreso.

---

## Contacto y Contribuciones

Si tienes sugerencias, errores o mejoras, ¡házmelo saber! Puedes contribuir con mejoras en el código o sugerencias de optimización.

**Autor:** Jorge Sislema