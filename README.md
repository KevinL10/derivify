# Derivify
Calculates the derivative of a graph from a given image using [potrace](http://potrace.sourceforge.net/) and Bezier curves.

# Usage
`python3 main.py [filename]` produces a derivative graph for the specified file. Currently, only black and white bitmaps (PBM, PGM, PPM, BMP) are supported.


**Note**: The graph must be continuous.
# Examples
See [examples](/examples).

# Requirements
`pip install -r requirements.txt` and [potrace](`http://potrace.sourceforge.net/#downloading`).

# Todo
- [ ] Make the svg parser more robust
- [ ] Support PNG and JPG images
- [ ] Use lines in addition to curves when calculating the derivative
- [ ] Average out the values at every x-coordinate
- [ ] Create a simple website that runs Derivify on uploaded images