from flask import Blueprint, render_template, current_app

# self import
from backend.forms import SettingForm

table_blueprint = Blueprint('table', __name__)


@table_blueprint.route("/table")
def table():
    game = current_app.config["blackjack_game"]
    banker = game.banker
    players = game.players.in_
    return render_template('table.html', banker=banker, players=players), 200

