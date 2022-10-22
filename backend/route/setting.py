from flask import render_template, current_app

# self import
from backend.forms import SettingForm
from . import game_route


# Setting
@game_route.route('/setting', methods=['GET', 'POST'])
def setting():
    setting_form = SettingForm()
    game = current_app.config["GAME"]
    submit_result = False
    if setting_form.validate_on_submit():
        submit_result = True
        # Deck Number
        deck_num = setting_form.decks.data
        game.set_deck_num(deck_num)
        # Player Number
        players_num = setting_form.players.data
        game.set_player_num(players_num)

        # Insurance
        is_insurance = setting_form.is_insurance.data
        game.set_is_insurance(is_insurance)

        # Face Card  Insurance
        is_over_10 = setting_form.is_over_10.data
        game.set_insurance_over_10(is_over_10)

        # Double
        is_double = setting_form.is_double.data
        game.set_is_double(is_double)

        # BlackJack ratio
        bj_ratio = setting_form.bj_ratio.data
        game.set_blackjack_ratio(bj_ratio)

    return render_template('setting.html', setting_form=setting_form, game=game, submit_result=submit_result), 200
