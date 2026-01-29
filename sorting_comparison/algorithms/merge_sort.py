"""
Merge Sort Algorithm Implementation

Merge Sort is an efficient, stable, comparison-based, divide and conquer
sorting algorithm. It divides the input array into two halves, recursively
sorts them, and then merges the two sorted halves. The merge operation is
the key process that assumes the two halves are sorted and merges them.

Time Complexity:
    - Best Case: O(n log n)
    - Average Case: O(n log n)
    - Worst Case: O(n log n)

    The time complexity is always O(n log n) regardless of input distribution,
    making it highly predictable.

Space Complexity: O(n) - Requires additional space for merging

Stability: Stable - Equal elements maintain their relative order

Use Cases:
    - Large datasets where consistent O(n log n) performance is needed
    - External sorting (sorting data that doesn't fit in memory)
    - When stability is required
    - Linked list sorting (can be implemented with O(1) extra space)
    - Parallel processing environments (naturally parallelizable)
    - When worst-case performance guarantees are important

Key Characteristics:
    - Divide and Conquer: Breaks problem into smaller subproblems
    - Predictable: Always O(n log n), no worst-case degradation
    - Parallelizable: Subproblems can be solved independently
    - External Sorting: Excellent for sorting data on disk
"""

from typing import List


def merge_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Merge Sort algorithm.

    This implementation uses the top-down recursive approach:
    1. Divide the array into two halves
    2. Recursively sort each half
    3. Merge the sorted halves

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list (original array is not modified)

    Example:
        >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
        [3, 9, 10, 27, 38, 43, 82]
    """
    # Base case: array with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr.copy()

    # Find the middle point to divide the array
    mid = len(arr) // 2

    # Recursively sort the two halves
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves
    return _merge(left_half, right_half)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merge two sorted arrays into a single sorted array.

    Args:
        left: First sorted array
        right: Second sorted array

    Returns:
        List[int]: Merged sorted array
    """
    result = []
    i = j = 0

    # Compare elements from both arrays and add the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= ensures stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements from left array (if any)
    result.extend(left[i:])

    # Add remaining elements from right array (if any)
    result.extend(right[j:])

    return result


def merge_sort_iterative(arr: List[int]) -> List[int]:
    """
    Bottom-up iterative implementation of Merge Sort.

    This avoids recursion overhead and can be more cache-friendly.
    It starts by merging pairs of single elements, then pairs of
    two-element arrays, and so on.

    Args:
        arr: List of integers to be sorted

    Returns:
        List[int]: New sorted list
    """
    result = arr.copy()
    n = len(result)

    # Start with subarrays of size 1, then 2, 4, 8, ...
    size = 1
    while size < n:
        # Merge subarrays of current size
        for start in range(0, n, 2 * size):
            mid = min(start + size, n)
            end = min(start + 2 * size, n)

            # Merge result[start:mid] and result[mid:end]
            merged = _merge(result[start:mid], result[mid:end])
            result[start:start + len(merged)] = merged

        size *= 2

    return result


def merge_sort_verbose(arr: List[int]) -> tuple:
    """
    Merge Sort with detailed statistics for analysis.

    Args:
        arr: List of integers to be sorted

    Returns:
        tuple: (sorted_array, comparisons_count, merge_operations_count)
    """
    stats = {'comparisons': 0, 'merges': 0}

    def _merge_verbose(left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            stats['comparisons'] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        stats['merges'] += 1
        return result

    def _sort(arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr.copy()

        mid = len(arr) // 2
        left_half = _sort(arr[:mid])
        right_half = _sort(arr[mid:])
        return _merge_verbose(left_half, right_half)

    sorted_arr = _sort(arr)
    return sorted_arr, stats['comparisons'], stats['merges']


if __name__ == "__main__":
    # Test the implementation
    test_array = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {test_array}")

    sorted_arr, comps, merges = merge_sort_verbose(test_array)
    print(f"Sorted array: {sorted_arr}")
    print(f"Comparisons: {comps}, Merge operations: {merges}")

    # Test iterative version
    print(f"\nIterative merge sort: {merge_sort_iterative(test_array)}")

    # Test with larger array
    import random
    large_array = [random.randint(1, 1000) for _ in range(1000)]
    sorted_large, comps_large, merges_large = merge_sort_verbose(large_array)
    print(f"\nLarge array (1000 elements):")
    print(f"Comparisons: {comps_large}, Merge operations: {merges_large}")
    print(f"Theoretical comparisons (n log n): {1000 * 10:.0f} (approximately)")
