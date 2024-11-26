import hashlib
import bisect

class LoadBalancer:
    def __init__(self, nodes=None):
        self.nodes = nodes or []
        self.ring = []
        self.node_map = {}

        for node in self.nodes:
            self.add_node(node)

    def add_node(self, node):
        node_hash = self._hash(node)
        self.rΩing.append(node_hash)
        self.node_map[node_hash] = node
        self.ring.sort()

    def remove_node(self, node):
        node_hash = self._hash(node)
        self.ring.remove(node_hash)
        del self.node_map[node_hash]

    def get_node(self, key):
        key_hash = self._hash(key)
        index = bisect.bisect(self.ring, key_hash) % len(self.ring)
        node_hash = self.ring[index]
        return self.node_map[node_hash]

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

# Example usage:
# lb = LoadBalancer(["http://localhost:8081", "http://localhost:8082", "http://localhost:8083"])
# node = lb.get_node("some_key")
