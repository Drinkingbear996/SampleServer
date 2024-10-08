import logging
import time

# 配置日志记录
logging.basicConfig(filename='kv_store.log', level=logging.INFO)

def log_operation(op, key=None, value=None):
    """ 记录每次操作 """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if op == "SAVE":
        logging.info(f"{timestamp} - {op}: Periodic save to disk.")
    elif value:
        logging.info(f"{timestamp} - {op} - Key: {key}, Value: {value}")
    else:
        logging.info(f"{timestamp} - {op} - Key: {key}")
