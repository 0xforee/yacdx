
import datetime

log_file = 'logs/log.txt'


def log(msg):
    with open(log_file, 'a') as f:
        cur = datetime.datetime.now()
        f.write(str(cur) + ":" + str(msg) + "\n")

