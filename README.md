# Derivify
Calculates the derivative of a graph from a given image using [potrace](http://potrace.sourceforge.net/) and Bezier curves.

Check it out [here](https://derivify.herokuapp.com/). **Note:** it may take a few moments to initially load the app due to Heroku's dyno sleeping.

# Usage
`python3 main.py [filename]` produces a (raw) derivative graph for the specified file, while `python3 smooth.py [filename]` creates a smoothened version of the graph. Currently, only black and white images (PNG, JPG, BMP) are supported.

![Website Prototype](/examples/Derivify_Canvas.gif)

Alternatively, you can deploy the flask application with `flask run` in the [website](/website) folder.

**Note**: The graph must be continuous.
# Examples
See [examples](/examples).

# Requirements
`pip install -r requirements.txt` and [potrace](`http://potrace.sourceforge.net/#downloading`).

# Todo
- [ ] Make the svg parser more robust
- [x] Support PNG and JPG images
- [x] Smooth out the resulting derivative graph
- [x] Create a simple website that runs Derivify on uploaded images
- [x] Host the flask app
- [x] Create a canvas for users to directly draw graphs
- [ ] Substitute Bezier curves with polynomials using least squares
- [ ] Include a similar antiderivative functionality