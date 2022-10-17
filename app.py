import random
from flask_bootstrap import Bootstrap
from flask import Flask, render_template

# self module
from backend.game import Blackjack
from backend.table import table_blueprint
from backend.card import card_blueprint
from backend.player import player_blueprint
from backend.setting import setting_blueprint


def create_app():
    app = Flask(__name__)

    # BluePrint
    app.register_blueprint(card_blueprint)
    app.register_blueprint(table_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(setting_blueprint)

    # WTF Form
    app.config['SECRET_KEY'] = "Jim's Secret key"
    Bootstrap(app)

    # Initial the blackjack game
    game = Blackjack()
    game.reset_player()
    game.reset()
    game.deal_to_all()
    app.config["blackjack_game"] = game

    @app.route("/")
    def home():
        return render_template('index.html'), 200

    @app.route("/rule")
    def rule():
        return render_template('rule.html'), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
