"""Remote sync – stub for compatibility."""
import os
import json
import time
from . import constants as C
from .config import get_settings
from .swaxx_common import cls, console

def sync(force=False):
    return True, "local"

def get_manifest():
    return {"config_rev": "0", "latest_version": C.VERSION}

def config_rev():
    return "0"

def has_pending_update():
    return False

def mark_seen():
    pass

def show_discord_join_gate():
    pass

def show_announcement_block():
    pass

def status_badge():
    return ""