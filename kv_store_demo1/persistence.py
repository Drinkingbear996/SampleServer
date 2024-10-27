import json
import time
import os
from logging_utils import log_operation

PERSISTENCE_FILE = 'kv_store.json'  #  The path of persistent files 持久化文件路径

def load_from_disk(store):
    """ Loading data from disk to memory  """
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r') as f:
            try:
                store.update(json.load(f))
                print("Data loaded from disk.")
            except json.JSONDecodeError:
                print("Error loading data from disk. Starting with empty store.")

def save_to_disk(store):
    """ Saving data from memory to disk """
    with open(PERSISTENCE_FILE, 'w') as f:
        json.dump(store, f)
    # 在每次保存成功后记录日志
    log_operation("SAVE")
    print("Data saved to disk.")

#   Interval : The frequency of saving data
def periodic_save(store, interval=10):
    """ Saving data every 15 sec """
    while True:
        time.sleep(interval)
        save_to_disk(store)
