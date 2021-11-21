import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide='ignore', invalid='ignore')

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 main.py [filename]")
		sys.exit()

	nonce = os.urandom(8).hex()
	inputfile = sys.argv[1].split('.')[0]
	svgfile = f'{inputfile}-{nonce}.svg'

	res = os.system(f'potrace -b svg -a 200 {sys.argv[1]} -o {svgfile}')
	if res != 0:
		print("Specify a valid filename")
		sys.exit()

	print("[+] Converted to an svg file")

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

	plotfile = f'{inputfile}_deriv.png'
	print(f"[+] Plotted derivative graph to {plotfile}")

	os.remove(svgfile)
	plt.savefig(plotfile)
