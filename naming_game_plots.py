import csv
from pathlib import Path
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
n_agents = 1000
n_turns = 100000
# List the exact filenames here; the newer runs include their random seeds.
run_filenames = [
    "run_001_100000t_1000a_1o.csv",
    "run_002_100000t_1000a_1o_s43.csv",
    "run_003_100000t_1000a_1o_s44.csv",
    "run_004_100000t_1000a_1o_s45.csv",
]
success_window = 50


def load_run(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    if not rows:
        raise ValueError(f"{csv_path.name} contains no measurements.")
    if any(row["success"] not in ("True", "False") for row in rows):
        raise ValueError(f"{csv_path.name} has an invalid success value.")

    return {
        "name": csv_path.name,
        "turns": [int(row["turn"]) for row in rows],
        "total_words": [int(row["population_total_words"]) for row in rows],
        "distinct_words": [int(row["population_distinct_words"]) for row in rows],
        "successes": [int(row["success"] == "True") for row in rows],
    }


def validate_runs(runs):
    # Every run must contribute to the average at every turn.
    expected_turns = list(range(1, n_turns + 1))
    for index, run in enumerate(runs):
        if run["turns"] != expected_turns:
            raise ValueError(
                f"{run['name']} must contain every turn from 1 to {n_turns}."
            )

        # Reusing seed 42 would reproduce the same trajectory.
        for previous_run in runs[:index]:
            if all(
                run[metric] == previous_run[metric]
                for metric in ("total_words", "distinct_words", "successes")
            ):
                raise ValueError(
                    f"{run['name']} and {previous_run['name']} contain identical "
                    "measurements. Check that each simulation used a different seed."
                )


def average_runs(runs, metric):
    # At each turn, add the measurements from all runs and divide by run count.
    return [
        sum(run[metric][index] for run in runs) / len(runs)
        for index in range(len(runs[0]["turns"]))
    ]


def moving_average(values, window):
    # This is an additional average over time, used only for the success panel.
    averages = []
    for index in range(len(values)):
        start = max(0, index - window + 1)
        recent_values = values[start:index + 1]
        averages.append(sum(recent_values) / len(recent_values))
    return averages


def create_figure(runs):
    turns = runs[0]["turns"]
    fig, axes = plt.subplots(
        3, 1, figsize=(9, 8), sharex=True, layout="constrained"
    )

    # Word counts: faint individual runs and a bold mean, without time smoothing.
    for ax, metric, color, label in (
        (axes[0], "total_words", "steelblue", "Total stored words"),
        (axes[1], "distinct_words", "darkorange", "Distinct names"),
    ):
        for index, run in enumerate(runs):
            ax.plot(
                turns, run[metric], color=color, alpha=0.25, linewidth=0.8,
                label="Individual runs" if index == 0 else None,
            )
        ax.plot(
            turns, average_runs(runs, metric), color=color, linewidth=1.8,
            label=f"Mean of {len(runs)} runs",
        )
        ax.set_ylabel(label)
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=8, frameon=False)

    # At a given turn, this is the fraction of runs whose exchange succeeded.
    mean_success = average_runs(runs, "successes")
    axes[2].plot(
        turns, mean_success, color="seagreen", alpha=0.2, linewidth=0.5,
        label="Per-turn mean across runs",
    )
    axes[2].plot(
        turns, moving_average(mean_success, success_window),
        color="seagreen", linewidth=1.5,
        label=f"Mean, trailing {success_window} exchanges",
    )
    axes[2].set_ylabel("Success rate")
    axes[2].set_title(
        "Success only: moving-average overlay; shorter window at the start",
        fontsize=9,
    )
    axes[2].set_ylim(-0.02, 1.02)
    axes[2].set_yticks([0, 0.5, 1])
    axes[2].set_xlabel("Turn (one speaker–listener exchange)")
    axes[2].set_xlim(0, turns[-1])
    axes[2].legend(fontsize=8, frameon=False)

    for ax in axes:
        ax.grid(alpha=0.2)

    fig.suptitle(
        f"Naming game: average of {len(runs)} runs\n"
        f"{n_agents:,} agents, one object, {len(turns):,} exchanges per run"
    )
    return fig


def main():
    csv_paths = [folder / filename for filename in run_filenames]
    missing_paths = [path for path in csv_paths if not path.is_file()]
    if missing_paths:
        print(f"The average needs all {len(csv_paths)} run files. Still missing:")
        for path in missing_paths:
            print(f"  {path.name}")
        return

    runs = [load_run(path) for path in csv_paths]
    validate_runs(runs)
    fig = create_figure(runs)

    output_path = folder / f"naming_game_average_{len(runs)}_runs.png"
    fig.savefig(output_path, dpi=200)
    print(f"Averaged {len(runs)} runs and saved figure to {output_path}")
    plt.show()


if __name__ == "__main__":
    main()
