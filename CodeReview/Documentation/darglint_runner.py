# CodeReview/Documentation/darglint_runner.py

import subprocess
from typing import Dict

def run_darglint(file_path: str) -> Dict:
    """
    Run darglint on a Python file to check docstring compliance.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: Contains return code, stdout, stderr, and success flag.
    """
    cmd = ["darglint", file_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "file": file_path,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "success": result.returncode == 0
    }
