from flask import render_template, current_app, redirect, url_for, session
from flask_login import current_user



# self import
from . import game_route
from app.game_component.card import Card
from app.extension import check_blackjack, set_cards_location


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
