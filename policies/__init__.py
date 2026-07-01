from policies.fifo import FIFO
from policies.lfu import LFU
from policies.lru import LRU


def create_policy(name: str, capacity: int):
    policies = {
        "fifo": FIFO,
        "lfu": LFU,
        "lru": LRU,
    }

    return policies[name](capacity)
