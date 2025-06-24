import subprocess
from typing import Dict

def run_pipreqs(path: str, savepath: str = None) -> Dict:
    """
    Run pipreqs on a directory to generate requirements.txt.

    Args:
        path (str): The directory path to analyze.
        savepath (str, optional): The path to save the requirements file.
                                  Defaults to None (pipreqs default: requirements.txt in path).

    Returns:
        dict: Result containing success status and output message.
    """
    cmd = ['pipreqs', path]
    if savepath:
        cmd += ['--savepath', savepath]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return {
            "success": True,
            "message": result.stdout.strip()
        }
    else:
        return {
            "success": False,
            "error": result.stderr.strip()
        }
