# VideoSlim 
> A video compression software

![GitHub release (latest by date)](https://img.shields.io/github/release-date/viera97/VideoSlim)
![Language](https://img.shields.io/badge/language-python-green)
![Platforms](https://img.shields.io/badge/platforms-Linux%20,%20Windows%20and%20Mac-blue)
![License](https://img.shields.io/github/license/viera97/VideoSlim)

#### What is VideoSlim

VideoSlim is a video compression tool made in python, and using ffmpeg binaries for windows, linux and mac. It transcodes videos into `hevc` codec, wich is one of the lastest and more efficient video codec, it tries to keep the video quality the same. For audio the codec `aac` is used, and a cfr of 28 wich is a good number for quality and file size. You can change all this parameters in the cli interface.

For now is a console application, but a gui interface will be made for impoving user friendliness.

## Installation

For the installation you can download the binaries and use it as a portable app, a proper installation will be made, or install the dependencies and use it as a python script.

```bash
git clone https://github.com/viera97/VideoSlim.git
cd VideoSlim
pip install -r requirements.txt
```

As the VideoSlim depends on ffmpeg you need to install it into your system and make it accesible in the variable path.

### Windows
```bash
winget ffmpeg
```
### Linux
It is probably on you package manager so:

**For Arch based distro**
```bash
pacman -S ffmpeg
```

**For Debian based distro**
```bash
apt install ffmpeg
```

**For Fedora**
```bash
dnf install ffmpeg
```

and then you just have to execute the python file `main.py` with the parameters.

If you want to compile it your self just need to do:

```bash
pyinstaller --onefile main.py
```

It will generate into the directory `dist` a binary for your operative system.

You can also compile it with the ffmpeg and probe binaries included.

```bash
pyinstaller --onefile --add-data "/path/to/your/ffmpeg/binary:." --add-data "path/to/your/ffprobe/binary:." main.py
```

## Usage

For the usage you need to use a terminal emulator of some kind.

```bash
./VideoSlim --path="/path/to/folder/or/file/"
```

you can add some more parameters like `vcodec`, `acodec` and `crf`. an example:

```bash
./VideoSlim --path="/path/to/folder/or/file/" --vcodec=`hevc` --acodec=`acc` --crf=28
```

If you are using the python script you should execute:

```bash
python main.py --path="/path/to/folder/or/file/"
```

## License

VideSlim is licensed under the [GPL-3.0 license](/LICENSE).