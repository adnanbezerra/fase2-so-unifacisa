from collections import deque


class FIFO:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = set()
        self.order = deque()

    def access(self, item_id: int) -> bool:
        if item_id in self.cache:
            return True

        if len(self.cache) >= self.capacity:
            oldest_item = self.order.popleft()
            self.cache.remove(oldest_item)

        self.cache.add(item_id)
        self.order.append(item_id)
        return False
