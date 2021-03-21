from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User
from flask_login import login_user
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login_post'))

    login_user(user, remember=remember)
    return redirect(url_for('profile.profile'))

@auth.route('/login', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        return render_template('html/login.html')
    else:
        return redirect(url_for('profile.profile'))

@auth.route('/signup')
def signup():
    return render_template('html/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    if '@sliceum.com' not in email:
        flash('Email address must contain @sliceum.com')
        return redirect(url_for('auth.signup'))
    name = request.form.get('name')
    password = request.form.get('password')
    group = request.form.get('group')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, group=group, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login_post'))