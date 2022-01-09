from math import sqrt

# Convert a 2d array of RGB pixels to a list of y-coordinates for each x-coordinate
def pixels_to_list(pixels, width, height):
	y_coordinates = []
	# Average out the y-coordinates for each x-coordinate
	for i in range(width):
		sum_of_y = 0
		total_y = 0
		for a in range(height):
			# Luminance equation taken from https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
			luminance = sqrt(0.299 * pixels[i, a][0] ** 2 + 0.587 * pixels[i, a][1] ** 2 + 0.114 * pixels[i, a][2] ** 2)
			if luminance < 127.5:
				sum_of_y += a
				total_y += 1

		if total_y != 0:
			y_coordinates.append(height - sum_of_y/total_y)

	return y_coordinates

# Return a list of coefficients for the derivative of the given polynomial
def poly_derivative(coeffs):
	poly_degree = len(coeffs) - 1
	deriv_coeffs = []
	for i in range(len(coeffs) - 1):
		deriv_coeffs.append(coeffs[i] * (poly_degree - i))

	return deriv_coeffs

# Return the value for f(x) given its coefficients and x
def evaluate_poly(coeffs, x):
	return sum([coeffs[i] * x ** (len(coeffs) - 1 - i) for i in range(len(coeffs))])