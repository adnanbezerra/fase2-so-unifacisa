class LFU:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.frequencies = {}
        self.last_used_at = {}
        self.current_time = 0

    def access(self, item_id: int) -> bool:
        self.current_time += 1

        if item_id in self.frequencies:
            self.frequencies[item_id] += 1
            self.last_used_at[item_id] = self.current_time
            return True

        if len(self.frequencies) >= self.capacity:
            item_to_remove = min(
                self.frequencies,
                key=lambda current_item: (
                    self.frequencies[current_item],
                    self.last_used_at[current_item],
                ),
            )
            del self.frequencies[item_to_remove]
            del self.last_used_at[item_to_remove]

        self.frequencies[item_id] = 1
        self.last_used_at[item_id] = self.current_time
        return False
