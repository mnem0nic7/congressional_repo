"""
Bubble Sort Algorithm Implementation

Bubble Sort is one of the simplest sorting algorithms. It works by repeatedly
stepping through the list, comparing adjacent elements and swapping them if
they are in the wrong order. The pass through the list is repeated until
the list is sorted.

Time Complexity:
    - Best Case: O(n) - when array is already sorted (with optimization)
    - Average Case: O(n²)
    - Worst Case: O(n²) - when array is reverse sorted

Space Complexity: O(1) - In-place sorting algorithm

Stability: Stable - Equal elements maintain their relative order

Use Cases:
    - Educational purposes to understand sorting concepts
    - Very small datasets where simplicity is preferred
    - Nearly sorted data (with early termination optimization)
    - When memory is extremely limited
"""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Bubble Sort algorithm.

    This implementation includes an optimization that terminates early
    if no swaps are made in a pass, indicating the array is already sorted.

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list (original array is not modified)

    Example:
        >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    # Create a copy to avoid modifying the original array
    result = arr.copy()
    n = len(result)

    # Traverse through all array elements
    for i in range(n):
        # Flag to detect if any swap occurred in this pass
        swapped = False

        # Last i elements are already in place after i iterations
        # So we only need to check elements up to n-i-1
        for j in range(0, n - i - 1):
            # Compare adjacent elements
            if result[j] > result[j + 1]:
                # Swap if the element found is greater than the next element
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # If no swapping occurred in this pass, array is already sorted
        # This optimization makes best case O(n) for already sorted arrays
        if not swapped:
            break

    return result


def bubble_sort_verbose(arr: List[int]) -> tuple:
    """
    Bubble Sort with detailed statistics for analysis.

    Args:
        arr: List of integers to be sorted

    Returns:
        tuple: (sorted_array, comparisons_count, swaps_count, passes_count)
    """
    result = arr.copy()
    n = len(result)
    comparisons = 0
    swaps = 0
    passes = 0

    for i in range(n):
        swapped = False
        passes += 1

        for j in range(0, n - i - 1):
            comparisons += 1
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return result, comparisons, swaps, passes


if __name__ == "__main__":
    # Test the implementation
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_array}")

    sorted_arr, comps, swaps, passes = bubble_sort_verbose(test_array)
    print(f"Sorted array: {sorted_arr}")
    print(f"Comparisons: {comps}, Swaps: {swaps}, Passes: {passes}")
