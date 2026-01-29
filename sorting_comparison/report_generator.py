"""
Report Generator Module

This module generates comprehensive reports from benchmark results, including:
- Formatted tables showing execution times
- Best algorithm recommendations for each scenario
- Performance comparisons and summaries
- Export to various formats (text, markdown, CSV)
"""

import csv
import os
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

from benchmark import Benchmark, AggregatedResult
from data_generator import DatasetType


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    title: str = "Sorting Algorithm Performance Comparison"
    include_std_dev: bool = True
    decimal_places: int = 6
    output_dir: str = "results"


class ReportGenerator:
    """
    Generates formatted reports from benchmark results.

    Supports multiple output formats and customizable report content.
    """

    def __init__(self, benchmark: Benchmark, config: ReportConfig = None):
        """
        Initialize the report generator.

        Args:
            benchmark: Benchmark instance with results
            config: Report configuration options
        """
        self.benchmark = benchmark
        self.config = config or ReportConfig()
        self.aggregated = benchmark.aggregate_results()

        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)

    def _format_time(self, seconds: float) -> str:
        """Format time value with configured decimal places."""
        return f"{seconds:.{self.config.decimal_places}f}s"

    def _get_table_header(self, columns: List[str], widths: List[int]) -> str:
        """Generate a formatted table header row."""
        header = " | ".join(
            col.center(width) for col, width in zip(columns, widths)
        )
        separator = "-+-".join("-" * width for width in widths)
        return f"{header}\n{separator}"

    def generate_summary_table(self) -> str:
        """
        Generate a summary table of all benchmark results.

        Returns:
            Formatted string containing the summary table
        """
        lines = []
        lines.append("=" * 80)
        lines.append(self.config.title.center(80))
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append("")

        # Group by dataset type for cleaner presentation
        by_type: Dict[str, List[AggregatedResult]] = {}
        for result in self.aggregated:
            if result.dataset_type not in by_type:
                by_type[result.dataset_type] = []
            by_type[result.dataset_type].append(result)

        for dtype, results in by_type.items():
            lines.append(f"\n{'='*80}")
            lines.append(f"Dataset Type: {dtype.upper()}")
            lines.append("=" * 80)

            # Create header
            columns = ["Algorithm", "Size", "Mean Time", "Std Dev", "Min", "Max"]
            widths = [15, 8, 14, 12, 12, 12]
            lines.append(self._get_table_header(columns, widths))

            # Sort results by size, then by mean time
            sorted_results = sorted(results, key=lambda x: (x.size, x.mean_time))

            current_size = None
            for result in sorted_results:
                if result.size != current_size:
                    if current_size is not None:
                        lines.append("-" * sum(widths) + "-" * (len(widths) - 1) * 3)
                    current_size = result.size

                row = [
                    result.algorithm.ljust(widths[0]),
                    str(result.size).center(widths[1]),
                    self._format_time(result.mean_time).rjust(widths[2]),
                    self._format_time(result.std_dev).rjust(widths[3]),
                    self._format_time(result.min_time).rjust(widths[4]),
                    self._format_time(result.max_time).rjust(widths[5]),
                ]
                lines.append(" | ".join(row))

        return "\n".join(lines)

    def generate_comparison_matrix(self) -> str:
        """
        Generate a matrix comparing algorithms across all scenarios.

        Returns:
            Formatted comparison matrix
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("ALGORITHM COMPARISON MATRIX (Mean Execution Time)")
        lines.append("=" * 80)

        # Get unique sizes and algorithms
        sizes = sorted(set(r.size for r in self.aggregated))
        algorithms = sorted(set(r.algorithm for r in self.aggregated))

        for dtype in [dt.value for dt in DatasetType]:
            lines.append(f"\n--- {dtype.upper()} ---")

            # Header with algorithm names
            header = "Size".rjust(10) + " | " + " | ".join(
                alg[:12].center(12) for alg in algorithms
            )
            lines.append(header)
            lines.append("-" * len(header))

            for size in sizes:
                row = [str(size).rjust(10)]
                for alg in algorithms:
                    # Find the result for this combination
                    matching = [
                        r for r in self.aggregated
                        if r.algorithm == alg and r.dataset_type == dtype and r.size == size
                    ]
                    if matching:
                        time_str = f"{matching[0].mean_time:.4f}s"
                    else:
                        time_str = "N/A"
                    row.append(time_str.center(12))
                lines.append(" | ".join(row))

        return "\n".join(lines)

    def generate_best_algorithm_table(self) -> str:
        """
        Generate a table showing the best algorithm for each scenario.

        Returns:
            Formatted table of best algorithms
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("BEST ALGORITHM PER SCENARIO")
        lines.append("=" * 80)
        lines.append("")

        sizes = sorted(set(r.size for r in self.aggregated))

        # Header
        header = "Size".rjust(10) + " | " + " | ".join(
            dtype.value[:15].center(15) for dtype in DatasetType
        )
        lines.append(header)
        lines.append("-" * len(header))

        for size in sizes:
            row = [str(size).rjust(10)]
            for dtype in DatasetType:
                best = self.benchmark.get_best_algorithm(dtype.value, size)
                if best:
                    # Abbreviate algorithm names
                    name = best.algorithm.replace(" Sort", "")
                    row.append(name.center(15))
                else:
                    row.append("N/A".center(15))
            lines.append(" | ".join(row))

        return "\n".join(lines)

    def generate_speedup_analysis(self) -> str:
        """
        Generate analysis showing speedup ratios between algorithms.

        Returns:
            Formatted speedup analysis
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("SPEEDUP ANALYSIS (vs Merge Sort baseline)")
        lines.append("=" * 80)
        lines.append("")

        sizes = sorted(set(r.size for r in self.aggregated))

        for dtype in DatasetType:
            lines.append(f"\n--- {dtype.value.upper()} ---")

            for size in sizes:
                # Get merge sort time as baseline
                merge_results = [
                    r for r in self.aggregated
                    if r.algorithm == "Merge Sort" and
                    r.dataset_type == dtype.value and
                    r.size == size
                ]

                if not merge_results:
                    continue

                merge_time = merge_results[0].mean_time
                lines.append(f"\n  Size: {size}")

                # Compare all algorithms to merge sort
                for result in self.aggregated:
                    if result.dataset_type != dtype.value or result.size != size:
                        continue

                    if result.mean_time > 0:
                        ratio = result.mean_time / merge_time
                        if ratio > 1:
                            comparison = f"{ratio:.2f}x slower"
                        elif ratio < 1:
                            comparison = f"{1/ratio:.2f}x faster"
                        else:
                            comparison = "baseline"
                    else:
                        comparison = "N/A"

                    lines.append(f"    {result.algorithm:15}: {comparison}")

        return "\n".join(lines)

    def generate_recommendations(self) -> str:
        """
        Generate algorithm recommendations based on results.

        Returns:
            Formatted recommendation guide
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("ALGORITHM RECOMMENDATIONS")
        lines.append("=" * 80)

        recommendations = {
            "random": {
                "description": "Random/Unsorted Data",
                "recommendation": "",
                "reasoning": ""
            },
            "sorted": {
                "description": "Already Sorted Data",
                "recommendation": "",
                "reasoning": ""
            },
            "reverse_sorted": {
                "description": "Reverse Sorted Data",
                "recommendation": "",
                "reasoning": ""
            },
            "partially_sorted": {
                "description": "Partially Sorted Data",
                "recommendation": "",
                "reasoning": ""
            }
        }

        # Analyze results for each scenario
        largest_size = max(r.size for r in self.aggregated)

        for dtype in DatasetType:
            best = self.benchmark.get_best_algorithm(dtype.value, largest_size)
            if best:
                recommendations[dtype.value]["recommendation"] = best.algorithm

                # Generate reasoning based on the data type
                if dtype == DatasetType.SORTED:
                    if "Insertion" in best.algorithm:
                        recommendations[dtype.value]["reasoning"] = (
                            "Insertion Sort's adaptive nature makes it optimal "
                            "for already sorted data with O(n) time complexity."
                        )
                    else:
                        recommendations[dtype.value]["reasoning"] = (
                            f"{best.algorithm} performed best in our tests."
                        )
                elif dtype == DatasetType.REVERSE:
                    recommendations[dtype.value]["reasoning"] = (
                        f"{best.algorithm} handles worst-case scenarios efficiently "
                        "with consistent O(n log n) performance."
                    )
                elif dtype == DatasetType.PARTIAL:
                    recommendations[dtype.value]["reasoning"] = (
                        f"{best.algorithm} excels with partially sorted data "
                        "due to its adaptive behavior."
                    )
                else:
                    recommendations[dtype.value]["reasoning"] = (
                        f"{best.algorithm} provides the best average-case performance "
                        "for random data with guaranteed O(n log n) complexity."
                    )

        for dtype_val, rec in recommendations.items():
            lines.append(f"\n{rec['description']}:")
            lines.append(f"  Recommended: {rec['recommendation']}")
            lines.append(f"  Reasoning: {rec['reasoning']}")

        return "\n".join(lines)

    def generate_full_report(self) -> str:
        """
        Generate a complete benchmark report.

        Returns:
            Complete formatted report
        """
        sections = [
            self.generate_summary_table(),
            self.generate_comparison_matrix(),
            self.generate_best_algorithm_table(),
            self.generate_speedup_analysis(),
            self.generate_recommendations(),
        ]

        return "\n".join(sections)

    def save_report(self, filename: str = "benchmark_report.txt") -> str:
        """
        Save the full report to a text file.

        Args:
            filename: Name of the output file

        Returns:
            Path to the saved file
        """
        filepath = os.path.join(self.config.output_dir, filename)
        report = self.generate_full_report()

        with open(filepath, 'w') as f:
            f.write(report)

        return filepath

    def save_csv(self, filename: str = "benchmark_results.csv") -> str:
        """
        Save results to CSV format for further analysis.

        Args:
            filename: Name of the output file

        Returns:
            Path to the saved file
        """
        filepath = os.path.join(self.config.output_dir, filename)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Algorithm', 'Dataset Type', 'Size',
                'Mean Time (s)', 'Std Dev (s)', 'Min Time (s)', 'Max Time (s)', 'Runs'
            ])

            for result in self.aggregated:
                writer.writerow([
                    result.algorithm,
                    result.dataset_type,
                    result.size,
                    result.mean_time,
                    result.std_dev,
                    result.min_time,
                    result.max_time,
                    result.runs
                ])

        return filepath

    def save_markdown(self, filename: str = "benchmark_report.md") -> str:
        """
        Save results in Markdown format.

        Args:
            filename: Name of the output file

        Returns:
            Path to the saved file
        """
        filepath = os.path.join(self.config.output_dir, filename)
        lines = []

        # Title
        lines.append(f"# {self.config.title}")
        lines.append(f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        # Summary table
        lines.append("## Performance Results\n")

        for dtype in DatasetType:
            lines.append(f"### {dtype.value.replace('_', ' ').title()}\n")
            lines.append("| Algorithm | Size | Mean Time | Std Dev |")
            lines.append("|-----------|------|-----------|---------|")

            matching = [r for r in self.aggregated if r.dataset_type == dtype.value]
            matching.sort(key=lambda x: (x.size, x.mean_time))

            for result in matching:
                lines.append(
                    f"| {result.algorithm} | {result.size} | "
                    f"{result.mean_time:.6f}s | {result.std_dev:.6f}s |"
                )
            lines.append("")

        # Best algorithms
        lines.append("## Best Algorithm per Scenario\n")
        lines.append("| Size | " + " | ".join(dt.value for dt in DatasetType) + " |")
        lines.append("|------|" + "|".join("---" for _ in DatasetType) + "|")

        sizes = sorted(set(r.size for r in self.aggregated))
        for size in sizes:
            row = [str(size)]
            for dtype in DatasetType:
                best = self.benchmark.get_best_algorithm(dtype.value, size)
                row.append(best.algorithm if best else "N/A")
            lines.append("| " + " | ".join(row) + " |")

        with open(filepath, 'w') as f:
            f.write("\n".join(lines))

        return filepath


if __name__ == "__main__":
    # Demo report generation
    print("Running benchmark for report demo...")

    benchmark = Benchmark(sizes=[100, 500], num_runs=2, verbose=False)
    benchmark.run_benchmarks(skip_slow_combinations=False)

    generator = ReportGenerator(benchmark)

    print("\n" + generator.generate_full_report())

    # Save reports
    txt_path = generator.save_report()
    csv_path = generator.save_csv()
    md_path = generator.save_markdown()

    print(f"\nReports saved to:")
    print(f"  Text: {txt_path}")
    print(f"  CSV: {csv_path}")
    print(f"  Markdown: {md_path}")
