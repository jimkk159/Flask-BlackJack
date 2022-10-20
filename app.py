from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_socketio import SocketIO

# self module
from backend.game_component.game import Blackjack
from SQL.SQL_management import setup_db, db_drop_and_create, User

# Internet Socket
socketio = SocketIO(logger=True)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

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

    # BluePrint
    import backend.socket
    from backend.route import game_route
    app.register_blueprint(game_route)

    # Internet Socket
    socketio.init_app(app)

    return app
