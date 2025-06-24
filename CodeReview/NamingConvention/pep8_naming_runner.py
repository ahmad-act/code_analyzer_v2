import subprocess
import re
from typing import Dict, List

def run_pep8_naming(file_path: str) -> List[Dict]:
    """Run flake8 with pep8-naming plugin and parse the output."""
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    return parse_pep8_naming_output(result.stdout)

def parse_pep8_naming_output(output: str) -> List[Dict]:
    """
    Parses flake8/pep8-naming output and returns a list of issue dictionaries.
    Expected format: filename:line:col: CODE message
    Only includes issues starting with N (pep8-naming)
    """
    pattern = re.compile(r'^(.*?):(\d+):(\d+):\s(N\d+)\s+(.*)$')
    issues = []

    for line in output.strip().splitlines():
        match = pattern.match(line)
        if match:
            file_path, line_num, col_num, code, message = match.groups()
            issues.append({
                "file": file_path.strip(),
                "line": int(line_num),
                "column": int(col_num),
                "code": code.strip(),
                "message": message.strip()
            })

    return issues
