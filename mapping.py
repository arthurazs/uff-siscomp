from random import randint

RANDOM = 0
FIFO = 1
LRU = 2
LFU = 3


class Direct:
    def __init__(self, cache_size):
        self._cache_size = cache_size
        self._cache = [None] * self._cache_size
        self._hit = 0
        self._miss = 0
        print('Mapping -> Direct')

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
    def __init__(self, policy, cache_size):
        self._cache_size = cache_size
        self._cache = [None] * self._cache_size
        self._hit = 0
        self._miss = 0
        self._counter = 0
        self._policy = policy
        print('Mapping -> Associative')
        if self._policy == RANDOM:
            print('Policy -> Random')
            self.alloc = self.random_alloc
        elif self._policy == FIFO:
            print('Policy -> FIFO')
            self.alloc = self.fifo_alloc
        elif self._policy == LRU:
            print('Policy -> LRU')
            self.alloc = self.lru_alloc
        elif self._policy == LFU:
            print('Policy -> LFU')
            self._cache = {}
            self.alloc = self.lfu_alloc

    def random_alloc(self, tag):
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

    def fifo_alloc(self, tag):
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

    def lru_alloc(self, tag):
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

    def _find_tag(self, tag):
        for frequency, tags in self._cache.items():
            if tag in tags:
                return frequency
        return None

    def lfu_alloc(self, tag):
        frequency = self._find_tag(tag)
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
            try:
                tag_output += '{0: [' + str(len(self._cache[min(self._cache)])) + ']}'
            except ValueError:
                try:
                    tag_output += '{0: [' + str(len(self._cache[0])) + ']}'
                except KeyError:
                    tag_output += '{0: [' + str(0) + ']}'
            try:
                self._cache[0].append(tag)
            except KeyError:
                self._cache[0] = [tag]
            self._counter += 1
            self._miss += 1
        else:
            tag_output += f' ({result}) -> lfu position '
            least = min(self._cache)
            tag_output += '{' + str(min(self._cache)) + ': [' + str(len(self._cache[min(self._cache)]) - 1) + ']}'
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
