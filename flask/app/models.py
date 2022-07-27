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

class ESD(db.Model):
    code = db.Column(db.Integer, primary_key=True,autoincrement=False)
    name = db.Column(db.String(200),nullable=False)
    address_id = db.Column(db.Integer,db.ForeignKey("address.id"),unique=True)
    administrator_id = db.Column(db.Integer,db.ForeignKey('administrator.id'),unique=True)

    address = db.relationship('Address',back_populates='esd',uselist=False)
    administrator = db.relationship('Administrator',back_populates='esd',uselist=False)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(200),nullable=False)
    line_two = db.Column(db.String(200),nullable=True)
    state = db.Column(db.String(200),nullable=False)
    zip = db.Column(db.String(10), nullable=False)

    esd = db.relationship('ESD',back_populates='address')
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    esd = db.relationship('ESD',back_populates="administrator") 
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

    


