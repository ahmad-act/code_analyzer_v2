# CodeReview/Performance/scalene_runner.py

import subprocess
import tempfile
import os
import json
from typing import Dict, Any


def run_scalene(file_path: str) -> Dict[str, Any]:
    """
    Runs Scalene profiler on a given Python file and returns parsed results.

    Args:
        file_path (str): Path to the Python file to profile.

    Returns:
        Dict: A dictionary with profiling results.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, "scalene_output.json")

        try:
            subprocess.run(
                [
                    "scalene",
                    "--json",
                    "--outfile", output_file,
                    file_path
                ],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            return {"error": f"Scalene failed: {e.stderr.strip()}"}

        try:
            with open(output_file, "r", encoding="utf-8") as f:
                result = json.load(f)
        except Exception as e:
            return {"error": f"Could not read Scalene output: {e}"}

        return result
