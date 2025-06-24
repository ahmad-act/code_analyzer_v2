import subprocess
import json
import re
from typing import List, Dict


def run_pytest(path: str) -> List[Dict]:
    """
    Run pytest on the specified path and return structured results.
    """
    result = subprocess.run(
        ['pytest', '--tb=short', '--maxfail=5', path],
        capture_output=True,
        text=True
    )
    return parse_pytest_output(result.stdout + result.stderr)


def parse_pytest_output(output: str) -> List[Dict]:
    """
    Parses pytest output into a list of dictionaries with test results.
    """
    results = []
    current_test = None

    for line in output.splitlines():
        if re.match(r"^FAILED .*::.* - .*", line):
            parts = line.split(" - ")
            if len(parts) == 2:
                results.append({
                    "status": "FAILED",
                    "test": parts[0].strip(),
                    "reason": parts[1].strip()
                })
        elif re.match(r"^PASSED .*", line):
            results.append({
                "status": "PASSED",
                "test": line.strip()
            })
        elif re.match(r"^ERROR .*::.*", line):
            results.append({
                "status": "ERROR",
                "test": line.strip()
            })

    # Optional summary match
    summary_match = re.search(r"==+ (.+) ==+", output)
    if summary_match:
        results.append({
            "summary": summary_match.group(1).strip()
        })

    return results
