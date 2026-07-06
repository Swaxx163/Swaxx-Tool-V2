"""Swaxx-Tools — constants, paths, theme palette."""
import colorsys
import os

REMOTE_MANIFEST_URL = (
    "https://raw.githubusercontent.com/swaxx163/Swaxx-Tools/main/Swaxx/config/remote-manifest.json"
)

VERSION = "1.0.0"
GITHUB = "https://github.com/yourusername/swaxx163"
AUTHOR = "swaxx"
DISCORD = "https://discord.com/users/1323093967914405939"
TELEGRAM = "https://t.me/swaxx163"

SWAXX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(SWAXX_DIR)
CONFIG_DIR = os.path.join(SWAXX_DIR, "config")
DATA_DIR = os.path.join(SWAXX_DIR, "data")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")
NUKER_CFG_PATH = os.path.join(CONFIG_DIR, "discord-nuker.json")
CUSTOM_TOOLS_DIR = os.path.join(SWAXX_DIR, "tools", "custom")

CHANGELOG = """SWAXX-TOOLS v1.0.0
- Initial release based on swaxx-Tools.
- All tools ported and renamed.
- Keyboard-driven dashboard.
- nigger
"""

# Theme palette
THEMES = {
    "cyan": {
        "blood": "#003344", "dark": "#004455", "mid": "#006677",
        "red": "#008899", "neon": "#00DDFF", "bright": "#88EEFF",
    },
    "red": {
        "blood": "#4a0000", "dark": "#6a0000", "mid": "#990000",
        "red": "#cc0000", "neon": "#FF2020", "bright": "#FF4444",
    },
    "green": {
        "blood": "#0a3d0a", "dark": "#0d5c0d", "mid": "#118811",
        "red": "#22aa22", "neon": "#00FF88", "bright": "#88FFAA",
    },
    "blue": {
        "blood": "#0a1a4a", "dark": "#1a2a6a", "mid": "#2244aa",
        "red": "#3366cc", "neon": "#4488FF", "bright": "#88BBFF",
    },
    "purple": {
        "blood": "#2a0a4a", "dark": "#3a126a", "mid": "#551a99",
        "red": "#7733cc", "neon": "#AA44FF", "bright": "#CC88FF",
    },
    "gold": {
        "blood": "#3d2e00", "dark": "#5c4500", "mid": "#886600",
        "red": "#bb9900", "neon": "#FFCC00", "bright": "#FFE566",
    },
}

THEME_ORDER = list(THEMES.keys())
_THEME_ALIASES = {}

_ACTIVE_THEME = "cyan"

C_WHITE = "#FFFFFF"
C_SILVER = "#CCCCCC"
C_DIM = "#444444"
C_GOLD = "#FFD700"
C_GOLD2 = "#FFA500"

# These are updated by apply_theme
C_BLOOD = THEMES["cyan"]["blood"]
C_DARK = THEMES["cyan"]["dark"]
C_MID = THEMES["cyan"]["mid"]
C_RED = THEMES["cyan"]["red"]
C_NEON = THEMES["cyan"]["neon"]
C_BRIGHT = THEMES["cyan"]["bright"]

def apply_theme(name: str):
    global C_BLOOD, C_DARK, C_MID, C_RED, C_NEON, C_BRIGHT, _ACTIVE_THEME
    name = _THEME_ALIASES.get(name, name)
    if name not in THEMES:
        name = "cyan"
    _ACTIVE_THEME = name
    p = THEMES[name]
    C_BLOOD, C_DARK, C_MID = p["blood"], p["dark"], p["mid"]
    C_RED, C_NEON, C_BRIGHT = p["red"], p["neon"], p["bright"]

def active_theme():
    return _ACTIVE_THEME

def palette(phase=0.0):
    """Return current theme colors (for rainbow, you'd add later)."""
    return {
        "blood": C_BLOOD, "dark": C_DARK, "mid": C_MID,
        "red": C_RED, "neon": C_NEON, "bright": C_BRIGHT,
    }