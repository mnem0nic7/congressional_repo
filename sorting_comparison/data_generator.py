"""
Data Generator Module

This module generates different types of datasets for testing sorting algorithms.
It provides four distinct data distributions that reveal different performance
characteristics of sorting algorithms:

1. Random: Uniformly distributed random integers
2. Sorted: Already sorted in ascending order
3. Reverse Sorted: Sorted in descending order (worst case for many algorithms)
4. Partially Sorted: Mostly sorted with some elements out of place

Each dataset type helps identify:
- Random: Average case performance
- Sorted: Best case performance (for adaptive algorithms)
- Reverse: Worst case performance (for some algorithms)
- Partial: Real-world performance (most real data has some order)
"""

import random
from typing import List, Tuple, Dict
from enum import Enum


class DatasetType(Enum):
    """Enumeration of available dataset types."""
    RANDOM = "random"
    SORTED = "sorted"
    REVERSE = "reverse_sorted"
    PARTIAL = "partially_sorted"


class DataGenerator:
    """
    Generator for creating test datasets with various characteristics.

    Attributes:
        seed: Random seed for reproducibility (optional)
    """

    def __init__(self, seed: int = None):
        """
        Initialize the data generator.

        Args:
            seed: Random seed for reproducible results. If None, results vary.
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def generate_random(self, size: int, min_val: int = 1, max_val: int = None) -> List[int]:
        """
        Generate a list of random integers.

        Args:
            size: Number of elements to generate
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive). Defaults to size * 10

        Returns:
            List of random integers
        """
        if max_val is None:
            max_val = size * 10
        return [random.randint(min_val, max_val) for _ in range(size)]

    def generate_sorted(self, size: int, min_val: int = 1, max_val: int = None) -> List[int]:
        """
        Generate a sorted list of integers (ascending order).

        Args:
            size: Number of elements to generate
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive). Defaults to size * 10

        Returns:
            Sorted list of integers
        """
        data = self.generate_random(size, min_val, max_val)
        return sorted(data)

    def generate_reverse_sorted(self, size: int, min_val: int = 1, max_val: int = None) -> List[int]:
        """
        Generate a reverse-sorted list of integers (descending order).

        This represents the worst case for algorithms like Bubble Sort
        and Insertion Sort.

        Args:
            size: Number of elements to generate
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive). Defaults to size * 10

        Returns:
            Reverse-sorted list of integers
        """
        data = self.generate_random(size, min_val, max_val)
        return sorted(data, reverse=True)

    def generate_partially_sorted(
        self, size: int, disorder_ratio: float = 0.1,
        min_val: int = 1, max_val: int = None
    ) -> List[int]:
        """
        Generate a partially sorted list with some disorder.

        Creates a sorted list and then swaps a percentage of elements
        to introduce disorder. This simulates real-world data that
        often has some inherent order.

        Args:
            size: Number of elements to generate
            disorder_ratio: Fraction of elements to swap (0.0 to 1.0)
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive). Defaults to size * 10

        Returns:
            Partially sorted list of integers
        """
        data = self.generate_sorted(size, min_val, max_val)

        # Calculate number of swaps to perform
        num_swaps = int(size * disorder_ratio / 2)

        for _ in range(num_swaps):
            # Pick two random indices and swap
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            data[i], data[j] = data[j], data[i]

        return data

    def generate_dataset(
        self, dataset_type: DatasetType, size: int, **kwargs
    ) -> List[int]:
        """
        Generate a dataset of the specified type.

        Args:
            dataset_type: Type of dataset to generate
            size: Number of elements
            **kwargs: Additional arguments passed to specific generators

        Returns:
            Generated dataset

        Raises:
            ValueError: If dataset_type is not recognized
        """
        generators = {
            DatasetType.RANDOM: self.generate_random,
            DatasetType.SORTED: self.generate_sorted,
            DatasetType.REVERSE: self.generate_reverse_sorted,
            DatasetType.PARTIAL: self.generate_partially_sorted,
        }

        if dataset_type not in generators:
            raise ValueError(f"Unknown dataset type: {dataset_type}")

        return generators[dataset_type](size, **kwargs)

    def generate_all_types(self, size: int, **kwargs) -> Dict[DatasetType, List[int]]:
        """
        Generate datasets of all types with the specified size.

        Args:
            size: Number of elements in each dataset
            **kwargs: Additional arguments passed to generators

        Returns:
            Dictionary mapping dataset types to generated data
        """
        return {
            dtype: self.generate_dataset(dtype, size, **kwargs)
            for dtype in DatasetType
        }

    def generate_test_suite(
        self, sizes: List[int], **kwargs
    ) -> Dict[int, Dict[DatasetType, List[int]]]:
        """
        Generate a complete test suite with multiple sizes and all types.

        Args:
            sizes: List of dataset sizes to generate
            **kwargs: Additional arguments passed to generators

        Returns:
            Nested dictionary: size -> type -> data
        """
        return {
            size: self.generate_all_types(size, **kwargs)
            for size in sizes
        }


def get_dataset_description(dataset_type: DatasetType) -> str:
    """
    Get a human-readable description of a dataset type.

    Args:
        dataset_type: The type of dataset

    Returns:
        Description string
    """
    descriptions = {
        DatasetType.RANDOM: "Random: Uniformly distributed random integers with no particular order",
        DatasetType.SORTED: "Sorted: Already sorted in ascending order (best case for adaptive sorts)",
        DatasetType.REVERSE: "Reverse Sorted: Sorted in descending order (worst case for many sorts)",
        DatasetType.PARTIAL: "Partially Sorted: Mostly sorted with ~10% disorder (realistic scenario)",
    }
    return descriptions.get(dataset_type, "Unknown dataset type")


if __name__ == "__main__":
    # Demonstrate the data generator
    gen = DataGenerator(seed=42)

    print("=== Data Generator Demo ===\n")

    # Generate small samples of each type
    size = 20
    print(f"Generating {size} elements of each type:\n")

    for dtype in DatasetType:
        data = gen.generate_dataset(dtype, size)
        print(f"{dtype.value}:")
        print(f"  {data[:10]}... (showing first 10)")
        print(f"  {get_dataset_description(dtype)}")
        print()

    # Show test suite generation
    print("=== Test Suite Generation ===\n")
    sizes = [100, 500, 1000]
    suite = gen.generate_test_suite(sizes)

    for size, datasets in suite.items():
        print(f"Size {size}:")
        for dtype, data in datasets.items():
            print(f"  {dtype.value}: {len(data)} elements generated")
