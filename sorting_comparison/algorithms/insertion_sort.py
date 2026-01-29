"""
Insertion Sort Algorithm Implementation

Insertion Sort is a simple sorting algorithm that builds the final sorted
array one item at a time. It is much like sorting playing cards in your hands.
The array is virtually split into a sorted and an unsorted part. Values from
the unsorted part are picked and placed at the correct position in the sorted part.

Time Complexity:
    - Best Case: O(n) - when array is already sorted
    - Average Case: O(n²)
    - Worst Case: O(n²) - when array is reverse sorted

Space Complexity: O(1) - In-place sorting algorithm

Stability: Stable - Equal elements maintain their relative order

Use Cases:
    - Small datasets (typically n < 50)
    - Nearly sorted data (adaptive - runs in O(n) time)
    - Online sorting (can sort a list as it receives elements)
    - When simplicity and low overhead are important
    - As a subroutine in more complex algorithms (e.g., Timsort uses it)
    - When the dataset fits in CPU cache (good cache locality)

Key Characteristics:
    - Adaptive: Efficient for nearly sorted data
    - Online: Can sort data as it receives it
    - In-place: Only requires O(1) additional memory
    - Stable: Preserves order of equal elements
"""

from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Insertion Sort algorithm.

    The algorithm iterates through the array, growing the sorted portion
    behind it. For each element, it finds the appropriate position in the
    sorted portion and inserts it there, shifting all larger elements one
    position to the right.

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list (original array is not modified)

    Example:
        >>> insertion_sort([12, 11, 13, 5, 6])
        [5, 6, 11, 12, 13]
    """
    # Create a copy to avoid modifying the original array
    result = arr.copy()
    n = len(result)

    # Traverse from the second element (index 1) to the end
    for i in range(1, n):
        # Store the current element to be inserted
        key = result[i]

        # Move elements of result[0..i-1] that are greater than key
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        # Insert the key at its correct position
        result[j + 1] = key

    return result


def insertion_sort_verbose(arr: List[int]) -> tuple:
    """
    Insertion Sort with detailed statistics for analysis.

    Args:
        arr: List of integers to be sorted

    Returns:
        tuple: (sorted_array, comparisons_count, shifts_count)
    """
    result = arr.copy()
    n = len(result)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = result[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if result[j] > key:
                result[j + 1] = result[j]
                shifts += 1
                j -= 1
            else:
                break

        result[j + 1] = key

    return result, comparisons, shifts


def binary_insertion_sort(arr: List[int]) -> List[int]:
    """
    Optimized Insertion Sort using binary search to find insertion position.

    This reduces comparisons from O(n²) to O(n log n), but shifts remain O(n²).
    Useful when comparisons are more expensive than moves.

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list
    """
    import bisect

    result = arr.copy()
    n = len(result)

    for i in range(1, n):
        key = result[i]
        # Find the position where key should be inserted
        pos = bisect.bisect_left(result, key, 0, i)
        # Shift elements and insert
        result[pos + 1:i + 1] = result[pos:i]
        result[pos] = key

    return result


if __name__ == "__main__":
    # Test the implementation
    test_array = [12, 11, 13, 5, 6]
    print(f"Original array: {test_array}")

    sorted_arr, comps, shifts = insertion_sort_verbose(test_array)
    print(f"Sorted array: {sorted_arr}")
    print(f"Comparisons: {comps}, Shifts: {shifts}")

    # Test with nearly sorted data
    nearly_sorted = [1, 2, 3, 5, 4, 6, 7, 8, 10, 9]
    print(f"\nNearly sorted array: {nearly_sorted}")

    sorted_arr2, comps2, shifts2 = insertion_sort_verbose(nearly_sorted)
    print(f"Sorted array: {sorted_arr2}")
    print(f"Comparisons: {comps2}, Shifts: {shifts2}")
    print("(Notice fewer operations for nearly sorted data)")
