from flask import Blueprint, render_template

# self import

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def home():
    return render_template('index.html'), 200