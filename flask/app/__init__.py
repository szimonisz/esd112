from flask import Flask
from flask_cors import CORS

# fix this!
UPLOAD_FOLDER = '/app/app/uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'abcd123'
CORS(app, resources={r"/*":{'origins':"*"}})

from app import views
