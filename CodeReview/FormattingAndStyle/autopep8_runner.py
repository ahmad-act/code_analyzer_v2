# CodeReview/CodeQuality/autopep8_runner.py

import subprocess
from typing import Dict

def run_autopep8(file_path: str, check: bool = True, diff: bool = False) -> Dict:
    """
    Run autopep8 on a Python file to check/fix PEP8 formatting.

    Args:
        file_path (str): Path to the Python file.
        check (bool): If True, only check if file needs formatting (no changes applied).
        diff (bool): If True, show diff of changes.

    Returns:
        dict: Result including whether reformatting is needed, output, and errors.
    """
    cmd = ['autopep8', file_path]
    if check:
        cmd.append('--diff')
    if not diff:
        # If check=True but diff=False, disable diff output, so no output returned
        cmd.append('--exit-code')
    
    result = subprocess.run(cmd, capture_output=True, text=True)

    output = result.stdout.strip()
    error = result.stderr.strip()

    # exit code 0 means no changes needed; 1 means changes needed
    reformat_needed = (result.returncode == 1)

    return {
        "file": file_path,
        "reformat_needed": reformat_needed,
        "stdout": output,
        "stderr": error,
        "returncode": result.returncode,
    }
