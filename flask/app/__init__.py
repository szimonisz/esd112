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
db.session.commit()

from app import views
