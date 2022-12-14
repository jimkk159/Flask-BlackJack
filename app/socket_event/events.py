from app import socketio
from flask import session, current_app
from flask_socketio import emit, join_room, leave_room
from app.game_component.card import Card


@socketio.on('joined', namespace='/table')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('left', namespace='/table')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)

    # emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


@socketio.on('screen_size', namespace='/table')
def screen_size(message):
    print('I got size')

    session['height'] = message['height']
    session['width'] = message['width']


@socketio.on('start', namespace='/table')
def start(message):
    print("I got start")
    game = current_app.config["GAME"]

    room = session.get('room', '')

    table = game.get_table_by_name(table_name=room)

    table.set_owner()
    table.reset()

    emit('start_ans', {}, room=room)


@socketio.on('pay', namespace='/table')
def pay(message):
    print("I got pay")
    game = current_app.config["GAME"]

    room = session.get('room', '')

    table = game.get_table_by_name(table_name=room)

    player_id = message['player_id']
    player = table.get_player_by_id(player_id)

    # ToDo need to check player is able to pay
    table.player_pay_stake(player)

    emit('pay_ans', {}, room=room)


@socketio.on('deal', namespace='/table')
def deal(message):
    print("I got deal")
    game = current_app.config["GAME"]

    room = session.get('room', '')

    table = game.get_table_by_name(table_name=room)

    if not table.get_is_deal_initial():
        table.deal_initial()
        table.set_is_deal_initial(True)
        # table.banker = [Card(symbol='K', suit='spade', value=10, faced=False),
        #                 Card(symbol='A', suit='heart', value=11)]

    emit('reload', {}, room=room)


@socketio.on('continue_', namespace='/table')
def continue_(message):
    print("I got continue")

    # Config
    game = current_app.config["GAME"]

    room = session.get('room', '')
    table_ = game.get_table_by_name(table_name=room)

    player_id = message['player_id']
    player = table_.get_player_by_id(player_id)

    player.set_is_ready(True)
    if table_.get_is_ready():
        table_.set_game_wait(True)

    emit('reload', {}, room=room)


@socketio.on('hit_', namespace='/table')
def hit_(message):
    print('I got hit')

    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    hand_id = message['hand_id']
    hand = table.get_hand_by_id(hand_id)

    player = table.get_player_by_hand_id(hand_id)

    table.hit_process(hand)
    emit('reload', {}, room=room)
    banker_check(player)


@socketio.on('double_', namespace='/table')
def double_(message):
    print('I got double')

    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    player_id = message['player_id']
    player = table.get_player_by_id(player_id)

    table.double_down_process(player)
    emit('reload', {}, room=room)
    banker_check(player)


@socketio.on('split_', namespace='/table')
def split_(message):
    print('I got split')

    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    player_id = message['player_id']
    player = table.get_player_by_id(player_id)

    hand_id = message['hand_id']
    hand = player.get_hand_by_id(hand_id)

    table.split_process(player, hand)
    emit('reload', {}, room=room)


@socketio.on('stand_', namespace='/table')
def stand_(message):
    print('I got stand')

    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    hand_id = message['hand_id']
    hand = table.get_hand_by_id(hand_id)
    player = table.get_player_by_hand_id(hand_id)

    table.stand_process(hand)
    emit('reload', {}, room=room)
    banker_check(player)


@socketio.on('fold_', namespace='/table')
def fold_(message):
    print('I got fold')

    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    player_id = message['player_id']
    player = table.get_player_by_id(player_id)

    table.fold_process(player)
    emit('reload', {}, room=room)
    banker_check(player)


def banker_check(player):
    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)
    if table.get_is_players_finish():
        # Banker Round
        banker_()
        print('All Players are finish')
        return

    if table.get_is_player_finish(player):
        # Next Player Round
        table.set_next()
        socketio.emit('reload', {}, room=room)
        print('Player is finish')
        return

    # Player Next Hand action
    print('Player next hand')
    socketio.emit('reload', {}, room=room)


def banker_():
    print("I got banker")
    room = session.get('room')
    game = current_app.config["GAME"]
    table = game.get_table_by_name(table_name=room)

    table.reveal_banker_card()
    table.deal_to_banker()

    if table.get_is_banker_bust():
        table.banker_bust_process()
    else:
        table.compare_cards()

    table.end_process()
    emit('reload', {}, room=room)
