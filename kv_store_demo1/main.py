from server import app, store
import threading

#  1. benchmarking
#2. nginx
#
if __name__ == '__main__':

    # Optimized for multi-threading
    app.run(host="0.0.0.0", port=8080,threaded=True)
