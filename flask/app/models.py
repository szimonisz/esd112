from app import db 
from datetime import datetime

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200),nullable=False)
    #filesize = db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

association_table = db.Table(
    'school_to_schoolcategory',
    db.Model.metadata,
    db.Column('school_code', db.ForeignKey('school.code')),
    db.Column('schoolcategory_id', db.ForeignKey('schoolcategory.id')),
)

class SchoolCategory(db.Model):
    __tablename__ = 'schoolcategory'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class GradeCategory(db.Model):
    __tablename__ = 'gradecategory'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    schools = db.relationship('School',back_populates='grade_category')
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class School(db.Model):
    __tablename__ = 'school'
    code = db.Column(db.Integer, primary_key=True,autoincrement=False)
    name = db.Column(db.String(200),nullable=False)
    lowest_grade = db.Column(db.String(2))
    highest_grade = db.Column(db.String(2))
    ayp_code = db.Column(db.String(1))

    address_id = db.Column(db.Integer,db.ForeignKey("address.id"),unique=True,nullable=True)
    administrator_id = db.Column(db.Integer,db.ForeignKey('administrator.id'),unique=True,nullable=True)
    district_code = db.Column(db.Integer, db.ForeignKey('district.code'))
    grade_category_id = db.Column(db.Integer, db.ForeignKey('gradecategory.id'))
    
    school_categories = db.relationship("SchoolCategory",secondary=association_table)
    grade_category = db.relationship('GradeCategory',back_populates='schools')
    address = db.relationship('Address',back_populates='school',uselist=False)
    administrator = db.relationship('Administrator',back_populates='school',uselist=False)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class ESD(db.Model):
    __tablename__ = 'esd'
    code = db.Column(db.String(10), primary_key=True,autoincrement=False)
    name = db.Column(db.String(200),nullable=True)
    address_id = db.Column(db.Integer,db.ForeignKey("address.id"),unique=True,nullable=True)
    administrator_id = db.Column(db.Integer,db.ForeignKey('administrator.id'),unique=True,nullable=True)
    districts = db.relationship("District")

    address = db.relationship('Address',back_populates='esd',uselist=False)
    administrator = db.relationship('Administrator',back_populates='esd',uselist=False)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class District(db.Model):
    __tablename__ = 'district'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=True)
    address_id = db.Column(db.Integer,db.ForeignKey("address.id"),unique=True,nullable=True)
    administrator_id = db.Column(db.Integer,db.ForeignKey('administrator.id'),unique=True,nullable=True)
    esd_code = db.Column(db.String(10),db.ForeignKey('esd.code'))
    schools = db.relationship("School")

    address = db.relationship('Address',back_populates='district',uselist=False)
    administrator = db.relationship('Administrator',back_populates='district',uselist=False)
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(200),nullable=True)
    line_two = db.Column(db.String(200),nullable=True)
    city = db.Column(db.String(200),nullable=True)
    state = db.Column(db.String(200),nullable=True)
    zip = db.Column(db.String(10), nullable=True)

    esd = db.relationship('ESD',back_populates='address')
    district = db.relationship('District',back_populates='address')
    school = db.relationship('School',back_populates='address')
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=True)
    middlename = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    esd = db.relationship('ESD',back_populates="administrator") 
    district = db.relationship('District',back_populates="administrator") 
    school = db.relationship('School',back_populates="administrator") 

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs }