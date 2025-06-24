import subprocess
from typing import Dict

def run_sphinx(source_dir: str, build_dir: str = "docs/build", builder: str = "html") -> Dict:
    """
    Run Sphinx to build documentation.

    Args:
        source_dir (str): Path to Sphinx source directory (where conf.py is).
        build_dir (str): Path to output directory for built docs.
        builder (str): The type of builder to use (default: 'html').

    Returns:
        dict: Contains success flag, return code, stdout, stderr.
    """
    cmd = [
        "sphinx-build",
        "-b", builder,
        source_dir,
        build_dir
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "source_dir": source_dir,
        "build_dir": build_dir,
        "builder": builder,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "success": result.returncode == 0
    }
