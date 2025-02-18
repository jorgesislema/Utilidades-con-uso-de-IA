# 🎥 Descargador de Videos y Audio con Interfaz Gráfica (GUI)

Este proyecto es una aplicación de escritorio para descargar videos y audios desde múltiples plataformas, utilizando `yt-dlp` y una interfaz gráfica creada con `Tkinter`. También permite transcribir audio utilizando `Whisper` AI de OpenAI.

## 🚀 Características

✅ Descarga videos y audios desde múltiples plataformas.  
✅ Opción para extraer solo el audio en formato MP3.  
✅ Barra de progreso en tiempo real.  
✅ Selección de carpeta de destino para las descargas.  
✅ Interfaz gráfica intuitiva y fácil de usar.  
✅ Opción de transcripción de audio con IA (Whisper).  

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Descripción |
|------------|------------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Fork avanzado de `youtube-dl` para descargar videos y audios. |
| [Whisper](https://github.com/openai/whisper) | Modelo de IA de OpenAI para transcripción de audio. |
| [Tkinter](https://docs.python.org/3/library/tkinter.html) | Biblioteca estándar de Python para la creación de interfaces gráficas. |
| [tqdm](https://github.com/tqdm/tqdm) | Biblioteca para mostrar barras de progreso en la terminal. |
| [threading](https://docs.python.org/3/library/threading.html) | Módulo de Python para ejecución de tareas en segundo plano. |

---

## 📥 Instalación

### 1️⃣ Clona el repositorio  
```bash
git clone https://github.com/tu-usuario/descargador-videos.git
cd descargador-videos
```

## 2️⃣ Crea un entorno virtual e instala dependencias
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
- Nota: Asegúrate de tener ffmpeg instalado en tu sistema. Puedes instalarlo con:

    Windows: Descarga FFmpeg y configúralo en las variables de entorno.
---
## 🎯 Uso

1️⃣ Ejecuta el programa
```bash
python main.py
```
---

## 🐄 **Licencia**
Este proyecto está bajo la Licencia **MIT**, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente.