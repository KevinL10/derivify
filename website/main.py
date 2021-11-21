import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide='ignore', invalid='ignore')

def deriv(input_file, output_file):
	svgfile = f'{output_file}.svg'

	res = os.system(f'potrace -b svg -a 200 {input_file} -o {svgfile}')
	if res != 0:
		return

	with open(svgfile, 'r') as f:
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

	os.remove(svgfile)
	plt.savefig(output_file)
