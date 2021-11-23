from PIL import Image
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
	svg_path = f'{file_name}.svg'
	bmp_path = f'{file_name}.bmp'

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

	plt.figure()
	for c in curves:
		try:
			plot = plt.plot(bezier_x(c, t), bezier_slope(c, t))
		except:
			pass

	# Remove frame from matplotlib graph
	ax = plt.gca()
	ax.axis('off')

	plotfile = f'{file_name}_deriv.png'
	plt.savefig(plotfile)
	print(f"[+] Plotted derivative graph to {plotfile}")

	# Clean up .bmp and .svg files
	os.remove(svg_path)
	os.remove(bmp_path)