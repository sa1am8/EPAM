from flask_login import UserMixin
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class Employee(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salary = db.Column(db.Integer, index=True)
    name = db.Column(db.String(60), index=True, unique=True)
    date_of_birth = db.Column(db.Date, index=True)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __repr__(self):
        return '<Employee: {}>'.format(self.name)


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)


class Grades(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    grade_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Post %r>' % (self.id)