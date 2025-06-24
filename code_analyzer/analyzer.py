#analyzer.py
import os
from CodeReview.CodeQuality.flake8_runner import run_flake8
from CodeReview.CodeQuality.mypy_runner import run_mypy
from CodeReview.CodeQuality.pylint_runner import run_pylint
from CodeReview.SpellingAndGrammar.pyspellchecker_runner import run_pyspellchecker
from CodeReview.NamingConvention.pep8_naming_runner import run_pep8_naming
from CodeReview.ClarityAndMaintainability.radon_runner import run_radon_cc, run_radon_mi
from CodeReview.ClarityAndMaintainability.refactor_runner import run_refactor
from CodeReview.TestingAndTestCoverage.pytest_runner import run_pytest
from CodeReview.TestingAndTestCoverage.coverage_runner import run_coverage
from CodeReview.TestingAndTestCoverage.hypothesis_runner import run_hypothesis
from CodeReview.SecurityAndSafety.bandit_runner import run_bandit
from CodeReview.DependencyManagement.pipreqs_runner import run_pipreqs
from CodeReview.DependencyManagement.pip_audit_runner import run_pip_audit
from CodeReview.DependencyManagement.deptry_runner import run_deptry
from CodeReview.PerformanceAndEfficiency.cprofile_runner import run_cprofile
from CodeReview.PerformanceAndEfficiency.line_profiler_runner import run_line_profiler
from CodeReview.PerformanceAndEfficiency.memory_profiler_runner import run_memory_profiler
from CodeReview.PerformanceAndEfficiency.scalene_runner import run_scalene
from CodeReview.FormattingAndStyle.black_runner import run_black
from CodeReview.FormattingAndStyle.isort_runner import run_isort
from CodeReview.FormattingAndStyle.autopep8_runner import run_autopep8
from CodeReview.Documentation.pdoc_runner import run_pdoc
from CodeReview.Documentation.sphinx_runner import run_sphinx
from CodeReview.Documentation.docformatter_runner import run_docformatter
from CodeReview.Documentation.darglint_runner import run_darglint

def analyze_file(file_path):
    """Run all tools on one Python file and return results."""
    results = {
        # CodeQuality/Static Analysis
        'pylint': run_pylint(file_path),
        'flake8': run_flake8(file_path),
        'mypy': run_mypy(file_path),

        # SpellingAndGrammar
        'pyspellchecker': run_pyspellchecker(file_path),

        # NamingConvention
        'pep8_naming': run_pep8_naming(file_path),

        # ClarityAndMaintainability
        'radon-cc': run_radon_cc(file_path),
        'radon-mi': run_radon_mi(file_path),
        'refactor': run_refactor(file_path),

        # TestingAndTestCoverage
        'pytest': run_pytest(file_path),
        'coverage': run_coverage(file_path),
        'hypothesis': run_hypothesis(file_path),

        # SecurityAndSafety
        'bandit': run_bandit(file_path),

        # DependencyManagement
        'pipreqs': run_pipreqs(file_path),
        'pip-audit': run_pip_audit(file_path),
        'deptry': run_deptry(file_path),

        # PerformanceAndEfficiency
        'cprofile': run_cprofile(file_path),
        'line_profiler': run_line_profiler(file_path),
        'memory_profiler': run_memory_profiler(file_path),
        'scalene': run_scalene(file_path),

        # FormattingAndStyle
        'black': run_black(file_path),
        'isort': run_isort(file_path),
        'autopep8': run_autopep8(file_path),

        # Documentation
        'sphinx': run_sphinx(file_path),
        'docformatter': run_docformatter(file_path),
        'darglint': run_darglint(file_path),
        'pdoc': run_pdoc(file_path),
    }
    return results

def analyze_project(path):
    """
    Analyze all Python files in `path`.

    Args:
        path (str): Root folder of the Python project.

    Returns:
        dict: Report with per-file results.
    """
    report = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, path)
                try:
                    report[rel_path] = analyze_file(full_path)
                except Exception as e:
                    report[rel_path] = {'error': str(e)}
    return report
