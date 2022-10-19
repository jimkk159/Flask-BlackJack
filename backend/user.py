from flask import Blueprint, render_template, redirect, url_for

# self import
from backend.extension import db
from backend.forms import RegisterForm
from SQL.SQL_management import User

user_blueprint = Blueprint('user', __name__)


# Setting
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():

        new_user = User(name=register_form.name.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('table.reset'))
    return render_template('login.html', register_form=register_form), 200
