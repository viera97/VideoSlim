import os
import transcoding
import argparse

global video_extensions
video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv',
                    '.webm', '.m4v', '.3gp', '.ts', '.m2ts', '.vob',
                    '.ogv', '.divx', '.mpg']

def send_transcode(path, video_file):
    input_file_path = os.path.join(path,video_file)
    output_file_aux = os.path.splitext(video_file)
    
    output_file = output_file_aux[0]+'_encoded'+output_file_aux[1]
    output_file_path = os.path.join(path, output_file)
    
    try:
        print("\033[0;32m"+'Transcoding  '+"\033[0m"+"\033[5m\033[1m"+'⭕'+"\033[0m")
        transcoding.transcode(input_file_path, output_file_path, vcodec, crf, acodec)
    except KeyboardInterrupt:
        print("\n\033[0;31m"+'Transcoding Terminated'+"\033[0m")
        os.remove(output_file_path)
        os._exit(0)
    
def transcode_folder(path):

    video_files = [file for file in os.listdir(path) if os.path.splitext(file)[1].lower() in video_extensions]

    if len(video_files) == 0:
        print("\n\033[0;31m"+'Not videos found'+"\033[0m")
    else:
        video_files_codecs = []
        for file in video_files:
            video_files_codecs.append(transcoding.get_codec(os.path.join(path, file)))

        for i in range(len(video_files)):
            text = "\033[1;30m"+"\033[1m"+video_files[i]+"\033[0m"+'\033[0;37m  --  \033[0m'+"\033[1;30m"+"\033[1m"+video_files_codecs[i]+"\033[0m"
            if video_files_codecs[i].lower() != "vp9" and video_files_codecs[i].lower() != "hevc":
                text += '  ✔️'
                print(text)
                send_transcode(path, video_files[i])

                output_file_path = os.path.join(path, os.path.splitext(video_files[i])[0]+'_encoded'+os.path.splitext(video_files[i])[1])
                if os.path.getsize(os.path.join(path,video_files[i])) < os.path.getsize(output_file_path):
                    os.remove(output_file_path)
                    print("\033[0;31m"+'Transcoding finished, but file size bigger  '+"\033[0m"+"\033[5m\033[1m"+'❌'+"\033[0m")
                else:
                    print("\033[0;32m"+f'Transcoding finished, file size decresed from {round(os.path.getsize(os.path.join(path,video_files[i]))/1024**2,2)} Mb to {round(os.path.getsize(output_file_path)/1024**2,2)} Mb'+"\033[0m"+"\033[5m\033[1m"+'✔️'+"\033[0m")
                    os.remove(os.path.join(path,video_files[i]))
                    os.rename(output_file_path, os.path.join(path,video_files[i]))
            else:
                text += '  ❌'
                print(text)

def transcode_file(path):
    if os.path.splitext(path)[1].lower() in video_extensions:
        send_transcode(os.path.dirname(path),path, transcoding.get_codec(path))
    else:
        print("\n\033[0;31m"+'The selected file is not a video'+"\033[0m")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to file or directory")
    parser.add_argument("--vcodec", type=int, help="Video Codec")
    parser.add_argument("--crf", type=int, help="Video CRF")
    parser.add_argument("--acodec", type=int, help="Audio Codec")
    args = parser.parse_args()

    global vcodec, crf, acodec

    vcodec='hevc'
    crf=28
    acodec='aac'

    if args.path != None:
        path = args.path

        if args.vcodec != None:
            vcodec = args.vcodec
        if args.crf != None:
            crf = args.crf
        if args.acodec != None:
            acodec = args.acodec

        if os.path.isdir(path):
            transcode_folder(path)
        else:
            transcode_file(path)