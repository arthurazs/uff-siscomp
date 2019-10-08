from random import randint

RANDOM = 0
FIFO = 1
LRU = 2
LFU = 3

DIRECT = 0
ASSOCIATIVE = 1
SET_ASSOCIATIVE = 2


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
        output = ''
        result = 'MISS'
        if tag == self._cache[position]:
            self._hit += 1
            result = 'HIT'
        else:
            output += f'Old cache:\t{self._cache}\n'
            self._miss += 1
            self._cache[position] = tag

        tag_output += f' ({result}) -> position {position}'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}\n'
        print(f'{tag_output}\n{output}')


class Associative:
    def __init__(self, cache_size, policy=RANDOM):
        self._cache_size = cache_size
        self._cache = [None] * self._cache_size
        self._hit = 0
        self._miss = 0
        self._counter = 0
        self._policy = policy
        if self._policy == RANDOM:
            print('Policy => Random')
            self.alloc = self._random_alloc
        elif self._policy == FIFO:
            print('Policy => FIFO')
            self.alloc = self._fifo_alloc
        elif self._policy == LRU:
            print('Policy => LRU')
            self.alloc = self._lru_alloc
        elif self._policy == LFU:
            print('Policy => LFU')
            self._cache = {}
            self.alloc = self._lfu_alloc

    def _random_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
            tag_output += f' ({result}) -> position {self._cache.index(tag)}'
        elif self._counter < self._cache_size:  # NOT FULL
            output += f'Old cache:\t{self._cache}\n'
            self._cache[self._counter] = tag
            tag_output += f' ({result}) -> position {self._counter}'
            self._counter += 1
            self._miss += 1
        else:
            self._miss += 1
            position = randint(0, self._cache_size - 1)
            tag_output += f' ({result}) -> random position {position}'
            output += f'Old cache:\t{self._cache}\n'
            self._cache[position] = tag
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')

    def _fifo_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
            tag_output += f' ({result}) -> position {self._cache.index(tag)}'
        elif self._counter < self._cache_size:  # NOT FULL
            output += f'Old cache:\t{self._cache}\n'
            self._cache[self._counter] = tag
            tag_output += f' ({result}) -> position {self._counter}'
            self._counter += 1
            self._miss += 1
        else:
            output += f'Old cache:\t{self._cache}\n'
            self._miss += 1
            self._cache.pop(0)
            self._cache.append(tag)
            tag_output += f' ({result}) -> fifo position {self._counter - 1}'
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')

    def _lru_alloc(self, tag):
        tag_output = f'\nTag:\t\t{tag}'
        output = ''
        result = 'MISS'
        output += f'Old cache:\t{self._cache}\n'
        if tag in self._cache:
            self._hit += 1
            result = 'HIT'
            tag_output += f' ({result}) -> position {self._cache.index(tag)}'
            self._cache.remove(tag)
            self._cache.append(tag)
        else:
            tag_output += f' ({result}) -> lru position {len(self._cache) - 1}'
            self._cache.pop(0)
            self._cache.append(tag)
            self._miss += 1
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
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
        output += f'Old cache:\t{self._cache}\n'
        if frequency is not None:
            result = 'HIT'
            tag_output += f' ({result}) -> position '
            tag_output += '{' + str(frequency) + ': ['
            tag_output += str(self._cache[frequency].index(tag)) + ']}'
            self._hit += 1
            self._cache[frequency].remove(tag)
            if len(self._cache[frequency]) == 0:
                del self._cache[frequency]
            try:
                self._cache[frequency + 1].append(tag)
            except KeyError:
                self._cache[frequency + 1] = [tag]
        elif self._counter < self._cache_size:  # NOT FULL
            tag_output += f' ({result}) -> position '
            if self._cache:
                new_pos = str(len(self._cache[min(self._cache)]))
                tag_output += '{0: [' + new_pos + ']}'
            else:
                tag_output += '{0: [0]}'
            try:
                self._cache[0].append(tag)
            except KeyError:
                self._cache[0] = [tag]
            self._counter += 1
            self._miss += 1
        else:
            least = min(self._cache)
            tag_output += f' ({result}) -> lfu position '
            tag_output += '{' + str(least) + ': [0]}'
            self._cache[least].pop(0)
            if len(self._cache[least]) == 0:
                del self._cache[least]
            try:
                self._cache[0].append(tag)
            except KeyError:
                self._cache[0] = [tag]
            self._miss += 1
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')


