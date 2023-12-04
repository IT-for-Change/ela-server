import logging
import os
import sys
from pathlib import Path

def initialize(appConfig):
    
    logDir = 'files/log'
    if (os.path.exists(logDir) == False):
        Path(logDir).mkdir()

    logfile = 'ela.log'
    logfilefull = os.path.join(logDir,logfile)
    print('logging initialized: '.format(logfilefull))

    logging.basicConfig( filename = logfilefull,filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%d/%m/%Y %I:%M:%S %p' )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO) #log info and error to console. debug goes only to file
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%d/%m/%Y %I:%M:%S %p' ))
    logging.getLogger().addHandler(stream_handler)

    logging.info('Logging initialized')