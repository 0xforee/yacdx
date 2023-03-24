import sys
import threading

import socket_server
from log import log
from connections import Connections

conn = None


def start_websocket_server():
    socket_server.start()


def start_connections_parser():
    log("start connections server")
    global conn
    conn = Connections()
    conn.start()


def handler(signum, frame):
    print('exception exit')
    global conn
    if conn:
        conn.teardown()

    socket_server.stop()

    sys.exit()


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


    log("start connections parser")
    connections_server = threading.Thread(target=start_connections_parser)
    connections_server.start()

    log("start server beginning...")
    socket_server_thread = threading.Thread(target=start_websocket_server)
    socket_server_thread.start()
    log("start all server end, enjoy it")
    socket_server_thread.join()
