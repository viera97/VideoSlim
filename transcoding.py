"""VideoSlim Release - Video compression tool using FFmpeg binaries."""

import argparse
import os
import subprocess
import sys
from typing import Optional, List

# =============================================================================
# CONFIGURACIÓN DE COLORES ANSI
# =============================================================================
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"

# =============================================================================
# RUTAS DE BINARIOS FFmpeg (ubicados junto al ejecutable en sys._MEIPASS)
# =============================================================================
def get_binary_dir() -> str:
    """Obtiene el directorio donde están los binarios."""
    if getattr(sys, 'frozen', False):
        # Cuando está compilado con PyInstaller, está en sys._MEIPASS
        return sys._MEIPASS
    else:
        # Cuando se ejecuta como script, está en el mismo directorio que este archivo
        return os.path.dirname(os.path.abspath(__file__))

def get_ffmpeg_path() -> str:
    """Obtiene la ruta al binario de ffmpeg."""
    binary_dir = get_binary_dir()
    if sys.platform == 'win32':
        return os.path.join(binary_dir, 'ffmpeg.exe')
    return os.path.join(binary_dir, 'ffmpeg')

def get_ffprobe_path() -> str:
    """Obtiene la ruta al binario de ffprobe."""
    binary_dir = get_binary_dir()
    if sys.platform == 'win32':
        return os.path.join(binary_dir, 'ffprobe.exe')
    return os.path.join(binary_dir, 'ffprobe')

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================
import logging
logging.basicConfig(
    level=logging.INFO,
    format=f"{DIM}%(asctime)s{RESET} - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTES
# =============================================================================
VIDEO_EXTENSIONS = frozenset([
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv',
    '.webm', '.m4v', '.3gp', '.ts', '.m2ts', '.vob',
    '.ogv', '.divx', '.mpg'
])

VALID_VCODECS = frozenset(['hevc', 'h264', 'vp9', 'av1'])
VALID_ACODECS = frozenset(['aac', 'mp3', 'opus', 'flac', 'ac3'])

# =============================================================================
# FUNCIONES UTILITARIAS
# =============================================================================
def validate_codecs(vcodec: str, acodec: str, crf: int) -> tuple[bool, Optional[str]]:
    """Valida los parámetros de códec."""
    if vcodec not in VALID_VCODECS:
        return False, f"Invalid video codec: {vcodec}. Valid options: {', '.join(VALID_VCODECS)}"
    if acodec not in VALID_ACODECS:
        return False, f"Invalid audio codec: {acodec}. Valid options: {', '.join(VALID_ACODECS)}"
    if not 0 <= crf <= 51:
        return False, f"CRF must be between 0 and 51, got {crf}"
    return True, None


def check_ffmpeg_installed() -> bool:
    """Verifica si los binarios de FFmpeg existen."""
    ffmpeg_path = get_ffmpeg_path()
    ffprobe_path = get_ffprobe_path()
    
    ffmpeg_exists = os.path.exists(ffmpeg_path)
    ffprobe_exists = os.path.exists(ffprobe_path)
    
    if not ffmpeg_exists:
        logger.error(f"FFmpeg not found at: {ffmpeg_path}")
    if not ffprobe_exists:
        logger.error(f"FFprobe not found at: {ffprobe_path}")
    
    return ffmpeg_exists and ffprobe_exists


def get_codec(input_file: str) -> str:
    """Obtiene el códec de video usando ffprobe."""
    ffprobe_path = get_ffprobe_path()
    
    if not os.path.exists(input_file):
        logger.error(f"File not found for codec detection: {input_file}")
        return 'unknown'
    
    try:
        cmd = [
            ffprobe_path,
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'csv=p=0',
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        codec = result.stdout.strip()
        return codec if codec else 'unknown'
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout reading codec from: {input_file}")
        return 'unknown'
    except Exception as e:
        logger.error(f"Error probing file: {e}")
        return 'unknown'


def transcode(input_file: str, output_file: str, vcodec: str = "hevc", crf: int = 28, acodec: str = "aac") -> None:
    """Transcode un archivo de video usando ffmpeg."""
    ffmpeg_path = get_ffmpeg_path()
    
    if not os.path.exists(input_file):
        raise Exception(f"Input file not found: {input_file}")
    
    try:
        cmd = [
            ffmpeg_path,
            '-i', input_file,
            '-c:v', vcodec,
            '-crf', str(crf),
            '-c:a', acodec,
            '-preset', 'medium',
            '-y',  # Sobrescribir archivo de salida
            output_file
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")
            
    except Exception as e:
        raise Exception(f"Error transcoding: {e}")


def send_transcode(path: str, video_file: str, vcodec: str, crf: int, acodec: str) -> Optional[str]:
    """Prepara y ejecuta la transcodificación de un video."""
    input_file_path = os.path.join(path, video_file)
    output_file_aux = os.path.splitext(video_file)
    
    # Cambiar extensión a .mp4 si se usa HEVC/H.264 y el archivo es WebM
    output_ext = output_file_aux[1]
    if vcodec.lower() in ('hevc', 'h264') and output_ext.lower() == '.webm':
        output_ext = '.mp4'
    
    output_file = f"{output_file_aux[0]}_encoded{output_ext}"
    output_file_path = os.path.join(path, output_file)
    
    try:
        logger.info(f"{BOLD}Transcoding:{RESET} {DIM}{video_file}{RESET} ⭔")
        transcode(input_file_path, output_file_path, vcodec, crf, acodec)
        return output_file_path
    except KeyboardInterrupt:
        logger.warning("Transcoding terminated by user")
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
            logger.debug("Cleaned up incomplete output file")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error transcoding {video_file}: {e}")
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        return None


def transcode_recursive(path: str, vcodec: str, crf: int, acodec: str, delete: bool) -> int:
    """Transcode todos los videos recursivamente en un directorio."""
    video_files = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS:
                video_files.append(os.path.join(root, file))
    
    if not video_files:
        logger.warning("No videos found in directory")
        return 0
    
    logger.info(f"Found {len(video_files)} video(s) to transcode")
    success_count = 0
    
    for file_path in video_files:
        if transcode_file(file_path, vcodec, crf, acodec, delete):
            success_count += 1
    
    logger.info(f"Successfully transcoded {success_count}/{len(video_files)} video(s)")
    return success_count


def transcode_folder(path: str, vcodec: str, crf: int, acodec: str, delete: bool) -> int:
    """Transcode todos los videos en un directorio (no recursivo)."""
    video_files = [
        os.path.join(path, file) 
        for file in os.listdir(path) 
        if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS
    ]
    
    if not video_files:
        logger.warning("No videos found in directory")
        return 0
    
    logger.info(f"Found {len(video_files)} video(s) to transcode")
    success_count = 0
    
    for file_path in video_files:
        if transcode_file(file_path, vcodec, crf, acodec, delete):
            success_count += 1
    
    logger.info(f"Successfully transcoded {success_count}/{len(video_files)} video(s)")
    return success_count


def transcode_file(file_path: str, vcodec: str, crf: int, acodec: str, delete: bool) -> bool:
    """Transcode un archivo de video si necesita compresión."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in VIDEO_EXTENSIONS:
        logger.error(f"File is not a supported video: {file_path}")
        return False
    
    try:
        current_codec = get_codec(file_path)
    except Exception as e:
        logger.error(f"Error reading video codec for {file_path}: {e}")
        return False
    
    file_name = os.path.basename(file_path)
    codec_info = f"{file_name} {DIM}({current_codec}){RESET}"
    
    # Saltar si ya es HEVC o VP9 (códecs eficientes)
    if current_codec.lower() in ('hevc', 'vp9'):
        logger.info(f"{codec_info} {RED}❌ Already efficient codec{RESET}")
        return False
    
    logger.info(f"{codec_info} {GREEN}✔️ Will be transcoded{RESET}")
    
    output_path = send_transcode(
        os.path.dirname(file_path), 
        os.path.basename(file_path), 
        vcodec, 
        crf, 
        acodec
    )
    
    if output_path is None:
        return False
    
    try:
        original_size = os.path.getsize(file_path)
        output_size = os.path.getsize(output_path)
    except OSError as e:
        logger.error(f"Error reading file sizes: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return False
    
    if original_size < output_size:
        os.remove(output_path)
        logger.warning(f"Transcoding skipped: output larger than original ({original_size/1024**2:.2f}MB → {output_size/1024**2:.2f}MB) ❌")
        return False
    
    original_size_mb = original_size / 1024**2
    output_size_mb = output_size / 1024**2
    saved_mb = original_size_mb - output_size_mb
    saved_percent = (1 - output_size / original_size) * 100
    
    logger.info(f"Transcoding complete: {original_size_mb:.2f}MB → {output_size_mb:.2f}MB (saved {saved_mb:.2f}MB, {saved_percent:.1f}%) {GREEN}✔️{RESET}")
    
    if delete:
        try:
            os.remove(file_path)
            os.rename(output_path, file_path)
            logger.debug("Replaced original with compressed version")
        except OSError as e:
            logger.error(f"Error replacing original file: {e}")
            return False
    
    return True


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="VideoSlim",
        description="Video compression tool using FFmpeg with HEVC codec",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  ./VideoSlim --path /videos/
  ./VideoSlim --path video.mp4 --crf 23
  ./VideoSlim --path /videos/ --vcodec hevc --crf 28 --acodec aac
  ./VideoSlim --path /videos/ --recursive --delete
        """
    )
    parser.add_argument(
        "--path", "-p",
        type=str,
        required=True,
        help="Path to file or directory"
    )
    parser.add_argument(
        "--vcodec", "-v",
        type=str,
        default="hevc",
        help="Video codec (hevc, h264, vp9, av1) [default: hevc]"
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=28,
        help="Constant Rate Factor for quality (0-51, lower=better) [default: 28]"
    )
    parser.add_argument(
        "--acodec", "-a",
        type=str,
        default="aac",
        help="Audio codec (aac, mp3, opus, flac, ac3) [default: aac]"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Search recursively in directories"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete original files after successful compression"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress console output"
    )
    
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # Mostrar información del modo
    mode = "Release (Binary)" if getattr(sys, 'frozen', False) else "Development"
    logger.info(f"{CYAN}{BOLD}VideoSlim{RESET} - Mode: {mode}")
    logger.info(f"  FFmpeg: {get_ffmpeg_path()}")
    logger.info(f"  FFprobe: {get_ffprobe_path()}")
    
    # Check if FFmpeg binaries are available
    if not check_ffmpeg_installed():
        logger.error("FFmpeg binaries not found!")
        logger.info("Please ensure ffmpeg and ffprobe are in the same directory as the executable.")
        sys.exit(1)
    
    # Validate parameters
    valid, error_msg = validate_codecs(args.vcodec, args.acodec, args.crf)
    if not valid:
        logger.error(error_msg)
        sys.exit(1)
    
    path = os.path.abspath(args.path)
    
    if not os.path.exists(path):
        logger.error(f"Path does not exist: {path}")
        sys.exit(1)
    
    logger.info(f"{CYAN}{BOLD}VideoSlim{RESET} - Starting compression")
    logger.info(f"  Codec: {args.vcodec} | CRF: {args.crf} | Audio: {args.acodec}")
    
    if os.path.isdir(path):
        if args.recursive:
            transcode_recursive(path, args.vcodec, args.crf, args.acodec, args.delete)
        else:
            transcode_folder(path, args.vcodec, args.crf, args.acodec, args.delete)
    else:
        transcode_file(path, args.vcodec, args.crf, args.acodec, args.delete)


if __name__ == "__main__":
    main()
