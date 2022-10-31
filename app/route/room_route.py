from flask_login import current_user
from flask import render_template, current_app, redirect, url_for, session, flash

# self import
from . import game_route
from app.forms import SettingForm


@game_route.route("/room")
def room_map():
    print('I got room')

    # Config
    game = current_app.config["GAME"]

    # Session
    room = session.get('room', '')

    return render_template('room.html', game=game), 200


@game_route.route('/room/enter/<room>')
def enter_room(room):
    print('I got enter room')

    game = current_app.config["GAME"]

    # Room Name
    session['room'] = room
    game.enter_table(table_name=room, player_id=current_user.id, player_name=current_user.name,
                     money=current_user.money)

    # Set Ready
    table_ = game.get_table_by_name(room)
    player = table_.get_player_by_id(current_user.id)
    player.set_is_ready(True)

    return redirect(url_for('game_route.wait'))


@game_route.route('/room/create', methods=['GET', 'POST'])
def create_room():
    print('I got create room')

    setting_form = SettingForm()
    game = current_app.config["GAME"]

    if setting_form.validate_on_submit():

        name = session.get('name', '')
        if name == '':
            flash('Login Please')
            return redirect(url_for('game_route.login'))

        room = setting_form.room.data

        if room == '':
            flash('Empty Room name')
            print(1)
            return redirect(url_for('game_route.create_room'))

        if room == '' or game.get_is_table_exit(room):
            flash('Room already exists')
            return redirect(url_for('game_route.create_room'))

        # Room Name
        session['room'] = setting_form.room.data

        # Deck Number
        deck_num = setting_form.decks.data

        # Player Number
        max_player = setting_form.players.data

        # Minimum wager
        min_bet = setting_form.min_bet.data

        # BlackJack ratio
        bj_ratio = setting_form.bj_ratio.data

        # Insurance
        is_insurance = setting_form.is_insurance.data

        # Face Card  Insurance
        is_over_10 = setting_form.is_over_10.data

        # Double
        is_double = setting_form.is_double.data

        game.create_table(table_name=room, deck_num=deck_num, max_player=max_player, min_bet=min_bet, bj_ratio=bj_ratio,
                          is_insurance=is_insurance, is_insurance_over_10=is_over_10, is_double=is_double)

        game.enter_table(table_name=room, player_id=current_user.id, player_name=current_user.name,
                         money=current_user.money)
        table_ = game.get_table_by_name(room)

        # Set Ready
        player = table_.get_player_by_id(current_user.id)
        player.set_is_ready(True)

        table_.set_owner()
        return redirect(url_for('game_route.wait'))

    return render_template('setting.html', setting_form=setting_form, game=game), 200
