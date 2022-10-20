from app import socketio


@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)


@socketio.on('my event')
def handle_message2(message):
    print("Received my event message: " + message)


@socketio.on('my event2')
def handle_message3(message):
    print("Received my event2 message: " + message)
