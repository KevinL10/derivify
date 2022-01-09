from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, session
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

    # If the user has previous graphs, display those
    user_graphs_path = os.path.join(app.config['UPLOAD_PATH'], session['user_id'])
    if os.path.exists(user_graphs_path):
        return render_template('index.html', files=os.listdir(user_graphs_path))

    return render_template('index.html')

@app.route('/derivify', methods = ['POST'])
def derivify():
    user_image = request.files['file']
    user_graphs_path = os.path.join(app.config['UPLOAD_PATH'], session['user_id'])

    if user_image.filename != '':
        # Remove the user's previous directory and create a new one
        shutil.rmtree(user_graphs_path, ignore_errors=True)
        os.mkdir(user_graphs_path)

        user_image_path = os.path.join(user_graphs_path, 'user_image.png')
        user_image.save(user_image_path)

        # If any errors occur, delete the temporary files within the user's directory
        try:
            derivify_least_squares(user_image_path, os.path.join(user_graphs_path, 'deriv_least_squares.png'))
            derivify_bezier(user_image_path, os.path.join(user_graphs_path, 'deriv_bezier.png'))
        except Exception as e:
            print(f"[+] Error occured {e}")
            shutil.rmtree(user_graphs_path, ignore_errors=True)

    return redirect(url_for('index'))


@app.route('/antiderivify', methods = ['GET'])
def index_antiderivify():
    return 'To be added'
    

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_PATH'], session['user_id']), filename)