# CodeReview/Performance/line_profiler_runner.py

from line_profiler import LineProfiler
import importlib.util
import os
import sys
import ast
from typing import List, Dict, Tuple


def extract_function_names(file_path: str) -> List[str]:
    """
    Extracts top-level function names from a Python file using AST.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def run_line_profiler(file_path: str, function_names: List[str] = None, test_args: Dict[str, Tuple] = None) -> List[Dict]:
    """
    Profiles specific functions in a Python file using line_profiler.

    Args:
        file_path (str): Path to the Python file.
        function_names (List[str], optional): Function names to profile.
        test_args (Dict[str, Tuple], optional): Arguments to pass per function.

    Returns:
        List[Dict]: Profiling data or error message.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_dir = os.path.dirname(os.path.abspath(file_path))

    # Add module path to sys.path
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if not spec or not spec.loader:
        return [{"error": f"Could not import file: {file_path}"}]

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return [{"error": f"Execution failed: {e}"}]

    if function_names is None:
        function_names = extract_function_names(file_path)
        if not function_names:
            return [{"error": f"No functions found in {file_path} to profile."}]

    test_args = test_args or {}
    profiler = LineProfiler()

    for func_name in function_names:
        func = getattr(module, func_name, None)
        if callable(func):
            profiler.add_function(func)
        else:
            return [{"error": f"Function '{func_name}' not found in {file_path}"}]

    # Run profiler
    try:
        for func_name in function_names:
            func = getattr(module, func_name)
            args = test_args.get(func_name, ())
            profiler(func)(*args)
    except Exception as e:
        return [{"error": f"Function '{func_name}' execution failed: {e}"}]

    # Capture results
    output = []
    stats = profiler.get_stats()
    for func in stats.timings:
        filename, lineno, name = func
        timings = stats.timings[func]
        for line_no, time, hits in timings:
            output.append({
                "file": filename,
                "function": name,
                "line": line_no,
                "hits": hits,
                "time_microseconds": time
            })

    return output
