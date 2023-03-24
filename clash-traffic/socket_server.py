from threading import Lock
from flask import Flask
from flask_socketio import SocketIO
import time
from log import *

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
        log_info('websocket stoped')


def start():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 9001), app, handler_class=WebSocketHandler)
    server.serve_forever()


def background_data_push():
    db_helper = DBHelper()
    log_debug('background_data_push called')
    global connections, thread
    while connections > 0:
        log_debug('start fetch data: ' + str(time.time()))
        res_json = {}
        for key, value in config.configs.statistic_config.items():
            res_json[key] = db_helper.parse_res_value(value)

        socketio.emit('statistic', res_json)
        log_debug('end fetch data at: ' + str(time.time()) + str(res_json))
        socketio.sleep(5)
    thread = None


@socketio.on('connect')
def handle_connect():
    log_info("handle_connect")
    global thread, connections
    with thread_lock:
        connections += 1
        log_info('Connection + 1, cur is ' + str(connections) + ", thread: " + str(thread))
        if thread is None:
            thread = socketio.start_background_task(background_data_push)


@socketio.on('disconnect')
def handle_disconnect():
    log_info("handle_disconnect")
    global thread, thread_lock, connections
    with thread_lock:
        connections -= 1
        log_info('Connection -1, cur is ' + str(connections))


if __name__ == '__main__':
    start()
