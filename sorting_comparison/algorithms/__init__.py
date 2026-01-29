"""
Sorting Algorithms Package

This package contains implementations of four classic sorting algorithms:
- Bubble Sort: Simple comparison-based algorithm with O(n²) complexity
- Selection Sort: In-place comparison sort with O(n²) complexity
- Insertion Sort: Efficient for small/nearly-sorted data with O(n²) worst case
- Merge Sort: Divide-and-conquer algorithm with O(n log n) complexity
"""

from .bubble_sort import bubble_sort
from .selection_sort import selection_sort
from .insertion_sort import insertion_sort
from .merge_sort import merge_sort

__all__ = ['bubble_sort', 'selection_sort', 'insertion_sort', 'merge_sort']
