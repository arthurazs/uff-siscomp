from random import randint

RANDOM = 1
FIFO = 2
LRU = 3
LFU = 4

DIRECT = 1
ASSOCIATIVE = 2
SET_ASSOCIATIVE = 3


class Cache:
    def __init__(self, mapping, cache_size, policy=RANDOM, frame_size=2):
        if mapping == DIRECT:
            print('Mapping => Direct')
            self._cache = Direct(cache_size)
            self.alloc = self._cache.alloc
        elif mapping == ASSOCIATIVE:
            print('Mapping => Associative')
            self._cache = Associative(cache_size, policy)
            self.alloc = self._cache.alloc
        elif mapping == SET_ASSOCIATIVE:
            print('Mapping => Set Associative')
            self._cache = SetAssociative(cache_size, frame_size, policy)
            self.alloc = self._cache.alloc


class Direct:
    def __init__(self, cache_size):
        self._cache_size = cache_size
        self._cache = [None] * self._cache_size
        self._hit = 0
        self._miss = 0

    def alloc(self, tag):
        position = tag % self._cache_size
        tag_output = f'\nTag:\t\t{tag}'
        output = f'Old cache:\t{self._cache}\n'
        result = 'MISS'

        if tag == self._cache[position]:
            self._hit += 1
            result = 'HIT'
        else:
            self._miss += 1
            self._cache[position] = tag

        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')


class Associative:
    def __init__(self, cache_size, policy=RANDOM):
        self._cache_size = cache_size
        self._cache = [None] * self._cache_size
        self._hit = 0
        self._miss = 0
        self._counter = 0
        if policy == RANDOM:
            print('Policy => Random')
            self.alloc = self._random_alloc
        elif policy == FIFO:
            print('Policy => FIFO')
            self.alloc = self._fifo_alloc
        elif policy == LRU:
            print('Policy => LRU')
            self.alloc = self._lru_alloc
        elif policy == LFU:
            print('Policy => LFU')
            self._cache = {}
            self.alloc = self._lfu_alloc

    def _random_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        output += f'Old cache:\t{self._cache}\n'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
        elif self._counter < self._cache_size:  # NOT FULL
            self._cache[self._counter] = tag
            self._counter += 1
            self._miss += 1
        else:
            self._miss += 1
            position = randint(0, self._cache_size - 1)
            self._cache[position] = tag
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _fifo_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        output += f'Old cache:\t{self._cache}\n'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
        elif self._counter < self._cache_size:  # NOT FULL
            self._cache[self._counter] = tag
            self._counter += 1
            self._miss += 1
        else:
            self._miss += 1
            self._cache.pop(0)
            self._cache.append(tag)
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _lru_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        output += f'Old cache:\t{self._cache}\n'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
            self._cache.remove(tag)
            self._cache.append(tag)
        else:
            self._cache.pop(0)
            self._cache.append(tag)
            self._miss += 1
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _lfu_alloc(self, tag):
        def find_tag(tag):
            for frequency, tags in self._cache.items():
                if tag in tags:
                    return frequency
            return None
        frequency = find_tag(tag)
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        output += 'Old cache:\t{'
        for key, value in sorted(self._cache.items()):
            output += f'{key}: {value}, '
        output = output[:-2] + '}\n'

        if frequency is not None:
            result = 'HIT'
            self._hit += 1
            self._cache[frequency].remove(tag)
            if len(self._cache[frequency]) == 0:
                del self._cache[frequency]
            try:
                self._cache[frequency + 1].append(tag)
            except KeyError:
                self._cache[frequency + 1] = [tag]
        elif self._counter < self._cache_size:  # NOT FULL
            try:
                self._cache[0].append(tag)
            except KeyError:
                self._cache[0] = [tag]
            self._counter += 1
            self._miss += 1
        else:
            least = min(self._cache)
            self._cache[least].pop(0)
            if len(self._cache[least]) == 0:
                del self._cache[least]
            try:
                self._cache[0].append(tag)
            except KeyError:
                self._cache[0] = [tag]
            self._miss += 1
        tag_output += f' ({result})'
        output += 'New cache:\t{'
        for key, value in sorted(self._cache.items()):
            output += f'{key}: {value}, '
        output = output[:-2] + '}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')


