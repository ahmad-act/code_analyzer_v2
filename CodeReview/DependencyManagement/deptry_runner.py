# CodeReview\DependencyManagement\deptry_runner.py

import subprocess
import json
import tempfile
import os
from typing import List, Dict, Union


def run_deptry(path: str) -> Union[List[Dict], Dict]:
    """
    Run deptry on a Python project directory to find dependency issues.

    Args:
        path (str): Path to the root of the Python project.

    Returns:
        list or dict: List of issue dictionaries if found, or dict with error info.
    """
    tmp_path = None

    try:
        # Create a temporary file to capture JSON output
        with tempfile.NamedTemporaryFile(mode='r+', delete=False, suffix='.json') as tmp_file:
            tmp_path = tmp_file.name

        # Run deptry and output JSON to the temp file
        result = subprocess.run(
            ['deptry', path, '--json-output', tmp_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # If deptry failed, but JSON file exists and is not empty, try to parse it
            if tmp_path and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                try:
                    with open(tmp_path, 'r', encoding='utf-8') as f:
                        issues = json.load(f)
                    return parse_deptry_errors(issues)
                except json.JSONDecodeError:
                    # JSON file is corrupted or incomplete, fall back to error message
                    pass

            # Return stderr message as error info (not JSON)
            return {
                "error": "deptry failed",
                "message": parse_traceback_message(result.stderr.strip()) or "Unknown error"
            }

        # On success, read JSON output from file and parse it
        with open(tmp_path, 'r', encoding='utf-8') as f:
            issues = json.load(f)

        return parse_deptry_errors(issues)

    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }
    finally:
        # Clean up temp file if it exists
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def parse_deptry_errors(data: dict) -> list:
    parsed = []
    for file_path, tool_data in data.items():
        deptry_data = tool_data.get("deptry", {})
        error = deptry_data.get("error", "Unknown")
        raw_message = deptry_data.get("message", "")

        # Default to full message if no parsing done
        parsed_message = raw_message

        # Check for the specific error type in the traceback
        if "DependencySpecificationNotFoundError" in raw_message:
            # Split traceback by lines and strip whitespace
            lines = [line.strip() for line in raw_message.splitlines() if line.strip()]
            # The error message we want is usually the last line starting with "deptry.exceptions.DependencySpecificationNotFoundError"
            # or the actual descriptive message right after that line.
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i]
                if "No file called" in line:
                    parsed_message = line
                    break
                if line.startswith("deptry.exceptions.DependencySpecificationNotFoundError"):
                    # Sometimes the message is in this line after colon
                    parts = line.split(":", 1)
                    if len(parts) == 2 and parts[1].strip():
                        parsed_message = parts[1].strip()
                        break

        parsed.append({
            "file": file_path,
            "error": error,
            "message": parsed_message,
            "missing_dependency_file": "DependencySpecificationNotFoundError" in raw_message
        })

    return parsed



def parse_traceback_message(traceback_str: str) -> Dict:
    """
    Parses a Python traceback string to extract structured error info.

    Args:
        traceback_str (str): Full traceback string.

    Returns:
        dict: Parsed information including error_type, message, and full traceback.
    """
    lines = [line.strip() for line in traceback_str.strip().splitlines() if line.strip()]

    parsed = {
        "error_type": "Unknown",
        "message": "Unknown error",
        "traceback": traceback_str
    }

    # Try to find the last line that has the actual exception
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if line.startswith("deptry.exceptions.") and ":" in line:
            # Example:
            # deptry.exceptions.DependencySpecificationNotFoundError: No file called ...
            parts = line.split(":", 1)
            if len(parts) == 2:
                parsed["error_type"] = parts[0].split('.')[-1].strip()
                parsed["message"] = parts[1].strip()
            break

    return parsed

from typing import Dict


def parse_traceback(traceback_str: str) -> Dict:
    """
    Parses a Python traceback string and extracts structured error info.

    Args:
        traceback_str (str): Full traceback string.

    Returns:
        dict: Parsed error info with keys:
            - error_type
            - message
            - traceback
    """
    result = {
        "error_type": "Unknown",
        "message": "Unknown error",
        "traceback": traceback_str.strip()
    }

    lines = traceback_str.strip().splitlines()
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        # Look for the exception with message
        if line.startswith("deptry.exceptions.") and ":" in line:
            try:
                exception_class, message = line.split(":", 1)
                result["error_type"] = exception_class.split('.')[-1].strip()
                result["message"] = message.strip()
                break
            except ValueError:
                continue  # Malformed line, skip

    return result
