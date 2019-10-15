from mapping import Cache
from mapping import DIRECT, ASSOCIATIVE, SET_ASSOCIATIVE
from mapping import RANDOM, FIFO, LRU, LFU


FILENAME = 'example.txt'
CACHE_SIZE = 4
MAPPING = ASSOCIATIVE
POLICY = FIFO
FRAME_SIZE = 2

with open(FILENAME) as addresses:
    cache = Cache(mapping=MAPPING, cache_size=CACHE_SIZE,
                  policy=POLICY, frame_size=FRAME_SIZE)
    for tag in addresses.readlines():
        tag = int(tag.strip())
        cache.alloc(tag)
