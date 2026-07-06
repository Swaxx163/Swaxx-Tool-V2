"""Swaxx-Tools — settings.json load/save."""
import json
import os
from . import constants as C

DEFAULTS = {
    "language": "en",
    "theme": "cyan",
    "username": "Operator",
    "skip_boot": False,
    "setup_complete": False,
    "last_setup_config_rev": "0",
    "last_seen_config_rev": "0",
    "last_seen_discord_invite": "",
    "last_seen_community_key": "",
    "last_remote_sync": 0,
}

class Settings:
    def __init__(self):
        self.data = dict(DEFAULTS)
        self.load()

    def load(self):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        if os.path.isfile(C.SETTINGS_PATH):
            try:
                with open(C.SETTINGS_PATH, encoding="utf-8") as f:
                    merged = {**DEFAULTS, **json.load(f)}
                self.data = merged
            except Exception:
                # If JSON is corrupt, reset to defaults
                self.data = dict(DEFAULTS)
                self.save()
        else:
            # First run – create default settings
            self.data = dict(DEFAULTS)
            self.save()
        C.apply_theme(self.data.get("theme", "cyan"))

    def reload(self):
        self.load()

    def save(self):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.data.get(key, default if default is not None else DEFAULTS.get(key))

    def set(self, key, value):
        self.data[key] = value
        if key == "theme":
            C.apply_theme(value)
        self.save()  # save immediately

    @property
    def lang(self):
        raw = str(self.data.get("language") or "en").strip().lower()
        return raw if raw in ("sv", "en") else "en"

    @property
    def username(self):
        return self.data.get("username", "Operator")

_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def nuker_status():
    return (False, False)  # simplified
 
DEFAULTS = {
    "language": "en",
    "theme": "cyan",
    "username": "Operator",
    "discord_id": "",
    "skip_boot": False,
    "setup_complete": False,
    "last_setup_config_rev": "0",
    "last_seen_config_rev": "0",
    "last_seen_discord_invite": "",
    "last_seen_community_key": "",
    "last_remote_sync": 0,
}