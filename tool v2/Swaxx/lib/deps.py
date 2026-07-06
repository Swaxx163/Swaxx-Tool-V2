"""Check and optionally install dependencies."""
import importlib
import subprocess
import sys

REQUIRED = [
    ("rich", "rich"),
    ("pynput", "pynput"),
    ("colorama", "colorama"),
]

def check_deps(auto_install=True):
    missing = []
    for mod, pkg in REQUIRED:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(pkg)
    if missing and auto_install:
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=False)
    return len(missing) == 0