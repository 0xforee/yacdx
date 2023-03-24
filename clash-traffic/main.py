import sys
import threading

import socket_server
from log import log_info,log_error,log_debug
from connections import Connections

conn = None


def start_websocket_server():
    log_info("start websocket server")
    socket_server.start()


def start_connections_parser():
    log_info("start connections server")
    global conn
    conn = Connections()
    conn.start()


def handler(signum, frame):
    log_error('exception occurs!!')
    global conn
    if conn:
        conn.teardown()

    socket_server.stop()

    sys.exit()


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    connections_server = threading.Thread(target=start_connections_parser)
    connections_server.start()

    socket_server_thread = threading.Thread(target=start_websocket_server)
    socket_server_thread.start()
    log_info("start all server end, enjoy it")
    socket_server_thread.join()
