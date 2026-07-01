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

Ele cria 10.000 registros determinísticos na coluna `item_id`, usando uma seed fixa. O trace combina 3 comportamentos:

- localidade temporal em conjuntos de trabalho que mudam, favorecendo LRU;
- itens quentes de longa duração misturados com ruído, favorecendo LFU;
- varredura de itens frios intercalada com retorno dos itens quentes, expondo custo de substituições ruins.

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

O `cache_simulator.py` executa apenas uma simulação com a policy e a capacity informadas. Para gerar os gráficos comparativos, use `helpers/run_policy_graphics.py`.

O script de gráficos gera um PNG em `output/` com o padrão `{policy}-hit-rates.png`.

O gráfico compara as capacities 25, 50, 100, 250, 500 e 1000 no eixo X com o hit rate (%) no eixo Y.

Para gerar os gráficos das 3 policies:

```bash
python helpers/run_policy_graphics.py
```

Esse script gera 3 gráficos no total: `fifo-hit-rates.png`, `lru-hit-rates.png` e `lfu-hit-rates.png`.

Com o trace atual, os resultados esperados sao:

| Capacidade | FIFO | LRU | LFU |
| --- | ---: | ---: | ---: |
| 25 | 24.76% | 25.81% | 12.81% |
| 50 | 38.50% | 43.50% | 30.05% |
| 100 | 50.52% | 55.06% | 50.31% |
| 250 | 57.39% | 58.62% | 60.14% |
| 500 | 60.55% | 62.68% | 63.46% |
| 1000 | 62.33% | 63.55% | 63.56% |

### Interpretacao dos resultados

O trace usado nos testes foi montado para misturar tres cenarios comuns em memoria: acessos com localidade temporal, itens quentes que aparecem muitas vezes ao longo da execucao e varreduras de itens frios que tendem a poluir a cache. Por isso, os resultados mostram comportamentos diferentes em vez de tres curvas praticamente iguais.

#### FIFO

O FIFO remove sempre o item mais antigo da cache. O ponto forte e a simplicidade: ele e facil de implementar, tem baixo custo de controle e nao precisa armazenar historico de uso recente ou contagem de frequencia.

O ponto fraco e que idade nao significa inutilidade. Um item pode ser antigo e ainda ser muito acessado. No nosso resultado, isso aparece quando FIFO fica abaixo de LRU e LFU na maior parte das capacities. Com capacidade 50, por exemplo, FIFO fica em 38.50%, enquanto LRU chega a 43.50%. A diferenca acontece porque FIFO pode remover itens que ainda fazem parte do conjunto de trabalho ativo, apenas porque entraram antes.

Com capacities maiores, FIFO melhora porque ha mais espaco para manter itens uteis e absorver parte da varredura de itens frios. Ainda assim, em 1000 ele fica em 62.33%, abaixo de LRU e LFU, porque continua sem distinguir item frio de item importante.

#### LRU

O LRU remove o item menos recentemente usado. O ponto forte e aproveitar localidade temporal: se um item foi usado ha pouco tempo, existe boa chance de ser usado novamente em breve.

Esse comportamento explica por que LRU e o melhor algoritmo nas capacities pequenas e medias do teste. Em capacidade 100, LRU chega a 55.06%, contra 50.52% do FIFO e 50.31% do LFU. Nessa faixa, a cache ainda e limitada, entao priorizar o que foi usado recentemente ajuda a manter o conjunto de trabalho atual dentro da memoria.

O ponto fraco do LRU aparece em varreduras longas. Quando muitos itens frios aparecem em sequencia, eles parecem recentes e podem expulsar itens quentes que serao usados novamente depois. Por isso, quando a capacidade aumenta e ha espaco para guardar melhor os itens frequentes, LFU passa LRU: em 250, LFU faz 60.14% e LRU faz 58.62%.

#### LFU

O LFU remove o item menos frequente. O ponto forte e proteger itens muito acessados ao longo da execucao. Ele funciona bem quando existem paginas quentes recorrentes, mesmo que elas passem algum tempo sem aparecer.

No resultado, LFU comeca mal em caches pequenas: com capacidade 25, fica em 12.81%, bem abaixo de FIFO e LRU. Isso acontece porque a cache e pequena demais para o LFU formar um historico util; itens com frequencia acumulada podem ocupar espaco enquanto o conjunto de trabalho recente muda.

Quando a capacidade aumenta, o ponto forte do LFU aparece. Em 250, ele passa os outros algoritmos com 60.14%. Em 500 e 1000, continua no topo, chegando a 63.46% e 63.56%. Isso mostra que, com espaco suficiente, manter os itens mais frequentes compensa melhor do que olhar apenas para ordem de chegada ou uso recente.

#### Comparacao geral

FIFO serve como baseline simples, mas perde precisao por ignorar comportamento real dos acessos. LRU e melhor quando a execucao tem localidade temporal forte e a cache precisa acompanhar rapidamente o conjunto de trabalho atual. LFU e melhor quando ha itens quentes recorrentes e capacidade suficiente para manter historico de frequencia sem travar a adaptacao.

Assim, os resultados refletem diretamente os pontos fortes e fracos de cada politica: LRU vence no inicio por recencia, LFU vence depois por frequencia, e FIFO fica atras por usar apenas ordem de entrada.

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
