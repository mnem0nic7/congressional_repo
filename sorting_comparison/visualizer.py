"""
Visualization Module

This module creates charts and graphs to visualize sorting algorithm
performance comparisons. It generates:
- Bar charts comparing algorithms for each dataset type
- Line charts showing scaling behavior across sizes
- Heatmaps showing relative performance
- Combined comparison plots
"""

import os
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from benchmark import Benchmark, AggregatedResult
from data_generator import DatasetType


class Visualizer:
    """
    Creates visualizations for sorting algorithm benchmark results.
    """

    # Color scheme for algorithms
    COLORS = {
        'Bubble Sort': '#e74c3c',      # Red
        'Selection Sort': '#f39c12',   # Orange
        'Insertion Sort': '#27ae60',   # Green
        'Merge Sort': '#3498db',       # Blue
    }

    # Markers for line plots
    MARKERS = {
        'Bubble Sort': 'o',
        'Selection Sort': 's',
        'Insertion Sort': '^',
        'Merge Sort': 'D',
    }

    def __init__(self, benchmark: Benchmark, output_dir: str = "results"):
        """
        Initialize the visualizer.

        Args:
            benchmark: Benchmark instance with results
            output_dir: Directory to save generated plots
        """
        self.benchmark = benchmark
        self.aggregated = benchmark.aggregate_results()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Set matplotlib style
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12

    def _get_color(self, algorithm: str) -> str:
        """Get color for an algorithm."""
        return self.COLORS.get(algorithm, '#95a5a6')

    def _get_marker(self, algorithm: str) -> str:
        """Get marker for an algorithm."""
        return self.MARKERS.get(algorithm, 'o')

    def plot_bar_comparison(
        self,
        size: int,
        save: bool = True,
        show: bool = False
    ) -> Optional[str]:
        """
        Create a bar chart comparing all algorithms for a specific size.

        Args:
            size: Dataset size to plot
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved file if save=True, else None
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Algorithm Comparison for n={size}', fontsize=16, fontweight='bold')

        dataset_types = [dt.value for dt in DatasetType]
        algorithms = sorted(set(r.algorithm for r in self.aggregated))

        for ax, dtype in zip(axes.flat, dataset_types):
            # Get data for this dataset type and size
            times = []
            colors = []
            labels = []

            for alg in algorithms:
                matching = [
                    r for r in self.aggregated
                    if r.algorithm == alg and r.dataset_type == dtype and r.size == size
                ]
                if matching:
                    times.append(matching[0].mean_time)
                    colors.append(self._get_color(alg))
                    labels.append(alg.replace(' Sort', ''))
                else:
                    times.append(0)
                    colors.append('#cccccc')
                    labels.append(alg.replace(' Sort', '') + ' (N/A)')

            x = np.arange(len(labels))
            bars = ax.bar(x, times, color=colors, edgecolor='black', linewidth=0.5)

            # Add value labels on bars
            for bar, time in zip(bars, times):
                if time > 0:
                    height = bar.get_height()
                    ax.annotate(f'{time:.4f}s',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

            ax.set_xlabel('Algorithm')
            ax.set_ylabel('Time (seconds)')
            ax.set_title(dtype.replace('_', ' ').title())
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha='right')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, f'comparison_size_{size}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath

        if show:
            plt.show()
        plt.close()
        return None

    def plot_scaling_behavior(
        self,
        dataset_type: str = None,
        save: bool = True,
        show: bool = False
    ) -> Optional[str]:
        """
        Create line charts showing how algorithms scale with input size.

        Args:
            dataset_type: Specific type to plot, or None for all types
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved file if save=True, else None
        """
        if dataset_type:
            dtypes = [dataset_type]
            fig, ax = plt.subplots(figsize=(12, 8))
            axes = [ax]
        else:
            dtypes = [dt.value for dt in DatasetType]
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            axes = axes.flat

        fig.suptitle('Algorithm Scaling Behavior', fontsize=16, fontweight='bold')

        algorithms = sorted(set(r.algorithm for r in self.aggregated))
        sizes = sorted(set(r.size for r in self.aggregated))

        for ax, dtype in zip(axes, dtypes):
            for alg in algorithms:
                x_vals = []
                y_vals = []

                for size in sizes:
                    matching = [
                        r for r in self.aggregated
                        if r.algorithm == alg and r.dataset_type == dtype and r.size == size
                    ]
                    if matching:
                        x_vals.append(size)
                        y_vals.append(matching[0].mean_time)

                if x_vals:
                    ax.plot(x_vals, y_vals,
                            marker=self._get_marker(alg),
                            color=self._get_color(alg),
                            label=alg,
                            linewidth=2,
                            markersize=8)

            ax.set_xlabel('Dataset Size (n)')
            ax.set_ylabel('Time (seconds)')
            ax.set_title(dtype.replace('_', ' ').title())
            ax.legend(loc='upper left')
            ax.set_xscale('log')
            ax.set_yscale('log')

        plt.tight_layout()

        if save:
            suffix = f"_{dataset_type}" if dataset_type else "_all"
            filepath = os.path.join(self.output_dir, f'scaling{suffix}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath

        if show:
            plt.show()
        plt.close()
        return None

    def plot_heatmap(
        self,
        size: int,
        save: bool = True,
        show: bool = False
    ) -> Optional[str]:
        """
        Create a heatmap showing relative performance across scenarios.

        Args:
            size: Dataset size to visualize
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved file if save=True, else None
        """
        algorithms = sorted(set(r.algorithm for r in self.aggregated))
        dataset_types = [dt.value for dt in DatasetType]

        # Build the data matrix
        data = np.zeros((len(algorithms), len(dataset_types)))

        for i, alg in enumerate(algorithms):
            for j, dtype in enumerate(dataset_types):
                matching = [
                    r for r in self.aggregated
                    if r.algorithm == alg and r.dataset_type == dtype and r.size == size
                ]
                if matching:
                    data[i, j] = matching[0].mean_time
                else:
                    data[i, j] = np.nan

        # Normalize for better visualization (optional)
        fig, ax = plt.subplots(figsize=(10, 8))

        # Create heatmap
        im = ax.imshow(data, cmap='RdYlGn_r', aspect='auto')

        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Execution Time (seconds)', rotation=-90, va="bottom")

        # Set ticks and labels
        ax.set_xticks(np.arange(len(dataset_types)))
        ax.set_yticks(np.arange(len(algorithms)))
        ax.set_xticklabels([dt.replace('_', ' ').title() for dt in dataset_types])
        ax.set_yticklabels(algorithms)

        # Rotate x labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Add text annotations
        for i in range(len(algorithms)):
            for j in range(len(dataset_types)):
                if not np.isnan(data[i, j]):
                    text = ax.text(j, i, f'{data[i, j]:.4f}s',
                                   ha="center", va="center", color="black", fontsize=9)

        ax.set_title(f'Performance Heatmap (n={size})', fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, f'heatmap_size_{size}.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath

        if show:
            plt.show()
        plt.close()
        return None

    def plot_speedup_ratios(
        self,
        baseline_algorithm: str = "Merge Sort",
        save: bool = True,
        show: bool = False
    ) -> Optional[str]:
        """
        Create a chart showing speedup ratios relative to a baseline.

        Args:
            baseline_algorithm: Algorithm to use as baseline (ratio = 1.0)
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved file if save=True, else None
        """
        algorithms = sorted(set(r.algorithm for r in self.aggregated))
        sizes = sorted(set(r.size for r in self.aggregated))

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Performance Ratio (relative to {baseline_algorithm})',
                     fontsize=16, fontweight='bold')

        for ax, dtype in zip(axes.flat, [dt.value for dt in DatasetType]):
            x = np.arange(len(sizes))
            width = 0.2
            offset = 0

            for alg in algorithms:
                if alg == baseline_algorithm:
                    continue

                ratios = []
                for size in sizes:
                    alg_result = [
                        r for r in self.aggregated
                        if r.algorithm == alg and r.dataset_type == dtype and r.size == size
                    ]
                    baseline_result = [
                        r for r in self.aggregated
                        if r.algorithm == baseline_algorithm and
                        r.dataset_type == dtype and r.size == size
                    ]

                    if alg_result and baseline_result and baseline_result[0].mean_time > 0:
                        ratio = alg_result[0].mean_time / baseline_result[0].mean_time
                        ratios.append(ratio)
                    else:
                        ratios.append(0)

                ax.bar(x + offset, ratios, width,
                       label=alg, color=self._get_color(alg))
                offset += width

            ax.axhline(y=1, color='black', linestyle='--', linewidth=1, label='Baseline')
            ax.set_xlabel('Dataset Size')
            ax.set_ylabel('Ratio (higher = slower)')
            ax.set_title(dtype.replace('_', ' ').title())
            ax.set_xticks(x + width)
            ax.set_xticklabels(sizes)
            ax.legend(loc='upper left', fontsize=8)
            ax.set_yscale('log')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'speedup_ratios.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath

        if show:
            plt.show()
        plt.close()
        return None

    def plot_combined_overview(
        self,
        save: bool = True,
        show: bool = False
    ) -> Optional[str]:
        """
        Create a comprehensive overview plot combining multiple visualizations.

        Args:
            save: Whether to save the plot
            show: Whether to display the plot

        Returns:
            Path to saved file if save=True, else None
        """
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('Sorting Algorithm Performance Overview',
                     fontsize=18, fontweight='bold')

        algorithms = sorted(set(r.algorithm for r in self.aggregated))
        sizes = sorted(set(r.size for r in self.aggregated))
        max_size = max(sizes)

        # Create grid
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Plot 1: Bar comparison for largest size
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_title(f'Comparison at n={max_size}')

        dtype = 'random'
        times = []
        colors = []
        labels = []

        for alg in algorithms:
            matching = [
                r for r in self.aggregated
                if r.algorithm == alg and r.dataset_type == dtype and r.size == max_size
            ]
            if matching:
                times.append(matching[0].mean_time)
                colors.append(self._get_color(alg))
                labels.append(alg.replace(' Sort', ''))

        if times:
            ax1.barh(labels, times, color=colors)
            ax1.set_xlabel('Time (seconds)')

        # Plot 2: Scaling for random data
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_title('Scaling Behavior (Random Data)')

        for alg in algorithms:
            x_vals = []
            y_vals = []
            for size in sizes:
                matching = [
                    r for r in self.aggregated
                    if r.algorithm == alg and r.dataset_type == 'random' and r.size == size
                ]
                if matching:
                    x_vals.append(size)
                    y_vals.append(matching[0].mean_time)

            if x_vals:
                ax2.plot(x_vals, y_vals,
                         marker=self._get_marker(alg),
                         color=self._get_color(alg),
                         label=alg, linewidth=2)

        ax2.set_xlabel('Dataset Size (n)')
        ax2.set_ylabel('Time (seconds)')
        ax2.legend(loc='upper left', fontsize=9)
        ax2.set_xscale('log')
        ax2.set_yscale('log')

        # Plot 3: Best algorithm per scenario
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.set_title('Best Algorithm per Scenario')

        # Create a simple matrix visualization
        best_matrix = []
        for dtype in DatasetType:
            row = []
            for size in sizes:
                best = self.benchmark.get_best_algorithm(dtype.value, size)
                row.append(algorithms.index(best.algorithm) if best else -1)
            best_matrix.append(row)

        im = ax3.imshow(best_matrix, cmap='Set1', aspect='auto')
        ax3.set_xticks(range(len(sizes)))
        ax3.set_yticks(range(len(DatasetType)))
        ax3.set_xticklabels(sizes)
        ax3.set_yticklabels([dt.value.replace('_', ' ').title() for dt in DatasetType])
        ax3.set_xlabel('Dataset Size')

        # Create legend
        patches = [mpatches.Patch(color=self._get_color(alg), label=alg)
                   for alg in algorithms]
        ax3.legend(handles=patches, loc='center left', bbox_to_anchor=(1.02, 0.5),
                   fontsize=8)

        # Plot 4: Summary text
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')

        # Generate summary text
        summary_lines = [
            "Key Findings:",
            "",
        ]

        # Find best overall algorithm for random data at largest size
        best_random = self.benchmark.get_best_algorithm('random', max_size)
        if best_random:
            summary_lines.append(f"• Best for random data: {best_random.algorithm}")
            summary_lines.append(f"  (n={max_size}): {best_random.mean_time:.4f}s")
            summary_lines.append("")

        # Find best for sorted data
        best_sorted = self.benchmark.get_best_algorithm('sorted', max_size)
        if best_sorted:
            summary_lines.append(f"• Best for sorted data: {best_sorted.algorithm}")
            summary_lines.append(f"  (n={max_size}): {best_sorted.mean_time:.4f}s")
            summary_lines.append("")

        summary_lines.extend([
            "Recommendations:",
            "",
            "• Use Merge Sort for general-purpose sorting",
            "• Use Insertion Sort for small/nearly-sorted data",
            "• Avoid Bubble Sort for large datasets",
        ])

        summary_text = "\n".join(summary_lines)
        ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes,
                 fontsize=11, verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'overview.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath

        if show:
            plt.show()
        plt.close()
        return None

    def generate_all_plots(self) -> List[str]:
        """
        Generate all available visualizations.

        Returns:
            List of paths to saved plot files
        """
        saved_files = []

        sizes = sorted(set(r.size for r in self.aggregated))

        # Bar comparisons for each size
        for size in sizes:
            filepath = self.plot_bar_comparison(size, save=True)
            if filepath:
                saved_files.append(filepath)

        # Scaling behavior plot
        filepath = self.plot_scaling_behavior(save=True)
        if filepath:
            saved_files.append(filepath)

        # Heatmaps for each size
        for size in sizes:
            filepath = self.plot_heatmap(size, save=True)
            if filepath:
                saved_files.append(filepath)

        # Speedup ratios
        filepath = self.plot_speedup_ratios(save=True)
        if filepath:
            saved_files.append(filepath)

        # Combined overview
        filepath = self.plot_combined_overview(save=True)
        if filepath:
            saved_files.append(filepath)

        return saved_files


if __name__ == "__main__":
    print("Running visualization demo...")

    # Run a quick benchmark
    benchmark = Benchmark(sizes=[100, 500, 1000], num_runs=2, verbose=False)
    benchmark.run_benchmarks(skip_slow_combinations=False)

    # Create visualizations
    viz = Visualizer(benchmark)

    print("Generating plots...")
    saved_files = viz.generate_all_plots()

    print(f"\nGenerated {len(saved_files)} plots:")
    for f in saved_files:
        print(f"  - {f}")
