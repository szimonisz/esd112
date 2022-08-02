from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# fix this!
UPLOAD_FOLDER = '/app/app/uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///directory.db'
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'abcd123'
CORS(app)

# Initialize the database
db = SQLAlchemy(app)

from app.models import *

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

from app import views
