import subprocess
import json
import re
from typing import Dict, List

def run_coverage(source_path: str) -> Dict:
    """
    Run coverage.py to measure code coverage on the given source_path.
    Returns a parsed summary report as a dictionary.
    """
    # Run coverage: erase old data, run tests, then report in terminal
    subprocess.run(['coverage', 'erase'], capture_output=True, text=True)
    run_result = subprocess.run(['coverage', 'run', '-m', 'pytest', source_path], capture_output=True, text=True)
    
    report_result = subprocess.run(['coverage', 'report', '-m'], capture_output=True, text=True)

    parsed_report = parse_coverage_report(report_result.stdout)
    return {
        "run_output": run_result.stdout,
        "run_error": run_result.stderr,
        "report": parsed_report
    }


def parse_coverage_report(report_output: str) -> List[Dict]:
    """
    Parses the text output of 'coverage report -m' into structured JSON.
    """
    lines = report_output.strip().splitlines()
    results = []

    # Expect lines like:
    # Name                             Stmts   Miss  Cover   Missing
    # ----------------------------------------------------------------
    # code_analyzer/analyzer.py          100     10    90%   45-50, 78

    # Find the header line index (Name ... Missing)
    header_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("Name") and "Missing" in line:
            header_idx = i
            break

    # Parse subsequent lines until empty or summary
    for line in lines[header_idx+2:]:
        if not line.strip() or line.startswith("TOTAL"):
            # Optionally, parse TOTAL line as summary
            if line.startswith("TOTAL"):
                parts = re.split(r"\s+", line)
                if len(parts) >= 5:
                    results.append({
                        "file": "TOTAL",
                        "statements": int(parts[1]),
                        "missed": int(parts[2]),
                        "coverage": parts[3]
                    })
            break
        parts = re.split(r"\s+", line)
        if len(parts) >= 5:
            results.append({
                "file": parts[0],
                "statements": int(parts[1]),
                "missed": int(parts[2]),
                "coverage": parts[3],
                "missing_lines": parts[4] if len(parts) > 4 else ""
            })

    return results
