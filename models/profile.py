from flask import render_template, Blueprint, url_for, redirect, request, flash, jsonify
from models.models import object_to_id, Grades, User
from api.layout import *
from app import db
from flask_login import login_required, current_user
from datetime import *
import pdb

prf = Blueprint("profile", __name__)

stamp = 1630454400
delta = 86400

dates = [datetime.fromtimestamp(i * delta + stamp).strftime('%d.%m') for i in range(25)]
timestamps = [i * delta + stamp for i in range(25)]


@prf.route('/profile')
@login_required
def profile():
    groups = list()
    if current_user.groups is not None:
        groups = [i for i in current_user.groups]
        gr = list()

        for i in range(int(len(groups) / 2)):
            gr.append(str(groups[2 * i]) + str(groups[2 * i + 1]))

        groups = gr
    return render_template('html/profile.html', current_user=current_user, name=current_user.name, id=current_user.id,
                           title="Profile", groups=groups)


@prf.route('/profile/grades')
@login_required
def show_grades():
    names = object_to_id.query.all()
    grades = Grades.query.filter_by(user_id=current_user.id).all()
    objects = grades_schema.dump(grades)
    rates = {object['object_id']: dict() for object in objects}

    for object in objects:
        rates[object['object_id']][object['timestamp']] = object['grade_id'] if object['grade_id'] != 13 else 'Abs'

    return render_template('html/grades.html', dates=dates, names=names,
                           timestamps=timestamps, rates=rates, title='Grades')


@prf.route("/profile/group/<int:group_id>/<string:objective>", methods=["GET", "POST"])
@login_required
def show_group(group_id, objective):
    if current_user.role == 1:
        group = User.query.filter_by(group=group_id).all()
        profiles = profiles_schema.dump(group)
        ids = [i['name'] for i in profiles]
        results = dict()
        for i in profiles:
            grades = Grades.query.filter_by(user_id=i['id']).all()
            objects = grades_schema.dump(grades)
            grades = {object['object_id']: dict() for object in objects}
            for object in objects:
                grades[object['object_id']][object['timestamp']] = object['grade_id'] \
                    if object['grade_id'] != 13 else 'Abs'
            results[i['id']] = grades
        objects = objects_schema.dump(object_to_id.query.all())
        ids.reverse()
        for i in objects:
            if i['name'].lower() == objective.lower():
                objective = i['id']
                break
        return render_template('html/group.html', title=str(group_id) + ' group', users=results,
                               dates=dates, timestamps=timestamps, ids=ids, objects=objects, objective=objective)
    else:
        return redirect(url_for('main.home'))
