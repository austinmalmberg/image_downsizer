import os
from typing import Tuple
from pathlib import Path

from PIL import Image

import config as cfg

def main():
    downsize_images_in_directory(cfg.directory, cfg.max_size, append=cfg.append, output_file_type=cfg.output_file_type)


def downsize_images_in_directory(directory: str, max_size: Tuple[int, int], append: str = None, output_file_type: str = None) -> None:
    """ Downsizes all JPG, JPEG, and PNG files in the given directory. """

    supported_file_types = ('.jpg', '.jpeg', '.png', '.bmp')

    if output_file_type is not None and output_file_type not in supported_file_types:
        raise ValueError(f'Unsupported output file type, {output_file_type}')

    resize_count: int = 0

    # iterate over images
    for child in Path(directory).iterdir():
        # ignore non-files and unsupported file types
        if not child.is_file() or child.suffix.lower() not in supported_file_types:
            continue

        # resize the image and append 
        resized: bool = downsize_image(child.absolute(), max_size, append=append, output_file_type=output_file_type)

        if resized:
            resize_count += 1
        else:
            print (f'{child.name} within size constraints')

    print(f'Completed. {resize_count} images resized.')



def downsize_image(path: Path, max_size: Tuple[int, int], append: str = None, output_file_type: str = None) -> bool:
    """
    Attempts to downsize the image at image_path. Returns true if the downsize was successful.
    Returns false if the image is within the max_size constraints.
    """ 

    print(f'Resizing {path.name}...')

    # open the image
    image = Image.open(path.absolute())

    # get the optimal size for the image, ensuring the dimensions are less than both size dimensions
    new_size = get_optimal_size(image.size, max_size)

    if new_size is None:
        return False

    # resize the image to its new size
    new_image = image.resize(new_size)

    new_name = path.name.replace(path.suffix, '')

    if append is not None:
        new_name = f'{new_name}{append}'

    # change the file type, if provided
    file_type = path.suffix if output_file_type is None else output_file_type
    output_path = f'{path.parent}\{new_name}{file_type}'

    # save the image
    new_image.save(output_path)

    print(f'{path.name} resized and saved to "{output_path}"')

    return True


def get_optimal_size(size: Tuple[int, int], max_size: Tuple[int, int]) -> Tuple[int, int]:
    """
    Scales down size to fall within max_size while maintaining the same aspect ration.
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


if __name__ == '__main__':
    main()
