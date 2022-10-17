from flask import Blueprint, render_template, current_app, redirect, url_for

# self import
from backend.forms import SettingForm

table_blueprint = Blueprint('table', __name__)


@table_blueprint.route("/table")
def table():
    game = current_app.config["blackjack_game"]
    banker = game.banker
    players = game.players.in_
    return render_template('table.html', banker=banker, players=players), 200


@table_blueprint.route("/table/double/<int:player_id>")
def double(player_id):
    print('I got double')
    game = current_app.config["blackjack_game"]
    for player in game.players.in_:
        if player.id == player_id:
            game.double_down_process(player)
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/split")
def split():
    print('I got split')
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/hit/<int:player_id>/<int:hand_id>")
def hit(player_id, hand_id):
    print('I got hit')
    game = current_app.config["blackjack_game"]
    for player in game.get_players_in():
        if player.id == player_id:
            for hand in player.get_hands():
                if hand.id == hand_id:
                    game.hit_process(hand)
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/stand")
def stand():
    print('I got stand')
    return redirect(url_for('table.table'))
