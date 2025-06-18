# 📖 De Texto a Audio Audiobook Converter

![Audiolibros](https://github.com/jorgesislema/Utilidades-con-uso-de-IA/blob/main/imagenes/audiolibros.jpg)


Este proyecto convierte documentos en **audiolibros** utilizando **Google Text-to-Speech (gTTS)** y permite la **traducción automática** con **Deep Translator**. Es ideal para transformar libros, artículos o cualquier documento de texto en archivos de audio en **múltiples idiomas**. La interfaz gráfica desarrollada con **Tkinter** facilita la selección de archivos y la configuración del proceso.

---

## 🚀 Tecnologías Utilizadas

Este proyecto emplea múltiples tecnologías y bibliotecas para garantizar una conversión eficiente y fluida:

### 🔹 Lenguaje de Programación

- **Python 3.10** → Se eligió esta versión por su compatibilidad con la mayoría de las bibliotecas utilizadas, evitando errores en dependencias.

### 🔹 Bibliotecas y Recursos

- **gTTS** → Convierte texto a voz con la API de Google.
- **Deep Translator** → Traducción automática de texto con Google Translate.
- **Tkinter** → Interfaz gráfica para seleccionar archivos y gestionar la conversión.
- **PDFPlumber** → Extracción de texto de archivos PDF.
- **Docx2txt** → Procesamiento de archivos DOCX.
- **EbookLib** → Manejo de archivos EPUB.
- **Textwrap** → Divide el texto en fragmentos adecuados para gTTS.

### 🔹 Virtualización con Conda

Para evitar conflictos de versiones y garantizar un entorno aislado y estable, se utilizó **Anaconda** con un entorno virtual en **Conda**. Esto permite reproducir el entorno en cualquier máquina sin afectar otras instalaciones de Python.

---

## 💻 Instalación y Configuración

Sigue estos pasos para clonar y ejecutar el proyecto:

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/text-to-speech-audiobook.git
```

### 2️⃣ Instalar dependencias

Se recomienda usar un entorno virtual (por ejemplo, conda o venv):

```bash
cd trasforma\ texto\ a\ audio
pip install -r requirements.txt
```

### 3️⃣ Ejecutar la aplicación

```bash
python "de texto a audio .py"
```

---

## 📝 Notas
- Asegúrate de tener conexión a internet para la traducción y la conversión de texto a voz.
- El programa soporta archivos PDF, DOCX, EPUB y TXT.
- Los archivos de audio se guardarán en la carpeta de salida seleccionada.

---

## 📂 Estructura del Proyecto

- `de texto a audio .py`: Script principal con la interfaz gráfica.
- `utils_archivos.py`: Utilidades para extracción de texto de archivos.
- `utils_traduccion.py`: Utilidades para traducción de texto.
- `utils_tts.py`: Utilidades para conversión de texto a audio.
- `requirements.txt`: Dependencias necesarias.

---

## ⚠️ Advertencia sobre Tiempo de Conversión

📌 **El tiempo de conversión depende del número de páginas del documento.**  
Los documentos muy extensos pueden tardar **varios minutos** en procesarse completamente.  
La barra de progreso ayuda a visualizar el avance del proceso.  

Si el documento es muy grande, se recomienda **fragmentarlo** antes de convertirlo.

---

## 🎯 Conclusión

Este proyecto facilita la creación de **audiolibros** y mejora la **accesibilidad a la información** mediante la conversión de texto a voz.  
Gracias a la **virtualización con Conda** y el uso de **Python 3.10**, garantizamos un **entorno estable y eficiente** para la ejecución de la aplicación.

💡 **¿Te gustó el proyecto?** ¡Siéntete libre de contribuir o reportar mejoras en el repositorio! 🚀🎧

---

📚 **¡Disfruta tu audiolibro y optimiza tu tiempo de lectura!** 🎧📖

