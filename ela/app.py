import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            if event.is_directory:
                return
            if os.path.basename(event.src_path) == "ela-package.id":
                print(f'File ela-package.id has been modified')
                with open(event.src_path, 'r') as file:
                    staging_path = os.environ.get('ELA_TRIGGER_DIR')
                    print('staging file path inside callback {0}',staging_path)
                    upload_file_id = file.read()
                    if (upload_file_id == None or upload_file_id == ''):
                        return
                    print(upload_file_id)
                    print('upload file inside callback {0}',upload_file_id)
                    upload_file_path = os.path.join(staging_path, upload_file_id)
                    with open(upload_file_path, 'w') as file:
                        file.write('hello! created new file')
                        print('created new file {0}', upload_file_path)
        except Exception as e:
            self.on_error(e)

    def on_error(self, e):
        print('oops! but soldiering on...{}',e)
# Set the file path to the current directory
staging_path = os.environ.get('ELA_TRIGGER_DIR')
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
    print(f'Watching file: {file_path}')
    observer.start()
    # Keep the script running
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()
