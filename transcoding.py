import ffmpeg

#Release
#import os
#import sys

#global ffmpeg_binary_path, ffprobe_binary_path

#ffmpeg_binary_path = os.path.join(sys._MEIPASS, 'ffmpeg')
#ffprobe_binary_path = os.path.join(sys._MEIPASS, 'ffprobe')

def get_codec(input_file):
    #Release
    #probe = ffmpeg.probe(input_file, ffprobe_binary_path)

    probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    
    if video_stream:
        file_codec = video_stream['codec_name']
    
    return file_codec

def transcode(input_file, output_file, vcodec="hevc", crf=18, acodec='aac'):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, vcodec=vcodec, crf=crf, acodec=acodec, ab=128000)

    #Release
    #ffmpeg.run(stream, quiet=False, cmd=[ffmpeg_binary_path])
    ffmpeg.run(stream, quiet=False)