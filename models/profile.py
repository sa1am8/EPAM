from flask import render_template, Blueprint, url_for, redirect, request, flash
from app import db
from flask_login import login_required, current_user


prf = Blueprint("profile", __name__)


@prf.route('/profile')
@login_required
def profile():
    return render_template('html/profile.html', current_user=current_user, name=current_user.name, id=current_user.id)
