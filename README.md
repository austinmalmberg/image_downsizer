# Image Downsizer

Downsize images in a directory to fall within the configured maximum dimensions. Supports changing the output's file name and file type.

## Prequisites

- [Python](https://www.python.org/) >= 3.11
- [Pip](https://pypi.org/project/pip/)

## Setup

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

### Update configuration

Use your favorite IDE or text editor to update the configuration variables in `config.py`

### Run the file

```
(venv) image_downsizer> python main.py
```

__NOTE:__ If python is not recognized, reference the full python path or add the python path to your system's environment variables.

