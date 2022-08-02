from app import app, db
import re
import os
from flask import flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from app.models import FileUpload, ESD, Administrator, Address, District, School, SchoolCategory, GradeCategory
import csv


@app.route("/")
def hello_world():
    return "<p>I love Helen</p>"


@app.route("/helen", methods=['GET'])
def helen():
    return("I love Helen <3")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Think security!!


@app.route("/esd/<id>", methods=['PATCH'])
def update_esd(id):
    esd = db.session.get(ESD, id)
    data = request.get_json()
    esd.name = data.get('name')

    if data.get('address_id') is not None:
        address = db.session.get(Address, data.get('address_id'))
        address.line_one = data.get('line_one')
        address.line_two = data.get('line_two')
        address.city = data.get('city')
        address.state = data.get('state')
        address.zip = data.get('zip')
    else:
        address = Address(
            line_one=data.get('line_one'),
            line_two=data.get('line_two'),
            state=data.get('state'),
            zip=data.get('zip')
        )
        db.session.add(address)
        db.session.flush()
        esd.address_id = address.id

    if data.get('administrator_id') is not None:
        admin = db.session.get(Administrator, data.get('administrator_id'))
        admin.firstname = data.get('firstname')
        admin.phone_number = data.get('phone_number')
        admin.email = data.get('email')
    else:
        admin = Administrator(
            firstname=data.get('firstname'),
            middlename=data.get('firstname'),
            lastname=data.get('firstname'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(admin)
        db.session.flush()
        esd.admin = admin.id

    print(data)
    db.session.commit()
    return 'Success!'


@app.route('/esd', methods=['POST'])
def new_esd():
    # note: json().get() will return None if key does not exist in request
    data = request.get_json()
    print(data.get('code'))
    if data.get('code') is None or data.get('code') == '':
        return "Need ESD code to create entry.", 422

    esd = db.session.get(ESD, data.get('code'))
    if esd is not None:
        return "ESD with code " + data.get('code') + " already exists.", 422
    else:
        address = Address(
            line_one=data.get('line_one'),
            line_two=data.get('line_two'),
            state=data.get('state'),
            zip=data.get('zip')
        )
        admin = Administrator(
            firstname=data.get('firstname'),
            middlename=data.get('firstname'),
            lastname=data.get('firstname'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(address)
        db.session.add(admin)
        db.session.flush()
        esd = ESD(
            code=data.get('code'),
            name=data.get('name'),
            address_id=address.id,
            administrator_id=admin.id
        )
        db.session.add(esd)
        db.session.commit()
        return "Success!"


@app.route('/district', methods=['POST'])
def new_district():
    # note: json().get() will return None if key does not exist in request
    data = request.get_json()
    district_code = data.get('code')

    if district_code is None or district_code == "":
        return "Need District code to create entry.", 422
    try:
        district_code = int(district_code)
    except ValueError:
        return "District code must be an integer", 422

    district = db.session.get(District, data.get('code'))
    if district is not None:
        return "District with code " + data.get('code') + " already exists.", 422
    else:
        address = Address(
            line_one=data.get('line_one'),
            line_two=data.get('line_two'),
            state=data.get('state'),
            zip=data.get('zip')
        )
        admin = Administrator(
            firstname=data.get('firstname'),
            middlename=data.get('firstname'),
            lastname=data.get('firstname'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(address)
        db.session.add(admin)
        db.session.flush()
        district = District(
            code=data.get('code'),
            name=data.get('name'),
            address_id=address.id,
            administrator_id=admin.id
        )
        db.session.add(district)
        db.session.commit()
        return "Success!"


@app.route("/district/<id>", methods=['PATCH'])
def update_district(id):
    data = request.get_json()

    district = db.session.get(District, id)
    district.name = data.get('name')
    district.esd_code = data.get('esd_code')

    if data.get('address_id') is not None:
        address = db.session.get(Address, data.get('address_id'))
        address.line_one = data.get('line_one')
        address.line_two = data.get('line_two')
        address.city = data.get('city')
        address.state = data.get('state')
        address.zip = data.get('zip')
    else:
        address = Address(
            line_one=data.get('line_one'),
            line_two=data.get('line_two'),
            state=data.get('state'),
            zip=data.get('zip')
        )
        db.session.add(address)
        db.session.flush()
        didstrict.address_id = address.id

    if data.get('administrator_id') is not None:
        admin = db.session.get(Administrator, data.get('administrator_id'))
        admin.firstname = data.get('firstname')
        admin.phone_number = data.get('phone_number')
        admin.email = data.get('email')
    else:
        admin = Administrator(
            firstname=data.get('firstname'),
            middlename=data.get('firstname'),
            lastname=data.get('firstname'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(admin)
        db.session.flush()
        district.admin = admin.id

    print(data)
    db.session.commit()
    return 'Success!'


@app.route("/school/<id>", methods=['POST'])
def update_school(id):
    data = request.get_json()

    school = db.session.get(School, id)
    school.name = data.get('name')
    school.district_code = data.get('district_code')
    school.lowest_grade = data.get('lowest_grade')
    school.highest_grade = data.get('highest_grade')
    school.ayp_code = data.get('ayp_code')

    address = db.session.get(Address, data.get('address_id'))
    address.line_one = data.get('line_one')
    address.line_two = data.get('line_two')
    address.city = data.get('city')
    address.state = data.get('state')
    address.zip = data.get('zip')

    admin = db.session.get(Administrator, data.get('administrator_id'))
    admin.firstname = data.get('firstname')
    admin.phone_number = data.get('phone_number')
    admin.email = data.get('email')

    # clear original school categories
    for school_category in school.school_categories:
        school.school_categories.remove(school_category)
    db.session.flush()

    # update with new school categories
    for school_category_id in data.get('school_category_ids'):
        school_category = db.session.get(SchoolCategory, school_category_id)
        school.school_categories.append(school_category)

    school.grade_category_id = data.get('grade_category_id')

    grade_category = db.session.get(GradeCategory, school.grade_category_id)
    school.grade_category = grade_category

    print(school.to_dict())
    db.session.commit()
    return 'Success!'


def insert_esd(row):
    esd = db.session.get(ESD, row['ESD Code'])
    if esd:
        # Update address
        if esd.address_id is None:
            address = Address(
                line_one=row['AddressLine1'],
                line_two=row['AddressLine2'],
                state=row['State'],
                zip=row['ZipCode']
            )
            db.session.add(address)
            db.session.flush()
            esd.address_id = address.id
        # Update administrator
        if esd.administrator_id is None:
            admin = Administrator(
                firstname=row['Administrator Name'],
                middlename=row['Administrator Name'],
                lastname=row['Administrator Name'],
                email=row['Email'],
                phone_number=row['Phone']
            )
            db.session.add(admin)
            db.session.flush()
            esd.administrator_id = admin.id
    else:
        address = Address(
            line_one=row['AddressLine1'],
            line_two=row['AddressLine2'],
            state=row['State'],
            zip=row['ZipCode']
        )
        admin = Administrator(
            firstname=row['Administrator Name'],
            middlename=row['Administrator Name'],
            lastname=row['Administrator Name'],
            email=row['Email'],
            phone_number=row['Phone']
        )
        db.session.add(address)
        db.session.add(admin)
        db.session.flush()
        esd = ESD(
            code=row['ESD Code'],
            name=row['ESD Name'],
            address_id=address.id,
            administrator_id=admin.id
        )
        db.session.add(esd)


def insert_district(row):
    district = db.session.get(District, row['DistrictCode'])
    if district:
        if district.address_id is None:
            address = Address(
                line_one=row['AddressLine1'],
                line_two=row['AddressLine2'],
                city=row['City'].title(),
                state=row['State'],
                zip=row['Zipcode']
            )
            db.session.add(address)
            db.session.flush()
            district.address_id = address.id

        if district.administrator_id is None:
            admin = Administrator(
                firstname=row['AdministratorName'],
                middlename=row['AdministratorName'],
                lastname=row['AdministratorName'],
                email=row['Email'],
                phone_number=row['Phone']
            )
            db.session.add(admin)
            db.session.flush()
            district.administrator_id = admin.id

        if district.esd_code is None:
            esd = db.session.get(ESD, row['ESDCode'])
            if esd is None:
                esd = ESD(
                    code=row['ESDCode'],
                    name=row['ESDName'],
                )
                db.session.add(esd)
            district.esd_code = row['ESDCode']
    else:
        admin = Administrator(
            firstname=row['AdministratorName'],
            middlename=row['AdministratorName'],
            lastname=row['AdministratorName'],
            email=row['Email'],
            phone_number=row['Phone']
        )
        address = Address(
            line_one=row['AddressLine1'],
            line_two=row['AddressLine2'],
            city=row['City'].title(),
            state=row['State'],
            zip=row['Zipcode']
        )
        db.session.add(admin)
        db.session.add(address)
        db.session.flush()

        esd = db.session.query(ESD).filter(
            ESD.code == row['ESDCode']).first()

        if esd is None:
            esd = ESD(
                code=row['ESDCode'],
                name=row['ESDName'],
            )
            db.session.add(esd)

        district = District(
            code=row['DistrictCode'],
            name=row['DistrictName'],
            address_id=address.id,
            administrator_id=admin.id,
            esd_code=row['ESDCode']
        )
        db.session.add(district)


def insert_school(row):
    school = db.session.get(School, row['SchoolCode'])
    if school:
        if school.address_id is None:
            address = Address(
                line_one=row['AddressLine1'],
                line_two=row['AddressLine2'],
                city=row['City'].title(),
                state=row['State'],
                zip=row['Zipcode']
            )
            db.session.add(address)
            db.session.flush()
            school.address_id = address.id

        if school.administrator_id is None:
            admin = Administrator(
                firstname=row['AdministratorName'],
                middlename=row['AdministratorName'],
                lastname=row['AdministratorName'],
                email=row['Email'],
                phone_number=row['Phone']
            )
            db.session.add(admin)
            db.session.flush()
            school.administrator_id = admin.id

        district = db.session.get(District, row['LEACode'])
        if school.district_code is None:
            school.district_code = row['LEACode']

            if district is None:
                district = District(
                    code=row['LEACode'],
                    name=row['LEAName'],
                    esd_code=row['ESDCode']
                )
                db.session.add(district)

        if district.esd_code is None:
            district.esd_code = row['ESDCode']

        esd = db.session.get(ESD, row['ESDCode'])
        if esd is None:
            esd = ESD(
                code=row['ESDCode'],
                name=row['ESDName'],
            )
            db.session.add(esd)
    else:
        admin = Administrator(
            firstname=row['PrincipalName'],
            middlename=row['PrincipalName'],
            lastname=row['PrincipalName'],
            email=row['Email'],
            phone_number=row['Phone']
        )
        address = Address(
            line_one=row['AddressLine1'],
            line_two=row['AddressLine2'],
            city=row['City'].title(),
            state=row['State'],
            zip=row['ZipCode']
        )
        db.session.add(admin)
        db.session.add(address)
        db.session.flush()

        esd = db.session.get(ESD, row['ESDCode'])
        district = db.session.get(District, row['LEACode'])

        if esd is None:
            esd = ESD(
                code=row['ESDCode'],
                name=row['ESDName'],
            )
            db.session.add(esd)

        if district is None:
            district = District(
                code=row['LEACode'],
                name=row['LEAName'],
                esd_code=row['ESDCode']
            )
            db.session.add(district)

        #school_category_name_list = row['OrgCategoryList'].split("'")
        school_category_name_list = re.split("',|,\s?", row['OrgCategoryList'])
        school_category_list = []
        for category_name in school_category_name_list:
            school_category = db.session.query(SchoolCategory).filter(
                SchoolCategory.title == category_name.lstrip()).first()
            if school_category is None:
                school_category = SchoolCategory(
                    title=category_name.lstrip()
                )
                db.session.add(school_category)
                db.session.flush()
            school_category_list.append(school_category)

        grade_category = db.session.query(GradeCategory).filter(
            GradeCategory.title == row['GradeCategory']).first()
        if grade_category is None:
            grade_category = GradeCategory(
                title=row['GradeCategory']
            )
            db.session.add(grade_category)

        school = School(
            code=row['SchoolCode'],
            name=row['SchoolName'],
            ayp_code=row['AYPCode'],
            district_code=row['LEACode'],
            lowest_grade=row['LowestGrade'],
            highest_grade=row['HighestGrade'],
            address_id=address.id,
            administrator_id=admin.id,
            grade_category_id=grade_category.id,
        )
        db.session.add(school)
        school.school_categories.extend(school_category_list)


@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "File not in request.files"
    file = request.files['file']
    if file.filename == '':
        return "Filename is empty"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_upload = FileUpload(filename=filename)
        db.session.add(file_upload)
        db.session.commit()

        # ESD primary key: ESD Code
        # District primary key: LEACode
        # School primary key: SchoolCode

        esd_headers = ['ESD Name', 'ESD Code', 'AddressLine1', 'AddressLine2',
                       'State', 'ZipCode', 'Administrator Name', 'Phone', 'Email']
        district_headers = ['ESDCode', 'ESDName', 'DistrictCode', 'DistrictName', 'AddressLine1',
                            'AddressLine2', 'City', 'State', 'Zipcode', 'AdministratorName', 'Phone', 'Email']
        school_headers = ['ESDCode', 'ESDName', 'LEACode', 'LEAName', 'SchoolCode', 'SchoolName', 'LowestGrade', 'HighestGrade', 'AddressLine1',
                          'AddressLine2', 'City', 'State', 'ZipCode', 'PrincipalName', 'Email', 'Phone', 'OrgCategoryList', 'AYPCode', 'GradeCategory']

        # case expression to clean up if/else statements?
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            headers = csv_reader.fieldnames

            if sorted(headers) == sorted(esd_headers):
                report_type = 'esd'
            elif sorted(headers) == sorted(school_headers):
                report_type = 'school'
            elif sorted(headers) == sorted(district_headers):
                report_type = 'district'
            else:
                return "Upload failed. CSV does not have proper ESD, District, or School headers"

            for row in csv_reader:

                if report_type == 'esd':
                    insert_esd(row)

                if report_type == 'district':
                    insert_district(row)

                if report_type == 'school':
                    insert_school(row)

                db.session.flush()
            db.session.commit()

    return "Success!"


@app.route("/uploadHistory", methods=['GET'])
def uploadHistory():
    file_uploads = FileUpload.query.all()
    file_uploads_list = []
    for item in file_uploads:
        file_uploads_list.append(item.to_dict())

    return jsonify(file_uploads_list)


@app.route('/all_esds', methods=['GET'])
def all_esds():
    esds = db.session.query(ESD, Address, Administrator).outerjoin(Address, ESD.address_id == Address.id).outerjoin(
        Administrator, ESD.administrator_id == Administrator.id).all()
    esd_list = []
    for esd, address, admin in esds:
        esd_dict = {}
        esd_dict.update(esd.to_dict())
        if address is not None:
            esd_dict.update(address.to_dict())
        if admin is not None:
            esd_dict.update(admin.to_dict())
        esd_list.append(esd_dict)
    return jsonify(esd_list)


@app.route('/all_school_categorys', methods=['GET'])
def all_school_categories():
    school_categories = db.session.query(SchoolCategory).all()
    school_category_list = []
    for school_category in school_categories:
        school_category_list.append(school_category.to_dict())
    return jsonify(school_category_list)


@app.route('/all_grade_categorys', methods=['GET'])
def all_grade_categories():
    grade_categories = db.session.query(GradeCategory).all()
    grade_category_list = []
    for grade_category in grade_categories:
        grade_category_list.append(grade_category.to_dict())
    return jsonify(grade_category_list)


@app.route('/all_districts', methods=['GET'])
def all_districts():
    districts = db.session.query(District, Address, Administrator).outerjoin(Address, District.address_id == Address.id).outerjoin(
        Administrator, District.administrator_id == Administrator.id).all()
    district_list = []
    for district, address, admin in districts:
        district_dict = {}
        district_dict.update(district.to_dict())
        if (district.esd_code):
            esd = db.session.query(ESD).get(district.esd_code)
            district_dict.update({"esd_name": esd.name})
        else:
            district_dict.update({"esd_name": None})
        if address is not None:
            district_dict.update(address.to_dict())
        if admin is not None:
            district_dict.update(admin.to_dict())
        district_list.append(district_dict)
    return jsonify(district_list)


@app.route('/all_schools', methods=['GET'])
def all_schools():
    schools = db.session.query(School, Address, Administrator, GradeCategory).join(Address, School.address_id == Address.id).join(
        Administrator, School.administrator_id == Administrator.id).join(GradeCategory, School.grade_category_id == GradeCategory.id).all()
    school_list = []
    for school, address, admin, grade_category in schools:
        school_dict = {}
        school_dict.update(school.to_dict())

        school_categories = []
        if school.school_categories:
            for school_category in school.school_categories:
                school_categories.append(school_category.to_dict())
                school_dict.update(
                    # {'school_categories': ',\n'.join(school_category_names)})
                    {'school_categories': school_categories})

        if school.district_code:
            district = db.session.query(District).get(school.district_code)
            school_dict.update({"district_name": district.name})
            school_dict.update({"esd_code": district.esd_code})
            if district.esd_code:
                esd = db.session.query(ESD).get(district.esd_code)
                school_dict.update({"esd_name": esd.name})
            else:
                school_dict.update({"esd_name": None})

        if school.grade_category:
            school_dict.update({"grade_category": grade_category.title})

        school_dict.update(address.to_dict())
        school_dict.update(admin.to_dict())
        school_list.append(school_dict)
    return jsonify(school_list)


@app.route("/esd/<id>", methods=['DELETE'])
def delete_esd(id):
    esd = db.session.query(ESD).get(id)
    db.session.delete(esd)
    db.session.commit()

    return "ESD was successfully deleted"


@app.route("/district/<id>", methods=['DELETE'])
def delete_district(id):
    district = db.session.query(District).get(id)
    db.session.delete(district)
    db.session.commit()

    return "District was successfully deleted"


@app.route("/school/<id>", methods=['DELETE'])
def delete_school(id):
    school = db.session.query(School).get(id)
    db.session.delete(school)
    db.session.commit()

    return "School was successfully deleted"


@app.route("/delete_upload/<id>", methods=['DELETE'])
def delete_upload(id):
    file_upload = FileUpload.query.get(id)
    db.session.delete(file_upload)
    db.session.commit()

    return "FileUpload was successfully deleted"


@app.route("/esd/<id>", methods=['GET'])
def esd(id):
    query = db.session.query(ESD, Address, Administrator).outerjoin(Address, ESD.address_id == Address.id).outerjoin(
        Administrator, ESD.administrator_id == Administrator.id).filter(ESD.code == id)
    esd_dict = {}
    for esd, address, admin in query:
        esd_dict.update(esd.to_dict())
        if address:
            esd_dict.update(address.to_dict())
        if admin:
            esd_dict.update(admin.to_dict())
    return jsonify(esd_dict)


@app.route("/district/<id>", methods=['GET'])
def district(id):
    query = db.session.query(District, Address, Administrator, ESD).outerjoin(Address, District.address_id == Address.id).outerjoin(
        Administrator, District.administrator_id == Administrator.id).outerjoin(ESD, District.esd_code == ESD.code).filter(District.code == id)
    district_dict = {}
    for district, address, admin, esd in query:
        district_dict.update(district.to_dict())
        if address:
            district_dict.update(address.to_dict())
        if admin:
            district_dict.update(admin.to_dict())
        if esd:
            district_dict.update({"esd_name": esd.name})
    return jsonify(district_dict)


@app.route("/school/<id>", methods=['GET'])
def school(id):
    query = db.session.query(School, Address, Administrator, District, GradeCategory, ESD).outerjoin(Address, School.address_id == Address.id).outerjoin(
        Administrator, School.administrator_id == Administrator.id).outerjoin(District, School.district_code == District.code).outerjoin(GradeCategory, School.grade_category_id == GradeCategory.id).outerjoin(ESD, District.esd_code == ESD.code).filter(School.code == id)
    school_dict = {}
    for school, address, admin, district, gradecategory, esd in query:
        school_dict.update(school.to_dict())
        school_dict.update(address.to_dict())
        school_dict.update(admin.to_dict())

        school_categories = []
        if school.school_categories:
            for school_category in school.school_categories:
                school_categories.append(school_category.to_dict())
                school_dict.update(
                    {'school_categories': school_categories})
        if gradecategory:
            school_dict.update({"grade_category": gradecategory.title})
        if district:
            school_dict.update({"district_name": district.name})
        if esd:
            school_dict.update({"esd_code": esd.code})
            school_dict.update({"esd_name": esd.name})
    return jsonify(school_dict)
