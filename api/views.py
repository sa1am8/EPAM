from flask import Blueprint, request, jsonify
from models.models import Employee, Department, Grades, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from app import db
import datetime
import sys

sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM/api')
from layout import *

api = Blueprint("api", __name__)


@api.route("/api/profile", methods=["GET"])
@login_required
def get_grades_current_user():
    grades = Grades.query.filter_by(user_id=current_user.id).all()
    results = grades_schema.dump(grades)
    return jsonify(results)


@api.route("/api/group/<int:group_id>", methods=["GET"])
def get_group_members(group_id):
    group = User.query.filter_by(group=group_id).all()
    results = profiles_schema.dump(group)
    return jsonify(results)


@api.route("/api/group/<int:group_id>/<string:objective>", methods=["POST"])
def update_group_rates(group_id, objective):
    """
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    grade_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)"""
    object_id = request.json['object_id']
    user_id = request.json['user_id']
    grade_id = request.json['grade_id']
    timestamp = request.json['timestamp']

    new_grade = Grades(object_id=object_id,
                      user_id=user_id,
                      grade_id=grade_id,
                      timestamp=timestamp
                      )

    db.session.add(new_grade)
    db.session.commit()

    return profile_schema.jsonify(new_grade)


@api.route('/api/user', methods=['POST'])
def api_add_user():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    role = request.json['role'] if 'role' in request.json else 0
    group = request.json['group'] if role == 0 else None
    groups = request.json['groups'] if 'groups' in request.json else None

    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    role=role,
                    group=group,
                    groups=groups
                    )

    db.session.add(new_user)
    db.session.commit()

    return profile_schema.jsonify(new_user)


@api.route("/api/employee", methods=["GET"])
def get_employees():
    """Return data of all employees."""
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


@api.route("/api/employee/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    """Return data of an employee with a given id."""
    employee = Employee.query.get_or_404(employee_id)
    return employee_schema.jsonify(employee)


@api.route("/api/employee", methods=["POST"])
def api_add_employee():
    """Add a new employee."""
    # Get attributes for an employee from json.
    name = request.json["name"]
    date_of_birth = request.json["date_of_birth"]
    date_of_birth = datetime.date(int(date_of_birth.split('/')[2]),
                                  int(date_of_birth.split('/')[1]),
                                  int(date_of_birth.split('/')[0]))
    salary = request.json["salary"]
    department_id = request.json["department_id"]
    # Create a new employee with received values.
    new_employee = Employee(
        name=name,
        date_of_birth=date_of_birth,
        salary=salary,
        department_id=department_id
    )
    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


@api.route("/api/employee/<int:employee_id>", methods=["PUT"])
def api_update_employee(employee_id):
    """Update an employee with a given id."""

    employee = Employee.query.get_or_404(employee_id)
    # Get attributes for an employee from json.
    name = request.json["name"]
    date_of_birth = request.json["date_of_birth"]
    salary = request.json["salary"]
    department_id = request.json["department_id"]
    # Set new values for attributes.
    employee.name = name
    employee.date_of_birth = date_of_birth
    employee.salary = salary
    employee.department_id = department_id

    db.session.commit()

    return employee_schema.jsonify(employee)


@api.route("/api/employee/<int:employee_id>", methods=["DELETE"])
def api_delete_employee(employee_id):
    """Delete an employee with a given id."""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# =========== Departments ==========

@api.route("/api/department", methods=["GET"])
def get_departments():
    """Return data of all departments."""
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    return jsonify(result)


@api.route("/api/department/<int:department_id>", methods=["GET"])
def get_department(department_id):
    """Return data of a department with a given id."""
    department = Department.query.get_or_404(department_id)
    return department_schema.jsonify(department)


@api.route("/api/department", methods=["POST"])
def api_add_department():
    """Add a new department."""
    # Get name from json.
    name = request.json["name"]
    # Create department with name from json.
    new_department = Department(name=name)
    db.session.add(new_department)
    db.session.commit()

    return department_schema.jsonify(new_department)


@api.route("/api/department/<int:department_id>", methods=["PUT"])
def api_update_department(department_id):
    """Update a department with a given id."""
    department = Department.query.get_or_404(department_id)
    # Get name from json.
    name = request.json["name"]
    # Set new department name.
    department.name = name
    db.session.commit()

    return department_schema.jsonify(department)


@api.route("/api/department/<int:department_id>", methods=["DELETE"])
def api_delete_department(department_id):
    """Delete a department with a given id."""
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()

    return department_schema.jsonify(department)
