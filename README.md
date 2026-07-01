# Fase 2 - S.O. Unifacisa - Simulador de memória RAM

## Participantes do grupo

- Adnan Medeiros Bezerra
- Alice Bianca da Silva Cavalcanti
- Francinaldo Batista da Silva Filho
- Gabryell Leal Rocha
- Roberto Braga de Oliveira Filho

## Índice

1. [Gerador de input](#gerador-de-input)

## Gerador de input

O arquivo `helpers/csv-generator.py` gera o arquivo `input/trace.csv` usado como entrada do simulador.

Ele cria 10.000 registros na coluna `item_id`, com IDs aleatórios entre 1 e 50.

Para executar:

```bash
python3 helpers/csv-generator.py
```
