import re
import os
from flask import flash, request, redirect, jsonify, Blueprint
from werkzeug.utils import secure_filename
from app.models import FileUpload, ESD, Administrator, Address, District, School, SchoolCategory, GradeCategory
import csv
from .db import db

directory_blueprint = Blueprint('directory_blueprint',__name__)

@directory_blueprint.route("/<table>/<id>", methods=['PATCH'])
def update_record(table,id):
    data = request.get_json()
    if table == 'esd':
        esd = db.session.get(ESD, id)
        esd.name = data.get('name')
    elif table == 'district':
        district = db.session.get(District, id)
        district.name = data.get('name')
        district.esd_code = data.get('esd_code')
    elif table == 'school':
        school = db.session.get(School, id)
        school.name = data.get('name')
        school.district_code = data.get('district_code')
        school.lowest_grade = data.get('lowest_grade')
        school.highest_grade = data.get('highest_grade')
        school.ayp_code = data.get('ayp_code')

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
    else:
        return "No such table"
        
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

        if table == 'esd':
            esd.address_id = address.id
        if table == 'district':
            district.address_id = address.id
        if table == 'school':
            school.address_id = address.id

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
        if table == 'esd':
            esd.administrator_id = admin.id
        if table == 'district':
            district.administrator_id = admin.id
        if table == 'school':
            school.administrator_id = admin.id

    db.session.commit()
    return 'Success!'


@directory_blueprint.route('/<table>', methods=['POST'])
def new_record(table):
    # note: json().get() will return None if key does not exist in request
    data = request.get_json()

    if data.get('code') is None or data.get('code') == '':
        return "Need " + table.title() + " code to create entry.", 422

    if table == 'esd':
        esd = db.session.get(ESD, data.get('code'))
        if esd is not None:
            return "ESD with code " + data.get('code') + " already exists.", 422

    elif table == 'district':
        district_code = data.get('code')
        try: 
            district_code = int(district_code)
        except ValueError:
            return "District code must be an integer.",422
        district = db.session.get(District, district_code)
        if district is not None:
            return "District with code " + str(district_code) + " already exists.", 422

    elif table == 'school':

        school_code = data.get('code')
        try: 
            school_code = int(school_code)
        except ValueError:
            return "District code must be an integer.",422
        school = db.session.get(School, school_code)
        if school is not None:
            return "School with code " + str(school_code) + " already exists.", 422
    else:
        return "No such table"

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

    if table == 'esd':
        esd = ESD(
            code=data.get('code'),
            name=data.get('name'),
            address_id=address.id,
            administrator_id=admin.id
        )
        db.session.add(esd)

    elif table == 'district':
        district = District(
            code=data.get('code'),
            name=data.get('name'),
            address_id=address.id,
            administrator_id=admin.id
        )
        db.session.add(district)
    elif table == 'school':
        school = School(
            code=data.get('code'),
            name=data.get('name'),
            district_code=data.get('district_code'),
            lowest_grade=data.get('lowest_grade'),
            highest_grade=data.get('highest_grade'),
            ayp_code=data.get('ayp_code'),
            address_id=address.id,
            administrator_id=admin.id,
            grade_category_id=data.get('grade_category_id')
        )
        db.session.add(school)
        db.session.flush()
        if data.get('school_category_ids') is not None:
            for school_category_id in data.get('school_category_ids'):
                school_category = db.session.get(
                    SchoolCategory, school_category_id)
                school.school_categories.append(school_category)
        if school.grade_category_id is not None:
            grade_category = db.session.get(
                GradeCategory, school.grade_category_id)
            school.grade_category = grade_category

    db.session.commit()
    return "Success!"

@directory_blueprint.route('/<table>/all', methods=['GET'])
def all_records(table):
    if table == 'esd':
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

    elif table == 'district':
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

    elif table == 'school':
        schools = db.session.query(School, Address, Administrator, GradeCategory).outerjoin(Address, School.address_id == Address.id).outerjoin(
            Administrator, School.administrator_id == Administrator.id).outerjoin(GradeCategory, School.grade_category_id == GradeCategory.id).all()
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

    elif table == 'school_category':
        school_categories = db.session.query(SchoolCategory).all()
        school_category_list = []
        for school_category in school_categories:
            school_category_list.append(school_category.to_dict())
        return jsonify(school_category_list)

    elif table == 'grade_category':
        grade_categories = db.session.query(GradeCategory).all()
        grade_category_list = []
        for grade_category in grade_categories:
            grade_category_list.append(grade_category.to_dict())
        return jsonify(grade_category_list)
    elif table == 'upload':
        file_uploads = FileUpload.query.all()
        file_uploads_list = []
        for item in file_uploads:
            file_uploads_list.append(item.to_dict())

        return jsonify(file_uploads_list)

    else:
        return "Table does not exist."

@directory_blueprint.route("/<table>/<id>", methods=['DELETE'])
def delete_record(table,id):
    if table == 'esd':
        esd = db.session.query(ESD).get(id)
        db.session.delete(esd)
        db.session.commit()
        return "ESD was successfully deleted"
    elif table == 'district':
        district = db.session.query(District).get(id)
        db.session.delete(district)
        db.session.commit()
        return "District was successfully deleted"
    elif table == 'school':
        school = db.session.query(School).get(id)
        db.session.delete(school)
        db.session.commit()
        return "School was successfully deleted"
    elif table == 'upload':
        file_upload = FileUpload.query.get(id)
        db.session.delete(file_upload)
        db.session.commit()
        return "FileUpload was successfully deleted"
    else: 
        # need to return w/ HTTP error status
        return "Cannot delete record from requested table."

@directory_blueprint.route("/<table>/<id>", methods=['GET'])
def get_record(table,id):
    if table == 'esd':
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
    elif table == 'district':
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
    elif table == 'school':
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
    else:
        # need to return w/ HTTP error status
        return "Cannot get record from requested table."