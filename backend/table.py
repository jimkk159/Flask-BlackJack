from flask import Blueprint, render_template, current_app, redirect, url_for

# self import
from backend.forms import SettingForm

table_blueprint = Blueprint('table', __name__)


# Check Blackjack
def check_blackjack(game, player):
    if game.get_is_banker_blackjack():
        game.reveal_banker_card()
    return game.check_player_blackjack(player)


@table_blueprint.route("/table/<int:show_insurance>")
def table(show_insurance):
    game = current_app.config["blackjack_game"]
    banker = game.banker
    players = game.players.in_
    ask_insurance = show_insurance and game.get_is_insurance() and game.get_judge_insurance()
    return render_template('table.html', banker=banker, players=players, ask_insurance=ask_insurance), 200


@table_blueprint.route("/table/insurance/<int:player_id>/<int:answer>")
def insurance(player_id, answer):
    print('I got insurance')
    game = current_app.config["blackjack_game"]
    game_end = False
    for player in game.players.in_:
        if player.id == player_id:
            if answer == 1:
                game.player_has_insurance(player)
            game_end = check_blackjack(game, player)

    return redirect(url_for('table.table', show_insurance=0, game_end=game_end))


@table_blueprint.route("/table/double/<int:player_id>")
def double(player_id):
    print('I got double')
    game = current_app.config["blackjack_game"]
    game_end = False
    for player in game.players.in_:
        if player.id == player_id:
            game_end = game.double_down_process(player)
    return redirect(url_for('table.table', show_insurance=0, game_end=game_end))


@table_blueprint.route("/table/split")
def split():
    print('I got split')
    return redirect(url_for('table.table', show_insurance=0, game_end=False))


@table_blueprint.route("/table/hit/<int:player_id>/<int:hand_id>")
def hit(player_id, hand_id):
    print('I got hit')
    game = current_app.config["blackjack_game"]
    game_end = False
    for player in game.get_players_in():
        if player.id == player_id:
            for hand in player.get_hands():
                if hand.id == hand_id:
                    game.hit_process(hand)
            game_end = game.get_is_player_end(player)
    return redirect(url_for('table.table', show_insurance=0, game_end=game_end))


@table_blueprint.route("/table/stand")
def stand():
    print('I got stand')
    return redirect(url_for('table.table', show_insurance=0, game_end=False))
