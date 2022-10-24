from app import socketio
from flask import session, redirect, url_for, current_app
from flask_socketio import emit, join_room, leave_room


@socketio.on('joined', namespace='/table')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('left', namespace='/table')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


@socketio.on('hit_', namespace='/table')
def hit_(message):
    print('I got hit')
    game = current_app.config["GAME"]
    hand_id = message['hand_id']
    hand = game.get_hand_by_id(hand_id)
    game.hit_process(hand)


@socketio.on('double_', namespace='/table')
def double_(message):
    print('I got double')
    game = current_app.config["GAME"]
    player_id = message['player_id']
    player = game.get_player_by_id(player_id)


@socketio.on('split_', namespace='/table')
def split_(message):
    print('I got split')
    game = current_app.config["GAME"]

    player_id = message['player_id']
    hand_id = message['hand_id']

    player = game.get_player_by_id(player_id)
    hand = player.get_hand_by_id(hand_id)

    game.split_process(player, hand)


@socketio.on('stand_', namespace='/table')
def stand_(message):
    print('I got stand')
    game = current_app.config["GAME"]
    hand_id = message['hand_id']
    hand = game.get_hand_by_id(hand_id)
    game.stand_process(hand)


@socketio.on('fold_', namespace='/table')
def fold_(message):
    print('I got fold')
    game = current_app.config["GAME"]
    player_id = message['player_id']
    player = game.get_player_by_id(player_id)
    game.fold_process(player)


@socketio.on('banker_', namespace='/table')
def banker_(message):
    print("I got banker")
    game = current_app.config["GAME"]
    game.reveal_banker_card()
    game.deal_to_banker()
    if game.get_is_banker_bust():
        game.banker_bust_process()
    else:
        game.compare_cards()
