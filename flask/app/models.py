from app import db 
from datetime import datetime

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200),nullable=False)
    #filesize = db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class ESD(db.model):
    esd_code = db.Column(db.Integer, primary_key=True,autoincrement=False)
    name = db.Column(db.String(200),nullable=False)
    address = db.relationship('Address',lazy=True)
    administrator = db.relationship('Administrator',back_populates='esd')

class District(db.model):
    id = db.Column(db.Integer, primary_key=True)

class Address(db.model):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(200),nullable=False)
    line_two = db.Column(db.String(200),nullable=True)
    state = db.Column(db.String(200),nullable=False)
    zip = db.Column(db.String(10), nullable=False)

class Administrator(db.model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    esd = db.relationship('ESD',back_populates="administrator") 

    


