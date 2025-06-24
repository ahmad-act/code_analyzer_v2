#CodeReview\ClarityAndMaintainability\radon_runner.py
import os
import subprocess
import json
import re
from typing import List, Dict


def run_radon_cc(file_path: str) -> List[Dict]:
    """
    Run Radon Cyclomatic Complexity (CC) analysis on a Python file and parse output.
    """
    result = subprocess.run(['radon', 'cc', '-s', '-j', file_path], capture_output=True, text=True)
    return parse_radon_cc_output(result.stdout)

def parse_radon_cc_output(output: str) -> List[Dict]:
    """
    Parses Radon's CC (Cyclomatic Complexity) JSON output.
    """
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return [{"error": "Invalid Radon CC JSON output"}]

    results = []
    for file_path, blocks in data.items():
        for block in blocks:
            results.append({
                "file": file_path,
                "type": block.get("type"),
                "name": block.get("name"),
                "line": block.get("lineno"),
                "complexity": block.get("complexity"),
                "rank": block.get("rank")
            })

    return results


def run_radon_mi(file_path: str) -> Dict:
    """
    Run Radon Maintainability Index (MI) on a Python file.
    """
    project_root = find_project_root(file_path)
    result = subprocess.run(['radon', 'mi', '-s', '-j', project_root], capture_output=True, text=True)
    return parse_radon_mi_output(result.stdout, file_path, project_root)

def parse_radon_mi_output(output: str, file_path: str, project_root: str) -> Dict:
    try:
        data = json.loads(output)

        target_abs = os.path.normcase(os.path.abspath(file_path)).replace("\\", "/").strip()

        for radon_path, values in data.items():
            radon_abs = os.path.normcase(os.path.abspath(radon_path)).replace("\\", "/").strip()
            if radon_abs == target_abs:
                if isinstance(values, dict):
                    return {
                        "file": file_path,
                        "maintainability_index": float(values.get("mi", 0)),
                        "rank": values.get("rank", "N/A")
                    }
                elif isinstance(values, list) and values:
                    match = re.search(r'([A-F])\s*\(([\d.]+)\)', values[0])
                    if match:
                        grade, score = match.groups()
                        return {
                            "file": file_path,
                            "maintainability_index": float(score),
                            "rank": grade
                        }
                else:
                    print("Values not dict or list or empty:", values)

        return {"file": file_path, "error": f"Matching path not found: {target_abs} not in {[os.path.normcase(os.path.abspath(k)).replace('\\', '/').strip() for k in data.keys()]}"}
    except Exception as e:
        return {"file": file_path, "error": f"Could not parse Radon MI output: {e}"}

def find_project_root(start_path: str) -> str:
    """
    Traverse upward to find the project root (marker file or git repo).
    """
    current = os.path.abspath(start_path)

    while current != os.path.dirname(current):
        if any(os.path.exists(os.path.join(current, marker)) for marker in ['pyproject.toml', 'setup.py', '.git']):
            return current
        current = os.path.dirname(current)

    return os.path.abspath(start_path)  # fallback: return the directory of the file