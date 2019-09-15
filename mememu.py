import argparse
DIRECT = 0
CACHE_PAGES = 5
CACHE_MAPPING = DIRECT

parser = argparse.ArgumentParser(description='Memory Emulator.')
parser.add_argument('file', help='File to be read')
parser.add_argument('--fifo', help='First In First Out', action='store_true')

args = parser.parse_args()

cache = []

with open(args.file) as sequences:
    for sequence in sequences.readlines():
        sequence = sequence.strip()
        if len(cache) < CACHE_PAGES:
            cache.append(sequence)
        else:
            cache.pop(0)
            cache.append(sequence)
        print(cache)
