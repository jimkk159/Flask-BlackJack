from app import socketio


@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)

@socketio.on('my event')
def handle_message(message):
    print("Received my event message: " + message)