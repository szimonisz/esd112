from .db import db
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .upload import upload_blueprint
from .directory import directory_blueprint
from .models import SchoolCategory, GradeCategory

UPLOAD_FOLDER = '/esd112/app/uploads'
ALLOWED_EXTENSIONS = {'csv'}

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///directory.db'
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'abcd123'
    CORS(app)
    db.init_app(app)
    setup_database(app)
    app.register_blueprint(upload_blueprint)
    app.register_blueprint(directory_blueprint)

    return app

def setup_database(app):
    with app.app_context():
        db.create_all()
        school_categories = [
            'Public School',
            'Regular School',
            'Alternative School',
            'Special Education School',
            'Institution',
            'Contract School',
            'Preschool',
            'Vocational/technical school',
            'Adult Jail',
            'Affiliated With District',
            'Re-Engagement School',
            'Detention Center',
            'Charter',
            'Not Affiliated With District',
            'Tribal School',
            'College/University'
        ]
        grade_categories = [
            'PK-12',
            'Elementary School',
            'High School',
            'Middle School',
            'Other',
            'PK Only',
            'K-12',
            'Jr High'
        ]
        for school_category in school_categories:
            if db.session.query(SchoolCategory).filter(SchoolCategory.title == school_category).first() is None:
                db.session.add(SchoolCategory(title=school_category))
        for grade_category in grade_categories:
            if db.session.query(GradeCategory).filter(GradeCategory.title == grade_category).first() is None:
                db.session.add(GradeCategory(title=grade_category))

        db.session.commit()
