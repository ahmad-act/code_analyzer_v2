# CodeReview/CodeQuality/black_runner.py

import subprocess
from typing import Dict

def run_black(file_path: str, check: bool = True, diff: bool = False) -> Dict:
    """
    Run Black formatter on a Python file.

    Args:
        file_path (str): Path to the Python file.
        check (bool): If True, run in check mode (don't modify files, just check).
        diff (bool): If True, show diff of changes.

    Returns:
        dict: Results including if file would be reformatted and any diff output.
    """
    cmd = ['black']
    if check:
        cmd.append('--check')
    if diff:
        cmd.append('--diff')
    cmd.append(file_path)

    result = subprocess.run(cmd, capture_output=True, text=True)

    output = result.stdout.strip()
    error = result.stderr.strip()

    reformat_needed = 'would reformat' in output or result.returncode == 1

    return {
        "file": file_path,
        "reformat_needed": reformat_needed,
        "stdout": output,
        "stderr": error,
        "returncode": result.returncode,
    }
