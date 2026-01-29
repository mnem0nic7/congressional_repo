#!/usr/bin/env python3
"""
Sorting Algorithm Comparison Tool - Main Entry Point

This script runs a comprehensive benchmark comparing four sorting algorithms
(Bubble Sort, Selection Sort, Insertion Sort, Merge Sort) across different
dataset types and sizes, then generates reports and visualizations.

Usage:
    python main.py                  # Full benchmark with default settings
    python main.py --quick          # Quick test with smaller datasets
    python main.py --sizes 1000 5000  # Custom sizes
    python main.py --no-viz         # Skip visualization generation

Author: Sorting Comparison Tool
Date: 2024
"""

import argparse
import sys
import time
from datetime import datetime

from algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort
from data_generator import DataGenerator, DatasetType
from benchmark import Benchmark
from report_generator import ReportGenerator, ReportConfig


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Sorting Algorithm Comparison Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      # Full benchmark
  python main.py --quick              # Quick test mode
  python main.py --sizes 1000 5000    # Custom dataset sizes
  python main.py --runs 5             # More runs for accuracy
  python main.py --no-viz             # Skip chart generation
        """
    )

    parser.add_argument(
        '--quick', action='store_true',
        help='Quick test mode with smaller datasets (100, 500, 1000)'
    )

    parser.add_argument(
        '--sizes', nargs='+', type=int,
        help='Dataset sizes to test (default: 1000 5000 10000 50000)'
    )

    parser.add_argument(
        '--runs', type=int, default=3,
        help='Number of runs per configuration (default: 3)'
    )

    parser.add_argument(
        '--seed', type=int, default=42,
        help='Random seed for reproducibility (default: 42)'
    )

    parser.add_argument(
        '--no-viz', action='store_true',
        help='Skip visualization generation'
    )

    parser.add_argument(
        '--output-dir', type=str, default='results',
        help='Output directory for results (default: results)'
    )

    parser.add_argument(
        '--all-sizes', action='store_true',
        help='Run all algorithms on all sizes (skip the O(n^2) protection)'
    )

    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose output during benchmarking'
    )

    return parser.parse_args()


def print_header():
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print("   SORTING ALGORITHM COMPARISON TOOL")
    print("=" * 70)
    print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}\n")


def verify_algorithms():
    """Verify that all algorithms work correctly."""
    print_section("VERIFYING ALGORITHMS")

    test_data = [64, 34, 25, 12, 22, 11, 90]
    expected = sorted(test_data)

    algorithms = {
        'Bubble Sort': bubble_sort,
        'Selection Sort': selection_sort,
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
    }

    all_passed = True
    for name, func in algorithms.items():
        result = func(test_data.copy())
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"  {name:20} [{status}]")
        if not passed:
            all_passed = False
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")

    if all_passed:
        print("\n  All algorithms verified successfully!")
    else:
        print("\n  WARNING: Some algorithms failed verification!")
        sys.exit(1)


def run_benchmark(args):
    """Run the benchmark suite."""
    print_section("RUNNING BENCHMARKS")

    # Determine sizes
    if args.quick:
        sizes = [100, 500, 1000]
        print("  Running in QUICK mode with smaller datasets\n")
    elif args.sizes:
        sizes = args.sizes
    else:
        sizes = [1000, 5000, 10000, 50000]

    print(f"  Dataset sizes: {sizes}")
    print(f"  Runs per config: {args.runs}")
    print(f"  Random seed: {args.seed}")
    print(f"  Skip O(n^2) on large data: {not args.all_sizes}\n")

    # Create and run benchmark
    benchmark = Benchmark(
        sizes=sizes,
        num_runs=args.runs,
        seed=args.seed,
        verbose=args.verbose
    )

    start_time = time.time()
    benchmark.run_benchmarks(skip_slow_combinations=not args.all_sizes)
    elapsed = time.time() - start_time

    print(f"\n  Benchmark completed in {elapsed:.2f} seconds")

    return benchmark


def generate_reports(benchmark, output_dir: str):
    """Generate all reports."""
    print_section("GENERATING REPORTS")

    config = ReportConfig(
        title="Sorting Algorithm Performance Comparison",
        output_dir=output_dir
    )

    generator = ReportGenerator(benchmark, config)

    # Generate and save reports
    txt_path = generator.save_report('benchmark_report.txt')
    print(f"  Text report:     {txt_path}")

    csv_path = generator.save_csv('benchmark_results.csv')
    print(f"  CSV data:        {csv_path}")

    md_path = generator.save_markdown('benchmark_report.md')
    print(f"  Markdown report: {md_path}")

    # Print summary to console
    print_section("RESULTS SUMMARY")
    print(generator.generate_comparison_matrix())
    print(generator.generate_best_algorithm_table())

    return generator


def generate_visualizations(benchmark, output_dir: str):
    """Generate all visualizations."""
    print_section("GENERATING VISUALIZATIONS")

    try:
        from visualizer import Visualizer
        viz = Visualizer(benchmark, output_dir=output_dir)
        saved_files = viz.generate_all_plots()

        print(f"  Generated {len(saved_files)} visualization(s):")
        for f in saved_files:
            print(f"    - {f}")

        return saved_files
    except ImportError as e:
        print(f"  WARNING: Could not generate visualizations: {e}")
        print("  Make sure matplotlib is installed: pip install matplotlib")
        return []


def print_footer(output_dir: str):
    """Print completion message."""
    print_section("COMPLETE")
    print(f"  All results saved to: {output_dir}/")
    print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70 + "\n")


def main():
    """Main entry point."""
    args = parse_arguments()

    print_header()

    # Step 1: Verify algorithms
    verify_algorithms()

    # Step 2: Run benchmarks
    benchmark = run_benchmark(args)

    # Step 3: Generate reports
    generate_reports(benchmark, args.output_dir)

    # Step 4: Generate visualizations (if not skipped)
    if not args.no_viz:
        generate_visualizations(benchmark, args.output_dir)
    else:
        print_section("SKIPPING VISUALIZATIONS")
        print("  (Use without --no-viz to generate charts)")

    print_footer(args.output_dir)


if __name__ == "__main__":
    main()
