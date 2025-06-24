#CodeReview\mypy_runner.py
import subprocess
import re
from typing import List, Dict

def run_mypy(file_path):
    """Run mypy type checker on a Python file."""
    result = subprocess.run(['mypy', file_path], capture_output=True, text=True)
    return parse_mypy_output(result.stdout)

def parse_mypy_output(output: str) -> List[Dict]:
    """
    Parses the mypy output into a structured list of dictionaries.
    
    Expected format:
    path/to/file.py:line: type: message  [optional-code]
    """
    pattern = re.compile(
        r'^(.*?):(\d+): (error|note): (.*?)(?:\s\s\[(.*?)\])?$'
    )

    issues = []
    for line in output.strip().splitlines():
        match = pattern.match(line)
        if match:
            file_path, line_num, msg_type, message, code = match.groups()
            issue = {
                "file": file_path.strip(),
                "line": int(line_num),
                "type": msg_type,
                "message": message.strip()
            }
            if code:
                issue["code"] = code.strip()
            issues.append(issue)

    return issues
