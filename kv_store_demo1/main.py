from server import app, store
from persistence import load_from_disk, periodic_save
import threading

if __name__ == '__main__':
    # Load data from disk
    load_from_disk(store)

    # Start background thread to save periodically
    save_thread = threading.Thread(target=periodic_save, args=(store,), daemon=True)
    save_thread.start()

    # Run Flask application
    app.run(host="0.0.0.0", port=8080)
