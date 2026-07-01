import csv
from dataclasses import dataclass
from pathlib import Path

from helpers.graphic_generator import generate_hit_rates_graph
from helpers.use_flag_or_await_input import get_simulator_config
from policies import create_policy


GRAPHIC_CAPACITIES = (100, 250, 500, 750, 1000)


@dataclass(frozen=True)
class SimulationResult:
    total_accesses: int
    hits: int
    misses: int

    @property
    def hit_rate(self) -> float:
        if self.total_accesses == 0:
            return 0.0

        return self.hits / self.total_accesses

    @property
    def miss_rate(self) -> float:
        if self.total_accesses == 0:
            return 0.0

        return self.misses / self.total_accesses


def main() -> None:
    config = get_simulator_config()
    policy = create_policy(config.policy, config.capacity)

    try:
        result = run_simulation(config.input_path, policy)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        raise SystemExit(f"Erro: {error}") from error

    print_result(config.input_path, config.policy, config.capacity, result)
    graphic_path = generate_policy_hit_rates_graph(config.input_path, config.policy)
    print(f"Gráfico: {graphic_path}")


def run_simulation(input_path: Path, policy) -> SimulationResult:
    hits = 0
    misses = 0

    for line_number, item_id in read_trace(input_path):
        try:
            was_hit = policy.access(item_id)
        except Exception as error:
            raise RuntimeError(f"Erro ao processar linha {line_number}: {error}") from error

        if was_hit:
            hits += 1
        else:
            misses += 1

    return SimulationResult(
        total_accesses=hits + misses,
        hits=hits,
        misses=misses,
    )


def generate_policy_hit_rates_graph(input_path: Path, policy_name: str) -> Path:
    hit_rates = []

    for capacity in GRAPHIC_CAPACITIES:
        policy = create_policy(policy_name, capacity)
        result = run_simulation(input_path, policy)
        hit_rates.append(result.hit_rate)

    return generate_hit_rates_graph(
        policy_name=policy_name,
        capacities=list(GRAPHIC_CAPACITIES),
        hit_rates=hit_rates,
    )


def read_trace(input_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo de input não encontrado: {input_path}")

    with input_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None or "item_id" not in reader.fieldnames:
            raise ValueError("CSV precisa ter coluna item_id.")

        for line_number, row in enumerate(reader, start=2):
            raw_item_id = row["item_id"]

            try:
                yield line_number, int(raw_item_id)
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"item_id inválido na linha {line_number}: {raw_item_id}"
                ) from error


def print_result(
    input_path: Path,
    policy_name: str,
    capacity: int,
    result: SimulationResult,
) -> None:
    print("Resultado da simulação")
    print(f"Input: {input_path}")
    print(f"Política: {policy_name}")
    print(f"Capacidade: {capacity}")
    print(f"Total de acessos: {result.total_accesses}")
    print(f"Hits: {result.hits}")
    print(f"Misses: {result.misses}")
    print(f"Hit rate: {result.hit_rate:.2%}")
    print(f"Miss rate: {result.miss_rate:.2%}")


if __name__ == "__main__":
    main()
