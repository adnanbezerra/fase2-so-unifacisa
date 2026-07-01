from collections import OrderedDict


class LRU:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def access(self, item_id: int) -> bool:
        if item_id in self.cache:
            self.cache.move_to_end(item_id)
            return True

        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)

        self.cache[item_id] = None
        return False
