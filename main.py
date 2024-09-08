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

def transcode_recursive(path):
    video_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1].lower() in video_extensions:
                video_files.append(os.path.join(root, file))

    if len(video_files) == 0:
        print("\n\033[0;31m"+'Not videos found'+"\033[0m")
        return
    
    for file in video_files:
        transcode_file(file)

def transcode_folder(path):

    video_files = [os.path.join(path, file) for file in os.listdir(path) if os.path.splitext(file)[1].lower() in video_extensions]
    if len(video_files) == 0:
        print("\n\033[0;31m"+'Not videos found'+"\033[0m")
        return
    
    for file in video_files:
        transcode_file(file)

def transcode_file(path):
    if not os.path.exists(path):
        print("\n\033[0;31m"+'Not videos found'+"\033[0m")
        return
    
    if os.path.splitext(path)[1].lower() in video_extensions:
        video_files_codecs = transcoding.get_codec(path)
        text = "\033[1;30m"+"\033[1m"+path+"\033[0m"+'\033[0;37m  --  \033[0m'+"\033[1;30m"+"\033[1m"+video_files_codecs+"\033[0m"
        if transcoding.get_codec(path).lower() != "vp9" and transcoding.get_codec(path).lower() != "hevc":
            text += '  ✔️'
            print(text)

            send_transcode(os.path.dirname(path),path)
            output_file_path = os.path.join(os.path.splitext(path)[0]+'_encoded'+os.path.splitext(path)[1])

            if os.path.getsize(path) < os.path.getsize(output_file_path):
                    os.remove(output_file_path)
                    print("\033[0;31m"+'Transcoding finished, but file size bigger  '+"\033[0m"+"\033[5m\033[1m"+'❌'+"\033[0m")

            else:
                print("\033[0;32m"+f'Transcoding finished, file size decresed from {round(os.path.getsize(path)/1024**2,2)} Mb to {round(os.path.getsize(output_file_path)/1024**2,2)} Mb'+"\033[0m"+"\033[5m\033[1m"+'✔️'+"\033[0m")
                if delete:
                    os.remove(path)
                    os.rename(output_file_path,path)
                
        else:
            text += '  ❌'
            print(text)
    else:
        print("\n\033[0;31m"+'The selected file is not a video'+"\033[0m")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to file or directory")
    parser.add_argument("--vcodec", type=int, help="Video Codec")
    parser.add_argument("--crf", type=int, help="Video CRF")
    parser.add_argument("--acodec", type=int, help="Audio Codec")
    parser.add_argument("--recursive", type=str, help="Recursive finder")
    parser.add_argument("--delete", type=str, help="Delete Original file")
    args = parser.parse_args()

    global vcodec, crf, acodec, recursive, delete

    vcodec='hevc'
    crf=28
    acodec='aac'
    recursive = False
    delete = True

    if args.path != None:
        path = args.path

        if args.vcodec != None:
            vcodec = args.vcodec
        if args.crf != None:
            crf = args.crf
        if args.acodec != None:
            acodec = args.acodec
        if args.delete != None:
            if args.delete.lower() == "false":
                delete = False
        if args.recursive != None:
            if args.recursive.lower() == "true":
                recursive = True

        if os.path.isdir(path):
            if recursive:
                transcode_recursive(path)
            else:
                transcode_folder(path)
        else:
            transcode_file(path)