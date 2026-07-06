"""Dashboard UI — panels, theme colors."""
import math
import time
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich import box
from . import constants as C
from .swaxx_common import fmt_label, is_premium

def _phase():
    return (time.time() * 0.25) % 1.0

def _lerp_hex(c1, c2, t):
    t = max(0.0, min(1.0, t))
    r1,g1,b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2,g2,b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    r = int(r1 + (r2-r1)*t)
    g = int(g1 + (g2-g1)*t)
    b = int(b1 + (b2-b1)*t)
    return f"#{r:02x}{g:02x}{b:02x}"

def _breath(t=None):
    t = t or time.time()
    return (math.sin(t * 2.4) + 1.0) / 2.0

def make_online_text():
    br = _breath()
    pal = C.palette()
    color = _lerp_hex(C.C_DIM, pal["neon"], 0.05 + 0.95*br)
    dot = "●" if br >= 0.5 else "○"
    txt = Text()
    txt.append(f"{dot} ", style=color)
    txt.append("ONLINE", style=color)
    return txt

def make_title_text(text="SWAXX-TOOLS"):
    pal = C.palette()
    txt = Text()
    for i, char in enumerate(text):
        if i % 2 == 0:
            txt.append(char, style=pal["neon"])
        else:
            txt.append(char, style=pal["bright"])
    return txt

def make_card_cell(key, label, is_selected):
    pal = C.palette()
    gold = C.C_GOLD
    border = pal["mid"] if not is_selected else gold
    style = pal["neon"] if is_selected else pal["bright"]
    text = fmt_label(label, max_len=26)
    inner = Text.from_markup(
        f"[{style} bold] {text} [/]" if is_selected else f"   [{style}]{text}[/]   "
    )
    return Panel(
        Align.center(inner),
        title=f"[{gold} bold]{key}[/]",
        title_align="left",
        border_style=border,
        box=box.HEAVY if is_selected else box.ROUNDED,
        padding=(1, 1),
    )

def monitor_block(cat_label, n_tools, username):
    pal = C.palette()
    return Text.from_markup(
        f"\n\n[{C.C_BLOOD}]┌─ MONITOR\n"
        f"│ [bold {pal['neon']}]{username}[/]\n"
        f"│ [{C.C_GOLD}]9[/] free · [{pal['bright']}]0[/] vip\n"
        f"│ NUKER OK/OK\n"
        f"│ [{pal['red']}]{cat_label}[/] · [{C.C_GOLD}]{n_tools}[/] tools\n"
        f"└─ [{pal['neon']}]READY[/]"
    )