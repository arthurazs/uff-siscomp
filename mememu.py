from sys import argv
from mapping import Cache
from mapping import RANDOM, FIFO, LRU, LFU
from mapping import DIRECT, ASSOCIATIVE, SET_ASSOCIATIVE


with open(argv[1]) as addresses:
    cache = Cache(
        mapping=DIRECT, cache_size=6
        # Associative needs a Policy
        # mapping=ASSOCIATIVE, cache_size=6, policy=RANDOM
        # mapping=ASSOCIATIVE, cache_size=6, policy=FIFO
        # mapping=ASSOCIATIVE, cache_size=6, policy=LRU
        # mapping=ASSOCIATIVE, cache_size=6, policy=LFU
        # Set Associative needs a Policy and the Frame Size
        # mapping=SET_ASSOCIATIVE, cache_size=6, policy=RANDOM, frame_size=2
        # mapping=SET_ASSOCIATIVE, cache_size=6, policy=FIFO, frame_size=2
        # mapping=SET_ASSOCIATIVE, cache_size=6, policy=LRU, frame_size=2
        # mapping=SET_ASSOCIATIVE, cache_size=6, policy=LFU, frame_size=2
    )
    for tag in addresses.readlines():
        tag = int(tag.strip())
        cache.alloc(tag)
