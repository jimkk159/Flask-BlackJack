from flask import Blueprint, render_template, current_app, redirect, url_for

# self import
from backend.card import Card
from backend.forms import SettingForm

table_blueprint = Blueprint('table', __name__)


# Check Blackjack
def check_blackjack(game, player):
    if game.get_is_banker_blackjack():
        game.reveal_banker_card()
    return game.check_player_blackjack(player)


@table_blueprint.route("/table")
def table():
    game_end = current_app.config["game_end"]
    game = current_app.config["blackjack_game"]
    show_insurance = current_app.config["show_insurance"]
    is_check_blackjack = current_app.config["check_blackjack"]
    banker = game.get_banker_cards()
    players = game.get_players_in()

    if show_insurance:
        ask_insurance = show_insurance and game.get_is_insurance() and game.get_judge_insurance()
        return render_template('table.html', banker=banker, players=players, ask_insurance=ask_insurance,
                               game_end=game_end), 200
    else:
        if is_check_blackjack:
            current_app.config["check_blackjack"] = False
            if check_blackjack(game, player):
                return redirect(url_for('table.end'))
        return render_template('table.html', banker=banker, players=players, ask_insurance=False,
                               game_end=game_end), 200


@table_blueprint.route("/table/insurance/<int:player_id>/<int:answer>")
def insurance(player_id, answer):
    print('I got insurance')
    game = current_app.config["blackjack_game"]
    current_app.config["show_insurance"] = False
    current_app.config["check_blackjack"] = False
    for player in game.players.in_:
        if player.id == player_id:
            if answer == 1:
                game.player_has_insurance(player)
            if check_blackjack(game, player):
                return redirect(url_for('table.end'))
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/double/<int:player_id>")
def double(player_id):
    print('I got double')
    game = current_app.config["blackjack_game"]
    for player in game.get_players_in():
        if player.id == player_id:
            game.double_down_process(player)

    # ToDo after double need to wait for other player finish
    return redirect(url_for('table.end'))


@table_blueprint.route("/table/split/<int:player_id>/<int:hand_id>")
def split(player_id, hand_id):
    print('I got split')
    game = current_app.config["blackjack_game"]
    for player in game.get_players_in():
        if player.id == player_id:
            for hand in player.get_hands():
                if hand.id == hand_id:
                    game.split_process(player, hand)
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
            if game.get_is_player_end(player):
                return redirect(url_for('table.end'))
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/stand/<int:player_id>/<int:hand_id>")
def stand(player_id, hand_id):
    print('I got stand')
    game = current_app.config["blackjack_game"]
    for player in game.get_players_in():
        if player.id == player_id:
            for hand in player.get_hands():
                if hand.id == hand_id:
                    game.set_hand_stand(hand)
            game_end = game.get_is_player_end(player)
            if game_end:
                return redirect(url_for('table.banker'))
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/banker")
def banker():
    print("I got banker")
    game = current_app.config["blackjack_game"]
    game.reveal_banker_card()
    game.deal_to_banker()
    if game.get_is_banker_bust():
        game.banker_bust_process()
    else:
        game.compare_cards()
    return redirect(url_for('table.end'))


@table_blueprint.route("/table/end")
def end():
    print("I got end")
    game = current_app.config["blackjack_game"]
    # ToDo need to wait for other player finish
    game.give_money(player)
    current_app.config["game_end"] = True
    return redirect(url_for('table.table'))


@table_blueprint.route("/table/reset")
def reset():
    print("I got reset")
    game = current_app.config["blackjack_game"]
    current_app.config["game_end"] = False
    current_app.config["show_insurance"] = True
    current_app.config["check_blackjack"] = True
    game.reset()
    game.deal_initial()
    # game.banker = [Card(symbol='K', suit='spade', faced=False),
    #                Card(symbol='A', suit='heart')]
    # game.get_players_in()[0].get_hands()[0].cards = [Card(symbol='A', suit='spade'),
    #                                                  Card(symbol='A', suit='heart')]
    return redirect(url_for('table.table'))
