import subprocess
import json
from typing import List, Dict, Union

def run_pip_audit(_: str = "") -> Union[List[Dict], Dict]:
    """
    Run pip-audit to check installed packages for vulnerabilities.

    Args:
        _ (str): Optional file path (ignored). Present to match the per-file analysis function signature.

    Returns:
        list or dict: List of vulnerability dicts if found, or dict with error info.
    """
    try:
        result = subprocess.run(
            ['pip-audit', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        vulnerabilities = json.loads(result.stdout)
        return vulnerabilities

    except subprocess.CalledProcessError as e:
        return {
            "error": "pip-audit failed",
            "message": e.stderr.strip()
        }
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse pip-audit JSON output",
            "output": result.stdout.strip()
        }