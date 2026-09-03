"""Insertion sort and a small performance analyzer for sorting algorithms."""

from random import Random
from time import perf_counter


def insertion_sort(values):
    """Sort values in place and return (comparisons, shifts)."""
    comparisons = 0
    shifts = 0

    for index in range(1, len(values)):
        key = values[index]
        position = index - 1

        while position >= 0:
            comparisons += 1
            if values[position] <= key:
                break
            values[position + 1] = values[position]
            shifts += 1
            position -= 1

        values[position + 1] = key

    return comparisons, shifts


def bubble_sort(values):
    """Sort values in place and return (comparisons, swaps)."""
    comparisons = 0
    swaps = 0

    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            comparisons += 1
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return comparisons, swaps


def measure(algorithm, data):
    """Return elapsed time and operation counts for one algorithm run."""
    values = data.copy()
    start = perf_counter()
    operations = algorithm(values)
    elapsed = perf_counter() - start

    if values != sorted(data):
        raise RuntimeError(f"{algorithm.__name__} failed to sort the data")
    return elapsed, operations


def analyze(sizes=(100, 500, 1000, 2000), repetitions=3):
    """Compare bubble sort and insertion sort for several input sizes."""
    random = Random(42)
    algorithms = (bubble_sort, insertion_sort)

    print(f"{'n':>6}  {'algorithm':<14} {'time (ms)':>12} {'comparisons':>14} {'moves/swaps':>12}")
    print("-" * 66)

    for size in sizes:
        data = [random.randint(0, size * 10) for _ in range(size)]
        for algorithm in algorithms:
            measurements = [measure(algorithm, data) for _ in range(repetitions)]
            elapsed = sum(item[0] for item in measurements) / repetitions
            comparisons = sum(item[1][0] for item in measurements) / repetitions
            moves = sum(item[1][1] for item in measurements) / repetitions
            print(
                f"{size:>6}  {algorithm.__name__:<14} "
                f"{elapsed * 1000:>12.3f} {comparisons:>14.0f} {moves:>12.0f}"
            )


if __name__ == "__main__":
    analyze()