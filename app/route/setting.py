from flask import session, render_template, current_app

# self import
from app.forms import SettingForm
from . import game_route


# Setting
@game_route.route('/setting', methods=['GET', 'POST'])
def setting():
    setting_form = SettingForm()
    game = current_app.config["GAME"]

    room = session.get('room', '')

    submit_result = False
    if setting_form.validate_on_submit():
        submit_result = True
        # Deck Number
        deck_num = setting_form.decks.data
        game.set_table_name_deck_num(table_name=room, deck_num=deck_num)

        # Player Number
        players_num = setting_form.players.data
        game.set_table_name_max(table_name=room, max_player_num=players_num)

        # Minimum wager
        min_bet = setting_form.min_bet.data
        game.set_table_name_min_bet(table_name=room, min_bet=min_bet)

        # BlackJack ratio
        bj_ratio = setting_form.bj_ratio.data
        game.set_table_name_blackjack_ratio(table_name=room, bj_ratio=bj_ratio)

        # Insurance
        is_insurance = setting_form.is_insurance.data
        game.set_table_name_is_insurance(table_name=room, is_insurance=is_insurance)

        # Face Card  Insurance
        is_over_10 = setting_form.is_over_10.data
        game.set_table_name_insurance_over_10(table_name=room, is_over_10=is_over_10)

        # Double
        is_double = setting_form.is_double.data
        game.set_table_name_is_double(table_name=room, is_double=is_double)

    return render_template('setting.html', setting_form=setting_form, game=game, submit_result=submit_result,
                           room=room), 200
