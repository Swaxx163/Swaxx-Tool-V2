"""
HOME category tools.
"""
import time
import webbrowser
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich import box

console = Console()

def open_github():
    print("[yellow]Opening GitHub...[/yellow]")
    time.sleep(0.5)
    webbrowser.open("https://github.com/")
    print("[green]✓ GitHub opened in your browser[/green]")
    input("Press Enter to return...")

def discord_contact():
    """Show a message to contact @xx805 on Discord."""
    console.print(Panel(
        Align.center(
            "[bold yellow]📱 Contact @xx805 on Discord for a user[/bold yellow]\n\n"
            "[dim]Send a friend request or DM @xx805[/dim]\n"
            "[cyan]Discord: xx805[/cyan]"
        ),
        title="Contact for User",
        border_style="blue",
        box=box.ROUNDED
    ))
    input("Press Enter to return...")

def star_github():
    print("[yellow]Starring repository...[/yellow]")
    time.sleep(0.5)
    webbrowser.open("https://github.com/yourusername/Swaxx-Tools")
    print("[green]⭐ Starred! (opened repo in browser)[/green]")
    input("Press Enter to return...")

def show_changelog():
    print("[yellow]Changelog:[/yellow]")
    print("  v1.0 – Initial release")
    input("Press Enter to return...")

def show_credits():
    print("[yellow]Credits:[/yellow]")
    print("  Author: swaxx")
    print("  Inspired by Void-Tools")
    print("  Hello, friend.")
    input("Press Enter to return...")

TOOLS = {
    "GitHub": open_github,
    "Contact User": discord_contact,   # <-- Replaced "Discord" with this
    "Star GitHub": star_github,
    "Changelog": show_changelog,
    "Credits": show_credits,
}