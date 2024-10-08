from flask import Flask, request, jsonify
from kv_store_demo1.logging_utils import log_operation
import threading

app = Flask(__name__)

# 键值存储和锁 Lock and kv store
store = {}
locks = {}  # locks for each key
global_lock = threading.Lock()
# If multiples clients modify the same key simoutaneously, the global lock ensure only 1 thread to visit  shared resources

def get_lock_for_key(key):
    """ For each key,it inits or gets a lock for """
    with global_lock:
        if key not in locks:
            locks[key] = threading.Lock()
        return locks[key]


@app.route('/<key>', methods=['GET'])
def get_value(key):
    """ Getting value from key """
    lock = get_lock_for_key(key)  # Getting lock for key
    with lock:
        value = store.get(key)
        if value is None:
            return jsonify({'error': 'Key not found'}), 404
        log_operation('GET', key, value)
        return jsonify({'value': value})


@app.route('/<key>', methods=['POST'])
def put_value(key):
    """ store key-value pairs """
    value = request.json.get('value')
    if not value:
        return jsonify({'error': 'Invalid value'}), 400

    lock = get_lock_for_key(key)  # 获取对应键的锁
    with lock:
        store[key] = value  # Modify value
        log_operation('PUT', key, value)

    return jsonify({'message': 'Value stored successfully'})


@app.route('/<key>', methods=['DELETE'])
def delete_value(key):
    """ Delete key-value pairs """
    lock = get_lock_for_key(key)  # 获取对应键的锁
    with lock:
        if key in store:
            del store[key]
            log_operation('DEL', key)
            return jsonify({'message': 'Key deleted successfully'})
        else:
            return jsonify({'error': 'Key not found'}), 404
