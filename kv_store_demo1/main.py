from server import app, store
from persistence import load_from_disk, periodic_save
import threading

if __name__ == '__main__':
    # Loading data from disk
    load_from_disk(store)

    # Running backend thread and store data each 15 sec
    save_thread = threading.Thread(target=periodic_save, args=(store,), daemon=True)
    save_thread.start()

    # Running Flask Service
    app.run(host='0.0.0.0', port=8080)
