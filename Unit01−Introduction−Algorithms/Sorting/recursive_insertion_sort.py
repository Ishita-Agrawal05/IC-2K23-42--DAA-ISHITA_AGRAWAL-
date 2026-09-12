"""Recursive insertion sort implementation."""


def recursive_insertion_sort(values):
    """Sort values in place using recursive insertion sort."""
    def sort(length):
        if length <= 1:
            return

        sort(length - 1)

        key = values[length - 1]
        position = length - 2
        while position >= 0 and values[position] > key:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = key

    sort(len(values))


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]
    recursive_insertion_sort(sample)
    print(sample)