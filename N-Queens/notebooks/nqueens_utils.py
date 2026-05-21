"""Shared utilities for N-Queens algorithms."""

import csv
from dataclasses import dataclass
from html import escape
from pathlib import Path
import matplotlib.pyplot as plt


@dataclass
class RunResult:
    n: int
    status: str
    solved: bool
    steps: int
    conflicts: int | str
    time_seconds: float
    memory_mb: float
    note: str
    solution: list[int] | None = None
    image_path: str = "N/A"


def pair_conflicts(counts) -> int:
    return sum(count * (count - 1) // 2 for count in counts if count > 1)


def count_conflicts(board: list[int]) -> int:
    if not board:
        return 0
    n = len(board)
    col_counts = [0] * n
    diag_main = [0] * (2 * n - 1)
    diag_anti = [0] * (2 * n - 1)
    for row, col in enumerate(board):
        col_counts[col] += 1
        diag_main[row - col + n - 1] += 1
        diag_anti[row + col] += 1
    return pair_conflicts(col_counts) + pair_conflicts(diag_main) + pair_conflicts(diag_anti)


def render_board(board: list[int] | None, limit: int = 12) -> str:
    if board is None:
        return "No solution board available."
    n = len(board)
    if n > limit:
        return f"Board visual skipped for N = {n}. Small-board rendering is limited to N <= {limit}."

    lines = ["Solution Vector: [" + ", ".join(str(v) for v in board) + "]"]
    header = "    " + " ".join(f"{col:>2}" for col in range(n))
    border = "   +" + "---" * n + "+"
    lines.extend([header, border])
    for row, queen_col in enumerate(board):
        row_cells = ["Q" if col == queen_col else "." for col in range(n)]
        lines.append(f"{row:>2} | " + "  ".join(row_cells) + " |")
    lines.append(border)
    return "\n".join(lines)


def save_board_svg(board: list[int], title: str, output_path: Path, colors: dict) -> Path:
    n = len(board)
    cell_size = 56
    margin_left, margin_top, footer_height = 82, 110, 88
    width = margin_left + n * cell_size + 40
    height = margin_top + n * cell_size + footer_height
    solution_vector = "Solution vector: [" + ", ".join(str(v) for v in board) + "]"

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{margin_left}" y="42" font-size="28" font-family="Segoe UI, Arial, sans-serif" font-weight="700" fill="{colors["title"]}">{escape(title)}</text>',
        f'<text x="{margin_left}" y="74" font-size="20" font-family="Consolas, Courier New, monospace" fill="{colors["subtitle"]}">{escape(solution_vector)}</text>',
    ]

    for col in range(n):
        x = margin_left + col * cell_size + cell_size / 2
        svg_parts.append(f'<text x="{x}" y="{margin_top - 20}" text-anchor="middle" font-size="18" font-family="Segoe UI, Arial, sans-serif" fill="{colors["label"]}">{col}</text>')

    for row in range(n):
        y = margin_top + row * cell_size + cell_size / 2 + 7
        svg_parts.append(f'<text x="{margin_left - 28}" y="{y}" text-anchor="middle" font-size="18" font-family="Segoe UI, Arial, sans-serif" fill="{colors["label"]}">{row}</text>')
        for col in range(n):
            x = margin_left + col * cell_size
            y_cell = margin_top + row * cell_size
            fill = colors["light"] if (row + col) % 2 == 0 else colors["dark"]
            svg_parts.append(f'<rect x="{x}" y="{y_cell}" width="{cell_size}" height="{cell_size}" fill="{fill}" stroke="{colors["outline"]}" stroke-width="1.2"/>')
            if board[row] == col:
                cx, cy = x + cell_size / 2, y_cell + cell_size / 2
                svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{cell_size * 0.26}" fill="{colors["queen"]}" stroke="#ffffff" stroke-width="2.5"/>')
                svg_parts.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="28" font-family="Segoe UI Symbol, Arial Unicode MS, serif" fill="#ffffff">Q</text>')

    svg_parts.append('</svg>')
    output_path.write_text("\n".join(svg_parts), encoding="utf-8")
    return output_path


def format_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [max(len(header), *[len(row[i]) for row in rows]) for i, header in enumerate(headers)]
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    def render_row(values):
        return "| " + " | ".join(v.ljust(widths[i]) for i, v in enumerate(values)) + " |"
    lines = [border, render_row(headers), border]
    lines.extend(render_row(row) for row in rows)
    lines.append(border)
    return "\n".join(lines)


