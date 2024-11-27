from app import create_app
from flask_socketio import SocketIO

app = create_app()

# Enable SocketIO
socketio = SocketIO(app)

if __name__ == "__main__":
    # Run app with websockets enabled
    socketio.run(app, debug=True, port=5004)
