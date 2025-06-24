# CodeReview/Performance/memory_profiler_runner.py

from memory_profiler import memory_usage
import importlib.util
import os
import sys
import ast
from typing import Dict, List, Any, Optional


def extract_function_names(file_path: str) -> List[str]:
    """
    Extracts top-level function names using AST.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def run_memory_profiler(file_path: str, function_name: Optional[str] = None, test_args: Optional[tuple] = ()) -> List[Dict[str, Any]]:
    """
    Profiles memory usage of a specific function using memory_profiler.

    Args:
        file_path (str): Path to the Python file.
        function_name (str, optional): Function to profile. If not provided, auto-detects.
        test_args (tuple, optional): Arguments to pass into the function.

    Returns:
        List[Dict]: Memory usage information or error.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_dir = os.path.dirname(os.path.abspath(file_path))

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
        return [{"error": f"Failed to execute module: {e}"}]

    if function_name is None:
        functions = extract_function_names(file_path)
        if not functions:
            return [{"error": f"No functions found in {file_path}"}]
        function_name = functions[0]  # Pick the first one

    target_func = getattr(module, function_name, None)

    if not callable(target_func):
        return [{"error": f"Function '{function_name}' not found or not callable in {file_path}"}]

    try:
        mem_values = memory_usage((target_func, test_args, {}), interval=0.1, retval=False)
        return [{
            "function": function_name,
            "file": file_path,
            "peak_memory_MB": max(mem_values),
            "min_memory_MB": min(mem_values),
            "memory_samples": mem_values
        }]
    except Exception as e:
        return [{"error": f"Failed during memory profiling: {e}"}]
