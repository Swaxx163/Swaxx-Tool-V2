"""First-run setup wizard — asks for language, theme, username."""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
from rich import box
import msvcrt
import time

from . import constants as C
from .config import get_settings
from .swaxx_common import cls, console

def setup_required(force=False):
    s = get_settings()
    if force:
        return True
    return not s.get("setup_complete", False)

def run_setup_wizard(force=False):
    s = get_settings()
    if not setup_required(force):
        return

    cls()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[bold {C.C_GOLD}]SWAXX-TOOLS — SETUP WIZARD[/]\n"
            f"[dim]Configure your profile[/]"
        )),
        border_style=C.C_BLOOD,
        box=box.DOUBLE_EDGE,
        padding=(1, 3),
    ))
    console.print()

    # Language (English or Swedish)
    lang = Prompt.ask(
        "[bold cyan]Language / Språk[/bold cyan]",
        choices=["en", "sv"],
        default="en"
    )
    s.set("language", lang)

    # Theme
    theme_options = list(C.THEMES.keys()) + ["rainbow"]
    theme = Prompt.ask(
        "[bold cyan]Theme[/bold cyan]",
        choices=theme_options,
        default="cyan"
    )
    s.set("theme", theme)

    # Username
    username = Prompt.ask("[bold cyan]Username[/bold cyan]", default="Operator")
    s.set("username", username)

    # Skip boot animation
    skip_boot = Prompt.ask(
        "[bold cyan]Skip boot animation?[/bold cyan]",
        choices=["yes", "no"],
        default="no"
    ) == "yes"
    s.set("skip_boot", skip_boot)

    # Mark setup as complete
    s.set("setup_complete", True)
    s.set("last_setup_config_rev", "0")
    s.save()

    cls()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[bold {C.C_NEON}]✅ Setup complete![/]\n"
            f"[dim]Welcome, [bold]{username}[/bold][/]"
        )),
        border_style=C.C_GOLD,
        box=box.HEAVY,
        padding=(1, 3),
    ))
    time.sleep(1.5)