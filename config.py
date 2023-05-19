
# the maximum size (width and height) of the image. When resized,
# both width and height will fall within their respective constraints
# while maintaining the same aspect ratio.
max_size = 1080, 720

# the directory to iterate through. Any images where its width and/or
# height is larger than those specified in max_size will be resized
directory = 'path/to/directory'

# The text to be appended to the resized file name. When not given,
# the original file may be overwritten.
append = '_resize'

# The file type of the resized image. Setting this variable to None
# will cause the resized image to inherit the original file type.
output_file_type = '.jpg'
