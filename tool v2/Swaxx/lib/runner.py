"""Unified tool runner."""
import os
import subprocess
import sys
from . import constants as C
from .config import get_settings
from .swaxx_common import cls, console, error_box, pause, success_box

def run_script(fr_path, en_path, tool_name=None, extra_args=None):
    # simplified: just run the script with python
    src = fr_path if os.path.exists(fr_path) else en_path
    if not os.path.exists(src):
        error_box("Script missing", os.path.basename(src))
        pause()
        return
    try:
        subprocess.run([sys.executable, src] + (extra_args or []), shell=False)
    except Exception as e:
        error_box("Error", tool_name or "tool", str(e))
    pause()

def run(folder, fr_name="fr.py", en_name="en.py", tool_name=None):
    run_script(C.sp(folder, fr_name), C.sp(folder, en_name), tool_name)

def run_discord(tool_key):
    run_script(C.sp_discord("fr.py"), C.sp_discord("en.py"), tool_key)

def run_roblox(tool_key):
    run_script(C.sp_roblox("fr.py"), C.sp_roblox("en.py"), tool_key)

def run_social(tool_key):
    run_script(C.sp_social("fr.py"), C.sp_social("en.py"), tool_key)

def run_webhook(tool_key):
    run_script(C.sp_webhook("fr.py"), C.sp_webhook("en.py"), tool_key)

def run_premium(name):
    run("premium-tools", "fr.py", "en.py", name)

def run_nuker(action=None):
    error_box("NUKER", "Not implemented", "Void-Nuke not included.")
    pause()

def run_selfbot():
    error_box("SELFBOT", "Not implemented", "Selfbot not included.")
    pause()

def run_plugin(plugin_path):
    try:
        subprocess.run([sys.executable, plugin_path], shell=False)
    except Exception as e:
        error_box("Plugin", os.path.basename(plugin_path), str(e))
    pause()