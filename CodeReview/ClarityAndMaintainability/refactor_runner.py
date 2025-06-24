import subprocess
import json
import re
from typing import List, Dict


def run_refactor(file_path: str) -> List[Dict]:
    """
    Runs the refactor CLI tool on a Python file and parses its output.
    """
    result = subprocess.run(
        ['refactor', '--diff', file_path],
        capture_output=True,
        text=True
    )
    return parse_refactor_output(result.stdout)


def parse_refactor_output(output: str) -> List[Dict]:
    """
    Parses the output of refactor --diff and returns a list of changes.
    """
    if not output.strip():
        return [{"message": "No refactor suggestions found."}]

    changes = []
    current_file = None
    diff_lines = []

    for line in output.splitlines():
        if line.startswith('--- ') or line.startswith('+++ '):
            continue
        elif line.startswith('@@'):
            if diff_lines:
                changes.append({
                    "file": current_file,
                    "diff": "\n".join(diff_lines)
                })
                diff_lines = []
        elif line.startswith('refactor:'):
            current_file = line.split(':', 1)[1].strip()
        else:
            diff_lines.append(line)

    if diff_lines and current_file:
        changes.append({
            "file": current_file,
            "diff": "\n".join(diff_lines)
        })

    return changes
