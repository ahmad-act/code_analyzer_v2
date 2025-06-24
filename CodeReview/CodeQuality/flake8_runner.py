#CodeReview\flake8_runner.py
import subprocess
import re
from typing import List, Dict

def run_flake8(file_path):
    """Run flake8 on a Python file and parse the output."""
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    return parse_flake8_output(result.stdout)

def parse_flake8_output(output: str) -> List[Dict]:
    """
    Parses the flake8 output into a structured list of dictionaries.
    
    Example flake8 output line:
    path/to/file.py:3:1: E302 expected 2 blank lines, found 1
    """
    pattern = re.compile(r'^(.*?):(\d+):(\d+):\s([A-Z]\d{3})\s(.*)$')
    issues = []

    for line in output.strip().splitlines():
        match = pattern.match(line)
        if match:
            file_path, line_num, column_num, code, message = match.groups()
            issues.append({
                "file": file_path.strip(),
                "line": int(line_num),
                "column": int(column_num),
                "code": code,
                "message": message.strip()
            })

    return issues
