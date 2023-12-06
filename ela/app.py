#built-in modules
import os
import time
import logging
import traceback
from pathlib import Path
#3rd party modules
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#own modules
import elacore
from elautil import dataclasses as dc, logger, db, config


def initializeApp():
    logger.initialize()
    db.initialize()
    elacore.initialize()

def isValidTrigger(event):
    if event.is_directory:
        return False
    if os.path.basename(event.src_path) == config.ELA_TRIGGER_FILE:
        print('update detected')
        logger.debug(f'Update to trigger file {event.src_path} detected')
        with open(event.src_path, 'r') as file:
            upload_pkg_id = file.read()
            if (upload_pkg_id == None or upload_pkg_id == ''):
                return False

    #TODO
    #validate file contents i.e. value of string 'upload_pkg_id'
    #filter out duplicate event triggers for the same watch file modification event
    return True


class FileChangeHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
        logger.debug('File modification detected')
        try:
            if (isValidTrigger(event)):
                with open(event.src_path, 'r') as file:
                    upload_pkg_id = file.read()
                logger.info('Triggered ELA for package id {}'.format(upload_pkg_id))
                elacore.performAssessment(upload_pkg_id)
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            self.on_error(e)

    def on_error(self, e):
        print('oops! but soldiering on...{}',e)

def listen():
    try:
        trigger_file_dir = config.ELA_TRIGGER_DIR
        trigger_file = config.ELA_TRIGGER_FILE
        trigger_file_path = os.path.join(trigger_file_dir, trigger_file)
        logger.debug(f'staging file path {trigger_file_path}')

        if (os.path.exists(trigger_file_dir) == False):
            Path(trigger_file_dir).mkdir(parents=True)
    
        logger.info(f'Created trigger file {trigger_file_path}')

        event_handler = FileChangeHandler()
        file_full_path = os.path.abspath(trigger_file_path)
        print(f'file to watch {file_full_path}')
        observer = Observer()
        observer.schedule(event_handler, path=file_full_path, recursive=False)
        observer.start()
        logger.info(f'Watching file: {file_full_path}')
        while True:
            time.sleep(5)
            logger.info(f'Watching file: {file_full_path}')
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()

try:
    initializeApp()
    listen()
except Exception as err:
    traceback_str = traceback.format_exc()
    print(traceback_str)
    exit(1)
except KeyboardInterrupt:
    print('Stopping due to keyboard interrupt')