class SetAssociative:
    def __init__(self, cache_size, frame_size=2, policy=RANDOM):
        self._cache_size = cache_size
        self._frame_size = frame_size
        # self._cache = [None] * self._cache_size
        self._cache = []
        for row in range(self._cache_size // self._frame_size):
            self._cache.append([])
            for column in range(self._frame_size):
                self._cache[row].append(None)
        self._hit = 0
        self._miss = 0
        self._counter = {}
        for index in range(self._cache_size // self._frame_size):
            self._counter[index] = 0
        self._policy = policy
        if self._policy == RANDOM:
            print('Policy => Random')
            self.alloc = self._random_alloc
        elif self._policy == FIFO:
            print('Policy => FIFO')
            self.alloc = self._fifo_alloc
        elif self._policy == LRU:
            print('Policy => LRU')
            self.alloc = self._lru_alloc
        elif self._policy == LFU:
            self._cache = []
            for row in range(self._cache_size // self._frame_size):
                self._cache.append({})
            print('Policy => LFU')
            self.alloc = self._lfu_alloc

    def _random_alloc(self, tag):
        position = tag % (self._cache_size // self._frame_size)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        if tag in self._cache[position]:
            result = 'HIT'
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', position {self._cache[position].index(tag)}'
            self._hit += 1
        elif self._counter[position] < self._frame_size:  # NOT FULL
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', position {self._counter[position]}'
            self._cache[position][self._counter[position]] = tag
            self._counter[position] += 1
            self._miss += 1
        else:
            tag_output += f' ({result}) -> direct position {position}'
            self._miss += 1
            random_position = randint(0, self._frame_size - 1)
            tag_output += f', random position {random_position}'
            self._cache[position][random_position] = tag
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')

    def _fifo_alloc(self, tag):
        position = tag % (self._cache_size // self._frame_size)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        if tag in self._cache[position]:
            result = 'HIT'
            self._hit += 1
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', position {self._cache[position].index(tag)}'
        elif self._counter[position] < self._frame_size:  # NOT FULL
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', position {self._counter[position]}'
            self._cache[position][self._counter[position]] = tag
            self._counter[position] += 1
            self._miss += 1
        else:
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', fifo position {self._counter[position] - 1}'
            self._miss += 1
            self._cache[position].pop(0)
            self._cache[position].append(tag)
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')

    def _lru_alloc(self, tag):
        position = tag % (self._cache_size // self._frame_size)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        if tag in self._cache[position]:
            result = 'HIT'
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', position {self._cache[position].index(tag)}'
            self._hit += 1
            self._cache[position].remove(tag)
            self._cache[position].append(tag)
        else:
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += f', lru position {len(self._cache[position]) - 1}'
            self._cache[position].pop(0)
            self._cache[position].append(tag)
            self._miss += 1
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')

    def _lfu_alloc(self, tag):
        def find_tag_in_set(tag, position):
            for frequency, tags in self._cache[position].items():
                if tag in tags:
                    return frequency
            return None
        position = tag % (self._cache_size // self._frame_size)
        tag_output = f'\nTag:\t\t{tag}'
        result = 'MISS'
        output = f'Old cache:\t{self._cache}\n'
        frequency = find_tag_in_set(tag, position)
        if frequency is not None:
            result = 'HIT'
            tag_output += f' ({result}) -> direct position {position}'
            tag_output += ', position {' + str(frequency) + ': ['
            tag_output += str(self._cache[position][frequency].index(tag))
            tag_output += ']}'
            self._hit += 1
            self._cache[position][frequency].remove(tag)
            if len(self._cache[position][frequency]) == 0:
                del self._cache[position][frequency]
            try:
                self._cache[position][frequency + 1].append(tag)
            except KeyError:
                self._cache[position][frequency + 1] = [tag]
        elif self._counter[position] < self._frame_size:  # NOT FULL
            tag_output += f' ({result}) -> direct position {position}'
            cache_pos = self._cache[position]
            if cache_pos:
                new_pos = str(len(cache_pos[min(cache_pos)]))
                tag_output += ', position {0: [' + new_pos + ']}'
            else:
                tag_output += ', position {0: [0]}'
            try:
                self._cache[position][0].append(tag)
            except KeyError:
                self._cache[position][0] = [tag]
            self._counter[position] += 1
            self._miss += 1
        else:
            cache_pos = self._cache[position]
            tag_output += f' ({result}) -> direct position {position}'
            least = min(cache_pos)
            tag_output += ', lfu position {' + str(least) + ': [0]}'
            cache_pos[least].pop(0)
            if len(cache_pos[least]) == 0:
                del cache_pos[least]
            try:
                cache_pos[0].append(tag)
            except KeyError:
                cache_pos[0] = [tag]
            self._miss += 1
        output += f'New cache:\t{self._cache}\n'
        output += f'Hit/Miss:\t{self._hit}/{self._miss}'
        print(f'{tag_output}\n{output}')
