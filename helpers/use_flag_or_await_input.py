import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = ROOT_DIR / "input" / "trace.csv"
VALID_POLICIES = ("fifo", "lru", "lfu")


@dataclass(frozen=True)
class SimulatorConfig:
    input_path: Path
    policy: str
    capacity: int


def get_simulator_config() -> SimulatorConfig:
    args = _parse_args()

    input_path = _resolve_input_path(args.input)
    policy = args.policy or _ask_policy()
    capacity = args.capacity if args.capacity is not None else _ask_capacity()

    return SimulatorConfig(
        input_path=input_path,
        policy=_validate_policy(policy),
        capacity=_validate_capacity(capacity),
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulador de memória RAM",
    )
    parser.add_argument(
        "--input",
        help="Arquivo CSV contendo o trace de acessos",
    )
    parser.add_argument(
        "--policy",
        choices=VALID_POLICIES,
        help="Política de substituição: fifo, lru ou lfu",
    )
    parser.add_argument(
        "--capacity",
        type=int,
        help="Capacidade do cache",
    )

    return parser.parse_args()


def _resolve_input_path(input_value: str | None) -> Path:
    if input_value is None:
        return DEFAULT_INPUT_PATH

    input_path = Path(input_value)

    if input_path.exists():
        return input_path

    input_dir_path = ROOT_DIR / "input" / input_value

    if input_dir_path.exists():
        return input_dir_path

    return input_path


def _ask_policy() -> str:
    while True:
        policy = input("Política de substituição (fifo, lru, lfu): ").strip().lower()

        if policy in VALID_POLICIES:
            return policy

        print("Política inválida. Use fifo, lru ou lfu.")


def _ask_capacity() -> int:
    while True:
        capacity = input("Capacidade do cache: ").strip()

        try:
            return _validate_capacity(int(capacity))
        except ValueError as error:
            print(error)


def _validate_policy(policy: str) -> str:
    normalized_policy = policy.strip().lower()

    if normalized_policy not in VALID_POLICIES:
        valid_options = ", ".join(VALID_POLICIES)
        raise ValueError(f"Política inválida. Use uma destas opções: {valid_options}.")

    return normalized_policy


def _validate_capacity(capacity: int) -> int:
    if capacity <= 0:
        raise ValueError("Capacidade deve ser maior que zero.")

    return capacity
