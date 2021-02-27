from flask import render_template, Blueprint, url_for, redirect, request, flash, jsonify
from models.models import object_to_id, Grades
from api.layout import *
from app import db
from flask_login import login_required, current_user
from datetime import *

prf = Blueprint("profile", __name__)


@prf.route('/profile')
@login_required
def profile():
    return render_template('html/profile.html', current_user=current_user, name=current_user.name, id=current_user.id)


@prf.route('/profile/grades')
@login_required
def show_grades():
    stamp = 1630454400
    delta = 86400
    ids = range(1, 15)
    dates = [datetime.fromtimestamp(i * delta + stamp).strftime('%d.%m') for i in range(30)]
    timestamps = [i * delta + stamp for i in range(30)]
    grades = Grades.query.filter_by(user_id=current_user.id).all()
    objects = grades_schema.dump(grades)
    rates = {object['object_id']: dict() for object in objects}
    for object in objects:
        rates[object['object_id']][object['timestamp']] = object['grade_id'] if object['grade_id'] != 13 else 'Abs'
    print(rates)
    return render_template('html/grades.html', dates=dates, ids=ids,
                           timestamps=timestamps, rates=rates)
