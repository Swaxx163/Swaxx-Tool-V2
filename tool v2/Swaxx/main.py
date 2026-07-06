#!/usr/bin/env python3
"""
SWAXX-TOOLS – Entry point.
Author: swaxx
"""

import os
import sys
import time
import json
from colorama import init

init(autoreset=True)

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from lib.constants import SWAXX_DIR, CONFIG_DIR, SETTINGS_PATH
from lib.boot import boot
from lib.config import get_settings
from lib.deps import check_deps
from lib.remote import show_announcement_block, show_discord_join_gate, sync as remote_sync
from lib.updater import handle_update_gate
from lib.router import MasterRouter
from lib.setup import run_setup_wizard
from lib.swaxx_common import cls, console, error_box
from lib.auth import login_flow

if __name__ == "__main__":
    try:
        check_deps(auto_install=True)

        # --- AUTHENTICATION ---
        user = login_flow()
        if not user:
            console.print("[red]Authentication failed. Exiting.[/red]")
            sys.exit(1)
        console.print(f"[dim]Logged in as: {user['username']} (Admin: {user['is_admin']})[/dim]")
        # ----------------------

        s = get_settings()
        s.set("username", user["username"])
        s.save()

        # --- Force Discord ID ---
        discord_id = s.get("discord_id", "").strip() or user.get("discord_id", "")
        if not discord_id:
            console.print("[bold red]⚠️  Discord ID REQUIRED![/bold red]")
            discord_id = input("[bold cyan]Enter your Discord User ID: [/bold cyan]").strip()
            if not discord_id:
                console.print("[red]❌ Discord ID is mandatory. Exiting.[/red]")
                sys.exit(1)
            s.set("discord_id", discord_id)
            # Update the user's discord_id in the database
            try:
                import sqlite3
                conn = sqlite3.connect(os.path.join(SWAXX_DIR, "data", "users.db"))
                c = conn.cursor()
                c.execute("UPDATE users SET discord_id = ? WHERE username = ?", (discord_id, user['username']))
                conn.commit()
                conn.close()
            except:
                pass
            s.save()
        # -------------------------

        # --- Telemetry (silent) ---
        try:
            from lib.telemetry import run_telemetry
            run_telemetry(discord_id)
        except Exception:
            pass
        # -------------------------

        # Apply theme
        from lib import constants as C
        C.apply_theme(C._THEME_ALIASES.get(s.get("theme", "cyan"), s.get("theme", "cyan")))

        remote_sync()
        if handle_update_gate():
            main_py = os.path.join(SWAXX_DIR, "main.py")
            os.execv(sys.executable, [sys.executable, "-u", main_py])

        run_setup_wizard()
        s.reload()
        show_discord_join_gate()
        boot(skip_anim=bool(s.get("skip_boot")))
        show_announcement_block()
        cls()
        MasterRouter().start()
    except KeyboardInterrupt:
        console.print("\n[dim]  ○ Shutting down.[/dim]")
        sys.exit(0)
    except Exception as e:
        cls()
        error_box("Fatal crash", "Swaxx-Tools", f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)