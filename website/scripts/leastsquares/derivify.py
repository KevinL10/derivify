from PIL import Image
from utils import *
import numpy as np

# Takes in the image located at input_file and saves the derivative image at output_file
def derivify_least_squares(input_file, output_file):
	im = Image.open(input_file)
	pixels = im.load()
	y_coordinates = pixels_to_list(pixels, im.size)

	print(y_coordinates)


derivify_least_squares('test.png', 'out.png')