import csv
import random
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT_DIR / "input" / "trace.csv"
TOTAL_ENTRIES = 10_000
MIN_ITEM_ID = 1
MAX_ITEM_ID = 50


def main() -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with TRACE_PATH.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["item_id"])

        for _ in range(TOTAL_ENTRIES):
            writer.writerow([random.randint(MIN_ITEM_ID, MAX_ITEM_ID)])


if __name__ == "__main__":
    main()
