from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# self module
from app.game_component.game import Blackjack
from SQL.SQL_management import setup_db, db_drop_and_create, User

# Internet Socket
socketio = SocketIO(logger=True)


def create_app():
    app_ = Flask(__name__)
    app_.config.from_object('config')

    # WTF Form
    # app_.config['SECRET_KEY'] = "Jim's Secret key"
    Bootstrap(app_)

    setup_db(app_)
    with app_.app_context():
        db_drop_and_create()

    # Login
    login_manager = LoginManager()
    login_manager.init_app(app_)

    # Initial the blackjack game
    game = Blackjack(0)
    app_.config["GAME"] = game

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # BluePrint
    import app.socket_event
    from app.route import game_route
    app_.register_blueprint(game_route)

    # Internet Socket
    socketio.init_app(app_)

    return app_
