#CodeReview\pylint_runner.py
import subprocess
import re
from typing import Dict, List
   
def run_pylint(file_path):
    """Run Pylint analysis on a Python file and parse the output."""
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    return parse_pylint_output(result.stdout)

def parse_pylint_output(output: str) -> List[Dict]:
    """Parses Pylint output and returns a list of issue dictionaries."""
    pattern = re.compile(
        r'^(.*?):(\d+):(\d+):\s([A-Z]\d{4}):\s(.*)\s\((.*?)\)$',
        re.MULTILINE
    )

    issues = []

    for match in pattern.finditer(output):
        file_path, line, column, msg_id, message, symbolic_name = match.groups()
        issues.append({
            "file": file_path.strip(),
            "line": int(line),
            "column": int(column),
            "message_id": msg_id,
            "symbol": symbolic_name,
            "message": message.strip()
        })

    # Optionally extract final rating
    rating_match = re.search(r"Your code has been rated at ([\d\.]+)/10", output)
    if rating_match:
        issues.append({
            "summary": {
                "rating": float(rating_match.group(1))
            }
        })

    return issues