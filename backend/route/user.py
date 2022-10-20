import uuid
from flask import render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required

# self import
from . import game_route
from backend.extension import db
from backend.forms import LoginForm
from SQL.SQL_management import User


# Setting
@game_route.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():

        query_user = User.query.filter_by(name=login_form.name.data).first()
        if query_user:
            login_user(query_user)
        else:
            new_user = User(id=str(uuid.uuid1()), name=login_form.name.data, money=100)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        session['name'] = login_form.name.data
        session['room'] = login_form.room.data
        return redirect(url_for('game_route.reset'))
    login_form.name.data = session.get('name', '')
    login_form.room.data = session.get('room', '')
    return render_template('login.html', register_form=login_form), 200


# Logout
@game_route.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))
