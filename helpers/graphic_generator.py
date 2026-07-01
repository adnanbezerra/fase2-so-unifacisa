from pathlib import Path
import os


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "output"
DEFAULT_GRAPHIC_FORMAT = "png"

os.environ.setdefault("MPLCONFIGDIR", str(ROOT_DIR / ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT_DIR / ".cache"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def generate_hit_rates_graph(
    policy_name: str,
    capacities: list[int],
    hit_rates: list[float],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    graphic_format: str = DEFAULT_GRAPHIC_FORMAT,
) -> Path:
    if len(capacities) != len(hit_rates):
        raise ValueError("capacities e hit_rates precisam ter o mesmo tamanho.")

    output_dir.mkdir(parents=True, exist_ok=True)
    graphic_path = output_dir / f"{policy_name}-hit-rates.{graphic_format}"

    hit_rates_percent = [hit_rate * 100 for hit_rate in hit_rates]

    sns.set_theme(style="whitegrid")
    figure, axis = plt.subplots(figsize=(8, 5))

    sns.lineplot(
        x=capacities,
        y=hit_rates_percent,
        marker="D",
        markersize=8,
        linewidth=2.5,
        color="#6fbf4a",
        label="Hits",
        ax=axis,
    )

    axis.set_title(f"Hit ratio - {policy_name.upper()}")
    axis.set_xlabel("Cache Size")
    axis.set_ylabel("Hit Ratio (%)")
    axis.set_ylim(0, 100)
    axis.set_xticks(capacities)
    axis.set_xlim(min(capacities) * 0.9, max(capacities) * 1.1)
    axis.legend(title=None)

    figure.tight_layout()
    figure.savefig(graphic_path, format=graphic_format, dpi=150)
    plt.close(figure)

    return graphic_path
