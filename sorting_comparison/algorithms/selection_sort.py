"""
Selection Sort Algorithm Implementation

Selection Sort is an in-place comparison sorting algorithm. It divides the
input list into two parts: a sorted portion at the left end and an unsorted
portion at the right end. Initially, the sorted portion is empty. The algorithm
repeatedly selects the smallest element from the unsorted portion and moves
it to the sorted portion.

Time Complexity:
    - Best Case: O(n²) - always performs the same number of comparisons
    - Average Case: O(n²)
    - Worst Case: O(n²)

Space Complexity: O(1) - In-place sorting algorithm

Stability: Not Stable - Equal elements may change their relative order
    (can be made stable with modifications, but standard implementation is not)

Use Cases:
    - When memory writes are expensive (minimizes swaps - at most n-1 swaps)
    - Small datasets where simplicity is preferred
    - When auxiliary memory is limited
    - Situations where checking all elements is necessary anyway

Key Characteristic:
    Selection Sort makes the minimum number of swaps (O(n)) compared to
    Bubble Sort (O(n²)), making it preferable when write operations are costly.
"""

from typing import List


def selection_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Selection Sort algorithm.

    The algorithm maintains two subarrays:
    1. The subarray which is already sorted
    2. The remaining subarray which is unsorted

    In every iteration, the minimum element from the unsorted subarray
    is picked and moved to the sorted subarray.

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list (original array is not modified)

    Example:
        >>> selection_sort([64, 25, 12, 22, 11])
        [11, 12, 22, 25, 64]
    """
    # Create a copy to avoid modifying the original array
    result = arr.copy()
    n = len(result)

    # Traverse through all array elements
    for i in range(n):
        # Find the minimum element in the remaining unsorted array
        min_idx = i

        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j

        # Swap the found minimum element with the first element
        # of the unsorted portion
        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]

    return result


def selection_sort_verbose(arr: List[int]) -> tuple:
    """
    Selection Sort with detailed statistics for analysis.

    Args:
        arr: List of integers to be sorted

    Returns:
        tuple: (sorted_array, comparisons_count, swaps_count)
    """
    result = arr.copy()
    n = len(result)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            comparisons += 1
            if result[j] < result[min_idx]:
                min_idx = j

        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]
            swaps += 1

    return result, comparisons, swaps


if __name__ == "__main__":
    # Test the implementation
    test_array = [64, 25, 12, 22, 11]
    print(f"Original array: {test_array}")

    sorted_arr, comps, swaps = selection_sort_verbose(test_array)
    print(f"Sorted array: {sorted_arr}")
    print(f"Comparisons: {comps}, Swaps: {swaps}")

    # Demonstrate that comparisons are always the same regardless of input
    sorted_input = [1, 2, 3, 4, 5]
    _, comps_sorted, swaps_sorted = selection_sort_verbose(sorted_input)
    print(f"\nAlready sorted input: {sorted_input}")
    print(f"Comparisons: {comps_sorted}, Swaps: {swaps_sorted}")
