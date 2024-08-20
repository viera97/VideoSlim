import ffmpeg
import os
import sys

global ffmpeg_binary_path, ffprobe_binary_path

#ffmpeg_binary_path = os.path.join(os.path.dirname(__file__), 'resources', 'ffmpeg')
#ffprobe_binary_path = os.path.join(os.path.dirname(__file__), 'resources', 'ffprobe')

ffmpeg_binary_path = os.path.join(sys._MEIPASS, 'ffmpeg')
ffprobe_binary_path = os.path.join(sys._MEIPASS, 'ffprobe')

def get_codec(input_file):
    probe = ffmpeg.probe(input_file, ffprobe_binary_path)
    #probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    
    if video_stream:
        file_codec = video_stream['codec_name']
    
    return file_codec

def transcode(input_file, output_file, vcodec="hevc", crf=18, acodec='aac'):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, vcodec=vcodec, crf=crf, acodec=acodec, ab=128000)
    ffmpeg.run(stream, quiet=False, cmd=[ffmpeg_binary_path])

if __name__ == "__main__":
    input_file = "/mnt/Work/Learn Organizar/Hablar con Poder/Introducción.mp4"
    output_file = "/mnt/Work/Learn Organizar/Hablar con Poder/Introducción.mkv"

    input_file_codec = get_codec(input_file)

    if input_file_codec.lower() != "vp9" and input_file_codec.lower() != "hevc":
            transcode(input_file, output_file)