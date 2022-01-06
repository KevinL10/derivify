from PIL import Image
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from utils import *

np.seterr(divide="ignore", invalid="ignore")

def parse_svg(txt):
    txt = txt.split('<path d="')[-1]
    txt = txt.split('z"/>')[0]
    txt = txt.replace("\n", " ")
    txt = txt.split(" ")

    # Take out the initial M x y instruction
    txt = txt[2:]

    # Take out the initial c instruction
    txt[0] = txt[0][1:]

    txt = [int(num) for num in txt]
    curves = []
    cur_pos = (0, 0)

    for i in range(0, len(txt) - 2, 6):
        # Create a new curve "c"
        c = []
        c.append(cur_pos)

        for a in range(3):
            # Add the position relative to the current one
            c.append((cur_pos[0] + txt[i + a * 2], cur_pos[1] + txt[i + a * 2 + 1]))

        # Update the current position
        cur_pos = c[-1]
        curves.append(c)

    return curves[:-1]

# Produce the x coordinate of a Bezier curve at point t
def bezier_x(c, t):
    return (
        (1 - t) ** 3 * c[0][0]
        + 3 * (1 - t) ** 2 * t * c[1][0]
        + 3 * (1 - t) * t ** 2 * c[2][0]
        + t ** 3 * c[3][0]
    )

# Produce the y coordinate of a Bezier curve at point t
def bezier_y(c, t):
    return (
        (1 - t) ** 3 * c[0][1]
        + 3 * (1 - t) ** 2 * t * c[1][1]
        + 3 * (1 - t) * t ** 2 * c[2][1]
        + t ** 3 * c[3][1]
    )

# Produce the slope of a Bezier curve at point t
def bezier_slope(c, t):
    xDeriv = (
        3 * (1 - t) ** 2 * (c[1][0] - c[0][0])
        + 6 * (1 - t) * t * (c[2][0] - c[1][0])
        + 3 * t ** 2 * (c[3][0] - c[2][0])
    )
    yDeriv = (
        3 * (1 - t) ** 2 * (c[1][1] - c[0][1])
        + 6 * (1 - t) * t * (c[2][1] - c[1][1])
        + 3 * t ** 2 * (c[3][1] - c[2][1])
    )

    res = yDeriv / xDeriv

    # Unless it's an asymptote, you don't want giant spikes in the middle of your graph ...
    if max(res) - min(res) > 10:
        raise ValueError

    return res


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
