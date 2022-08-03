from flask import Blueprint, current_app, flash, request, redirect, jsonify
import re
import os
from werkzeug.utils import secure_filename
from .models import FileUpload, ESD, Administrator, Address, District, School, SchoolCategory, GradeCategory
import csv
from .db import db

upload_blueprint = Blueprint('upload_blueprint', __name__)

# This blueprint handles the API endpoints for uploading a CSV file, checking if the file is valid, and inserting the values of the CSV file into the database.
# The user may upload District, ESD, and School CSV reports.
# NOTE: Three assumptions are made for a CSV upload:
#           - Each CSV report will follow the same header format as those currently posted on the OSPI website
#           - Each District is paired with an ESD
#           - Each School is paired with a District

# Receive file, check if valid, and insert into database using helper functions (insert_esd, insert_district, insert_school).
@upload_blueprint.route("/api/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "File not in request.files"
    file = request.files['file']
    if file.filename == '':
        return "Filename is empty"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_upload = FileUpload(filename=filename)
        db.session.add(file_upload)
        db.session.commit()

        # ESD primary key: ESD Code
        # District primary key: LEACode
        # School primary key: SchoolCode

        # Lists of each report's CSV headers
        # Used to compare with uploaded file
        esd_headers = ['ESD Name', 'ESD Code', 'AddressLine1', 'AddressLine2',
                       'State', 'ZipCode', 'Administrator Name', 'Phone', 'Email']
        district_headers = ['ESDCode', 'ESDName', 'DistrictCode', 'DistrictName', 'AddressLine1',
                            'AddressLine2', 'City', 'State', 'Zipcode', 'AdministratorName', 'Phone', 'Email']
        school_headers = ['ESDCode', 'ESDName', 'LEACode', 'LEAName', 'SchoolCode', 'SchoolName', 'LowestGrade', 'HighestGrade', 'AddressLine1',
                          'AddressLine2', 'City', 'State', 'ZipCode', 'PrincipalName', 'Email', 'Phone', 'OrgCategoryList', 'AYPCode', 'GradeCategory']

        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            headers = csv_reader.fieldnames

            # Determine the report type of the uploaded CSV (and whether or not it is valid)
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

# Check if the uploaded file is allowed (.csv)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Insert ESD from CSV row into database.
def insert_esd(row):
    esd = db.session.get(ESD, row['ESD Code'])

    # If ESD already exists in database
    if esd is not None:
        # Create an address, if this ESD does not have one
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
        # Create an admin, if this ESD does not have one
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
    # ESD does not yet exist in database
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


# Insert District from CSV row into database.
def insert_district(row):
    district = db.session.get(District, row['DistrictCode'])
    # If District already exists in database
    if district is not None:
        # Create an address, if this District does not have one
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
        # Create an admin, if this District does not have one
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
            # Create an ESD, if this District has an ESD Code that does not yet belong to an ESD
            if esd is None:
                esd = ESD(
                    code=row['ESDCode'],
                    name=row['ESDName'],
                )
                db.session.add(esd)
            district.esd_code = row['ESDCode']
    # District does not yet exist in database
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

        # Create an ESD, if this District has an ESD Code that does not yet belong to an ESD
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

# Insert School from CSV row into database.
def insert_school(row):
    school = db.session.get(School, row['SchoolCode'])
    # If School already exists in database
    if school is not None:
        # Create an address, if this School does not have one
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

        # Create an admin, if this School does not have one
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

            # Create a District, if this School has a District Code that does not yet belong to a District
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
        # Create an ESD, if this School belongs to a District with an ESD that does not yet exist in the database
        if esd is None:
            esd = ESD(
                code=row['ESDCode'],
                name=row['ESDName'],
            )
            db.session.add(esd)
    # School does not yet exist in database
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

        # Create an ESD, if this School belongs to a District with an ESD that does not yet exist in the database
        if esd is None:
            esd = ESD(
                code=row['ESDCode'],
                name=row['ESDName'],
            )
            db.session.add(esd)

        # Create a District, if this School has a District Code that does not yet belong to a District
        if district is None:
            district = District(
                code=row['LEACode'],
                name=row['LEAName'],
                esd_code=row['ESDCode']
            )
            db.session.add(district)

        # List of this School's category names, seperated by a comma
        school_category_name_list = re.split("',|,\s?", row['OrgCategoryList'])

        school_category_list = []
        for category_name in school_category_name_list:
            school_category = db.session.query(SchoolCategory).filter(
                SchoolCategory.title == category_name.lstrip()).first()
            # Create a new School Category, if this School has a category name that does not yet exist 
            if school_category is None:
                school_category = SchoolCategory(
                    title=category_name.lstrip()
                )
                db.session.add(school_category)
                db.session.flush()
            school_category_list.append(school_category)

        grade_category = db.session.query(GradeCategory).filter(
            GradeCategory.title == row['GradeCategory']).first()
        # Create a new Grade Category, if this School has a grade category name that does not yet exist
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

