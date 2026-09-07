"""Quick sort implementation and performance analyzer."""

import csv
from random import Random
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def quick_sort(values):
    """Sort values in place using a median-of-three pivot strategy."""
    comparisons = 0
    swaps = 0

    def median_of_three(low, high):
        middle = (low + high) // 2
        a = values[low]
        b = values[middle]
        c = values[high]

        if (a <= b <= c) or (c <= b <= a):
            return middle
        if (b <= a <= c) or (c <= a <= b):
            return low
        return high

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot_index = median_of_three(low, high)
        pivot_value = values[pivot_index]

        values[pivot_index], values[high] = values[high], values[pivot_index]
        swaps += 1

        store_index = low
        for index in range(low, high):
            comparisons += 1
            if values[index] <= pivot_value:
                values[store_index], values[index] = values[index], values[store_index]
                if store_index != index:
                    swaps += 1
                store_index += 1

        values[store_index], values[high] = values[high], values[store_index]
        if store_index != high:
            swaps += 1
        return store_index

    def sort(low, high):
        while low < high:
            pivot_index = partition(low, high)

            if pivot_index - low < high - pivot_index:
                sort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                sort(pivot_index + 1, high)
                high = pivot_index - 1

    if len(values) > 1:
        sort(0, len(values) - 1)

    return comparisons, swaps


def measure(data):
    """Return elapsed seconds and operation counts for one sort."""
    values = data.copy()
    start = perf_counter()
    operations = quick_sort(values)
    elapsed = perf_counter() - start

    if values != sorted(data):
        raise RuntimeError("quick_sort failed to sort the data")

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
    csv_filename="quick_sort_results.csv",
    graph_filename="quick_sort_performance.png",
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

    axes[0].set_title("Quick Sort Runtime")
    axes[0].set_xlabel("Input size (n)")
    axes[0].set_ylabel("Average time (ms)")
    axes[1].set_title("Quick Sort Comparisons")
    axes[1].set_xlabel("Input size (n)")
    axes[1].set_ylabel("Average comparisons")

    for axis in axes:
        axis.grid(True, linestyle="--", alpha=0.6)
        axis.legend()

    figure.suptitle("Quick Sort Performance Analysis")
    figure.tight_layout()
    figure.savefig(filename, dpi=150)
    plt.close(figure)
    print(f"Graph saved to {filename}")


if __name__ == "__main__":
    analyze()