class SetAssociative:
    def __init__(self, cache_size, frame_size=2, policy=RANDOM):
        self._cache_size = cache_size
        self._frame_size = frame_size
        self._lines = cache_size // frame_size
        self._cache = [[None] * frame_size for i in range(self._lines)]
        self._hit = 0
        self._miss = 0
        self._counter = {}
        for index in range(self._lines):
            self._counter[index] = 0
        if policy == RANDOM:
            print('Policy => Random')
            self.alloc = self._random_alloc
        elif policy == FIFO:
            print('Policy => FIFO')
            self.alloc = self._fifo_alloc
        elif policy == LRU:
            print('Policy => LRU')
            self.alloc = self._lru_alloc
        elif policy == LFU:
            self._cache = [{} for _ in range(self._lines)]
            print('Policy => LFU')
            self.alloc = self._lfu_alloc

    def _random_alloc(self, tag):
        position = tag % (self._lines)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        cache_pos = self._cache[position]
        if tag in cache_pos:
            result = 'HIT'
            self._hit += 1
        elif self._counter[position] < self._frame_size:  # NOT FULL
            cache_pos[self._counter[position]] = tag
            self._counter[position] += 1
            self._miss += 1
        else:
            self._miss += 1
            random_position = randint(0, self._frame_size - 1)
            cache_pos[random_position] = tag
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _fifo_alloc(self, tag):
        position = tag % (self._lines)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        cache_pos = self._cache[position]
        if tag in cache_pos:
            result = 'HIT'
            self._hit += 1
        elif self._counter[position] < self._frame_size:  # NOT FULL
            cache_pos[self._counter[position]] = tag
            self._counter[position] += 1
            self._miss += 1
        else:
            self._miss += 1
            cache_pos.pop(0)
            cache_pos.append(tag)
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _lru_alloc(self, tag):
        position = tag % (self._lines)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        cache_pos = self._cache[position]
        if tag in cache_pos:
            result = 'HIT'
            self._hit += 1
            cache_pos.remove(tag)
            cache_pos.append(tag)
        else:
            cache_pos.pop(0)
            cache_pos.append(tag)
            self._miss += 1
        tag_output += f' ({result})'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')

    def _lfu_alloc(self, tag):
        def find_tag_in_set(tag, position, cache):
            for frequency, tags in cache.items():
                if tag in tags:
                    return frequency
            return None
        position = tag % (self._lines)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'

        output = 'Old cache:\t['
        for elements in self._cache:
            output += '{'
            if elements.items():
                for key, value in sorted(elements.items()):
                    output += f'{key}: {value}, '
                output = output[:-2] + '}, '
            else:
                output += '}, '
        output = output[:-2] + ']\n'

        cache_pos = self._cache[position]
        frequency = find_tag_in_set(tag, position, cache_pos)
        if frequency is not None:
            result = 'HIT'
            self._hit += 1
            cache_pos[frequency].remove(tag)
            if len(cache_pos[frequency]) == 0:
                del cache_pos[frequency]
            try:
                cache_pos[frequency + 1].append(tag)
            except KeyError:
                cache_pos[frequency + 1] = [tag]
        elif self._counter[position] < self._frame_size:  # NOT FULL
            try:
                cache_pos[0].append(tag)
            except KeyError:
                cache_pos[0] = [tag]
            self._counter[position] += 1
            self._miss += 1
        else:
            least = min(cache_pos)
            cache_pos[least].pop(0)
            if len(cache_pos[least]) == 0:
                del cache_pos[least]
            try:
                cache_pos[0].append(tag)
            except KeyError:
                cache_pos[0] = [tag]
            self._miss += 1
        tag_output += f' ({result})'

        output += 'New cache:\t['
        for elements in self._cache:
            output += '{'
            if elements.items():
                for key, value in sorted(elements.items()):
                    output += f'{key}: {value}, '
                output = output[:-2] + '}, '
            else:
                output += '}, '
        output = output[:-2] + ']\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        percentage = self._hit / (self._hit + self._miss) * 100
        output += f'\nHit rate:\t{percentage:.2f}%'
        print(f'{tag_output}\n{output}')
