# VideoSlim

A modern video compression tool that leverages FFmpeg to reduce video file sizes while maintaining quality. VideoSlim supports both a graphical user interface (GUI) and command-line interface (CLI), making it accessible for both beginners and advanced users.

## Features

- **Dual Interface**: Modern GUI with CustomTkinter or CLI mode for automation
- **Multiple Codec Support**: HEVC (H.265), H.264, VP9, and AV1 video codecs
- **Audio Codec Options**: AAC, MP3, Opus, FLAC, AC3
- **Smart Compression**: Automatically skips videos already using efficient codecs (HEVC/VP9)
- **Batch Processing**: Compress entire folders with optional recursive search
- **Quality Control**: Adjustable CRF (0-51) for fine-tuned quality/size balance
- **Safe Processing**: Only saves output if compressed file is smaller than original
- **Progress Tracking**: Real-time progress bar and logs in GUI mode
- **Stop/Start Control**: Cancel compression operations mid-process

## Installation

### Prerequisites

- Python 3.10 or higher
- FFmpeg and FFprobe binaries (included in releases)

### From Source

```bash
# Clone the repository
git clone https://github.com/your-repo/VideoSlim-new.git
cd VideoSlim-new

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .
```

### From Release (Binary)

Download the pre-compiled release for your platform. FFmpeg binaries are included.

## Usage

### GUI Mode

Simply run the executable without arguments to launch the graphical interface:

```bash
# Linux/Mac
./VideoSlim

# Windows
VideoSlim.exe
```

The GUI allows you to:
- Select individual video files or entire folders
- Choose video and audio codecs
- Adjust quality (CRF) with a slider
- Enable recursive folder search
- Optionally delete original files after compression

### CLI Mode

```bash
# Compress a single file
VideoSlim --path video.mp4

# Compress folder (non-recursive)
VideoSlim --path /videos/

# Compress folder recursively
VideoSlim --path /videos/ --recursive

# Custom settings
VideoSlim --path video.mp4 --vcodec hevc --crf 23 --acodec aac

# Delete originals after compression
VideoSlim --path /videos/ --delete

# Quiet mode (minimal output)
VideoSlim --path video.mp4 --quiet
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--path`, `-p` | Path to video file or folder | Required |
| `--vcodec`, `-v` | Video codec (hevc, h264, vp9, av1) | hevc |
| `--crf` | Quality (0=best, 51=worst) | 28 |
| `--acodec`, `-a` | Audio codec (aac, mp3, opus, flac, ac3) | aac |
| `--recursive`, `-r` | Search folders recursively | False |
| `--delete` | Delete originals after compression | False |
| `--quiet`, `-q` | Suppress console output | False |

## Supported Formats

### Video Extensions
`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.3gp`, `.ts`, `.m2ts`, `.vob`, `.ogv`, `.divx`, `.mpg`

### Codecs

**Video:**
- **HEVC (H.265)**: Best compression, widely supported
- **H.264**: Maximum compatibility
- **VP9**: Open, royalty-free
- **AV1**: Next-gen, best compression

**Audio:**
- **AAC**: Standard, good compatibility
- **MP3**: Universal support
- **Opus**: High quality, low latency
- **FLAC**: Lossless
- **AC3**: Dolby compatibility

## Technical Architecture

```
VideoSlim/
├── main.py           # Entry point (GUI/CLI detection)
├── gui.py            # CustomTkinter GUI implementation
├── transcoding.py    # Core FFmpeg transcoding logic
├── pyproject.toml    # Project configuration
├── ffmpeg/           # FFmpeg binary (Linux/Mac)
├── ffprobe/          # FFprobe binary
├── ffmpeg.exe/       # FFmpeg binary (Windows)
└── ffprobe.exe/      # FFprobe binary (Windows)
```

### How It Works

1. **FFmpeg Detection**: Locates bundled FFmpeg binaries relative to the executable
2. **Codec Detection**: Uses ffprobe to detect the current video codec
3. **Smart Skip**: Skips already efficient codecs (HEVC/VP9)
4. **Transcoding**: Re-encodes with selected codec and CRF value
5. **Size Check**: Only saves output if compression actually reduces file size
6. **Optional Cleanup**: Deletes originals if `--delete` flag is set

### CRF Quality Guide

| CRF | Quality | Use Case |
|-----|---------|----------|
| 18-23 | Visually lossless | High quality archival |
| 24-28 | Good quality | Recommended for most use |
| 29-35 | Moderate quality | Storage-constrained |
| 36-51 | Low quality | Maximum compression |

## Building from Source

### Compile with PyInstaller

```bash
# Windows
pyinstaller --onefile --add-data "ffmpeg.exe;." --add-data "ffprobe.exe;." --icon=icon.ico main.py

# Linux/Mac
pyinstaller --onefile --add-data "ffmpeg:." --add-data "ffprobe:." main.py
```

## Dependencies

- **customtkinter**: Modern Tkinter GUI framework
- **pyinstaller**: Compiles Python to standalone executable

## License

See LICENSE file for details.

## Downloads

- **Windows**: https://www.gyan.dev/ffmpeg/builds/
- **Linux**: https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`