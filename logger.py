import logging
import os
import time
from os.path import abspath


timestamp = int(time.time())
logs_dir = abspath('./logs')

if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

LOG_FILE_PATH = './logs/' + str(timestamp) + ".log"
console_out = logging.StreamHandler()
file_log = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger()

log = logging