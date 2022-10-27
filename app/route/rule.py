from flask import render_template

# self import
from . import game_route


@game_route.route("/rule")
def rule():
    return render_template('rule.html'), 200
