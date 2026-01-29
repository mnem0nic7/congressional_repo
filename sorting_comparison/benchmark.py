"""
Benchmark Module

This module provides timing and performance measurement capabilities for
comparing sorting algorithms. It measures execution time with high precision
and supports multiple runs for statistical accuracy.

Features:
- High-precision timing using time.perf_counter()
- Multiple run support for statistical analysis
- Progress tracking for long-running benchmarks
- Memory-efficient data handling
- Result storage and retrieval
"""

import time
import gc
import statistics
from typing import Callable, List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort
from data_generator import DataGenerator, DatasetType


@dataclass
class BenchmarkResult:
    """
    Stores the result of a single benchmark run.

    Attributes:
        algorithm: Name of the sorting algorithm
        dataset_type: Type of dataset used
        size: Number of elements in the dataset
        execution_time: Time taken in seconds
        is_correct: Whether the sort produced correct output
        timestamp: When the benchmark was run
    """
    algorithm: str
    dataset_type: str
    size: int
    execution_time: float
    is_correct: bool
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "✓" if self.is_correct else "✗"
        return (f"{self.algorithm:15} | {self.dataset_type:15} | "
                f"{self.size:6} | {self.execution_time:10.6f}s | {status}")


@dataclass
class AggregatedResult:
    """
    Stores aggregated results from multiple benchmark runs.

    Attributes:
        algorithm: Name of the sorting algorithm
        dataset_type: Type of dataset used
        size: Number of elements
        mean_time: Average execution time
        std_dev: Standard deviation of execution times
        min_time: Minimum execution time
        max_time: Maximum execution time
        runs: Number of runs performed
    """
    algorithm: str
    dataset_type: str
    size: int
    mean_time: float
    std_dev: float
    min_time: float
    max_time: float
    runs: int

    def __str__(self) -> str:
        return (f"{self.algorithm:15} | {self.dataset_type:15} | "
                f"{self.size:6} | {self.mean_time:10.6f}s ± {self.std_dev:.6f}s")


