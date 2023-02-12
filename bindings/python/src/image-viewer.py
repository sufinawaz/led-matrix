#!/usr/bin/env python
import time
import sys
from rgbmatrix import graphics
font = graphics.Font()
font.LoadFont("/home/pi/code/matrix/fonts/7x13.bdf")
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.drop_privileges = False
options.brightness = 20
options.chain_length = 1
options.parallel = 1
options.led_rgb_sequence = 'rbg'
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)
text = 'LAUGHING IS THE \n BEST MEDICINE'
# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
# image.text((28, 36), "nice Car", fill=(255, 0, 0))
#image.text((5, 5), text, font = font, align ="left")
matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
