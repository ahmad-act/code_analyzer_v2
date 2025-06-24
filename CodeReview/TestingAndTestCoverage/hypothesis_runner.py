import subprocess
import re
from typing import Dict, List

def run_hypothesis(test_path: str) -> Dict:
    """
    Run pytest on test_path (with Hypothesis tests inside) and parse the output.
    Returns test summary info and any hypothesis failure details.
    """
    # Run pytest with verbose output and capture
    result = subprocess.run(
        ['pytest', '-v', test_path],
        capture_output=True,
        text=True
    )

    # Parse pytest summary (passed, failed, errors)
    summary = parse_pytest_summary(result.stdout)

    # Extract Hypothesis failure details if any
    hypothesis_failures = parse_hypothesis_failures(result.stdout)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "summary": summary,
        "hypothesis_failures": hypothesis_failures
    }


def parse_pytest_summary(output: str) -> Dict[str, int]:
    """
    Parse pytest test session summary line for passed, failed, skipped counts.
    Example line: '== 3 passed, 1 failed, 2 skipped in 0.12s =='
    """
    summary = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}
    match = re.search(r"==+ (.+) in [\d\.]+s ==+", output)
    if match:
        parts = match.group(1).split(',')
        for part in parts:
            part = part.strip()
            if 'passed' in part:
                summary['passed'] = int(re.search(r'(\d+)', part).group(1))
            elif 'failed' in part:
                summary['failed'] = int(re.search(r'(\d+)', part).group(1))
            elif 'skipped' in part:
                summary['skipped'] = int(re.search(r'(\d+)', part).group(1))
            elif 'error' in part or 'errors' in part:
                summary['errors'] = int(re.search(r'(\d+)', part).group(1))
    return summary


def parse_hypothesis_failures(output: str) -> List[Dict]:
    """
    Extract details about Hypothesis failures from pytest output.
    Hypothesis failures usually include phrases like 'Falsifying example' or 'hypothesis.errors'.
    """
    failures = []
    # Hypothesis prints "Falsifying example: ..."
    pattern = re.compile(r'Falsifying example:\n(.+?)(?:\n\n|\Z)', re.DOTALL)

    for match in pattern.finditer(output):
        example_text = match.group(1).strip()
        failures.append({"falsifying_example": example_text})

    return failures
