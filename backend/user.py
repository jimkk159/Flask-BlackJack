from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

# self import
from backend.extension import db
from backend.forms import RegisterForm
from SQL.SQL_management import User

user_blueprint = Blueprint('user', __name__)


# Setting
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    register_form = RegisterForm()
    if register_form.validate_on_submit():

        # repeat register
        query_user = User.query.filter_by(name=register_form.name.data).first()
        if query_user:
            login_user(query_user)
        else:
            new_user = User(name=register_form.name.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        return redirect(url_for('table.reset'))
    return render_template('login.html', register_form=register_form), 200


# Logout
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
