from flask import Blueprint

game_route = Blueprint('game_route', __name__)

from . import home, room_route, rule, setting, table_route, user
