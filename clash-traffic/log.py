
import datetime

import config.configs

log_file = 'logs/log.txt'


def log_error(msg):
    __log("error: " + str(msg))


def log_info(msg):
    __log("info: " + str(msg))


def log_debug(msg):
    if config.configs.log_level == 'debug':
        __log("debug: " + str(msg))


def __log(msg):
    # also can see in console
    print(str(msg))
    with open(log_file, 'a') as f:
        cur = datetime.datetime.now()
        f.write(str(cur) + ":" + str(msg) + "\n")

