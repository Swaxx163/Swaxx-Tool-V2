"""
User authentication – SQLite database, password hashing.
"""
import os
import sqlite3
import hashlib
import time
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

console = Console()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.db")

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            discord_id TEXT,
            created_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def _hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def user_exists(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username.strip(),))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def add_user(username, password, is_admin=0, discord_id=""):
    _ensure_db()
    username = username.strip()
    password = password.strip()
    if user_exists(username):
        return False, "Username already exists."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = _hash_password(password)
    c.execute(
        "INSERT INTO users (username, password, is_admin, discord_id, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, hashed, is_admin, discord_id.strip(), int(time.time()))
    )
    conn.commit()
    conn.close()
    return True, "User added."

def verify_user(username, password):
    _ensure_db()
    username = username.strip()
    password = password.strip()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = _hash_password(password)
    c.execute("SELECT id, username, is_admin, discord_id FROM users WHERE username = ? AND password = ?", (username, hashed))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "is_admin": bool(row[2]), "discord_id": row[3] or ""}
    return None

def delete_user(username):
    username = username.strip()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def list_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin, discord_id, created_at FROM users ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def is_admin_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE username = ?", (username.strip(),))
    row = c.fetchone()
    conn.close()
    return bool(row[0]) if row else False

def is_first_run():
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count == 0

def create_admin_user():
    console.print(Panel(
        Align.center(Text.from_markup(
            "[bold cyan]First run – create admin account[/]\n"
            "This account can add/remove other users."
        )),
        border_style="yellow", box=box.ROUNDED
    ))
    username = Prompt.ask("[bold cyan]Admin username[/bold cyan]")
    password = Prompt.ask("[bold cyan]Admin password[/bold cyan]", password=True)
    password2 = Prompt.ask("[bold cyan]Confirm password[/bold cyan]", password=True)
    if password != password2:
        console.print("[red]Passwords do not match.[/red]")
        return False
    discord_id = Prompt.ask("[bold cyan]Discord ID (optional)[/bold cyan]", default="")
    ok, msg = add_user(username, password, is_admin=1, discord_id=discord_id)
    if ok:
        console.print(f"[green]✓ {msg}[/green]")
    else:
        console.print(f"[red]✗ {msg}[/red]")
    return ok

def login_flow():
    _ensure_db()
    if is_first_run():
        console.print("[yellow]No users found. Creating admin account...[/yellow]")
        if not create_admin_user():
            console.print("[red]Admin creation failed. Exiting.[/red]")
            return None
    while True:
        console.clear()
        console.print(Panel(
            Align.center(Text.from_markup(
                "[bold cyan]SWAXX-TOOLS LOGIN[/]\n"
                "Enter your credentials"
            )),
            border_style="cyan", box=box.HEAVY
        ))
        username = Prompt.ask("[bold]Username[/bold]")
        password = Prompt.ask("[bold]Password[/bold]", password=True)
        user = verify_user(username, password)
        if user:
            console.print(f"[green]✓ Welcome, {user['username']}![/green]")
            time.sleep(0.5)
            return user
        else:
            # ========== CONTACT MESSAGE (as requested) ==========
            console.print(Panel(
                Align.center(Text.from_markup(
                    "[bold red]✗ ACCESS DENIED[/]\n\n"
                    "This system does not have public logins.\n"
                    "[yellow]Please contact [bold cyan]@xx805[/bold cyan] on Discord[/yellow]\n"
                    "to request a valid user account.\n\n"
                    "[dim]All login attempts are logged; guessing will not work.[/dim]"
                )),
                border_style="red",
                box=box.HEAVY,
                title="[bold]CONTACT ADMIN[/]",
                title_align="center"
            ))
            # =====================================================
            if not Confirm.ask("Try again?"):
                return None