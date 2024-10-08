import logging
import time

# Logging configuration
logging.basicConfig(filename='kv_store.log', level=logging.INFO)

def log_operation(op, key=None, value=None):
    """ Record each operation """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if op == "SAVE":
        logging.info(f"{timestamp} - {op}: Periodic save to disk.")
    elif value:
        logging.info(f"{timestamp} - {op} - Key: {key}, Value: {value}")
    else:
        logging.info(f"{timestamp} - {op} - Key: {key}")
