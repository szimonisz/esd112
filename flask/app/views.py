from app import app, db
import os
from flask import flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from app.models import FileUpload

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
        file_upload = FileUpload(filename=filename)
        db.session.add(file_upload)
        db.session.commit()
        #return FileUpload.query.order_by(FileUpload.date_added)
        file_uploads = FileUpload.query.all()
        file_uploads_list = []
        for item in file_uploads:
            file_uploads_list.append(item.to_dict())

        return jsonify(file_uploads_list)
        #return redirect(url_for('download_file'),name=filename)

@app.route("/uploadHistory", methods=['GET'])
def uploadHistory():
    file_uploads = FileUpload.query.all()
    file_uploads_list = []
    for item in file_uploads:
        file_uploads_list.append(item.to_dict())

    return jsonify(file_uploads_list)

@app.route("/delete_upload/<id>", methods=['DELETE'])
def delete_upload(id):
    file_upload = FileUpload.query.get(id)
    db.session.delete(file_upload)
    db.session.commit()

    return "FileUpload was successfully deleted"