def save_performance_chart(results: list[RunResult], algorithm_name: str, project_title: str, output_path: Path, primary_color: str) -> Path:
    plt.style.use("seaborn-v0_8-whitegrid")
    ns = [item.n for item in results]
    times = [item.time_seconds for item in results]
    memories = [item.memory_mb for item in results]
    statuses = [item.status for item in results]
    colors = [primary_color if s == "SOLVED" else "#f59e0b" if s == "TIMEOUT" else "#dc2626" for s in statuses]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    axes[0].plot(ns, times, color=primary_color, linewidth=2.4, marker="o", markersize=7)
    axes[0].scatter(ns, times, c=colors, s=90, edgecolors="#ffffff", linewidths=1.2, zorder=3)
    axes[0].set_title(f"{algorithm_name} - Execution Time", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Board Size (N)")
    axes[0].set_ylabel("Time (seconds)")
    axes[0].set_xticks(ns)
    axes[0].tick_params(axis="x", rotation=20)

    axes[1].bar([str(v) for v in ns], memories, color=primary_color, alpha=0.6, edgecolor=primary_color, linewidth=1.2)
    axes[1].set_title(f"{algorithm_name} - Peak Memory", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Board Size (N)")
    axes[1].set_ylabel("Peak Memory (MB)")

    for axis in axes:
        axis.grid(True, alpha=0.25)

    fig.suptitle(project_title, fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def refresh_combined_outputs(output_dir: Path, project_title: str) -> tuple[Path, Path]:
    comparison_csv = output_dir / "all_algorithms_comparison.csv"
    comparison_chart = output_dir / "charts" / "all_algorithms_comparison.png"
    source_files = [
        ("Exhaustive Depth-First Search", output_dir / "dfs_nqueens_results.csv"),
        ("Local Greedy Search (Hill Climbing)", output_dir / "greedy_nqueens_results.csv"),
        ("Local Simulated Annealing", output_dir / "simulated_annealing_nqueens_results.csv"),
        ("Genetic Algorithm", output_dir / "genetic_nqueens_results.csv"),
    ]

    combined_rows = []
    for algorithm, csv_path in source_files:
        if not csv_path.exists():
            continue
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                step_value = row.get("Steps") or row.get("Iterations") or row.get("Generations") or ""
                combined_rows.append({
                    "Algorithm": algorithm,
                    "N": row.get("N", ""),
                    "Status": row.get("Status", ""),
                    "Solved": row.get("Solved", ""),
                    "Steps": step_value,
                    "Conflicts": row.get("Conflicts", ""),
                    "TimeSeconds": row.get("TimeSeconds", ""),
                    "PeakMemoryMB": row.get("PeakMemoryMB", ""),
                    "ImagePath": row.get("ImagePath", "N/A"),
                })

    combined_rows.sort(key=lambda item: (item["Algorithm"], int(item["N"])))

    with comparison_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Algorithm", "N", "Status", "Solved", "Steps", "Conflicts", "TimeSeconds", "PeakMemoryMB", "ImagePath"])
        writer.writeheader()
        writer.writerows(combined_rows)

    if combined_rows:
        plt.style.use("seaborn-v0_8-whitegrid")
        fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
        palette = {
            "Exhaustive Depth-First Search": "#c0392b",
            "Local Greedy Search (Hill Climbing)": "#2d6a4f",
            "Local Simulated Annealing": "#006d77",
            "Genetic Algorithm": "#9d0208",
        }

        for algorithm in [item[0] for item in source_files]:
            rows = [row for row in combined_rows if row["Algorithm"] == algorithm]
            if not rows:
                continue
            ns = [int(row["N"]) for row in rows]
            times = [float(row["TimeSeconds"]) for row in rows]
            memories = [float(row["PeakMemoryMB"]) for row in rows]
            axes[0].plot(ns, times, marker="o", linewidth=2.2, label=algorithm, color=palette[algorithm])
            axes[1].plot(ns, memories, marker="o", linewidth=2.2, label=algorithm, color=palette[algorithm])

        axes[0].set_title("Execution Time Comparison", fontsize=13, fontweight="bold")
        axes[0].set_xlabel("Board Size (N)")
        axes[0].set_ylabel("Time (seconds)")
        axes[0].set_xticks([10, 30, 50, 100, 200, 500])
        axes[0].tick_params(axis="x", rotation=20)

        axes[1].set_title("Peak Memory Comparison", fontsize=13, fontweight="bold")
        axes[1].set_xlabel("Board Size (N)")
        axes[1].set_ylabel("Peak Memory (MB)")
        axes[1].set_xticks([10, 30, 50, 100, 200, 500])
        axes[1].tick_params(axis="x", rotation=20)

        for axis in axes:
            axis.grid(True, alpha=0.25)
            axis.legend(fontsize=8)

        fig.suptitle(project_title, fontsize=15, fontweight="bold")
        fig.tight_layout()
        fig.savefig(comparison_chart, dpi=180, bbox_inches="tight")
        plt.close(fig)

    return comparison_csv, comparison_chart
