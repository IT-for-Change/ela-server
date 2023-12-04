#built-in modules
import os
import time
import logging
import traceback
#3rd party modules
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#own modules
import elacore
from elautil import eladataclasses as dc, elalogger as logger


appConfig = None

def initializeApp():
    global appConfig
    appConfig = dc.RuntimeConfig()
    appConfig.set('ELA_LOG_DIR', 'files/log')
    logger.initialize(appConfig)

def isValidTrigger(event):
    if event.is_directory:
        return False
    if os.path.basename(event.src_path) == "ela-package.id":
        print(f'File ela-package.id has been modified')
        with open(event.src_path, 'r') as file:
            upload_pkg_id = file.read()
            if (upload_pkg_id == None or upload_pkg_id == ''):
                return False

    #TODO
    #validate file contents i.e. value of string 'upload_pkg_id'
    #filter out duplicate event triggers for the same watch file modification event
    return True


class FileChangeHandler(FileSystemEventHandler):
    
    global appConfig
    def on_modified(self, event):
        
        try:
            if (isValidTrigger(event)):
                with open(event.src_path, 'r') as file:
                    upload_pkg_id = file.read()
                    print(upload_pkg_id)
                    appConfig.set('PKG_ID',upload_pkg_id)
                print('upload file inside callback {0}',upload_pkg_id)
                elacore.performAssessment(upload_pkg_id)       
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            self.on_error(e)

    def on_error(self, e):
        print('oops! but soldiering on...{}',e)

# Set the file path to the current directory
staging_path = os.environ.get('ELA_TRIGGER_DIR')
if (staging_path == None or staging_path == ''):
    staging_path = 'files/id'
file_path = os.path.join(staging_path, "ela-package.id")
print('staging file path {0}',file_path)

if os.path.exists(staging_path) and os.path.isdir(staging_path):
    print(f"The directory '{staging_path}' exists.")
else:
    print(f"The directory '{staging_path}' does not exist.")

event_handler = FileChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)

try:
    initializeApp()
    logger.initialize(appConfig)
    elacore.initialize(appConfig)
    print(f'Watching file: {file_path}')
    observer.start()
    # Keep the script running
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()
