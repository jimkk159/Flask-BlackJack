from flask import render_template, current_app, redirect, url_for, session
from flask_login import current_user

# self import
from . import game_route
from app import socketio
from backend.game_component.card import Card


# Check Blackjack
def check_blackjack(game, player):
    if game.get_is_banker_blackjack():
        game.reveal_banker_card()
    return game.check_player_blackjack(player)


# Set Card Location
def set_cards_location(game):
    set_banker_location(game.get_banker_cards())
    if game.get_players_num() == 2:
        set_table_players_location(init_x=5, init_y=0, table_=game.get_table())


def set_banker_location(cards):
    if len(cards) > 0:
        cards[0].set_x(34)

    for num in range(len(cards)):
        if num > 1:
            cards[num].set_x(40 + 2 * num)


def set_table_players_location(init_x=0, init_y=0, x_space=30, y_space=0, table_=None):
    if table_:
        players = table_.get_players()
        for num in range(len(players)):
            set_player_location(init_x=init_x + num * x_space, init_y=init_y + num * y_space, player=players[num])


def set_player_location(init_x=0, init_y=0, x_space=10, y_space=0, player=None):
    if player:
        hands = player.get_hands()
        for num in range(len(hands)):
            set_hand_location(init_x=init_x + num * x_space, init_y=init_y + num * y_space, hand=hands[num])


def set_hand_location(init_x=0, init_y=0, x_space=2, y_space=15, hand=None):
    if hand:
        cards = hand.get_cards()
        for num in range(len(cards)):
            set_card_location(x=init_x + num * x_space, y=init_y + num * y_space, card=cards[num])


def set_card_location(x=0, y=0, card=None):
    card.set_x(x)
    card.set_y(y)


@game_route.route("/table")
def table():
    print('I got table')

    # Config
    game_end = current_app.config["END"]
    game = current_app.config["GAME"]
    show_insurance = current_app.config["SHOW_INSURANCE"]
    is_check_blackjack = current_app.config["SHOW_BLACKJACK"]

    # Session
    name = session.get('name', '')
    room = session.get('room', '')

    banker = game.get_banker_cards()
    set_cards_location(game)

    if show_insurance and game.get_is_insurance() and game.get_judge_insurance():
        return render_template('table.html', banker=banker, game=game, ask_insurance=True,
                               game_end=game_end, name=name, room=room), 200
    if is_check_blackjack:
        current_app.config["SHOW_BLACKJACK"] = False
        # ToDo remember to recover
        player = game.get_players()[0]
        # player = game.get_player_by_id(current_user.id)
        if check_blackjack(game, player):
            return redirect(url_for('game_route.end'))
    return render_template('table.html', banker=banker, game=game, ask_insurance=False,
                           game_end=game_end, name=name, room=room), 200


@game_route.route("/table/insurance/<int:answer>")
def insurance(answer):
    print('I got insurance')
    game = current_app.config["GAME"]
    current_app.config["SHOW_INSURANCE"] = False
    current_app.config["SHOW_BLACKJACK"] = False
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
    current_app.config["SHOW_INSURANCE"] = True
    current_app.config["SHOW_BLACKJACK"] = True
    game.set_players()
    # ToDo remember to recover
    # game.enter_table(id_=current_user.id, name=current_user.name, money=current_user.money)
    # player = game.get_player_by_id(current_user.id)
    game.reset()
    game.pay_all_stake()
    # game.pay_player_stake(player)
    game.deal_initial()
    # game.banker = [Card(symbol='K', suit='spade', value=10, faced=False),
    #                Card(symbol='A', suit='heart', value=11)]
    # game.get_players_in()[0].get_hands()[0].cards = [Card(symbol='A', value=11, suit='spade'),
    #                                                  Card(symbol='A', value=11, suit='heart')]
    game.get_players()[0].append_empty_hand()
    game.get_players()[0].get_hands()[1].cards = [Card(symbol='A', value=11, suit='spade'),
                                                  Card(symbol='A', value=11, suit='heart')]
    print(game.get_players()[0].get_hand(1))
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('game_route.login'))
    return redirect(url_for('game_route.table', name=name, room=room))
