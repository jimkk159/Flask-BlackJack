from flask import render_template

# self import
from . import game_route


@game_route.route("/")
def home():
    return render_template('index.html'), 200
