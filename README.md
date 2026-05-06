# VideoSlim

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern, efficient video compression tool that leverages FFmpeg to reduce video file sizes while maintaining quality. VideoSlim supports both a graphical user interface (GUI) and command-line interface (CLI), making it accessible for both beginners and advanced users.

## ✨ Features

- **🎨 Modern GUI**: Beautiful dark-themed interface built with CustomTkinter
- **⚡ Smart Compression**: Automatically skips videos already using efficient codecs (HEVC, VP9, AV1)
- **🎥 Multiple Codec Support**: HEVC (H.265), H.264, VP9, and AV1 video codecs
- **🔊 Audio Options**: AAC, MP3, Opus, FLAC, AC3 audio codecs
- **📁 Batch Processing**: Compress entire folders with optional recursive search
- **🎚️ Quality Control**: Adjustable CRF (0-51) for fine-tuned quality/size balance
- **🛡️ Safe Processing**: Only saves output if compressed file is smaller than original
- **📊 Real-time Progress**: Live progress tracking and detailed logs
- **⏹️ Stop/Start Control**: Cancel compression operations mid-process
- **🚀 Cross-platform**: Works on Windows, macOS, and Linux
- **📦 Standalone Executables**: No installation required for releases

## 📦 Installation

### System Requirements

- **Python**: 3.10 or higher
- **FFmpeg**: Latest version (automatically included in releases)
- **OS**: Windows 10+, macOS 10.15+, or Linux

### Option 1: Pre-compiled Release (Recommended)

1. Download the latest release for your platform from the [Releases](https://github.com/yourusername/VideoSlim/releases) page
2. Extract the archive
3. Run the executable:
   - **Windows**: `VideoSlim.exe`
   - **macOS/Linux**: `./VideoSlim`

FFmpeg binaries are included - no additional installation required!

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/VideoSlim.git
cd VideoSlim

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .
```

### Option 3: Build from Source

```bash
# Install build dependencies
pip install pyinstaller

# Build executable
pyinstaller --onefile --clean main.py

# The executable will be in the dist/ folder
```

## 🚀 Usage

### Graphical User Interface (GUI)

Simply run the executable without arguments to launch the modern GUI:

```bash
# Linux/macOS
./VideoSlim

# Windows
VideoSlim.exe
```

**GUI Features:**
- **File Selection**: Browse for individual video files or entire folders
- **Codec Settings**: Choose video and audio codecs from dropdown menus
- **Quality Slider**: Adjust CRF value (0=best quality, 51=worst)
- **Options**: Enable recursive folder search and original file deletion
- **Progress Tracking**: Real-time progress bar and expandable log viewer
- **Stop/Start**: Cancel operations at any time

### Command Line Interface (CLI)

For automation, scripting, or headless environments:

```bash
# Basic usage - compress single file
VideoSlim --path video.mp4

# Compress entire folder
VideoSlim --path /videos/

# Recursive folder compression
VideoSlim --path /videos/ --recursive

# Custom settings
VideoSlim --path video.mp4 --vcodec hevc --crf 23 --acodec aac

# Delete originals after compression
VideoSlim --path /videos/ --delete

# Quiet mode (minimal output)
VideoSlim --path video.mp4 --quiet
```

### Command Line Options

| Option | Short | Description | Default | Values |
|--------|-------|-------------|---------|---------|
| `--path` | `-p` | Path to video file or folder | Required | File path |
| `--vcodec` | `-v` | Video codec | `hevc` | `hevc`, `h264`, `vp9`, `av1` |
| `--crf` | | Quality (lower = better) | `28` | 0-51 |
| `--acodec` | `-a` | Audio codec | `aac` | `aac`, `mp3`, `opus`, `flac`, `ac3` |
| `--recursive` | `-r` | Search folders recursively | `False` | |
| `--delete` | | Delete originals after compression | `False` | |
| `--quiet` | `-q` | Suppress console output | `False` | |

## 🎥 Supported Formats

### Video File Extensions
`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.3gp`, `.ts`, `.m2ts`, `.vob`, `.ogv`, `.divx`, `.mpg`

### Video Codecs

| Codec | Description | Compatibility | Compression |
|-------|-------------|----------------|-------------|
| **HEVC (H.265)** | Best compression, modern standard | High | ⭐⭐⭐⭐⭐ |
| **H.264** | Maximum compatibility | Universal | ⭐⭐⭐⭐ |
| **VP9** | Open-source, royalty-free | Good | ⭐⭐⭐⭐⭐ |
| **AV1** | Next-generation, best compression | Emerging | ⭐⭐⭐⭐⭐ |

### Audio Codecs

| Codec | Description | Use Case |
|-------|-------------|----------|
| **AAC** | Standard, good quality | General use |
| **MP3** | Universal compatibility | Legacy devices |
| **Opus** | High quality, low latency | Modern applications |
| **FLAC** | Lossless compression | Archival |
| **AC3** | Dolby compatibility | Home theater |

## ⚙️ Quality Settings (CRF)

CRF (Constant Rate Factor) controls quality vs. file size:

| CRF Range | Quality | Typical Use Case | File Size Reduction |
|-----------|---------|------------------|-------------------|
| 18-23 | Visually lossless | High-quality archival | 30-50% |
| 24-28 | Excellent quality | Recommended for most use | 50-70% |
| 29-35 | Good quality | Storage-constrained | 70-80% |
| 36-51 | Acceptable quality | Maximum compression | 80-90% |

**Lower CRF = Better quality, larger files**  
**Higher CRF = Worse quality, smaller files**

## 🏗️ Technical Architecture

```
VideoSlim/
├── main.py              # Application entry point (GUI/CLI detection)
├── gui.py               # CustomTkinter GUI implementation
├── transcoding.py       # Core FFmpeg transcoding logic
├── pyproject.toml       # Project configuration and dependencies
├── ffmpeg/              # FFmpeg binary (Linux/macOS releases)
├── ffprobe/             # FFprobe binary (Linux/macOS releases)
├── ffmpeg.exe           # FFmpeg binary (Windows releases)
├── ffprobe.exe          # FFprobe binary (Windows releases)
└── build/               # Build artifacts (development only)
```

### How It Works

1. **Binary Detection**: Locates bundled FFmpeg/ffprobe executables
2. **Codec Analysis**: Uses ffprobe to detect current video codec
3. **Smart Filtering**: Skips already efficient codecs (HEVC, VP9, AV1)
4. **Transcoding**: Re-encodes with selected codec and quality settings
5. **Size Validation**: Only keeps output if compression reduces file size
6. **Cleanup**: Optionally replaces originals with compressed versions

### Smart Compression Logic

```python
# Skip if already using efficient codec
if current_codec in ['hevc', 'vp9', 'av1']:
    return False  # No transcoding needed

# Transcode and check size reduction
if output_size >= original_size:
    return False  # Compression ineffective
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/VideoSlim.git
cd VideoSlim

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest

# Build executable
pyinstaller --onefile main.py
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings to all functions
- Keep GUI and CLI logic separate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The powerful multimedia framework
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Tkinter UI framework
- [PyInstaller](https://www.pyinstaller.org/) - Python application packaging

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/VideoSlim/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/VideoSlim/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/VideoSlim/wiki)

---

**Made with ❤️ for efficient video compression**