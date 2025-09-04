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

### 1️⃣ Instala las dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecuta la aplicación mejorada
```bash
python descargador_mejorado.py
```

---

## ✨ Características de la Versión Mejorada

- **Validación de URL**: Verifica que la URL sea válida antes de descargar
- **Botón pegar**: Pega automáticamente desde el portapapeles  
- **Interfaz mejorada**: Diseño más limpio y profesional
- **Mejor manejo de errores**: Mensajes claros y específicos
- **Progreso detallado**: Porcentaje exacto de descarga
- **Arquitectura orientada a objetos**: Código más organizado y mantenible

---

## 🎯 Uso

1. Ejecuta `python descargador_mejorado.py`
2. Pega o escribe la URL del video
3. Selecciona formato (video completo o solo audio)
4. Elige la carpeta de destino
5. Haz clic en "Descargar"

---

# Descargador Multiplataforma (Windows)

GUI en Tkinter para descargar videos y audios desde múltiples plataformas usando `yt-dlp`.

## Requisitos
- Python 3.8+ (Windows)
- ffmpeg y ffprobe en el PATH (recomendado para conversiones/embeds). Si no están, la app te mostrará un aviso. Puedes instalar builds para Windows desde: https://github.com/yt-dlp/FFmpeg-Builds
- Paquetes Python:

```powershell
python -m pip install -r requirements.txt
```

## Cómo ejecutar
```powershell
python descargador_multiplataforma.py
```

## Funciones
- Detección de plataforma común (YouTube, TikTok, Instagram, Facebook, X/Twitter, Reddit, Vimeo, Twitch, Dailymotion, Bilibili, SoundCloud)
- Perfiles de formato: 1080p/720p/480p MP4, MP3, M4A, subtítulos (srt)
- Opciones avanzadas: descargar e incrustar subtítulos, incrustar miniatura en audio, usar cookies.txt o extraer cookies automáticamente desde el navegador (Chrome/Edge/Firefox) mediante `cookiesfrombrowser` de yt-dlp
- Barra de progreso, velocidad y ETA, carpeta de salida configurable

### Tema opcional (ttkbootstrap)
La app intenta usar un tema moderno ("darkly") con `ttkbootstrap` si está instalado. Es opcional, si no lo tienes, se usará Tkinter clásico.

Instalación opcional:

```powershell
python -m pip install ttkbootstrap
```

## Notas
- Algunas plataformas requieren autenticación/cookies. Puedes usar `cookies.txt` o seleccionar el navegador para que yt-dlp obtenga las cookies automáticamente.
- Para MP3/M4A y embebidos, `ffmpeg/ffprobe` debe estar disponible.

---

## 🔧 Solución de Problemas

Si tienes errores de módulos faltantes, instala usando tu versión específica de Python:

```powershell
C:/ruta/a/tu/python.exe -m pip install -r requirements.txt
```

## 🐄 **Licencia**
Este proyecto está bajo la Licencia **MIT**, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente.