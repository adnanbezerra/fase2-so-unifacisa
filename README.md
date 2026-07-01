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
3. [Ambiente virtual](#ambiente-virtual)
4. [Gráficos](#gráficos)
5. [Policies](#policies)

## Gerador de input

O arquivo `helpers/csv_generator.py` gera o arquivo `input/trace.csv` usado como entrada do simulador.

Ele cria 10.000 registros na coluna `item_id`, com IDs aleatórios entre 1 e 1000.

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

## Ambiente virtual

Os gráficos usam `matplotlib` e `seaborn`. Para instalar e rodar corretamente, use um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Depois disso, rode os scripts normalmente com o ambiente ativo:

```bash
python cache_simulator.py --policy lru --capacity 100
python helpers/run_policy_graphics.py
```

Para sair do ambiente virtual:

```bash
deactivate
```

## Gráficos

Ao final da execução, o simulador gera um gráfico PNG em `output/` com o padrão `{policy}-hit-rates.png`.

O gráfico compara as capacities 100, 250, 500, 750 e 1000 no eixo X com o hit rate (%) no eixo Y.

Para gerar os gráficos das 3 policies:

```bash
python helpers/run_policy_graphics.py
```

Esse script gera 3 gráficos no total: `fifo-hit-rates.png`, `lru-hit-rates.png` e `lfu-hit-rates.png`.

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
