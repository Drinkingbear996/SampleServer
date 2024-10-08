import json
import time
import os
from kv_store_demo1.logging_utils import log_operation

PERSISTENCE_FILE = 'kv_store.json'  # 持久化文件路径

def load_from_disk(store):
    """ 从磁盘加载数据到内存中 """
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r') as f:
            try:
                store.update(json.load(f))
                print("Data loaded from disk.")
            except json.JSONDecodeError:
                print("Error loading data from disk. Starting with empty store.")

def save_to_disk(store):
    """ 将内存中的数据保存到磁盘 """
    with open(PERSISTENCE_FILE, 'w') as f:
        json.dump(store, f)
    # 在每次保存成功后记录日志
    log_operation("SAVE")
    print("Data saved to disk.")

def periodic_save(store, interval=10):
    """ 每隔 interval 秒保存一次数据到磁盘 """
    while True:
        time.sleep(interval)
        save_to_disk(store)
