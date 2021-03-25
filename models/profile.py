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
days_per_page = 28
page = 1


def generate_dates_and_timestamps(page):
    dates, i, count = list(), days_per_page * (page - 1), days_per_page * (page - 1)
    while count < days_per_page * page:
        if datetime.fromtimestamp(i * delta + stamp).strftime('%A') == 'Sunday':
            i += 1
        elif datetime.fromtimestamp(i * delta + stamp).strftime('%A') == 'Saturday':
            i += 2
        else:
            dates.append(datetime.fromtimestamp(i * delta + stamp).strftime('%d.%m'))
            count += 1
            i += 1

    timestamps, i, count = list(), days_per_page * (page - 1), days_per_page * (page - 1)
    while count < days_per_page * page:
        if datetime.fromtimestamp(i * delta + stamp).strftime('%A') == 'Sunday':
            i += 1
        elif datetime.fromtimestamp(i * delta + stamp).strftime('%A') == 'Saturday':
            i += 2
        else:
            timestamps.append(i * delta + stamp)
            i += 1
            count += 1
    return dates, timestamps


_ = generate_dates_and_timestamps(page)
dates, timestamps = _[0], _[1]


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


@prf.route('/profile/grades/', methods=["GET", "POST"])
@login_required
def show_grades():
    if request.method == 'POST':
        print(request.data)
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])
    names = object_to_id.query.all()
    grades = Grades.query.filter_by(user_id=current_user.id).all()
    objects = grades_schema.dump(grades)
    rates = {object['object_id']: dict() for object in objects}
    for object in objects:
        rates[object['object_id']][object['timestamp']] = object['grade_id'] if object['grade_id'] != 13 else 'Abs'

    _ = generate_dates_and_timestamps(page)
    dates, timestamps = _[0], _[1]

    return render_template('html/grades.html', dates=dates, names=names, page=page,
                           timestamps=timestamps, rates=rates, title='Grades')


@prf.route("/profile/group/<int:group_id>/<string:objective>/", methods=["GET", "POST"])
@login_required
def show_group(group_id, objective):
    if current_user.role == 1:
        page = 1
        if 'page' in request.args:
            page = int(request.args['page'])

        _ = generate_dates_and_timestamps(page)
        dates, timestamps = _[0], _[1]

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
                objective_id = i['id']
                break

        return render_template('html/group.html', title=str(group_id) + ' group', users=results, group_id=group_id,
                               dates=dates, timestamps=timestamps, ids=ids, objects=objects, objective=objective,
                               objective_id=int(objective_id), page=page)
    else:
        return redirect(url_for('main.home'))


@prf.route("/profile/group/<int:group_id>/<string:objective>/change", methods=["GET"])
@login_required
def change_rates_group(group_id, objective):
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
                objective_id = i['id']
                break
        url = '/profile/group/{}/{}/change'.format(group_id, objective)

        return render_template('html/group_changes.html', title=str(group_id) + ' group', users=results,
                               objective=objective, group_id=group_id, url=url,  # object_name=object_name,
                               dates=dates, timestamps=timestamps, ids=ids, objects=objects,
                               objective_id=int(objective_id))

    else:
        return redirect(url_for('main.home'))


@prf.route("/profile/group/<int:group_id>/<string:objective>/change", methods=["POST"])
@login_required
def change_rates_group_update(group_id, objective):
    if current_user.role == 1:
        objective_id = objective
        group = User.query.filter_by(group=group_id).all()
        profiles = profiles_schema.dump(group)
        ids = [i['name'] for i in profiles]

        # object_name = {i.id : i.name for i in object_to_id.query.all()}[int(objective)]
        results_origin = dict()
        for i in profiles:
            grades = Grades.query.filter_by(user_id=i['id']).all()
            objects = grades_schema.dump(grades)
            grades = {object['object_id']: dict() for object in objects}
            for object in objects:
                grades[object['object_id']][object['timestamp']] = object['grade_id'] \
                    if object['grade_id'] != 13 else 'Abs'
            results_origin[i['id']] = grades
        objects = objects_schema.dump(object_to_id.query.all())
        for i in objects:

            if i['name'].lower() == objective.lower():
                objective_id = i['id']
                break

        ids.reverse()
        results = request.form
        for i in results:
            j = i
            i = i.replace('grade_input', '')
            user_id, time = i.split('_')[0], i.split('_')[1]
            rate = results[j] if results[j] != 'Abs' else 13
            grade = Grades.query.filter_by(user_id=user_id, timestamp=time,
                                           object_id=objective_id).first()

            if not grade:
                if rate != "-":
                    grade = Grades(user_id=user_id, object_id=objective_id, grade_id=rate, timestamp=time)
                    db.session.add(grade)

            else:
                if rate == "-":
                    db.session.delete(grade)

                else:
                    grade.grade_id = rate

            db.session.commit()

        url = '/profile/group/{}/{}/change'.format(group_id, objective)

        return redirect(url_for('profile.show_group', group_id=group_id, objective=objective))
    else:
        return redirect(url_for('main.home'))
