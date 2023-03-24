from threading import Lock
from flask import Flask
from flask_socketio import SocketIO
import time

import config.configs
from db_helper import DBHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

thread = None
thread_lock = Lock()
connections = 0

server = None


def stop():
    if server:
        server.stop()


def start():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    print("websocket server start ... ")
    server.serve_forever()


def background_data_push():
    db_helper = DBHelper()
    print('background_data_push')
    global connections
    while connections > 0:
        print('start fetch data: ' + str(time.time()))
        res_json = {}
        for key, value in config.configs.statistic_config.items():
            res_json[key] = db_helper.parse_res_value(value)

        print("DateTime: " + str(time.asctime()) + str(res_json))
        socketio.emit('statistic', res_json)
        print('end fetch data: ' + str(time.time()))
        socketio.sleep(5)


@socketio.on('connect')
def handle_connect():
    print("handle_connect")
    global thread, connections
    with thread_lock:
        connections += 1
        print('Connection +1')
        if thread is None:
            thread = socketio.start_background_task(background_data_push)


@socketio.on('disconnect')
def handle_disconnect():
    global thread, thread_lock, connections
    with thread_lock:
        connections -= 1
        print('Connection -1')


if __name__ == '__main__':
    start()
