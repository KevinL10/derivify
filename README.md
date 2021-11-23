# Derivify
Calculates the derivative of a graph from a given image using [potrace](http://potrace.sourceforge.net/) and Bezier curves.

# Usage
`python3 main.py [filename]` produces a derivative graph for the specified file. Currently, only black and white images (PNG, JPG, BMP) are supported.


![Website Prototype](/examples/Derivify.gif)

Alternatively, you can deploy the flask application with `flask run` in the [website](/website) folder.

**Note**: The graph must be continuous.
# Examples
See [examples](/examples).

# Requirements
`pip install -r requirements.txt` and [potrace](`http://potrace.sourceforge.net/#downloading`).

# Todo
- [ ] Make the svg parser more robust
- [x] Support PNG and JPG images
- [ ] Smooth out the resulting derivative graph
- [x] Create a simple website that runs Derivify on uploaded images
- [ ] Host the flask app