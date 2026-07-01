# Fase 2 - S.O. Unifacisa - Simulador de memória RAM

## Participantes do grupo

- Adnan Medeiros Bezerra
- Alice Bianca da Silva Cavalcanti
- Francinaldo Batista da Silva Filho
- Gabryell Leal Rocha
- Roberto Braga de Oliveira Filho

## Índice

1. [Gerador de input](#gerador-de-input)
2. [Execução do simulador](#execução-do-simulador)
3. [Policies](#policies)

## Gerador de input

O arquivo `helpers/csv_generator.py` gera o arquivo `input/trace.csv` usado como entrada do simulador.

Ele cria 10.000 registros na coluna `item_id`, com IDs aleatórios entre 1 e 50.

Para executar:

```bash
python3 helpers/csv_generator.py
```

## Execução do simulador

O arquivo `cache_simulator.py` lê as configurações por flags de terminal usando `helpers/use_flag_or_await_input.py`. Se alguma flag obrigatória não for informada, o programa solicita o valor pelo terminal.

O caminho do input usa `input/trace.csv` como padrão quando `--input` não é informado.

Exemplo:

```bash
python3 cache_simulator.py --input trace.csv --policy lru --capacity 100
```

Flags:

| Flag | Descrição |
| --- | --- |
| `--input` | Arquivo CSV contendo o trace de acessos |
| `--policy` | Política de substituição: `fifo`, `lru` ou `lfu` |
| `--capacity` | Capacidade do cache |

## Policies

Um hit acontece quando o `item_id` acessado já está na RAM/cache. Um miss acontece quando o item não está armazenado e precisa entrar no cache.

A `capacity` define o número máximo de itens que podem ficar armazenados ao mesmo tempo.

- `fifo`: remove o item mais antigo quando o cache está cheio.
- `lru`: remove o item menos recentemente usado quando o cache está cheio.
- `lfu`: remove o item menos frequente quando o cache está cheio. Em empate, remove o menos recentemente usado entre os empatados.

Exemplo:

```bash
python3 cache_simulator.py --input trace.csv --policy lru --capacity 100
```
