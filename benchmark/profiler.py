# profiler.py
import functools
import os
import platform
import time
from datetime import datetime
from typing import Any, Callable

import psutil
from feluda.operator import Operator
from memory_profiler import memory_usage


class Profiler:
    """Uniform profiler for benchmarking operators."""

    @staticmethod
    def get_system_info() -> dict[str, Any]:
        """Return system specifications."""
        cpu_freq = psutil.cpu_freq()
        return {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "cpu_freq": cpu_freq._asdict() if cpu_freq else None,
            "total_memory_gb": psutil.virtual_memory().total / (1024**3),
            "python_version": platform.python_version(),
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def _get_memory_mb() -> float:
        """Return current process memory in MB."""
        return psutil.Process().memory_info().rss / (1024 * 1024)

    @staticmethod
    def profile(func: Callable) -> Callable:
        """Decorator to profile memory and execution time."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mem_before = Profiler._get_memory_mb()
            start_wall = time.perf_counter()
            start_cpu = time.process_time()

            result = None

            def run_func():
                nonlocal result
                result = func(*args, **kwargs)
                return result

            mem_usage = memory_usage(run_func, interval=0.1, timeout=None)
            peak_memory = max(mem_usage) if mem_usage else mem_before

            end_wall = time.perf_counter()
            end_cpu = time.process_time()
            mem_after = Profiler._get_memory_mb()

            profile_data = {
                "execution_time_seconds": round(end_wall - start_wall, 4),
                "cpu_time_seconds": round(end_cpu - start_cpu, 4),
                "memory_before_mb": round(mem_before, 2),
                "memory_after_mb": round(mem_after, 2),
                "memory_change_mb": round(mem_after - mem_before, 2),
                "peak_memory_mb": round(peak_memory, 2),
            }
            return result, profile_data

        return wrapper

    @staticmethod
    def benchmark_operator(
        operator_class: type[Operator],
        operator_name: str,
        runtime_kwargs: dict,
        operator_kwargs: dict = {},
    ) -> dict[str, Any]:
        """Benchmark a single operator with given test data."""
        results = {
            "operator": operator_name,
            "timestamp": datetime.now().isoformat(),
        }
        try:
            # Initialization profiling
            init_start = time.perf_counter()
            init_mem_before = Profiler._get_memory_mb()

            op_instance = operator_class(**operator_kwargs)

            init_mem_after = Profiler._get_memory_mb()
            results["initialization"] = {
                "time_seconds": time.perf_counter() - init_start,
                "memory_change_mb": init_mem_after - init_mem_before,
            }

            # Execution profiling
            @Profiler.profile
            def run_operator():
                return op_instance.run(**runtime_kwargs)

            output, exec_profile = run_operator()
            results["execution"] = exec_profile

            # Cleanup profiling
            cleanup_start = time.perf_counter()
            cleanup_mem_before = Profiler._get_memory_mb()
            op_instance.cleanup()
            cleanup_mem_after = Profiler._get_memory_mb()

            results["cleanup"] = {
                "time_seconds": time.perf_counter() - cleanup_start,
                "memory_released_mb": cleanup_mem_before - cleanup_mem_after,
            }

            results["status"] = "success"

        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)

        return results
