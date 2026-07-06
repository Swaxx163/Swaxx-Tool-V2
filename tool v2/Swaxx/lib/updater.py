"""Updater – stub for compatibility."""
from . import constants as C

def handle_update_gate():
    return False

def version_update_available():
    return False

def version_prompt_was_shown():
    return False

def check_auto_update():
    return False

def check_for_updates(manual=False):
    return False