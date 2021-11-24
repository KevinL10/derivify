from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide='ignore', invalid='ignore')

def deriv(input_file, output_file):
	svg_path = f'{output_file}.svg'
	bmp_path = f'{output_file}.bmp'

	# Save the image as a .bmp file
	Image.open(input_file).save(bmp_path)


	res = os.system(f'potrace -b svg -a 200 {bmp_path} -o {svg_path}')
	if res != 0:
		return

	with open(svg_path, 'r') as f:
		curves = f.read()

	curves = parse_svg(curves)

	t = np.arange(0, 1, 0.001)

	plt.figure()
	for c in curves:
		try:
			plot = plt.plot(bezier_x(c, t), bezier_slope(c, t))
		except:
			pass

	# Remove frame from matplotlib graph
	ax = plt.gca()
	ax.axis('off')
	plt.savefig(output_file)

	# Clean up .bmp and .svg files
	os.remove(svg_path)
	os.remove(bmp_path)