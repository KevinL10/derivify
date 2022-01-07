from PIL import Image
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide="ignore", invalid="ignore")

# Takes in the image located at input_file and saves the derivative image at output_file
def derivify_bezier(input_file, output_file):
    svg_path = f"{output_file}.svg"
    bmp_path = f"{output_file}.bmp"

    # Save the image as a .bmp file
    Image.open(input_file).save(bmp_path)

    res = os.system(f"potrace -b svg -a 200 {bmp_path} -o {svg_path}")
    if res != 0:
        return

    with open(svg_path, "r") as f:
        curves = f.read()

    curves = parse_svg(curves)

    t = np.arange(0, 1, 0.001)
    x_data = []
    y_data = []

    # Keep track of all the points on the raw derivative graph
    for c in curves:
        try:
            x_values = bezier_x(c, t)
            slope_values = bezier_slope(c, t)
            x_data = np.concatenate([x_data, x_values])
            y_data = np.concatenate([y_data, slope_values])
        except ValueError:
            pass

    # Smoothen out the graph
    plt.figure()
    window_size = (
        (len(x_data) // 50) + 1 + (len(x_data) // 50) % 2
    )  # Window size must be odd
    y_hat = savgol_filter(y_data, window_size, 3)
    plot = plt.plot(x_data, y_hat)

    # Remove frame from matplotlib graph
    ax = plt.gca()
    ax.set_ylim([-5, 5])
    ax.axis("off")
    plt.savefig(output_file)

    # Clean up .bmp and .svg files
    os.remove(svg_path)
    os.remove(bmp_path)