class Benchmark:
    """
    Benchmark suite for sorting algorithm comparison.

    Provides methods to time sorting algorithms on various datasets
    and aggregate results for analysis.
    """

    # Default algorithms to benchmark
    DEFAULT_ALGORITHMS = {
        'Bubble Sort': bubble_sort,
        'Selection Sort': selection_sort,
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
    }

    # Default dataset sizes
    DEFAULT_SIZES = [1000, 5000, 10000, 50000]

    def __init__(
        self,
        algorithms: Dict[str, Callable] = None,
        sizes: List[int] = None,
        num_runs: int = 3,
        seed: int = 42,
        verbose: bool = True
    ):
        """
        Initialize the benchmark suite.

        Args:
            algorithms: Dictionary mapping names to sorting functions
            sizes: List of dataset sizes to test
            num_runs: Number of runs per configuration for averaging
            seed: Random seed for reproducible data generation
            verbose: Whether to print progress information
        """
        self.algorithms = algorithms or self.DEFAULT_ALGORITHMS
        self.sizes = sizes or self.DEFAULT_SIZES
        self.num_runs = num_runs
        self.data_generator = DataGenerator(seed=seed)
        self.verbose = verbose
        self.results: List[BenchmarkResult] = []

    def _time_sort(
        self, sort_func: Callable, data: List[int]
    ) -> tuple:
        """
        Time a single sort operation.

        Args:
            sort_func: Sorting function to benchmark
            data: Data to sort

        Returns:
            Tuple of (execution_time, sorted_result)
        """
        # Force garbage collection before timing
        gc.collect()

        # Make a copy to ensure fair comparison
        data_copy = data.copy()

        # Time the sorting operation
        start_time = time.perf_counter()
        result = sort_func(data_copy)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        return execution_time, result

    def _verify_sort(self, result: List[int], original: List[int]) -> bool:
        """
        Verify that the sorting result is correct.

        Args:
            result: Sorted array from the algorithm
            original: Original unsorted array

        Returns:
            True if the sort is correct, False otherwise
        """
        # Check length preservation
        if len(result) != len(original):
            return False

        # Check if result is sorted
        for i in range(len(result) - 1):
            if result[i] > result[i + 1]:
                return False

        # Check if result contains same elements as original
        return sorted(original) == result

    def run_single_benchmark(
        self,
        algorithm_name: str,
        sort_func: Callable,
        dataset_type: DatasetType,
        size: int
    ) -> BenchmarkResult:
        """
        Run a single benchmark configuration.

        Args:
            algorithm_name: Name of the algorithm
            sort_func: Sorting function
            dataset_type: Type of dataset to generate
            size: Size of the dataset

        Returns:
            BenchmarkResult with timing information
        """
        # Generate the dataset
        data = self.data_generator.generate_dataset(dataset_type, size)

        # Time the sort
        execution_time, result = self._time_sort(sort_func, data)

        # Verify correctness
        is_correct = self._verify_sort(result, data)

        return BenchmarkResult(
            algorithm=algorithm_name,
            dataset_type=dataset_type.value,
            size=size,
            execution_time=execution_time,
            is_correct=is_correct
        )

    def run_benchmarks(
        self,
        skip_slow_combinations: bool = True,
        slow_threshold_size: int = 10000
    ) -> List[BenchmarkResult]:
        """
        Run the complete benchmark suite.

        Args:
            skip_slow_combinations: Skip O(n²) algorithms on very large datasets
            slow_threshold_size: Size threshold for skipping slow algorithms

        Returns:
            List of all benchmark results
        """
        self.results = []
        slow_algorithms = {'Bubble Sort', 'Selection Sort', 'Insertion Sort'}

        total_configs = (
            len(self.algorithms) * len(self.sizes) *
            len(DatasetType) * self.num_runs
        )
        current = 0

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Starting Benchmark Suite")
            print(f"Algorithms: {list(self.algorithms.keys())}")
            print(f"Sizes: {self.sizes}")
            print(f"Dataset Types: {[dt.value for dt in DatasetType]}")
            print(f"Runs per configuration: {self.num_runs}")
            print(f"{'='*60}\n")

        for size in self.sizes:
            for dataset_type in DatasetType:
                # Generate data once for all algorithms at this size/type
                data = self.data_generator.generate_dataset(dataset_type, size)

                for alg_name, sort_func in self.algorithms.items():
                    # Skip slow algorithms on large datasets
                    if (skip_slow_combinations and
                        alg_name in slow_algorithms and
                        size > slow_threshold_size):
                        if self.verbose:
                            print(f"Skipping {alg_name} for size {size} "
                                  f"(would be too slow)")
                        current += self.num_runs
                        continue

                    for run in range(self.num_runs):
                        current += 1
                        if self.verbose:
                            print(f"[{current}/{total_configs}] "
                                  f"{alg_name} | {dataset_type.value} | "
                                  f"n={size} | run {run + 1}/{self.num_runs}",
                                  end='')

                        # Time the sort
                        execution_time, result = self._time_sort(sort_func, data)
                        is_correct = self._verify_sort(result, data)

                        bench_result = BenchmarkResult(
                            algorithm=alg_name,
                            dataset_type=dataset_type.value,
                            size=size,
                            execution_time=execution_time,
                            is_correct=is_correct
                        )

                        self.results.append(bench_result)

                        if self.verbose:
                            status = "✓" if is_correct else "✗"
                            print(f" -> {execution_time:.4f}s {status}")

        return self.results

    def aggregate_results(self) -> List[AggregatedResult]:
        """
        Aggregate results by algorithm, dataset type, and size.

        Returns:
            List of AggregatedResult objects with statistical summaries
        """
        # Group results by (algorithm, dataset_type, size)
        groups: Dict[tuple, List[float]] = {}

        for result in self.results:
            key = (result.algorithm, result.dataset_type, result.size)
            if key not in groups:
                groups[key] = []
            groups[key].append(result.execution_time)

        # Calculate statistics for each group
        aggregated = []
        for (alg, dtype, size), times in groups.items():
            if len(times) >= 2:
                std_dev = statistics.stdev(times)
            else:
                std_dev = 0.0

            aggregated.append(AggregatedResult(
                algorithm=alg,
                dataset_type=dtype,
                size=size,
                mean_time=statistics.mean(times),
                std_dev=std_dev,
                min_time=min(times),
                max_time=max(times),
                runs=len(times)
            ))

        return sorted(aggregated, key=lambda x: (x.size, x.dataset_type, x.mean_time))

    def get_results_by_size(self) -> Dict[int, List[AggregatedResult]]:
        """
        Get aggregated results organized by dataset size.

        Returns:
            Dictionary mapping size to list of results
        """
        aggregated = self.aggregate_results()
        by_size: Dict[int, List[AggregatedResult]] = {}

        for result in aggregated:
            if result.size not in by_size:
                by_size[result.size] = []
            by_size[result.size].append(result)

        return by_size

    def get_results_by_algorithm(self) -> Dict[str, List[AggregatedResult]]:
        """
        Get aggregated results organized by algorithm.

        Returns:
            Dictionary mapping algorithm name to list of results
        """
        aggregated = self.aggregate_results()
        by_alg: Dict[str, List[AggregatedResult]] = {}

        for result in aggregated:
            if result.algorithm not in by_alg:
                by_alg[result.algorithm] = []
            by_alg[result.algorithm].append(result)

        return by_alg

    def get_best_algorithm(
        self, dataset_type: str, size: int
    ) -> Optional[AggregatedResult]:
        """
        Get the best performing algorithm for a specific scenario.

        Args:
            dataset_type: Type of dataset
            size: Dataset size

        Returns:
            AggregatedResult for the best algorithm, or None if not found
        """
        aggregated = self.aggregate_results()
        matching = [
            r for r in aggregated
            if r.dataset_type == dataset_type and r.size == size
        ]

        if not matching:
            return None

        return min(matching, key=lambda x: x.mean_time)


if __name__ == "__main__":
    # Quick benchmark demo with smaller sizes
    print("Running quick benchmark demo...")

    benchmark = Benchmark(
        sizes=[100, 500, 1000],
        num_runs=2,
        verbose=True
    )

    results = benchmark.run_benchmarks(skip_slow_combinations=False)

    print("\n" + "="*60)
    print("Aggregated Results:")
    print("="*60)

    for result in benchmark.aggregate_results():
        print(result)
