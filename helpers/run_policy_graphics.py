from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from cache_simulator import print_result, run_simulation
from helpers.graphic_generator import generate_hit_rates_graph
from policies import create_policy

DEFAULT_INPUT_PATH = ROOT_DIR / "input" / "trace.csv"
POLICIES = ("fifo", "lru", "lfu")
CAPACITIES = (100, 250, 500, 750, 1000)


def main() -> None:
    for policy_name in POLICIES:
        hit_rates = []

        for capacity in CAPACITIES:
            policy = create_policy(policy_name, capacity)
            result = run_simulation(DEFAULT_INPUT_PATH, policy)
            hit_rates.append(result.hit_rate)

            print_result(DEFAULT_INPUT_PATH, policy_name, capacity, result)
            print()

        graphic_path = generate_hit_rates_graph(
            policy_name=policy_name,
            capacities=list(CAPACITIES),
            hit_rates=hit_rates,
        )
        print(f"Gráfico: {graphic_path}")
        print()


if __name__ == "__main__":
    main()
