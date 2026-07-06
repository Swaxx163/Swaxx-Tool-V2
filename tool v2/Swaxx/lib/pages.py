"""Dashboard page definitions – loads tools from modules."""
import sys
import webbrowser
import importlib
import os

from . import constants as C
from . import tools as T
from .runner import run, run_discord, run_roblox, run_social, run_webhook, run_premium, run_nuker, run_selfbot
from .swaxx_common import console

# Determine the path to the tools folder (parent of lib)
TOOLS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")
if TOOLS_PATH not in sys.path:
    sys.path.insert(0, TOOLS_PATH)

CATEGORY_MODULES = {
    "home": "home",
    "osint": "osint",
    "attack": "attack",
    "discord": "discord",
    "social": "social",
    "roblox": "roblox",
    "ip-web": "ipweb",
    "generator": "gen",
    "monitor": "monitor",
    "utils": "utils",
}

def load_category_tools(category_key, module_name):
    try:
        mod = importlib.import_module(module_name)
        tools = getattr(mod, "TOOLS", {})
        if tools:
            return tools
        else:
            console.print(f"[yellow]Warning: No TOOLS dict in {module_name}[/yellow]")
            return {}
    except ImportError as e:
        console.print(f"[yellow]Module {module_name} not found: {e}[/yellow]")
        return {}
    except Exception as e:
        console.print(f"[red]Error loading {category_key}: {e}[/red]")
        return {}

def build_pages_data(plugin_items=None):
    pages = {
        "home": [
            ("01", "GitHub", lambda: webbrowser.open(C.GITHUB)),
            ("02", "Discord", lambda: webbrowser.open(C.DISCORD)),
            ("03", "Changelog", T.tool_changelog),
            ("04", "Credits", T.tool_credits),
            ("05", "Setup Config", lambda: __import__("lib.setup", fromlist=["x"]).run_setup_wizard(force=True)),
        ],
    }

    for cat_key, mod_name in CATEGORY_MODULES.items():
        tools = load_category_tools(cat_key, mod_name)
        if tools:
            tool_list = []
            for idx, (name, func) in enumerate(tools.items(), 1):
                tool_list.append((f"{idx:02d}", name, func))
            pages[cat_key] = tool_list
        else:
            pages[cat_key] = []

    return pages