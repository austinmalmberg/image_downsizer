import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from PIL import Image

supported_image_formats = ['jpg', 'jpeg', 'png', 'bmp']

def main():
    parser: ArgumentParser = _build_parser()
    parsed_args: ParseOptions = parser.parse_args(sys.argv[1:], namespace=ParseOptions)

    path = Path(parsed_args.path)

    if path.is_dir():
        downsize_images_in_directory(path, **vars(parsed_args))
    else:
        downsize_image(path, **vars(parsed_args))


def downsize_images_in_directory(directory: Path, max_size: Tuple[int, int], overwrite: bool = False, append: str = None, output_dir: str = None, output_format: str = None, **kwargs) -> None:
    """ Downsizes all supported image files in the given directory. """

    if output_format is not None and output_format not in supported_image_formats:
        raise ValueError(f'Unsupported output format: {output_format}')

    resize_count: int = 0

    # iterate over the directory files
    for child in directory.iterdir():

        # ignore non-files and unsupported file types
        if not child.is_file() or child.suffix.lower().replace('.', '', 1) not in supported_image_formats:
            continue

        # resize the image
        resized: bool = downsize_image(child, max_size, overwrite=overwrite, append=append, output_dir=output_dir, output_format=output_format)

        if resized:
            resize_count += 1

    print(f'Done! {resize_count} image(s) resized.')



def downsize_image(image_path: Path, max_size: Tuple[int, int], overwrite: bool = False, append: str = None, output_dir: str = None, output_format: str = None, **kwargs) -> bool:
    """
    Attempts to downsize the image at path and saves it to output_format (or path.parent when not specified).
    Returns true if the downsize was successful. Otherwise, returns false if the image is already within the max_size constraints.
    """

    if output_dir is None:
        output_dir = image_path.parent
    else:
        # create the output directory when it doesn't exist
        output_path: Path = Path(output_dir)
        if not output_path.exists():
            output_path.mkdir()

    if output_format is None:
        # remove the first period from the suffix to conform with supported_image_formats
        output_format = image_path.suffix.replace('.', '', 1)

    if output_format not in supported_image_formats:
        # ensure the output format is a supported image format
        # this also serves to validate the image_path suffix when an output_format is not given
        raise ValueError(f'Unsupported output format: {output_format}')

    name_wo_ext = image_path.name.replace(image_path.suffix, '')
    if append is not None:
        name_wo_ext = f'{name_wo_ext}{append}'

    # construct the output path
    output_path: Path = Path(f'{output_dir}\{name_wo_ext}.{output_format}')

    if output_path.exists() and not overwrite:
        raise DuplicateFileNameError(f'{output_path} already exists. Use --overwrite to overwrite the file or provide one or more of the '
                                     '--append, --format, or --output arguments to ensure the output path is different.')

    # open the image
    image = Image.open(image_path.absolute())

    # get the optimal size for the image, ensuring the dimensions are less than both size dimensions
    new_size = get_optimal_size(image.size, max_size)

    if new_size is None:
        print (f'{image_path.name} within size constraints.')
        return False

    print(f'Resizing {image_path.name}...', end='')

    # resize the image to its new size
    new_image = image.resize(new_size)

    # save the image
    new_image.save(output_path)

    print(f'saved to {output_path}.')

    return True


def get_optimal_size(size: Tuple[int, int], max_size: Tuple[int, int]) -> Tuple[int, int]:
    """
    Scales down size to fall within max_size while maintaining the same aspect ratio.
    Returns a (int, int) tuple for the optimal size of the image.
    """

    # get the width and height component of the size tuple
    w, h = size
    max_width, max_height = max_size

    # find the value needed to scale down the image
    scale_width = max_width / w
    scale_height = max_height / h

    # use the minimum scaling value to ensure both dimensions are within the range
    scale = min(scale_width, scale_height)

    # image is already within the max_size constraints
    if scale >= 1.0:
        return None

    # apply the scale to width and height, convert them, and return a tuple
    return (int)(w * scale), (int)(h * scale)


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
            prog='Image Downsizer',
            description='Decrease the resolution of images.')

    parser.add_argument('path',
                        help=f'The image or directory to preform the operation on. Supported image formats: {supported_image_formats}.')

    parser.add_argument('--append',
                        dest='append',
                        help='Additional text that is appended to the resized images file name.')

    parser.add_argument('-f', '--format',
                        choices=supported_image_formats,
                        dest='output_format',
                        help='The output format of the downsized file. When not provided, uses the same image format as the original')

    parser.add_argument('-o', '--output',
                        dest='output_dir',
                        help='The output directory for scaled down images. Defaults to the parent directory. NOTE: '
                            'Original files may be overridden if the output file name and type matches that of the original.')

    parser.add_argument('--overwrite',
                        action='store_true',
                        dest='overwrite',
                        help='Flag to overwrite any existing file. WARNING: This may or may not be the original image!')

    parser.add_argument('-s', '--size',
                        nargs=2,
                        type=int,
                        default=(1920, 1080),
                        dest='max_size',
                        help='The maximum width and height of the image. Images with dimensions less than these constraints'
                            'will not be downsized. Defaults to 1920 x 1080.')

    return parser

@dataclass
class ParseOptions:
    path: str
    max_size: Tuple[int, int]
    append: str
    output_dir: str
    output_format: str
    overwrite: bool


class DuplicateFileNameError(RuntimeError):
    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)

        self.message = message

    def __repr__(self) -> str:
        return f'{self.message}'

    def __str__(self) -> str:
        return f'{self.message}'

if __name__ == '__main__':
    main()
