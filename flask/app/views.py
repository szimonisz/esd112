from app import app, db
import os
from flask import flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from app.models import FileUpload, ESD, Administrator, Address
import csv

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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_upload = FileUpload(filename=filename)
        db.session.add(file_upload)
        db.session.commit()

        rows = []
        # District report vs. ESD report vs. School report
        with open(file_path,'r') as csvfile:
            #ESD Name,ESD Code,AddressLine1,AddressLine2,State,ZipCode,Administrator Name,Phone,Email
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            for row in csv_reader:
                exists = db.session.get(ESD,row['ESD Code']) is not None
                if exists:
                    continue
                else:
                    admin = Administrator(
                        firstname=row['Administrator Name'],
                        middlename=row['Administrator Name'],
                        lastname=row['Administrator Name'],
                        email=row['Email'],
                        phone_number=row['Phone']
                    )
                    address = Address(
                        line_one=row['AddressLine1'],
                        line_two=row['AddressLine2'],
                        state=row['State'],
                        zip=row['ZipCode']
                    )
                    db.session.add(admin)
                    db.session.add(address)
                    db.session.commit()
                    esd = ESD(
                        code=row['ESD Code'],
                        name=row['ESD Name'],
                        address_id = address.id,
                        administrator_id = admin.id
                    )
                    db.session.add(esd)
                    db.session.commit()

        file_uploads = FileUpload.query.all()
        file_uploads_list = []
        for item in file_uploads:
            file_uploads_list.append(item.to_dict())

        return jsonify(file_uploads_list)

@app.route("/uploadHistory", methods=['GET'])
def uploadHistory():
    file_uploads = FileUpload.query.all()
    file_uploads_list = []
    for item in file_uploads:
        file_uploads_list.append(item.to_dict())

    return jsonify(file_uploads_list)

@app.route('/all_ESDs', methods=['GET'])
def all_ESDs():
    esds = db.session.query(ESD,Address,Administrator).join(Address,ESD.address_id==Address.id).join(Administrator,ESD.administrator_id==Administrator.id).all()
    esd_list = []
    for esd,address,admin in esds:
        esd_dict = {}
        esd_dict.update(esd.to_dict())
        esd_dict.update(address.to_dict())
        esd_dict.update(admin.to_dict())
        esd_list.append(esd_dict)
    return jsonify(esd_list)

@app.route("/delete_esd/<id>", methods=['DELETE'])
def delete_esd(id):
    esd = db.session.query(ESD).get(id)
    db.session.delete(esd)
    db.session.commit()

    return "FileUpload was successfully deleted"
@app.route("/delete_upload/<id>", methods=['DELETE'])
def delete_upload(id):
    file_upload = FileUpload.query.get(id)
    db.session.delete(file_upload)
    db.session.commit()

    return "FileUpload was successfully deleted"
