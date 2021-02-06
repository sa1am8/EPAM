from flask import render_template, Blueprint, url_for, redirect, request, flash
from models.models import Employee
from app import db
from forms.forms import EmployeeForm, SearchForm
from datetime import datetime

profile = Blueprint("profile", __name__)


@profile.route("/profile")
def show_profile():
    return render_template('/html/profile.html')
