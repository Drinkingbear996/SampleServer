from kv_store_demo1.server import app, store  # store 是全局的键值存储
from kv_store_demo1.persistence import load_from_disk, periodic_save
import threading

if __name__ == '__main__':
    # 从磁盘加载数据
    load_from_disk(store)

    # 启动后台线程，每隔15秒保存一次数据
    save_thread = threading.Thread(target=periodic_save, args=(store,), daemon=True)
    save_thread.start()

    # 启动 Flask 服务器
    app.run(host='0.0.0.0', port=8080)
