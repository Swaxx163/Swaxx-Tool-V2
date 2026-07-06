"""Swaxx-Tools — shared UI helpers."""
import os
import re
import shutil
import subprocess
import sys
import time
import msvcrt
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from . import constants as C
from .config import get_settings

console = Console(highlight=False)

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def tw():
    return shutil.get_terminal_size((100, 30)).columns

def th():
    return shutil.get_terminal_size((100, 30)).lines

def ansi_hex(h):
    hx = h.lstrip("#")
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"

def poll_console_key():
    if not msvcrt.kbhit():
        return None
    k = msvcrt.getch()
    if k in (b"\x00", b"\xe0"):
        k2 = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()
        return k2
    return k

def read_console_key():
    while True:
        k = poll_console_key()
        if k is not None:
            return k
        time.sleep(0.01)

def is_arrow(k):
    return k in (b"H", b"P", b"K", b"M")

def pause(msg=None):
    console.print()
    if msg is None:
        msg = "\033[38;2;120;0;0m  ► Press Enter to continue…\033[0m"
    input(msg)

def fmt_label(label: str, max_len: int = 24) -> str:
    clean = re.sub(r"\s*\[(PREMIUM|STAR)\]", "", label, flags=re.I).strip()
    if len(clean) > max_len:
        clean = clean[: max_len - 1] + "…"
    return clean

def is_premium(label: str) -> bool:
    return "[PREMIUM]" in str(label).upper()

def sort_free_first(items):
    if not items:
        return items
    free = [i for i in items if not is_premium(i[1])]
    prem = [i for i in items if is_premium(i[1])]
    out, n = [], 1
    for _, label, action in free + prem:
        out.append((f"{n:02d}", label, action))
        n += 1
    return out

def count_free_premium(items):
    free = sum(1 for _, label, _ in items if not is_premium(label))
    prem = len(items) - free
    return free, prem

def panel(title, desc):
    console.print()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[{C.C_GOLD} bold]◆ {title}[/]\n[{C.C_DIM}]{desc}[/]"
        )),
        border_style=C.C_BLOOD, box=box.DOUBLE_EDGE, padding=(1, 3),
        width=min(64, tw() - 2),
    ))
    console.print()

def error_box(title: str, message: str, detail: str = None):
    body = Text.from_markup(f"[{C.C_NEON} bold]{message}[/]")
    if detail:
        body.append("\n")
        body.append(Text.from_markup(f"[{C.C_DIM}]{detail}[/]"))
    console.print(Panel(body, title=f"[bold white]✖ {title}[/]", border_style=C.C_NEON, box=box.HEAVY, padding=(1, 2)))

def success_box(title: str, message: str):
    console.print(Panel(
        Text.from_markup(f"[#88FFAA bold]{message}[/]"),
        title=f"[bold white]✔ {title}[/]", border_style="#88FFAA", box=box.ROUNDED, padding=(0, 2),
    ))

def safe_action(tool_name, action):
    """Execute a tool function with full error handling."""
    try:
        if callable(action):
            action()
        else:
            console.print(f"[red]Tool '{tool_name}' is not callable.[/red]")
    except KeyboardInterrupt:
        console.print(f"\n[{C.C_DIM}]  ○ {tool_name} — cancelled[/]")
        time.sleep(0.6)
    except Exception as e:
        error_box("Error", tool_name, f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(2)