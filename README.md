# Sistemas de Computação (UFF)

## Simulador de Memória

Construa um simulador de algoritmos de substituição de página de memória em cache.

O simulador deve receber como entrada a sequência de referências às páginas de memória principal (endereços), e simular as substituições realizadas em cache após a ocorrência de um miss.

Algoritmos:

- FIFO (First In First Out)
-	LRU (Least Recently Used)
- LFU (Least-Frequently Used)
- Random

Parâmetros:

- Capacidade total da memória cache (ou seja, número total de páginas)
- Esquema de mapeamento (direto, associativo e associativo por conjunto) que a cache vai operar
- Nome do arquivo de entrada a ser lido pelo programa, contendo as sequências de referências dos acessos de páginas da memória

O arquivo de entrada consiste em um valor de endereço de memória (um número inteiro por linha) a ser carregado no programa.

Para cada política de substituição, a saída do simulador deve consistir de:

- A cada nova referência de memória do arquivo de entrada, imprimir a lista de todas as páginas armazenadas na memória cache;

- Ao final da execução, a fração de acertos às referências de memória para cada política.
