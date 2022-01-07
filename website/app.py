from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, session
from werkzeug.utils import secure_filename
from scripts.bezier.derivify import derivify_bezier
from scripts.leastsquares.derivify import derivify_least_squares
import os, shutil

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]
# Only accept files less than 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10
app.config['UPLOAD_PATH'] = 'graphs'

@app.route('/')
def derivify_redirect():
    return redirect(url_for('index'))

@app.route('/derivify', methods = ['GET'])
def index():
    # Give user a session id for their first visit
    if 'user_id' not in session:
        session['user_id'] = os.urandom(16).hex()

    return render_template('index.html')

@app.route('/derivify', methods = ['POST'])
def derivify():
    input_file = request.files['file']
    filename = secure_filename(input_file.filename)
    user_path = os.path.join(app.config['UPLOAD_PATH'], session['user_id'])

    if filename != '':
        # Remove the user's previous directory and create a new one
        shutil.rmtree(user_path, ignore_errors=True)
        os.mkdir(user_path)

        # Files named upload.bmp and deriv.png
        new_path = os.path.join(user_path, 'upload.bmp')
        input_file.save(new_path)
        derivify_bezier(new_path, os.path.join(user_path, 'deriv.png'))

    return redirect(url_for('index'))


@app.route('/antiderivify', methods = ['GET'])
def index_antiderivify():
    return 'To be added'
    

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_PATH'], session['user_id']), filename)