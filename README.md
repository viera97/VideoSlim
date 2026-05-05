# VideoSlim Releases

Esta carpeta contiene los binarios compilados de VideoSlim con los archivos de FFmpeg incluidos.

## Estructura

```
Releases/
├── VideoSlim.exe        # Ejecutable compilado (Windows)
├── VideoSlim            # Ejecutable compilado (Linux/Mac)
├── ffmpeg               # Binario de ffmpeg
├── ffprobe              # Binario de ffprobe
├── Videos/              # Carpeta para colocar videos a comprimir
└── README.md            # Este archivo
```

## Uso

1. Coloca tus videos en la carpeta `Videos/`
2. Ejecuta `VideoSlim.exe` (Windows) o `./VideoSlim` (Linux/Mac)
3. Los videos comprimidos se guardarán en la misma carpeta

## Compilación

Para compilar el proyecto con los binarios de FFmpeg:

```bash
# Windows (PowerShell)
pyinstaller --onefile --add-data "path\to\ffmpeg;." --add-data "path\to\ffprobe;." --icon=icon.ico main.py

# Linux/Mac
pyinstaller --onefile --add-data "path/to/ffmpeg:." --add-data "path/to/ffprobe:." main.py
```

## Descargar binarios de FFmpeg

- **Windows**: https://www.gyan.dev/ffmpeg/builds/
- **Linux**: Ya incluido en la mayoría de distribuciones, o descargar de https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
