from app import app
import os
from flask import flash, request, redirect
from werkzeug.utils import secure_filename

@app.route("/")
def hello_world():
    return "<p>I love Helen</p>"

@app.route("/helen", methods=['GET'])
def helen():
    return("I love Helen <3")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Think security!!
@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect("file not in request.files")
    file = request.files['file']
    if file.filename == '':
        return redirect("google.com")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "<p>I love Helen</p>"
        #return redirect(url_for('download_file'),name=filename)
