from flask import render_template, current_app, redirect, url_for, session
from flask_login import current_user

TABLE_WIDTH = 81
CARD_WIDTH = 5

INIT_CARD_X_SPACE = 2.0
INIT_CARD_Y_SPACE = 15.0
INIT_HAND_X_SPACE = 12.0
INIT_HAND_Y_SPACE = 0.0
INIT_PLAYER_X_SPACE = 30.0
INIT_PLAYER_Y_SPACE = 0.0

# self import
from . import game_route
from app.game_component.card import Card


# Check Blackjack
def check_blackjack(table_, player):
    if table_.get_is_banker_blackjack():
        table_.reveal_banker_card()

    if table_.check_player_blackjack(player):
        return True
    return False


# Set Card Location
def set_cards_location(table_):
    set_banker_location(table_.get_banker_cards())

    if table_.get_player_num() == 1:
        set_table_players_location(init_x=TABLE_WIDTH / 2 - CARD_WIDTH / 2,
                                   table_=table_)

    elif table_.get_player_num() == 2:
        set_table_players_location(init_x=TABLE_WIDTH / 4 - 2 * CARD_WIDTH, player_x_space=43 - CARD_WIDTH,
                                   table_=table_)

    elif table_.get_player_num() == 3:
        set_table_players_location(init_x=TABLE_WIDTH / 5 - 2 * CARD_WIDTH,
                                   player_x_space=30 - CARD_WIDTH,
                                   hand_x_space=INIT_HAND_X_SPACE - 2,
                                   table_=table_)

    elif table_.get_player_num() == 4:
        set_table_players_location(init_x=TABLE_WIDTH / 6 - 2 * CARD_WIDTH,
                                   player_x_space=25 - CARD_WIDTH,
                                   hand_x_space=INIT_HAND_X_SPACE - 2,
                                   table_=table_)


def set_banker_location(cards):
    if len(cards) > 0:
        cards[0].set_x(34)

    for num in range(len(cards)):
        if num > 1:
            cards[num].set_x(40 + 2 * num)


def set_table_players_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand_x_space=None,
                               hand_y_space=None, player_x_space=30.0, player_y_space=0.0, table_=None):
    if table_:
        players = table_.get_players()
        for num in range(len(players)):
            set_player_location(init_x=init_x + (num * player_x_space if player_x_space else num * INIT_PLAYER_X_SPACE),
                                init_y=init_y + (num * player_y_space if player_y_space else num * INIT_PLAYER_Y_SPACE),
                                card_x_space=card_x_space,
                                card_y_space=card_y_space,
                                hand_x_space=hand_x_space,
                                hand_y_space=hand_y_space,
                                player=players[num])


def set_player_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand_x_space=None,
                        hand_y_space=None, player=None):
    if player:
        hands = player.get_hands()
        for num in range(len(hands)):
            set_hand_location(init_x=init_x + (num * hand_x_space if hand_x_space else num * INIT_HAND_X_SPACE),
                              init_y=init_y + (num * hand_y_space if hand_y_space else num * INIT_HAND_Y_SPACE),
                              card_x_space=card_x_space,
                              card_y_space=card_y_space,
                              hand=hands[num])


def set_hand_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand=None):
    if hand:
        cards = hand.get_cards()
        for num in range(len(cards)):
            set_card_location(x=init_x + (num * card_x_space if card_x_space else num * INIT_CARD_X_SPACE),
                              y=init_y + (num * card_y_space if card_y_space else num * INIT_CARD_Y_SPACE),
                              card=cards[num])


def set_card_location(x=0.0, y=0.0, card=None):
    card.set_x(x)
    card.set_y(y)


@game_route.route("/table")
def table():
    print('I got table')

    # Config
    game = current_app.config["GAME"]
    show_insurance = current_app.config["SHOW_INSURANCE"]
    is_check_blackjack = current_app.config["SHOW_BLACKJACK"]

    # Session
    name = session.get('name', '')
    room = session.get('room', '')

    table_ = game.get_table_by_name(room)
    banker_ = table_.get_banker_cards()
    player = table_.get_player_by_id(current_user.id)
    set_cards_location(table_)

    if show_insurance and table_.get_is_insurance() and table_.get_judge_insurance():
        return render_template('table.html', banker=banker_, table=table_, ask_insurance=True, name=name,
                               room=room), 200

    if is_check_blackjack:
        current_app.config["SHOW_BLACKJACK"] = False
        table_.check_player_blackjack(player)
        return redirect(url_for('game_route.end'))

    return render_template('table.html', banker=banker_, table=table_, ask_insurance=False, name=name, room=room), 200


@game_route.route("/table/insurance/<int:answer>")
def insurance(answer):
    print('I got insurance')
    game = current_app.config["GAME"]
    room = session.get('room', '')

    current_app.config["SHOW_INSURANCE"] = False

    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)
    if answer == 1:
        table_.player_has_insurance(player)

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
        game.banker_bust_process(table)
    else:
        game.compare_cards(table)
    return redirect(url_for('game_route.end'))


@game_route.route("/table/end")
def end():
    print("I got end")
    game = current_app.config["GAME"]
    room = session.get('room', '')

    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)
    # ToDo need to wait for other player finish
    table_.give_money(player)
    return redirect(url_for('game_route.table'))


@game_route.route("/wait")
def wait():
    print("I got wait")
    game = current_app.config["GAME"]

    # ToDo need to split by table
    current_app.config["SHOW_INSURANCE"] = True
    current_app.config["SHOW_BLACKJACK"] = True

    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('game_route.login'))


    table = game.get_table_by_name(table_name=room)
    player = table.get_player_by_id(current_user.id)

    table.reset()
    table.player_pay_stake(player)
    table.deal_initial()

    # For Debug
    # if len(game.get_players()) > 1:
    #     print("Player 1", game.get_players()[0].get_id())
    #     print("Player 2", game.get_players()[1].get_id())
    # table.banker = [Card(symbol='K', suit='spade', value=10, faced=False),
    #                 Card(symbol='A', suit='heart', value=11)]

    return redirect(url_for('game_route.table'))