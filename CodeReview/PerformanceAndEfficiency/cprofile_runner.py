# CodeReview/Performance/cprofile_runner.py
import cProfile
import pstats
import io
from typing import List, Dict


def run_cprofile(file_path: str) -> List[Dict]:
    """
    Profiles the execution of a Python file using cProfile and returns sorted results.
    """
    profiler = cProfile.Profile()

    try:
        profiler.run(f'exec(open({repr(file_path)}).read(), {{}})')
    except Exception as e:
        return [{"error": f"Execution failed: {e}"}]

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats('cumulative')
    stats.print_stats()

    output = stream.getvalue()
    return parse_cprofile_output(output)


def parse_cprofile_output(output: str) -> List[Dict]:
    """
    Parses the cProfile output text and returns a list of performance entries.
    """
    results = []
    lines = output.splitlines()

    header_found = False
    for line in lines:
        if not header_found:
            if line.strip().startswith("ncalls"):
                header_found = True
            continue

        if header_found and line.strip():
            parts = line.strip().split(None, 5)
            if len(parts) == 6:
                ncalls, tottime, percall1, cumtime, percall2, filename_func = parts
                results.append({
                    "ncalls": ncalls,
                    "total_time": float(tottime),
                    "per_call_time": float(percall1),
                    "cumulative_time": float(cumtime),
                    "cumulative_per_call": float(percall2),
                    "location": filename_func
                })

    return results
