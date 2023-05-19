# Image Downsizer

Downsize images in a directory to fall within the configured maximum dimensions. Supports changing the output's file name and file type.


## Prequisites

- [Python](https://www.python.org/) >= 3.11
- [Pip](https://pypi.org/project/pip/)


## Development

### Download the Source Code

```
> git clone https://github.com/austinmalmberg/image_downsizer.git
```


### Change directories

```
> cd image_downsizer
```


### Create and activate a virtual environment

```
image_downsizer> python -m venv venv/
image_downsizer> source venv/Scripts/activate
```


### Download dependencies

```
(venv) image_downsizer> pip install -r requirements.txt
```


### Running the file

```
(venv) image_downsizer> python image_downsizer.py [-h]
```

__NOTE:__ If python is not recognized, reference the full python path or add the python path to your system's environment variables.


### Creating an executable

```
(venv) image_downsizer> pyinstaller --hiddenimport PIL --onefile [--clean] image_downsizer.py
```

Executable will be created at `dist/image_downsizer.exe`.

## Arguments

Arguments must be provided to the program or executable to run.

```
> image_downsizer.exe -h
usage: Image Downsizer [-h] [--append APPEND] [-f {jpg,jpeg,png,bmp}]
                       [-o OUTPUT_DIR] [--overwrite] [-s MAX_SIZE MAX_SIZE]
                       path

Decrease the resolution of images.

positional arguments:
  path                  The image or directory to preform the operation on.
                        Supported image formats: ['jpg', 'jpeg', 'png',
                        'bmp'].

options:
  -h, --help            show this help message and exit
  --append APPEND       Additional text that is appended to the resized images
                        file name.
  -f {jpg,jpeg,png,bmp}, --format {jpg,jpeg,png,bmp}
                        The output format of the downsized file. When not
                        provided, uses the same image format as the original.
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        The output directory for scaled down images. Defaults
                        to the parent directory.
  --overwrite           Flag to overwrite any existing file at the
                        destination. WARNING: This may or may not be the
                        original image path!
  -s MAX_SIZE MAX_SIZE, --size MAX_SIZE MAX_SIZE
                        The maximum width and height of the image. Images with
                        dimensions less than these constraints will not be
                        downsized. Defaults to 1920 x 1080.
```