import socketio

sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)


