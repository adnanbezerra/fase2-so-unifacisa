import csv
import random
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT_DIR / "input" / "trace.csv"
TOTAL_ENTRIES = 10_000
RANDOM_SEED = 2026


def build_trace() -> list[int]:
    rng = random.Random(RANDOM_SEED)
    trace = []

    # Fase 1: localidade temporal em conjuntos de trabalho que mudam.
    for base_item_id in (1, 151, 301):
        working_set = list(range(base_item_id, base_item_id + 90))

        for _ in range(700):
            if rng.random() < 0.90:
                trace.append(rng.choice(working_set))
            else:
                trace.append(rng.randint(1001, 1800))

    # Fase 2: itens quentes de longa duracao misturados com ruido.
    hot_items = list(range(1, 36))
    warm_items = list(range(36, 121))

    for _ in range(4300):
        random_value = rng.random()

        if random_value < 0.78:
            trace.append(rng.choice(hot_items))
        elif random_value < 0.90:
            trace.append(rng.choice(warm_items))
        else:
            trace.append(rng.randint(1801, 3600))

    # Fase 3: varredura de itens frios intercalada com retorno dos itens quentes.
    recurring_hot_items = list(range(1, 51))
    next_cold_item = 3601

    while len(trace) < TOTAL_ENTRIES:
        for _ in range(80):
            trace.append(rng.choice(recurring_hot_items))

            if len(trace) >= TOTAL_ENTRIES:
                break

        for _ in range(300):
            trace.append(next_cold_item)
            next_cold_item += 1

            if len(trace) >= TOTAL_ENTRIES:
                break

    return trace[:TOTAL_ENTRIES]


def main() -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    trace = build_trace()

    with TRACE_PATH.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["item_id"])

        for item_id in trace:
            writer.writerow([item_id])


if __name__ == "__main__":
    main()
