import uuid
from flask import render_template, redirect, url_for, session, current_app, flash
from flask_login import login_user, logout_user, login_required, current_user

# self import
from . import game_route
from app.extension import db
from app.forms import LoginForm
from SQL.SQL_management import User


# Setting
@game_route.route('/login', methods=['GET', 'POST'])
def login():
    print('I got login')
    game = current_app.config["GAME"]
    login_form = LoginForm()
    if login_form.validate_on_submit():

        query_user = User.query.filter_by(name=login_form.name.data).first()
        if query_user and game.get_player_name_table(login_form.name.data):
            flash('User Name already exist!')
            return redirect(url_for('game_route.login'))
        elif query_user:
            login_user(query_user)
        else:
            new_user = User(id=str(uuid.uuid1()), name=login_form.name.data, money=100)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        session['name'] = login_form.name.data
        return redirect(url_for('game_route.room_map'))

    login_form.name.data = session.get('name', '')
    return render_template('login.html', register_form=login_form), 200


# Logout
@game_route.route('/logout')
@login_required
def logout():
    print('I got logout')
    # Config
    game = current_app.config["GAME"]
    table = game.get_player_table(current_user)
    table_name = table.get_name()
    current_player = table.get_player_by_id(current_user.id)

    game.leave_table(current_user, table)
    logout_user()

    # Update Player money
    query_user = User.query.filter_by(name=current_player.get_name()).first()
    query_user.money = current_player.get_money()
    db.session.commit()

    if game.get_is_table_empty(table):
        game.delete_table(table_name)
    return redirect(url_for('game_route.home'))
