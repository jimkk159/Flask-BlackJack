from flask import Blueprint

game_route = Blueprint('game_route', __name__)

from . import home, rule, setting, table, user
