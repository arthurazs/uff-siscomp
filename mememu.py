from sys import argv
from random import randint

DIRECT = 0
ASSOCIATIVE = 1
CACHE_PAGES = 5
CACHE_MAPPING = ASSOCIATIVE
RANDOM = 0
FIFO = 1
LRU = 2
LFU = 3
POLICY = LFU

cache = [None] * 5
cache_dict = {}
hit = 0
miss = 0
counter = 0


def find_tag(tag):
    for hit, tags in cache_dict.items():
        if tag in tags:
            return hit
    return None


with open(argv[1]) as addresses:
    for tag in addresses.readlines():
        tag = int(tag.strip())

        if CACHE_MAPPING == DIRECT:
            position = tag % CACHE_PAGES
            if tag == cache[position]:
                hit += 1
            else:
                miss += 1
                cache[position] = tag
        elif CACHE_MAPPING == ASSOCIATIVE:
            if POLICY == RANDOM:
                if tag in cache:
                    hit += 1
                elif counter < CACHE_PAGES:  # NOT FULL
                    cache[counter] = tag
                    counter += 1
                    miss += 1
                else:
                    miss += 1
                    position = randint(0, CACHE_PAGES - 1)
                    cache[position] = tag
                    print(f'random: {position}')
            if POLICY == FIFO:
                if tag in cache:
                    hit += 1
                elif counter < CACHE_PAGES:  # NOT FULL
                    cache[counter] = tag
                    counter += 1
                    miss += 1
                else:
                    miss += 1
                    cache.pop(0)
                    cache.append(tag)
            if POLICY == LRU:
                if tag in cache:
                    hit += 1
                    cache.remove(tag)
                    cache.append(tag)
                else:
                    cache.pop(0)
                    cache.append(tag)
                    counter += 1
                    miss += 1
            if POLICY == LFU:
                key = find_tag(tag)
                if key:
                    hit += 1
                    cache_dict[key].remove(tag)
                    if len(cache_dict[key]) == 0:
                        del cache_dict[key]
                    try:
                        cache_dict[key + 1].append(tag)
                    except KeyError:
                        cache_dict = {key + 1: [tag]}
                elif counter < CACHE_PAGES:  # NOT FULL
                    try:
                        cache_dict[0].append(tag)
                    except KeyError:
                        cache_dict = {0: [tag]}
                    counter += 1
                    miss += 1
                else:
                    least = min(cache_dict)
                    cache_dict[least].pop()
                    miss += 1

        print(f'read:\t{tag}')
        print(f'CACHE:\t{cache_dict if POLICY == LFU else cache}')
        print(f'Hits:\t{hit}')
        print(f'Misses:\t{miss}\n')
