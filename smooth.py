from PIL import Image
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide='ignore', invalid='ignore')

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 main.py [filename]")
		sys.exit()

	file_name = sys.argv[1].split('.')[0]
	svg_path = f'{sys.argv[1]}.svg'
	bmp_path = f'{sys.argv[1]}.bmp'

	# Save the image as a .bmp file
	Image.open(sys.argv[1]).save(bmp_path)

	res = os.system(f'potrace -b svg -a 200 {bmp_path} -o {svg_path}')
	if res != 0:
		print("Specify a valid filename")
		sys.exit()

	print("[+] Converted to an svg file")

	with open(svg_path, 'r') as f:
		curves = f.read()

	curves = parse_svg(curves)
	t = np.arange(0, 1, 0.001)
	x_data = []
	y_data = []

	# Plot the raw derivative graph
	plt.figure()
	for c in curves:
		try:
			x_values = bezier_x(c, t)
			slope_values = bezier_slope(c, t)

			plot = plt.plot(x_values, slope_values)
			x_data = np.concatenate([x_data, x_values])
			y_data = np.concatenate([y_data, slope_values])
		except ValueError:
			pass

	# Remove frame from matplotlib graph
	ax = plt.gca()
	ax.axis('off')

	plotfile = f'{file_name}_raw_deriv.png'
	plt.savefig(plotfile)
	print(f"[+] Plotted raw derivative graph to {plotfile}")

	# Plot the smoothened derivative graph
	plt.figure()
	window_size = (len(x_data) // 50) + 1 + (len(x_data) // 50) % 2  # Window size must be odd
	y_hat = savgol_filter(y_data, window_size, 3)
	plot = plt.plot(x_data, y_hat)

	# Remove frames from graph
	ax = plt.gca()
	ax.axis('off')

	plotfile = f'{file_name}_smooth_deriv.png'
	plt.savefig(plotfile)
	print(f"[+] Plotted smooth derivative graph to {plotfile}")

	# Clean up .bmp and .svg files
	os.remove(svg_path)
	os.remove(bmp_path)