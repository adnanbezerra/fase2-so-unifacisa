from helpers.use_flag_or_await_input import get_simulator_config


def main() -> None:
    config = get_simulator_config()

    print(f"Input: {config.input_path}")
    print(f"Política: {config.policy}")
    print(f"Capacidade: {config.capacity}")


if __name__ == "__main__":
    main()
