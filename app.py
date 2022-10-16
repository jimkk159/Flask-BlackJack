import random
from flask import Flask, Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

# self module
from backend.game import game_blueprint
from backend.card import card_blueprint
from backend.player import player_blueprint

def create_app():
    app = Flask(__name__)

    # BluePrint
    app.register_blueprint(card_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(player_blueprint)


    @app.route("/")
    def home():
        return render_template('index.html'), 200

    @app.route("/game")
    def game():
        return render_template('game.html'), 200

    @app.route("/setting")
    def setting():
        return render_template('setting.html'), 200

    @app.route("/rule")
    def rule():
        return render_template('rule.html'), 200


    return app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
