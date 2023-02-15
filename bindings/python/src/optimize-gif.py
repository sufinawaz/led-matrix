#!/usr/bin/env python
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageSequence

if len(sys.argv) < 2:
    sys.exit("Require a gif argument")
else:
    image_file = sys.argv[1]

gif = Image.open(image_file)

try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("provided image is not a gif")

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.brightness = 20
options.chain_length = 1
options.parallel = 1
options.led_rgb_sequence = 'RBG'
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)

size = 64, 32
im = Image.open(image_file)
# Get gif frames
frames = ImageSequence.Iterator(im)


# Resize gif frames to matrix
def thumbnails(frames):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail(size, Image.ANTIALIAS)
        yield thumbnail


frames = thumbnails(frames)
# Save output
om = next(frames)  # Handle first frame separately
om.info = im.info  # Copy sequence info
om.save("out.gif", save_all=True, append_images=list(frames))
