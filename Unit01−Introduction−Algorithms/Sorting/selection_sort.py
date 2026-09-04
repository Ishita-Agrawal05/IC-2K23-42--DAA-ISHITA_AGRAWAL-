"""Selection sort performance analyzer.

The analyzer measures execution time, comparisons, and swaps for sorted,
random, and reverse-sorted inputs. Results are printed, saved as CSV, and
plotted as a PNG graph.
"""

import csv
from random import Random
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def selection_sort(values):
    """Sort values in place and return (comparisons, swaps)."""
    comparisons = 0
    swaps = 0

    for start in range(len(values) - 1):
        minimum = start

        for index in range(start + 1, len(values)):
            comparisons += 1
            if values[index] < values[minimum]:
                minimum = index

        if minimum != start:
            values[start], values[minimum] = values[minimum], values[start]
            swaps += 1

    return comparisons, swaps


def measure(data):
    """Return elapsed seconds and operation counts for one sort."""
    values = data.copy()
    start = perf_counter()
    operations = selection_sort(values)
    elapsed = perf_counter() - start

    if values != sorted(data):
        raise RuntimeError("selection_sort failed to sort the data")

    return elapsed, operations


def build_input(size, case, random):
    """Create one input of the requested size and case."""
    if case == "sorted":
        return list(range(size))
    if case == "reverse":
        return list(range(size, 0, -1))
    return [random.randint(0, size * 10) for _ in range(size)]


def analyze(
    sizes=(100, 500, 1000, 2000, 4000),
    repetitions=3,
    csv_filename="selection_sort_results.csv",
    graph_filename="selection_sort_performance.png",
):
    """Run the experiment, print results, and create CSV and graph files."""
    random = Random(42)
    cases = ("sorted", "random", "reverse")
    results = []

    print(
        f"{'n':>6}  {'case':<8} {'time (ms)':>12} "
        f"{'comparisons':>14} {'swaps':>8}"
    )
    print("-" * 58)

    for size in sizes:
        for case in cases:
            data = build_input(size, case, random)
            measurements = [measure(data) for _ in range(repetitions)]
            elapsed = sum(item[0] for item in measurements) / repetitions
            comparisons = sum(item[1][0] for item in measurements) / repetitions
            swaps = sum(item[1][1] for item in measurements) / repetitions

            result = {
                "input_size": size,
                "case": case,
                "time_sec": elapsed,
                "comparisons": comparisons,
                "swaps": swaps,
            }
            results.append(result)
            print(
                f"{size:>6}  {case:<8} {elapsed * 1000:>12.3f} "
                f"{comparisons:>14.0f} {swaps:>8.0f}"
            )

    save_results(results, csv_filename)
    plot_results(results, graph_filename)
    return results


def save_results(results, filename):
    """Save measured performance data as CSV."""
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["input_size", "case", "time_sec", "comparisons", "swaps"],
        )
        writer.writeheader()
        writer.writerows(results)
    print(f"CSV results saved to {filename}")


def plot_results(results, filename):
    """Save runtime and operation-count charts as one PNG."""
    cases = ("sorted", "random", "reverse")
    colors = {"sorted": "tab:green", "random": "tab:blue", "reverse": "tab:red"}
    sizes = sorted({result["input_size"] for result in results})

    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    for case in cases:
        case_results = [result for result in results if result["case"] == case]
        times = [result["time_sec"] * 1000 for result in case_results]
        comparisons = [result["comparisons"] for result in case_results]

        axes[0].plot(sizes, times, marker="o", color=colors[case], label=case.title())
        axes[1].plot(
            sizes,
            comparisons,
            marker="o",
            color=colors[case],
            label=case.title(),
        )

    axes[0].set_title("Selection Sort Runtime")
    axes[0].set_xlabel("Input size (n)")
    axes[0].set_ylabel("Average time (ms)")
    axes[1].set_title("Selection Sort Comparisons")
    axes[1].set_xlabel("Input size (n)")
    axes[1].set_ylabel("Average comparisons")

    for axis in axes:
        axis.grid(True, linestyle="--", alpha=0.6)
        axis.legend()

    figure.suptitle("Selection Sort Performance Analysis")
    figure.tight_layout()
    figure.savefig(filename, dpi=150)
    plt.close(figure)
    print(f"Graph saved to {filename}")


if __name__ == "__main__":
    analyze()