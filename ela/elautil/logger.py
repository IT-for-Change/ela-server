import logging
import os
import sys
from pathlib import Path
from elautil import config

def initialize():
    
    logDir = config.ELA_LOG_DIR
    logfile = os.path.join(config.ELA_LOG_DIR, config.ELA_LOG_FILE)
    if (os.path.exists(logDir) == False):
        Path(logDir).mkdir(parents=True)

    print(f'Initializing logging: {logfile}')

    logging.basicConfig( filename = logfile,filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%d/%m/%Y %I:%M:%S %p' )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO) #log info and error to console. debug goes only to file
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%d/%m/%Y %I:%M:%S %p' ))
    logging.getLogger().addHandler(stream_handler)

    logging.info(f'Logging initialized: {logfile}')

def info(message):
    logging.info(message)

def debug(message):
    logging.debug(message)

def error(message):
    logging.error(message)