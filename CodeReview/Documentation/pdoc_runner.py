# CodeReview/Documentation/pdoc_runner.py

import subprocess
from typing import Dict, Optional

def run_pdoc(module_or_package: str, output_dir: Optional[str] = None) -> Dict:
    """
    Generate documentation for a Python module or package using pdoc.

    Args:
        module_or_package (str): The name or path of the module/package to document.
        output_dir (Optional[str]): Directory to save HTML docs. If None, generates in current dir.

    Returns:
        dict: Contains status, output, and any errors.
    """
    cmd = ['pdoc', module_or_package]

    if output_dir:
        cmd.extend(['--output-dir', output_dir])
        cmd.append('--force')  # overwrite existing docs

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "module": module_or_package,
        "output_dir": output_dir,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode,
        "success": result.returncode == 0
    }
