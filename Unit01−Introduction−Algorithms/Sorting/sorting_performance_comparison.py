"""Sorting Performance Comparison System.

Compare Merge Sort, Quick Sort, and Heap Sort on identical random inputs.
The system verifies each sorted result, records average execution time, saves
the measurements as CSV, and plots input size against execution time.
"""

import csv
from random import Random
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from merge_sort import merge_sort
from quick_sort import quick_sort


def heap_sort(values):
    """Sort values in place using max-heap sort."""
    def sift_down(start, end):
        root = start
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end and values[child] < values[child + 1]:
                child += 1
            if values[root] >= values[child]:
                return
            values[root], values[child] = values[child], values[root]
            root = child

    last = len(values) - 1
    for start in range((last - 1) // 2, -1, -1):
        sift_down(start, last)
    for end in range(last, 0, -1):
        values[0], values[end] = values[end], values[0]
        sift_down(0, end - 1)


ALGORITHMS = {
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}


def measure(sort_function, data):
    """Return elapsed seconds after verifying the sorted output."""
    values = data.copy()
    expected = sorted(data)
    start = perf_counter()
    sort_function(values)
    elapsed = perf_counter() - start

    if values != expected:
        raise RuntimeError(f"{sort_function.__name__} failed to sort the data")
    return elapsed


def analyze(
    sizes=(100, 500, 1000, 2000, 4000, 8000),
    repetitions=5,
    seed=42,
    csv_filename="sorting_comparison_results.csv",
    graph_filename="sorting_comparison_performance.png",
):
    """Run the comparison and save the results and performance graph."""
    random_generator = Random(seed)
    results = []

    print(f"{'algorithm':<12} {'n':>8} {'time (ms)':>14}")
    print("-" * 38)

    for size in sizes:
        data = [random_generator.randint(0, size * 10) for _ in range(size)]
        for algorithm_name, sort_function in ALGORITHMS.items():
            times = [measure(sort_function, data) for _ in range(repetitions)]
            average_time = sum(times) / repetitions
            result = {
                "algorithm": algorithm_name,
                "input_size": size,
                "time_sec": average_time,
                "repetitions": repetitions,
            }
            results.append(result)
            print(f"{algorithm_name:<12} {size:>8} {average_time * 1000:>14.3f}")

    save_results(results, csv_filename)
    plot_results(results, graph_filename)
    return results


def save_results(results, filename):
    """Save comparison measurements as CSV."""
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["algorithm", "input_size", "time_sec", "repetitions"],
        )
        writer.writeheader()
        writer.writerows(results)
    print(f"CSV results saved to {filename}")


def plot_results(results, filename):
    """Save the n-versus-execution-time comparison graph."""
    figure, axis = plt.subplots(figsize=(9, 6))
    colors = {"Merge Sort": "tab:blue", "Quick Sort": "tab:orange", "Heap Sort": "tab:green"}

    for algorithm_name in ALGORITHMS:
        algorithm_results = [
            result for result in results if result["algorithm"] == algorithm_name
        ]
        sizes = [result["input_size"] for result in algorithm_results]
        times = [result["time_sec"] * 1000 for result in algorithm_results]
        axis.plot(
            sizes,
            times,
            marker="o",
            color=colors[algorithm_name],
            label=algorithm_name,
        )

    axis.set_title("Sorting Performance Comparison System")
    axis.set_xlabel("Input size (n)")
    axis.set_ylabel("Average execution time (ms)")
    axis.grid(True, linestyle="--", alpha=0.6)
    axis.legend()
    figure.tight_layout()
    figure.savefig(filename, dpi=150)
    plt.close(figure)
    print(f"Graph saved to {filename}")


if __name__ == "__main__":
    analyze()