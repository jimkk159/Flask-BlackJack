from flask import render_template, current_app, redirect, url_for, session
from flask_login import current_user

# self import
from . import game_route
from app.extension import set_cards_location


@game_route.route("/table")
def table():
    print('I got table')

    # Config
    game = current_app.config["GAME"]
    room = session.get('room', '')
    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)
    show_insurance = player.get_show_insurance()
    is_check_blackjack = player.get_show_blackjack()

    # Session
    name = session.get('name', '')
    room = session.get('room', '')

    table_ = game.get_table_by_name(room)
    banker_ = table_.get_banker_cards()
    player = table_.get_player_by_id(current_user.id)
    set_cards_location(table_)
    game_start = table_.get_game_start()

    if game_start and show_insurance and table_.get_is_insurance() and table_.get_judge_insurance():
        return render_template('table.html', banker=banker_, table=table_, ask_insurance=True, name=name,
                               room=room), 200

    if game_start and is_check_blackjack:
        player.set_show_blackjack(False)
        table_.check_player_blackjack(player)
        if player.get_is_blackjack():
            table_.give_player_money(player)
        table_.end_process()

    return render_template('table.html', banker=banker_, table=table_, ask_insurance=False, name=name, room=room), 200


@game_route.route("/table/insurance/<int:answer>")
def insurance(answer):
    print('I got insurance')

    # Config
    game = current_app.config["GAME"]
    room = session.get('room', '')
    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)

    player.set_show_insurance(False)

    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)
    if answer == 1:
        table_.player_has_insurance(player)

    return redirect(url_for('game_route.table'))


@game_route.route("/wait")
def wait():
    print("I got wait")

    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('game_route.login'))

    return redirect(url_for('game_route.table'))

