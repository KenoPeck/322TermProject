from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



# Tables to link positions with relevant research fields and programming language experience
# ---------------------------------------------------------------------------------------------------
posFields = db.Table('posFields', 
    db.Column('position_id', db.Integer, db.ForeignKey('position.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
)
posLanguages = db.Table('posLanguages',
    db.Column('position_id', db.Integer, db.ForeignKey('position.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
)
# ---------------------------------------------------------------------------------------------------

# Position Model
# ---------------------------------------------------------------------------------------------------
class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(1500))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_commitment = db.Column(db.Integer)
    research_fields = db.relationship(
        'Research_field',
        secondary = posFields,
        primaryjoin=(posFields.c.position_id == id),
        backref=db.backref('posFields', lazy='dynamic'),
        lazy='dynamic'
    )
    language_experience = db.relationship('Language',
        secondary = posLanguages,
        primaryjoin=(posLanguages.c.position_id == id),
        backref=db.backref('posLanguages', lazy='dynamic'),
        lazy='dynamic'
    )
    misc_requirements = db.Column(db.String(500))
    faculty_contact = db.Column(db.Integer, db.ForeignKey('user.id'))
    def get_fields(self):
        return self.research_fields
    def get_languages(self):
        return self.language_experience
# ---------------------------------------------------------------------------------------------------

# Relevant/Interested research field model
# ---------------------------------------------------------------------------------------------------
class Research_field(db.Model):
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    # positions  = db.relationship(
    #     'Position',
    #     secondary = posFields,
    #     primaryjoin=(posFields.c.field_id == id),
    #     lazy='dynamic',
    #     overlaps = "research_fields"
    # )
    def __repr__(self):
        return '<Research_field {}, {}>'.format(self.id,self.name)
# ---------------------------------------------------------------------------------------------------
    
# Required/Familiar Programming Language Model
# ---------------------------------------------------------------------------------------------------
class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    # positions  = db.relationship(
    #     'Position',
    #     secondary = posFields,
    #     primaryjoin=(posFields.c.language_id == id),
    #     lazy='dynamic',
    #     overlaps = "language_experience"
    # )
    def __repr__(self):
        return '<Language {}, {}>'.format(self.id,self.name)
# ---------------------------------------------------------------------------------------------------


# User loader function
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# User Model, Inherited by student and faculty models. Contains shared account info between the two models
# ---------------------------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    WSUID = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    user_type = db.Column(db.String(40))

    __mapper_args__ = {
        "polymorphic_identity": "User",
        "polymorphic_on": "user_type",
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return "<User {}, {}>".format(self.id,self.username)
# ---------------------------------------------------------------------------------------------------
    
# Tables to link students with Interested fields and languages they have experience in
# ---------------------------------------------------------------------------------------------------
studentFields = db.Table('studentFields', 
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
)
studentLanguages = db.Table('studentLanguages',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
)
# ---------------------------------------------------------------------------------------------------

# Student user model
# ---------------------------------------------------------------------------------------------------
class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.ForeignKey("user.id"), primary_key = True)
    major = db.Column(db.String(20))
    gpa = db.Column(db.Integer)
    grad_date = db.Column(db.DateTime)
    research_fields = db.relationship(
        'Research_field',
        secondary = studentFields,
        primaryjoin=(studentFields.c.student_id == id),
        backref=db.backref('studentFields', lazy='dynamic'),
        lazy='dynamic'
    )
    language_experience = db.relationship(
        'Language',
        secondary = studentLanguages,
        primaryjoin=(studentLanguages.c.student_id == id),
        backref = db.backref('studentLanguages', lazy = 'dynamic'),
        lazy='dynamic'
    )
    prior_experience = db.Column(db.String(200))
    __mapper_args__ = {"polymorphic_identity": "Student"}

    def is_faculty():
        return False
# ---------------------------------------------------------------------------------------------------

# Faculty user model
# ---------------------------------------------------------------------------------------------------
class Faculty(User):
    __tablename__ = 'faculty'
    id = db.Column(db.ForeignKey("user.id"), primary_key = True)
    primary_institution = db.Column(db.String(40))
    positions = db.relationship('Position', backref= 'faculty', lazy='dynamic')
    __mapper_args__ = {"polymorphic_identity": "Faculty"}

    def is_faculty():
        return True
# ---------------------------------------------------------------------------------------------------
