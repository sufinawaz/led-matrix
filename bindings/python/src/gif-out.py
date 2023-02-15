#!/usr/bin/env python

import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageSequence, GifImagePlugin

# Matrix size
size = 64, 64

# Configuration matrix for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.brightness = 20
options.chain_length = 1
options.parallel = 1
options.led_rgb_sequence = 'RBG'
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = 0
matrix = RGBMatrix(options = options)

# Pull back in resized gif
image = Image.open("out.gif")

# Loop through gif frames and display on matrix.
while True:
    for frame in range(0, image.n_frames):
        # print(image.n_frames)
        image.seek(frame)
        # print(image)
        matrix.SetImage(image.convert('RGB'))
        time.sleep(0.1)

# Handle quiting
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
