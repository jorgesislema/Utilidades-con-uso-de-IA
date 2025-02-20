# 📖 Text-to-Speech Audiobook Converter

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
cd text-to-speech-audiobook
```

### 2️⃣ Crear un Entorno Virtual con Conda

```bash
conda create --name tts_env python=3.10
conda activate tts_env
```

📌 **¿Por qué Conda y Python 3.10?**  
Conda permite administrar entornos de Python de manera aislada, asegurando que todas las dependencias sean compatibles y evitando problemas con versiones futuras de las bibliotecas.

### 3️⃣ Instalar Dependencias

```bash
pip install gtts soundfile docx2txt pdfplumber ebooklib deep-translator
```

🔹 **Nota:** `tkinter` ya viene instalado en Python por defecto, pero si experimentas problemas, asegúrate de que esté disponible en tu entorno.

---

## 🔧 Uso de la Aplicación

### 1️⃣ Ejecutar la Aplicación

```bash
python app.py
```

### 2️⃣ Seleccionar Archivo de Texto

📌 Puedes cargar archivos en los siguientes formatos:

- **PDF (`.pdf`)**
- **Word (`.docx`)**
- **EPUB (`.epub`)**
- **Texto plano (`.txt`)**

### 3️⃣ Seleccionar Idioma de Salida

📌 **Idiomas disponibles:**
- **Español (`es`)**
- **Inglés (`en`)**
- **Francés (`fr`)**
- **Alemán (`de`)**
- **Italiano (`it`)**
- **Portugués (`pt`)**

Si eliges un idioma diferente al original, el texto se traducirá automáticamente **antes** de convertirlo a audio.

### 4️⃣ Definir Carpeta de Salida

Elige la carpeta donde se guardarán los archivos de audio.  
Si el documento es muy largo, se dividirá en **múltiples archivos de audio** automáticamente.

### 5️⃣ Iniciar Conversión

- Presiona **"Convertir a Audiolibro"**.
- La **barra de progreso** mostrará el avance del proceso.
- Al finalizar, recibirás una **notificación** y los archivos estarán disponibles en la carpeta seleccionada.

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

