import subprocess
import json
from typing import Dict, List

def run_bandit(target_path: str) -> List[Dict]:
    """
    Run Bandit security analysis on the target_path (file or directory).
    Returns a list of issue dictionaries parsed from Bandit's JSON output.
    """
    # Run bandit with JSON output format
    result = subprocess.run(
        ['bandit', '-r', target_path, '-f', 'json'],
        capture_output=True,
        text=True
    )

    try:
        bandit_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        # If output is not JSON, return raw output as error info
        return [{"error": "Failed to parse Bandit JSON output", "output": result.stdout}]

    issues = []

    # Bandit JSON output has 'results' key with list of issues
    for issue in bandit_json.get('results', []):
        issues.append({
            "file": issue.get('filename'),
            "line": issue.get('line_number'),
            "issue_severity": issue.get('issue_severity'),
            "issue_confidence": issue.get('issue_confidence'),
            "issue_text": issue.get('issue_text'),
            "test_name": issue.get('test_name'),
            "test_id": issue.get('test_id')
        })

    return issues
