"""Main dashboard — Rich layout, live clock, sidebar scroll."""
import shutil
import time
import msvcrt
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from . import constants as C
from .config import get_settings
from .pages import build_pages_data
from .ui import make_card_cell, make_online_text, make_title_text, monitor_block
from .swaxx_common import cls, is_arrow, poll_console_key, safe_action, sort_free_first, console
from .i18n import t

class MasterRouter:
    MAX_ROWS = 4
    MAX_CAT_VISIBLE = 11

    def __init__(self):
        self.settings = get_settings()
        self.categories = [
            ("home", "HOME"),
            ("osint", "OSINT"),
            ("attack", "ATTACK"),
            ("discord", "DISCORD"),
            ("social", "SOCIAL"),
            ("roblox", "ROBLOX"),
            ("ip-web", "IP/WEB"),
            ("generator", "GEN"),
            ("monitor", "MONITOR"),
            ("utils", "UTILS"),
        ]
        self.cat_idx = 0
        self.cat_scroll = 0
        self.grid_idx = 0
        self.scroll_row = 0
        self.focus = "sidebar"
        self.running = True
        self.pages_data = build_pages_data([])

    def _cat_key(self):
        return self.categories[self.cat_idx][0]

    def _tools(self):
        return [
            (code, label, action)
            for code, label, action in self.pages_data.get(self._cat_key(), [])
        ]

    def _sync_cat_scroll(self):
        n = len(self.categories)
        max_scroll = max(0, n - self.MAX_CAT_VISIBLE)
        if self.cat_idx < self.cat_scroll:
            self.cat_scroll = self.cat_idx
        elif self.cat_idx >= self.cat_scroll + self.MAX_CAT_VISIBLE:
            self.cat_scroll = self.cat_idx - self.MAX_CAT_VISIBLE + 1
        self.cat_scroll = max(0, min(self.cat_scroll, max_scroll))

    def _sync_scroll(self):
        tools = self._tools()
        n = len(tools)
        if not n:
            self.scroll_row = 0
            return
        total_rows = (n + 1) // 2
        active_row = self.grid_idx // 2
        max_scroll = max(0, total_rows - self.MAX_ROWS)
        if active_row < self.scroll_row:
            self.scroll_row = active_row
        elif active_row >= self.scroll_row + self.MAX_ROWS:
            self.scroll_row = active_row - self.MAX_ROWS + 1
        self.scroll_row = max(0, min(self.scroll_row, max_scroll))

    def build_ui(self):
        self.settings.reload()
        s = self.settings
        tools = self._tools()
        n = len(tools)
        if n:
            self.grid_idx = max(0, min(n - 1, self.grid_idx))
        else:
            self.grid_idx = 0
        self._sync_cat_scroll()
        self._sync_scroll()

        layout = Layout()
        layout.split_column(Layout(name="header", size=4), Layout(name="main"))
        layout["main"].split_row(Layout(name="sidebar", size=30), Layout(name="body"))

        head = Table.grid(expand=True)
        head.add_column(ratio=1, justify="left")
        head.add_column(ratio=2, justify="center")
        head.add_column(ratio=1, justify="right")
        head.add_row(
            make_online_text(),
            make_title_text("SWAXX-TOOLS"),
            Text.from_markup(f"[bold {C.C_NEON}]{s.username[:16]}[/]"),
        )
        layout["header"].update(Panel(
            head, border_style=C.C_BLOOD, box=box.HEAVY_EDGE,
            subtitle=f"[ {time.strftime('%H:%M:%S')} ]"
        ))

        # Sidebar
        sidebar = Table.grid(expand=True)
        n_cat = len(self.categories)
        end_cat = min(n_cat, self.cat_scroll + self.MAX_CAT_VISIBLE)
        for i in range(self.cat_scroll, end_cat):
            _, label = self.categories[i]
            act = i == self.cat_idx
            foc = act and self.focus == "sidebar"
            if foc:
                sidebar.add_row(Text.from_markup(f"[black on {C.C_NEON} bold] » {label:<22} [/]"))
            elif act:
                sidebar.add_row(Text.from_markup(f"[{C.C_NEON} bold] █ {label:<22} [/]"))
            else:
                sidebar.add_row(Text.from_markup(f"[{C.C_DIM}] │ {label:<22} [/]"))

        cat_label = self.categories[self.cat_idx][1]
        layout["sidebar"].update(Panel(
            Group(sidebar, monitor_block(cat_label, n, s.username)),
            title=f"[bold white]{t('CATEGORIES', 'CATEGORIES')}[/]",
            border_style=C.C_MID,
            box=box.SQUARE,
            padding=(1, 2),
        ))

        # Grid
        start = self.scroll_row * 2
        end = min(n, start + self.MAX_ROWS * 2)
        visible = tools[start:end]
        grid = Table.grid(expand=True, padding=(1, 1))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)
        for i in range(0, len(visible), 2):
            L = visible[i]
            right = visible[i+1] if i+1 < len(visible) else None
            abs_l, abs_r = start + i, start + i + 1
            sel = self.focus == "grid"
            grid.add_row(
                make_card_cell(L[0], L[1], sel and self.grid_idx == abs_l),
                make_card_cell(right[0], right[1], sel and self.grid_idx == abs_r) if right else Text(""),
            )

        layout["body"].update(Panel(
            grid,
            title=f"[bold white]{cat_label}",
            border_style=C.C_BLOOD,
            box=box.DOUBLE,
            padding=(1, 2),
        ))
        return layout

    def _on_key(self, k):
        tools = self._tools()
        n = len(tools)
        if k == b"H":
            if self.focus == "sidebar":
                self.cat_idx = (self.cat_idx - 1) % len(self.categories)
                self.grid_idx = 0
            else:
                self.grid_idx = max(0, self.grid_idx - 2)
        elif k == b"P":
            if self.focus == "sidebar":
                self.cat_idx = (self.cat_idx + 1) % len(self.categories)
                self.grid_idx = 0
            else:
                if self.grid_idx + 2 < n:
                    self.grid_idx += 2
                elif self.grid_idx + 1 < n:
                    self.grid_idx += 1
        elif k == b"K":
            if self.focus == "grid":
                if self.grid_idx % 2 == 0:
                    self.focus = "sidebar"
                else:
                    self.grid_idx -= 1
        elif k == b"M":
            if self.focus == "sidebar":
                self.focus = "grid"
                self.grid_idx = 0
            elif self.grid_idx % 2 == 0 and n:
                self.grid_idx = min(n - 1, self.grid_idx + 1)
        elif k == b"\r":  # Enter key
            if self.focus == "grid":
                if tools and self.grid_idx < len(tools):
                    action = tools[self.grid_idx][2]
                    label = tools[self.grid_idx][1]
                    return (action, label)   # <-- FIXED: returns (action, label)
            else:
                self.focus = "grid"
                self.grid_idx = 0
        return "redraw"

    def start(self):
        cls()
        with Live(self.build_ui(), auto_refresh=False, screen=True) as live:
            while self.running:
                live.update(self.build_ui(), refresh=True)
                if msvcrt.kbhit():
                    k = poll_console_key()
                    if k is None:
                        continue
                    if k == b"\x03":
                        break
                    res = self._on_key(k)
                    if isinstance(res, tuple):
                        live.stop()
                        cls()
                        # res = (action, label)
                        action, label = res
                        console.print(f"[bold {C.C_NEON}]── Running: {label} ──[/]")
                        safe_action(label, action)   # <-- CORRECT order
                        cls()
                        live.start()
                    time.sleep(0.1)
                else:
                    time.sleep(0.05)