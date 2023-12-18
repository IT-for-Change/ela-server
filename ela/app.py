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
    elacore.initialize()

def isValidTrigger(event):
    if event.is_directory:
        return False
    if os.path.basename(event.src_path) == config.ELA_TRIGGER_FILE:

        with open(event.src_path, 'r') as file:
            upload_pkg_infotxt = file.read()
            if (upload_pkg_infotxt == None or upload_pkg_infotxt == ''):
                logger.error(f'No content in trigger file')
                return False
            
            upload_pkg_info = upload_pkg_infotxt.split('|')
            if len(upload_pkg_info) != 2:
                return False

            upload_pkg_id = upload_pkg_info[0]
            upload_pkg_type = upload_pkg_info[1]

            if (any(pkgtype.name == upload_pkg_type for pkgtype in dc.PackageType) == False):
                logger.error(f'Invalid package type {upload_pkg_type}')
                return False

            pkg_upload_dir = config.PKG_UPLOAD_BASE_DIR
            pkg_dir = os.path.join(pkg_upload_dir,upload_pkg_id)
            if (os.path.exists(pkg_dir) == False):
                logger.error(f'Path to package {pkg_dir} does not exist')
                return False

    #TODO
    #do more validations on upload dir..is directory empty or not. does it have the mandatory dirs and files or not.
    #filter out duplicate event triggers for the same watch file modification event
    return True


class FileChangeHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.last_modified = {}
    
    def isDuplicate(self,event):
        file_path = event.src_path
        mod_timestamp = os.path.getmtime(file_path)
        if file_path in self.last_modified and self.last_modified[file_path] == mod_timestamp:
            logger.debug(f'Ignoring as duplicate')
            return True
        
        self.last_modified[file_path] = mod_timestamp
        return False
    
    def on_modified(self, event):
        logger.info(f'Update to trigger file {event.src_path} detected')
        upload_pkg_id = ''
        upload_pkg_infotxt = ''
        
        if self.isDuplicate(event):
            return

        try:
            if (isValidTrigger(event)):
                with open(event.src_path, 'r') as file:
                    upload_pkg_infotxt = file.read()
                    upload_pkg_info = upload_pkg_infotxt.split('|')
                    upload_pkg_id = upload_pkg_info[0]
                    upload_pkg_type = upload_pkg_info[1]
                    logger.info('Triggered ELA for package id {} and package type {}'.format(upload_pkg_id, upload_pkg_type))
                    elacore.performAssessment(upload_pkg_id,upload_pkg_type)
            else:
                logger.info(f'Received invalid trigger {upload_pkg_infotxt}. Skipping.')
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
