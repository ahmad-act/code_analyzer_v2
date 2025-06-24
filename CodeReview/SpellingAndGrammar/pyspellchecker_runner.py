# CodeReview/SpellingAndGrammar/pyspellchecker_runner.py
from spellchecker import SpellChecker
import re
from typing import List, Dict

def run_pyspellchecker(file_path: str) -> List[Dict]:
    """
    Spellcheck the content of a Python file using pyspellchecker.
    Distinguishes between code strings and comments.
    """
    spell = SpellChecker()
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [{"error": f"Could not read file: {e}"}]

    for line_num, line in enumerate(lines, 1):
        # --- Check comments ---
        comment_match = re.search(r'#(.*)', line)
        if comment_match:
            comment_text = comment_match.group(1)
            words = re.findall(r'\b[a-zA-Z]+\b', comment_text)
            misspelled = spell.unknown(words)
            for word in misspelled:
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "word": word,
                    "suggestion": spell.correction(word),
                    "source": "comment"
                })

        # --- Check string literals ---
        # Capture single, double, triple-quoted strings (non-docstring context)
        string_matches = re.findall(
            r'(?:\"\"\"(.*?)\"\"\"|\'\'\'(.*?)\'\'\'|\"(.*?)\"|\'(.*?)\')',
            line,
            re.DOTALL
        )
        for match_group in string_matches:
            string_text = " ".join(filter(None, match_group))
            words = re.findall(r'\b[a-zA-Z]+\b', string_text)
            misspelled = spell.unknown(words)
            for word in misspelled:
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "word": word,
                    "suggestion": spell.correction(word),
                    "source": "code"
                })

    return issues
