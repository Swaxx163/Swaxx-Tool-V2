"""Built-in dashboard tools."""
import os, sys, time, json, random, string, webbrowser
from . import constants as C
from .swaxx_common import console, panel, pause, error_box, success_box, ansi_hex
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.padding import Padding
from rich import box

def tool_changelog():
    panel("CHANGELOG", f"Swaxx-Tools v{C.VERSION}")
    console.print(Panel(C.CHANGELOG, border_style=C.C_GOLD, padding=(1,2)))
    pause()

def tool_credits():
    panel("CREDITS", f"Swaxx-Tools · by {C.AUTHOR}")
    console.print(Panel(
        Text.from_markup(
            f"[{C.C_GOLD} bold]SWAXX-TOOLS v{C.VERSION}[/]\n\n"
            f"[{C.C_WHITE}]Developer  : [bold]{C.AUTHOR}[/]\n"
            f"[{C.C_SILVER}]Discord    : {C.DISCORD}\n"
            f"[{C.C_SILVER}]GitHub     : {C.GITHUB}[/]"
        ), border_style=C.C_BLOOD, padding=(1,3)))
    pause()