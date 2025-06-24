# CodeReview/Documentation/docformatter_runner.py

import subprocess
from typing import Dict

def run_docformatter(file_path: str, check_only: bool = False) -> Dict:
    """
    Run docformatter on a Python file.

    Args:
        file_path (str): Path to the Python file.
        check_only (bool): If True, only check formatting without modifying.

    Returns:
        dict: Contains return code, stdout, stderr, and success flag.
    """
    cmd = ["docformatter"]
    if check_only:
        cmd.append("--check")
    else:
        cmd.append("-i")  # In-place formatting

    cmd.append(file_path)

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "file": file_path,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "success": result.returncode == 0
    }
