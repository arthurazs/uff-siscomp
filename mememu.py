from sys import argv
from mapping import Direct, Associative


DIRECT = 0
ASSOCIATIVE = 1
SET_ASSOCIATIVE = 2
CACHE_SIZE = 6
FRAME_SIZE = 2
CACHE_MAPPING = ASSOCIATIVE
RANDOM = 0
FIFO = 1
LRU = 2
LFU = 3
POLICY = LFU

cache = [None] * CACHE_SIZE
cache_dict = {}
cache_set = []
for row in range(CACHE_SIZE // FRAME_SIZE):
    cache_set.append([])
    for column in range(FRAME_SIZE):
        cache_set[row].append(None)
cache_set_dict = []
for row in range(CACHE_SIZE // FRAME_SIZE):
    cache_set_dict.append({})
hit = 0
miss = 0
counter = {}
for index in range(CACHE_SIZE // FRAME_SIZE):
    counter[index] = 0


def find_tag(tag):
    for hit, tags in cache_dict.items():
        if tag in tags:
            return hit
    return None


def find_tag_in_set(tag, position):
    for hit, tags in cache_set_dict[position].items():
        if tag in tags:
            return hit
    return None


if CACHE_MAPPING == DIRECT:
    cache = Direct(CACHE_SIZE)
elif CACHE_MAPPING == ASSOCIATIVE:
    cache = Associative(POLICY, CACHE_SIZE)
with open(argv[1]) as addresses:
    for tag in addresses.readlines():
        tag = int(tag.strip())
        cache.alloc(tag)
        # if CACHE_MAPPING == DIRECT:
        #     position = tag % CACHE_SIZE
        #     print(f'pos:\t{position}')
        #     if tag == cache[position]:
        #         hit += 1
        #     else:
        #         miss += 1
        #         cache[position] = tag
        # if CACHE_MAPPING == ASSOCIATIVE:
        #     # if POLICY == RANDOM:
        #     #     if tag in cache:
        #     #         hit += 1
        #     #     elif counter[0] < CACHE_SIZE:  # NOT FULL
        #     #         cache[counter[0]] = tag
        #     #         counter[0] += 1
        #     #         miss += 1
        #     #     else:
        #     #         miss += 1
        #     #         position = randint(0, CACHE_SIZE - 1)
        #     #         cache[position] = tag
        #     #         print(f'pos:\t{position} (random)')
        #     if POLICY == FIFO:
        #         if tag in cache:
        #             hit += 1
        #         elif counter[0] < CACHE_SIZE:  # NOT FULL
        #             cache[counter[0]] = tag
        #             counter[0] += 1
        #             miss += 1
        #         else:
        #             miss += 1
        #             cache.pop(0)
        #             cache.append(tag)
        #     if POLICY == LRU:
        #         if tag in cache:
        #             hit += 1
        #             cache.remove(tag)
        #             cache.append(tag)
        #         else:
        #             cache.pop(0)
        #             cache.append(tag)
        #             miss += 1
        #     if POLICY == LFU:
        #         key = find_tag(tag)
        #         if key is not None:
        #             hit += 1
        #             cache_dict[key].remove(tag)
        #             if len(cache_dict[key]) == 0:
        #                 del cache_dict[key]
        #             try:
        #                 cache_dict[key + 1].append(tag)
        #             except KeyError:
        #                 cache_dict[key + 1] = [tag]
        #         elif counter[0] < CACHE_SIZE:  # NOT FULL
        #             try:
        #                 cache_dict[0].append(tag)
        #             except KeyError:
        #                 cache_dict[0] = [tag]
        #             counter[0] += 1
        #             miss += 1
        #         else:
        #             least = min(cache_dict)
        #             cache_dict[least].pop(0)
        #             if len(cache_dict[least]) == 0:
        #                 del cache_dict[least]
        #             try:
        #                 cache_dict[0].append(tag)
        #             except KeyError:
        #                 cache_dict[0] = [tag]
        #             miss += 1
        if CACHE_MAPPING == SET_ASSOCIATIVE:
            position = tag % (CACHE_SIZE // FRAME_SIZE)
            print(f'pos:\t{position} (DIRECT)')
            if POLICY == RANDOM:
                if tag in cache_set[position]:
                    hit += 1
                elif counter[position] < FRAME_SIZE:  # NOT FULL
                    cache_set[position][counter[position]] = tag
                    counter[position] += 1
                    miss += 1
                else:
                    miss += 1
                    random_position = randint(0, FRAME_SIZE - 1)
                    cache_set[position][random_position] = tag
                    print(f'pos:\t{random_position} (random ASSOCIATIVE)')
            if POLICY == FIFO:
                if tag in cache_set[position]:
                    hit += 1
                elif counter[position] < FRAME_SIZE:  # NOT FULL
                    cache_set[position][counter[position]] = tag
                    counter[position] += 1
                    miss += 1
                else:
                    miss += 1
                    cache_set[position].pop(0)
                    cache_set[position].append(tag)
            if POLICY == LRU:
                if tag in cache_set[position]:
                    hit += 1
                    cache_set[position].remove(tag)
                    cache_set[position].append(tag)
                else:
                    cache_set[position].pop(0)
                    cache_set[position].append(tag)
                    miss += 1
            if POLICY == LFU:
                key = find_tag_in_set(tag, position)
                if key is not None:
                    hit += 1
                    cache_set_dict[position][key].remove(tag)
                    if len(cache_set_dict[position][key]) == 0:
                        del cache_set_dict[position][key]
                    try:
                        cache_set_dict[position][key + 1].append(tag)
                    except KeyError:
                        cache_set_dict[position][key + 1] = [tag]
                elif counter[position] < FRAME_SIZE:  # NOT FULL
                    try:
                        cache_set_dict[position][0].append(tag)
                    except KeyError:
                        cache_set_dict[position][0] = [tag]
                    counter[position] += 1
                    miss += 1
                else:
                    least = min(cache_set_dict[position])
                    cache_set_dict[position][least].pop(0)
                    if len(cache_set_dict[position][least]) == 0:
                        del cache_set_dict[position][least]
                    try:
                        cache_set_dict[position][0].append(tag)
                    except KeyError:
                        cache_set_dict[position][0] = [tag]
                    miss += 1

        # print(f'read:\t{tag}')

        if CACHE_MAPPING == SET_ASSOCIATIVE:
            print(f'read:\t{tag}')
        # if CACHE_MAPPING != SET_ASSOCIATIVE:
        #     if POLICY == LFU:
        #         dic = cache_dict
        #         # dic = str(cache_dict.values())
        #         print(f'CACHE:\t{dic}')
        #     else:
        #         print(f'CACHE:\t{cache}')
        #     # print(f'CACHE:\t{cache_dict if POLICY == LFU else cache}')
        # else:
            if POLICY == LFU:
                dic = cache_set_dict
                # dic = str(cache_dict.values())
                print(f'CACHE:\t{dic}')
            else:
                print(f'CACHE:\t{cache_set}')
            print(f'Hits:\t{hit}')
            print(f'Misses:\t{miss}\n')
        # print(f'Hits:\t{hit}')
        # print(f'Misses:\t{miss}\n')
