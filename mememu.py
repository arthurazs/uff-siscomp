from sys import argv
from mapping import Cache
from mapping import DIRECT, SET_ASSOCIATIVE


policy = None
frame_size = None
with open(argv[1]) as addresses:
    cache_size = int(input('Entre com o tamanho da cache: '))

    print('\nMapeamento:')
    print(' 1 - Direto\n 2 - Associativo\n 3 - Associativo por Conjunto')
    mapping = int(input('Escolha o número do mapeamento desejado: '))
    if mapping != DIRECT:
        print('\nPolítica de Substituição:')
        print(' 1 - Aleatório')
        print(' 2 - FIFO (First in First Out)')
        print(' 3 - LRU (Least Recently Used)')
        print(' 4 - LFU (Least Frequently Used)')
        policy = int(input('Escolha o número da política desejada: '))
    if mapping == SET_ASSOCIATIVE:
        frame_size = int(input('\nEntre com o tamanho do conjunto: '))
    cache = Cache(mapping=mapping, cache_size=cache_size,
                  policy=policy, frame_size=frame_size)
    for tag in addresses.readlines():
        tag = int(tag.strip())
        cache.alloc(tag)
