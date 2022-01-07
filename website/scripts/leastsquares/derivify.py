from PIL import Image
from utils import *
from numpy import polyfit
import numpy as np

WINDOW_NUM = 20
MIN_WINDOW_SIZE = 25
POLY_DEGREE = 3

# Takes in the image located at input_file and saves the derivative image at output_file
def derivify_least_squares(input_file, output_file):
	im = Image.open(input_file)
	pixels = im.load()
	width, height = im.size
	y_coordinates = pixels_to_list(pixels, width, height)
	deriv_y_coordinates = []

	# Break y_coordinates into WINDOW_NUM sublists and find the best fit polynomial for each
	window_size = max(width // WINDOW_NUM, MIN_WINDOW_SIZE)

	for i in range(0, len(y_coordinates), window_size):
		y_coordinates_sublist = y_coordinates[i:i + window_size]
		x_coordinates_sublist = list(range(i, i + len(y_coordinates_sublist)))
		best_fit_poly = polyfit(x_coordinates_sublist, y_coordinates_sublist, POLY_DEGREE)
		deriv_coeffs = poly_derivative(best_fit_poly)

		for x in x_coordinates_sublist:
			deriv_y_coordinates.append(evaluate_poly(deriv_coeffs, x))

	return deriv_y_coordinates


derivify_least_squares('test.png', 'out.png')