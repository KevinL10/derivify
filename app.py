from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, session
from werkzeug.utils import secure_filename
from main import deriv
import os, shutil
import shutil


app = Flask(__name__)

app.secret_key = os.urandom(16)
# Only accept files less than 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10
app.config['UPLOAD_PATH'] = 'graphs'

@app.route('/')
def index():
    # Display user's graphs if they exist
    if 'user_id' in session and os.path.exists(os.path.join(app.config['UPLOAD_PATH'], session['user_id'])):
        return render_template('index.html', files=os.listdir(os.path.join(app.config['UPLOAD_PATH'], session['user_id'])))

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

        # For security, save the uploaded file with a different name
        new_path = os.path.join(user_path, 'a_input.bmp')
        input_file.save(new_path)
        deriv(new_path, os.path.join(user_path, 'deriv.png'))

    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_PATH'], session['user_id']), filename)