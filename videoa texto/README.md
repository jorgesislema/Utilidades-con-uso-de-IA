# 🎧 Transcriptor de Video a Texto con Vosk

## 📌 Descripción
Este proyecto es una herramienta avanzada para la transcripción de videos a texto utilizando tecnologías de reconocimiento de voz y procesamiento del lenguaje natural.

El objetivo es convertir automáticamente el audio de un video en texto, mejorar su legibilidad con corrección gramatical y estructurarlo con párrafos, palabras clave y un resumen.

### **📚 Tecnologías Utilizadas**
- **Vosk** 🗣️ - Reconocimiento de voz en español
- **Pydub** 🎵 - Manipulación y conversión de audio
- **SpaCy** 📚 - Procesamiento de lenguaje natural
- **LanguageTool** ✅ - Corrección gramatical y ortográfica
- **KeyBERT** 🔑 - Extracción de palabras clave
- **Transformers** 🤖 - Generación de resúmenes
- **Tkinter** 🖥️ - Interfaz gráfica de usuario (GUI)

---

## ⚙️ **Requisitos**
Antes de ejecutar el proyecto, asegúrate de cumplir con los siguientes requisitos:

- **Python 3.8 o superior** (Se recomienda Python 3.10, ya que algunas librerías no son compatibles con versiones más recientes)
- **Dependencias** listadas en `requirements.txt`
- **Modelo de Vosk en español** (`vosk-model-es-0.42`)
- **FFmpeg** instalado y configurado para la manipulación de audio

---

## 👅 **Instalación**
Sigue estos pasos para configurar y ejecutar el proyecto correctamente:

### **1️⃣ Clona el repositorio**
```bash
git clone https://github.com/tuusuario/videoa_texto.git
cd videoa_texto
```

### **2️⃣ Instala las dependencias**
```bash
pip install -r requirements.txt
```

### **3️⃣ Descarga e instala el modelo de Vosk**
- Puedes descargarlo desde: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
- Extrae el modelo en la carpeta raíz del proyecto con el nombre: `vosk-model-es-0.42`

### **4️⃣ Configura FFmpeg**
- Descárgalo desde: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Agrega el binario `ffmpeg.exe` a las variables de entorno del sistema.

---

## 🚀 **Uso**
Para ejecutar la aplicación, usa el siguiente comando:

```bash
python video_a_texto.py
```

### 📂 **Interfaz Gráfica (GUI)**
1. **Selecciona el archivo de video** 🎥
2. **Elige la carpeta de salida** 📎
3. **Especifica el nombre del archivo** 📝
4. **Inicia la transcripción** y espera a que termine ⏳

El resultado será un archivo `.txt` generado en la carpeta especificada.

---

## 🛠️ **Explicación del Código**
El código está organizado en una **clase principal** llamada `TranscriptorApp`, que maneja toda la funcionalidad de la aplicación.

### **🔹 Inicialización de la Aplicación**
```python
class TranscriptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Transcriptor Avanzado de Video a Texto")
        self.master.geometry("600x450")
```
- Crea la ventana principal con **Tkinter**.
- Define el tamaño y el título de la aplicación.

### **🔹 Configuración de Modelos**
```python
self.MODELO_VOSK = self.cargar_modelo_vosk()
self.nlp = spacy.load("es_core_news_sm")
self.kw_model = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')
```
- **Vosk** se carga para el reconocimiento de voz.
- **SpaCy** se usa para dividir el texto en oraciones.
- **KeyBERT** permite extraer palabras clave del texto.

### **🔹 Conversión del Video a Audio**
```python
def extraer_audio(self, video_path, audio_path):
    audio = AudioSegment.from_file(video_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(audio_path, format="wav")
```
- Extrae el **audio** del video y lo convierte a **formato WAV** compatible con **Vosk**.

### **🔹 Transcripción del Audio**
```python
def procesar_audio(self, audio_path):
    recognizer = KaldiRecognizer(self.MODELO_VOSK, 16000)
    texto_total = []
    with wave.open(audio_path, 'rb') as audio_file:
        while True:
            data = audio_file.readframes(4000)
            if not data:
                break
            if recognizer.AcceptWaveform(data):
                resultado = json.loads(recognizer.Result())
                texto_total.append(resultado.get('text', ''))
    return ' '.join(texto_total)
```
- **Vosk** procesa el audio y lo transcribe en **texto**.

### **📂 Estructura del Proyecto**
```
📁 videoa_texto
🌍 vosk-model-es-0.42    # Modelo de Vosk en español
📝 requirements.txt       # Dependencias del proyecto
📝 README.md              # Documentación del proyecto
📝 video_a_texto.py       # Código principal del transcriptor
```

---

## 🐄 **Licencia**
Este proyecto está bajo la Licencia **MIT**, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente.

---

🔹 **Conclusión:**  
Este proyecto es una herramienta potente para la transcripción automática de videos. Su arquitectura modular y su combinación de tecnologías lo hacen ideal para procesar grandes volúmenes de contenido audiovisual con alta precisión. 🚀

