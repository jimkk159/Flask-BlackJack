from flask import render_template, current_app, redirect, url_for, session
from flask_login import current_user

# self import
from . import game_route
from app import socketio


# Check Blackjack
def check_blackjack(game, player):
    if game.get_is_banker_blackjack():
        game.reveal_banker_card()
    return game.check_player_blackjack(player)


@game_route.route("/table")
def table():
    print('I got table')

    # Config
    game_end = current_app.config["END"]
    game = current_app.config["GAME"]
    show_insurance = current_app.config["show_insurance"]
    is_check_blackjack = current_app.config["check_blackjack"]

    # Session
    name = session.get('name', '')
    room = session.get('room', '')

    banker = game.get_banker_cards()
    players = game.get_players_in()
    if show_insurance and game.get_is_insurance() and game.get_judge_insurance():
        return render_template('table.html', banker=banker, players=players, ask_insurance=True,
                               game_end=game_end, name=name, room=room), 200
    if is_check_blackjack:
        current_app.config["check_blackjack"] = False
        player = game.get_player_by_id(current_user.id)
        if check_blackjack(game, player):
            return redirect(url_for('game_route.end'))
    return render_template('table.html', banker=banker, players=players, ask_insurance=False,
                           game_end=game_end, name=name, room=room), 200


@game_route.route("/table/insurance/<int:answer>")
def insurance(answer):
    print('I got insurance')
    game = current_app.config["GAME"]
    current_app.config["show_insurance"] = False
    current_app.config["check_blackjack"] = False
    player = game.get_player_by_id(current_user.id)
    if answer == 1:
        game.player_has_insurance(player)
    if check_blackjack(game, player):
        return redirect(url_for('game_route.end'))
    return redirect(url_for('game_route.table'))


@game_route.route("/table/double")
def double():
    print('I got double')
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    if game.double_down_process(player):
        return redirect(url_for('game_route.end'))
    # ToDo after double need to wait for other player finish
    return redirect(url_for('game_route.banker'))


@game_route.route("/table/split/<string:hand_id>")
def split(hand_id):
    print('I got split')
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    hand = player.get_hand_by_id(hand_id)
    game.split_process(player, hand)
    return redirect(url_for('game_route.table'))


@game_route.route("/table/hit/<string:hand_id>")
def hit(hand_id):
    print('I got hit')
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    hand = player.get_hand_by_id(hand_id)
    game.hit_process(hand)
    if game.get_is_player_end(player):
        return redirect(url_for('game_route.end'))

    if game.get_is_player_finish(player):
        return redirect(url_for('game_route.banker'))

    return redirect(url_for('game_route.table'))


@game_route.route("/table/stand/<string:hand_id>")
def stand(hand_id):
    print('I got stand')
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    hand = player.get_hand_by_id(hand_id)
    game.stand_process(hand)
    if game.get_is_player_finish(player):
        return redirect(url_for('game_route.banker'))
    return redirect(url_for('game_route.table'))


@game_route.route("/table/fold")
def fold():
    print('I got fold')
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    game.fold_process(player)
    return redirect(url_for('game_route.end'))


@game_route.route("/table/banker")
def banker():
    print("I got banker")
    game = current_app.config["GAME"]
    game.reveal_banker_card()
    game.deal_to_banker()
    if game.get_is_banker_bust():
        game.banker_bust_process()
    else:
        game.compare_cards()
    return redirect(url_for('game_route.end'))


@game_route.route("/table/end")
def end():
    print("I got end")
    game = current_app.config["GAME"]
    player = game.get_player_by_id(current_user.id)
    # ToDo need to wait for other player finish
    game.give_money(player)
    current_app.config["END"] = True
    return redirect(url_for('game_route.table'))


@game_route.route("/table/reset")
def reset():
    print("I got reset")
    game = current_app.config["GAME"]
    current_app.config["END"] = False
    current_app.config["show_insurance"] = True
    current_app.config["check_blackjack"] = True
    game.enter_table(id_=current_user.id, name=current_user.name, money=current_user.money)
    player = game.get_player_by_id(current_user.id)
    game.reset()
    game.pay_player_stake(player)
    game.deal_initial()
    # game.banker = [Card(symbol='K', suit='spade', value=10, faced=False),
    #                Card(symbol='A', suit='heart', value=11)]
    # game.get_players_in()[0].get_hands()[0].cards = [Card(symbol='A', value=11, suit='spade'),
    #                                                  Card(symbol='A', value=11, suit='heart')]
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('game_route.login'))
    return redirect(url_for('game_route.table', name=name, room=room))
