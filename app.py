from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_socketio import SocketIO

# self module
from backend.game_component.game import Blackjack
from backend.route.home import home_blueprint
from backend.route.rule import rule_blueprint
from backend.route.user import user_blueprint
from backend.route.table import table_blueprint
from backend.route.setting import setting_blueprint
from backend.game_component.card import card_blueprint
from backend.game_component.player import player_blueprint

from SQL.SQL_management import setup_db, db_drop_and_create, User



def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # BluePrint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(rule_blueprint)
    app.register_blueprint(card_blueprint)
    app.register_blueprint(table_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(setting_blueprint)
    app.register_blueprint(user_blueprint)

    # WTF Form
    # app.config['SECRET_KEY'] = "Jim's Secret key"
    Bootstrap(app)

    setup_db(app)
    with app.app_context():
        db_drop_and_create()

    # Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Initial the blackjack game
    game = Blackjack(0)
    app.config["GAME"] = game

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


def create_socket(app):
    # Internet Socket
    socketio = SocketIO(app)
    return socketio


app = create_app()
socketio = create_socket(app)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
