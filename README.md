# Derivify

Calculates the derivative of a graph from a given image. Check out an interactive demo [here](https://derivify.herokuapp.com/). 

**Note:** it may take a few moments to initally load the app.

# Usage

The [scripts](/website/scripts) folder contains the two algorithms currently used by Derivify. Calling the [derivify_bezier](/website/scripts/bezier/derivify.py) or [derivify_least_squares](/website/scripts/leastsquares/derivify.py) functions with arguments `(input_filepath, output_filepath)` saves a derivative graph for the specified file to the designated output path. Currently, only black and white images (PNG, JPG, BMP) are supported.

![Website Prototype](/examples/Derivify_Canvas.gif)

Alternatively, you can deploy the flask application with `flask run` in the [website](/website) folder.

**Note**: The graph should be continuous.
# Algorithms
- **Bezier Curves**: The first algorithm uses [potrace](http://potrace.sourceforge.net/#downloading) to convert the given image to SVG format, consisting of multiple [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) joined together. Afterward, the derivative (`dy/dx`) for each curve is calculated and plotted on a new graph. Since the resulting curves can have unwanted sudden spikes in values, the algorithm applies a [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter) to smoothen the data.
- **Least Squares Polynomial**: The second algorithm relies on a more straightforward approach – it first examines the pixels of the image and determines the average y-value for every x-coordinate. For every window of ~50 x-coordinates, the algorithm computes the best fit cubic polynomial and calculates the resulting derivative. Finally, it joins these results together to produce an overall graph of the derivative function.

# Examples
See [examples](/examples).

# Requirements
`pip install -r requirements.txt` and [potrace](http://potrace.sourceforge.net/#downloading).

# Todo
- [ ] Make the svg parser more robust
- [x] Support PNG and JPG images
- [x] Smooth out the resulting derivative graph
- [x] Create a simple website that runs Derivify on uploaded images
- [x] Host the flask app
- [x] Create a canvas for users to directly draw graphs
- [x] Substitute Bezier curves with polynomials using least squares
- [ ] Include a similar antiderivative functionality
- [ ] Allow users to adjust parameters for the derivify functions