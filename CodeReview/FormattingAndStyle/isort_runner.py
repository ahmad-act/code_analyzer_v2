# CodeReview/CodeQuality/isort_runner.py

import subprocess
from typing import Dict

def run_isort(file_path: str, check: bool = True, diff: bool = False) -> Dict:
    """
    Run isort on a Python file to check/fix import sorting.

    Args:
        file_path (str): Path to the Python file.
        check (bool): If True, run in check mode (don't modify files, just check).
        diff (bool): If True, show diff of changes.

    Returns:
        dict: Result containing info about sorting and diff output if requested.
    """
    cmd = ['isort']
    if check:
        cmd.append('--check-only')
    if diff:
        cmd.append('--diff')
    cmd.append(file_path)

    result = subprocess.run(cmd, capture_output=True, text=True)

    output = result.stdout.strip()
    error = result.stderr.strip()

    # isort returns 0 if everything is fine, 1 if changes needed
    reformat_needed = (result.returncode == 1)

    return {
        "file": file_path,
        "reformat_needed": reformat_needed,
        "stdout": output,
        "stderr": error,
        "returncode": result.returncode,
    }
