from flask import Flask, request, jsonify
from kv_store_demo1.logging_utils import log_operation
import threading

app = Flask(__name__)

# 键值存储和锁
store = {}
locks = {}  # 用于每个键的锁
global_lock = threading.Lock()  # 全局锁用于创建新键的锁


def get_lock_for_key(key):
    """ 为每个键生成或获取一个锁 """
    with global_lock:
        if key not in locks:
            locks[key] = threading.Lock()
        return locks[key]


@app.route('/<key>', methods=['GET'])
def get_value(key):
    """ 获取键对应的值 """
    lock = get_lock_for_key(key)  # 获取对应键的锁
    with lock:
        value = store.get(key)
        if value is None:
            return jsonify({'error': 'Key not found'}), 404
        log_operation('GET', key, value)
        return jsonify({'value': value})


@app.route('/<key>', methods=['POST'])
def put_value(key):
    """ 存储键值对 """
    value = request.json.get('value')
    if not value:
        return jsonify({'error': 'Invalid value'}), 400

    lock = get_lock_for_key(key)  # 获取对应键的锁
    with lock:
        store[key] = value  # 修改键值
        log_operation('PUT', key, value)

    return jsonify({'message': 'Value stored successfully'})


@app.route('/<key>', methods=['DELETE'])
def delete_value(key):
    """ 删除键值对 """
    lock = get_lock_for_key(key)  # 获取对应键的锁
    with lock:
        if key in store:
            del store[key]
            log_operation('DEL', key)
            return jsonify({'message': 'Key deleted successfully'})
        else:
            return jsonify({'error': 'Key not found'}), 404
