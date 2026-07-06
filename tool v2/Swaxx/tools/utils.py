"""
UTILS – Configuration, sync, user management, and more tools.
"""
import time
import os
import sys
import hashlib
import base64
import uuid
import webbrowser
import urllib.parse
import platform
import requests
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.console import Console
console = Console()

try:
    import lorem
except ImportError:
    lorem = None

try:
    import psutil
except ImportError:
    psutil = None

from lib.auth import (
    add_user, delete_user, list_users, user_exists,
    is_admin_user, get_user_info, update_password
)
from lib.config import get_settings

def setup_config():
    print("[yellow]Opening setup config...[/yellow]")
    time.sleep(0.5)
    try:
        from lib.setup import run_setup_wizard
        run_setup_wizard(force=True)
    except:
        print("[red]Could not load setup wizard.[/red]")
    input("Press Enter to return...")

def remote_sync():
    print("[yellow]Syncing remote manifest...[/yellow]")
    time.sleep(0.5)
    try:
        from lib.remote import sync
        ok, src = sync(force=True)
        if ok:
            print(f"[green]Sync complete from {src}.[/green]")
        else:
            print("[red]Sync failed.[/red]")
    except:
        print("[red]Remote sync unavailable.[/red]")
    input("Press Enter to return...")

def user_manager():
    """User management submenu – only for admins."""
    s = get_settings()
    username = s.get("username", "")
    if not is_admin_user(username):
        console.print("[red]Access denied. Admin privileges required.[/red]")
        input("Press Enter...")
        return

    while True:
        console.print(Panel(
            "[bold yellow]👤 User Manager[/bold yellow]\n\n"
            "[cyan]1.[/cyan] List users\n"
            "[cyan]2.[/cyan] Add user\n"
            "[cyan]3.[/cyan] View user details (shows password)\n"
            "[cyan]4.[/cyan] Change user password\n"
            "[cyan]5.[/cyan] Delete user\n"
            "[cyan]6.[/cyan] Return\n",
            title="[bold]User Management[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        choice = Prompt.ask("[cyan]Select an option[/cyan]", default="6")

        if choice == "1":
            rows = list_users()
            if not rows:
                console.print("[yellow]No users found.[/yellow]")
            else:
                table = Table(title="Users", box=box.ROUNDED)
                table.add_column("ID", style="dim")
                table.add_column("Username", style="cyan")
                table.add_column("Password", style="red")
                table.add_column("Admin", style="green")
                table.add_column("Discord ID", style="yellow")
                table.add_column("Created", style="dim")
                for row in rows:
                    created = time.strftime('%Y-%m-%d', time.gmtime(row[5]))
                    table.add_row(
                        str(row[0]),
                        row[1],
                        row[2],
                        "✓" if row[3] else "",
                        row[4] or "-",
                        created
                    )
                console.print(table)

        elif choice == "2":
            username_new = Prompt.ask("[bold cyan]Username[/bold cyan]")
            if user_exists(username_new):
                console.print("[red]Username already exists.[/red]")
            else:
                password1 = Prompt.ask("[bold cyan]Password[/bold cyan]", password=True)
                password2 = Prompt.ask("[bold cyan]Confirm password[/bold cyan]", password=True)
                if password1 != password2:
                    console.print("[red]Passwords do not match.[/red]")
                else:
                    is_admin = Confirm.ask("[bold cyan]Admin user?[/bold cyan]", default=False)
                    discord_id = Prompt.ask("[bold cyan]Discord ID (optional)[/bold cyan]", default="")
                    ok, msg = add_user(username_new, password1, is_admin=1 if is_admin else 0, discord_id=discord_id)
                    if ok:
                        console.print(f"[green]✓ {msg}[/green]")
                    else:
                        console.print(f"[red]✗ {msg}[/red]")

        elif choice == "3":
            view_user = Prompt.ask("[bold cyan]Username to view[/bold cyan]")
            info = get_user_info(view_user)
            if not info:
                console.print("[red]User not found.[/red]")
            else:
                created = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(info['created_at']))
                console.print(Panel(
                    f"[cyan]Username:[/] {info['username']}\n"
                    f"[cyan]Password:[/] [bold red]{info['password']}[/bold red]\n"
                    f"[cyan]Admin:[/] {'Yes' if info['is_admin'] else 'No'}\n"
                    f"[cyan]Discord ID:[/] {info['discord_id'] or 'Not set'}\n"
                    f"[cyan]Created:[/] {created}",
                    title="User Details (Password Visible)",
                    border_style="red"
                ))

        elif choice == "4":
            change_user = Prompt.ask("[bold cyan]Username to change password[/bold cyan]")
            if not user_exists(change_user):
                console.print("[red]User not found.[/red]")
            else:
                new_pw1 = Prompt.ask("[bold cyan]New password[/bold cyan]", password=True)
                new_pw2 = Prompt.ask("[bold cyan]Confirm new password[/bold cyan]", password=True)
                if new_pw1 != new_pw2:
                    console.print("[red]Passwords do not match.[/red]")
                else:
                    ok, msg = update_password(change_user, new_pw1)
                    if ok:
                        console.print(f"[green]✓ {msg}[/green]")
                    else:
                        console.print(f"[red]✗ {msg}[/red]")

        elif choice == "5":
            username_del = Prompt.ask("[bold cyan]Username to delete[/bold cyan]")
            if username_del == username:
                console.print("[red]Cannot delete your own account.[/red]")
            else:
                if Confirm.ask(f"[bold red]Delete user '{username_del}'?[/bold red]"):
                    if delete_user(username_del):
                        console.print("[green]User deleted.[/green]")
                    else:
                        console.print("[red]User not found.[/red]")

        else:
            break
        input("Press Enter to continue...")

def more_tools():
    """Show a submenu with additional utilities."""
    while True:
        console.print(Panel(
            "[bold yellow]🚀 More Tools[/bold yellow]\n\n"
            "[cyan]1.[/cyan] Hash Generator (MD5, SHA1, SHA256)\n"
            "[cyan]2.[/cyan] Base64 Encoder/Decoder\n"
            "[cyan]3.[/cyan] QR Code Generator\n"
            "[cyan]4.[/cyan] URL Shortener\n"
            "[cyan]5.[/cyan] UUID Generator\n"
            "[cyan]6.[/cyan] Lorem Ipsum Generator\n"
            "[cyan]7.[/cyan] System Info\n"
            "[cyan]8.[/cyan] User Manager (Admin only)\n"
            "[cyan]9.[/cyan] Return to menu\n",
            title="[bold]More Tools[/bold]",
            border_style="blue",
            box=box.ROUNDED
        ))
        choice = Prompt.ask("[cyan]Select a tool[/cyan]", default="9")

        if choice == "1":
            text = Prompt.ask("[cyan]Enter text to hash[/cyan]")
            print(f"[green]MD5: {hashlib.md5(text.encode()).hexdigest()}")
            print(f"SHA1: {hashlib.sha1(text.encode()).hexdigest()}")
            print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}[/green]")

        elif choice == "2":
            mode = Prompt.ask("[cyan]Encode or decode?[/cyan]", choices=["encode", "decode"], default="encode")
            text = Prompt.ask("[cyan]Enter text[/cyan]")
            if mode == "encode":
                print(f"[green]{base64.b64encode(text.encode()).decode()}[/green]")
            else:
                try:
                    print(f"[green]{base64.b64decode(text).decode()}[/green]")
                except:
                    print("[red]Invalid Base64.[/red]")

        elif choice == "3":
            text = Prompt.ask("[cyan]Enter text or URL for QR[/cyan]")
            url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(text)}"
            webbrowser.open(url)
            print(f"[green]QR code opened in browser: {url}[/green]")

        elif choice == "4":
            long_url = Prompt.ask("[cyan]Enter long URL[/cyan]")
            try:
                resp = requests.get(f"https://is.gd/create.php?format=simple&url={long_url}", timeout=5)
                if resp.status_code == 200:
                    print(f"[green]Short URL: {resp.text.strip()}[/green]")
                else:
                    print("[red]Shortening failed.[/red]")
            except:
                print("[red]Shortening service unavailable.[/red]")

        elif choice == "5":
            print(f"[green]UUID: {uuid.uuid4()}[/green]")

        elif choice == "6":
            if lorem:
                print(f"[green]{lorem.text()}[/green]")
            else:
                print("[red]lorem module not installed. Install with: pip install lorem[/red]")

        elif choice == "7":
            if psutil:
                print(f"[green]OS: {platform.platform()}\nCPU: {psutil.cpu_percent()}%\nRAM: {psutil.virtual_memory().percent}%[/green]")
            else:
                print("[red]psutil not installed. Install with: pip install psutil[/red]")

        elif choice == "8":
            user_manager()

        else:
            break
        input("Press Enter to return to submenu...")

TOOLS = {
    "Setup Config": setup_config,
    "Remote Sync": remote_sync,
    "More Tools": more_tools,
}