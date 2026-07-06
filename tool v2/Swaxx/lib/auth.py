"""
User authentication – SQLite database (plaintext passwords).
"""
import os
import sqlite3
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

def user_exists(username):
    username = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE LOWER(username) = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def add_user(username, password, is_admin=0, discord_id=""):
    _ensure_db()
    username = username.strip().lower()
    password = password.strip()
    if user_exists(username):
        return False, "Username already exists."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (username, password, is_admin, discord_id, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, password, is_admin, discord_id.strip(), int(time.time()))
    )
    conn.commit()
    conn.close()
    return True, "User added."

def verify_user(username, password):
    _ensure_db()
    username = username.strip().lower()
    password = password.strip()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin, discord_id FROM users WHERE LOWER(username) = ? AND password = ?", (username, password))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "is_admin": bool(row[2]), "discord_id": row[3] or ""}
    return None

def delete_user(username):
    username = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE LOWER(username) = ?", (username,))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def list_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password, is_admin, discord_id, created_at FROM users ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_info(username):
    username = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password, is_admin, discord_id, created_at FROM users WHERE LOWER(username) = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "password": row[2],
            "is_admin": bool(row[3]),
            "discord_id": row[4] or "",
            "created_at": row[5]
        }
    return None

def update_password(username, new_password):
    username = username.strip().lower()
    if not user_exists(username):
        return False, "User not found."
    if len(new_password.strip()) < 4:
        return False, "Password must be at least 4 characters."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE LOWER(username) = ?", (new_password.strip(), username))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected > 0:
        return True, "Password updated successfully."
    return False, "No changes made."

def is_admin_user(username):
    username = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE LOWER(username) = ?", (username,))
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
                "Enter your credentials\n\n"
                "[dim]Contact @xx805 on Discord for a user[/dim]"
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
            console.print("[red]✗ Invalid username or password.[/red]")
            if not Confirm.ask("Try again?"):
                return None