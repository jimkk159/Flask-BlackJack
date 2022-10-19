from app import app
from backend.socket.socket import *

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
