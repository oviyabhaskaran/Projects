import os
import time
import threading

UPLOAD_DIR = "uploads/"
EXPIRATION_TIME = 3600  # 1 hour

def cleanup_old_files():
    """Runs a background thread to remove old incomplete files."""
    def _cleanup():
        while True:
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.stat(file_path).st_mtime < time.time() - EXPIRATION_TIME:
                    os.remove(file_path)
            time.sleep(1800)  # Run every 30 minutes
    
    thread = threading.Thread(target=_cleanup, daemon=True)
    thread.start()
