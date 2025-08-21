# benchmark_report.py

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

import numpy as np
from profiler import Profiler


class BenchmarkReport:
    """Generate, summarize, and save benchmark results."""

    def __init__(self) -> None:
        self.results: list[dict[str, Any]] = []
        self.system_info: dict[str, Any] = Profiler.get_system_info()

    def add_results(self, result: dict[str, Any]) -> None:
        """Add a benchmark result to the report."""
        self.results.append(result)

    def generate_summary(self) -> dict[str, Any]:
        """Generate summary statistics for all benchmarked operators."""
        summary = {
            "system_info": self.system_info,
            "total_benchmarks": len(self.results),
            "results": self.results,
            "statistics": {},
        }

        # Group results by operator
        operators: dict[str, list[dict[str, Any]]] = {}
        for result in self.results:
            op_name = result.get("operator", "unknown")
            operators.setdefault(op_name, []).append(result)

        # Compute statistics per operator
        for op_name, op_results in operators.items():
            exec_times = [
                r["execution"]["execution_time_seconds"]
                for r in op_results
                if r.get("status") == "success" and "execution" in r
            ]
            mem_changes = [
                r["execution"]["memory_change_mb"]
                for r in op_results
                if r.get("status") == "success" and "execution" in r
            ]
            peak_memories = [
                r["execution"]["peak_memory_mb"]
                for r in op_results
                if r.get("status") == "success" and "execution" in r
            ]

            if exec_times:
                summary["statistics"][op_name] = {
                    "avg_execution_time": float(np.mean(exec_times)),
                    "min_execution_time": float(np.min(exec_times)),
                    "max_execution_time": float(np.max(exec_times)),
                    "std_execution_time": float(np.std(exec_times)),
                    "avg_memory_change": float(np.mean(mem_changes))
                    if mem_changes
                    else 0.0,
                    "max_memory_peak": float(max(peak_memories))
                    if peak_memories
                    else 0.0,
                    "total_runs": len(exec_times),
                    "success_rate": len(exec_times) / len(op_results),
                }

        return summary

    def save_json(self, filepath: str | Path = None) -> None:
        """Save the benchmark summary as JSON."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"results/benchmark_results_{timestamp}.json"
        Path(filepath).write_text(
            json.dumps(self.generate_summary(), indent=2, default=str),
            encoding="utf-8",
        )

    def save_markdown(self, filepath: str | Path = None) -> None:
        """Save the benchmark summary as a Markdown report."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"results/benchmark_results_{timestamp}.md"
        summary = self.generate_summary()
        sysinfo = self.system_info

        md_content = f"""# Benchmark Report

Generated: {sysinfo["timestamp"]}

## System Information

- Platform: {sysinfo["platform"]}
- Processor: {sysinfo["processor"]}
- CPU Count: {sysinfo["cpu_count"]}
- Total Memory: {sysinfo["total_memory_gb"]:.2f} GB
- Python Version: {sysinfo["python_version"]}

## Operator Statistics
"""

        for op_name, stats in sorted(summary["statistics"].items()):
            md_content += f"""
### {op_name}

- Total Runs: {stats["total_runs"]}
- Success Rate: {stats["success_rate"] * 100:.1f}%
- Avg Execution Time: {stats["avg_execution_time"]:.3f}s
- Min/Max Time: {stats["min_execution_time"]:.3f}s / {stats["max_execution_time"]:.3f}s
- Avg Memory Change: {stats["avg_memory_change"]:.2f} MB
- Peak Memory: {stats["max_memory_peak"]:.2f} MB
"""

        md_content += "\n## Detailed Results\n"
        for result in self.results:
            md_content += f"""
### {result["operator"]} - {result["data_description"]}
"""
            if result["status"] == "success":
                exec_data = result["execution"]
                md_content += f"""- Execution Time: {exec_data["execution_time_seconds"]:.3f}s
- Memory Change: {exec_data["memory_change_mb"]:.2f} MB
- Peak Memory: {exec_data["peak_memory_mb"]:.2f} MB
- CPU Time: {exec_data["cpu_time_seconds"]:.3f}s
"""
            else:
                md_content += f"""- Status: Failed
- Error: {result.get("error", "Unknown")}
"""

        Path(filepath).write_text(md_content, encoding="utf-8")
