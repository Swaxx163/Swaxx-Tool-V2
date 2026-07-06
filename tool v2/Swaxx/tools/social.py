"""
SOCIAL – Check username existence on platforms.
"""
import time
import requests
from rich.prompt import Prompt

def check_platform(url, platform_name):
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        if r.status_code == 200:
            return f"[green]✓ {platform_name}: exists[/green]"
        elif r.status_code == 404:
            return f"[red]✗ {platform_name}: not found[/red]"
        else:
            return f"[yellow]? {platform_name}: status {r.status_code}[/yellow]"
    except:
        return f"[yellow]? {platform_name}: connection error[/yellow]"

def twitter_osint():
    username = Prompt.ask("[cyan]Enter Twitter username[/cyan]")
    print(check_platform(f"https://twitter.com/{username}", "Twitter"))
    input("Press Enter...")

def instagram_osint():
    username = Prompt.ask("[cyan]Enter Instagram username[/cyan]")
    print(check_platform(f"https://www.instagram.com/{username}/", "Instagram"))
    input("Press Enter...")

def facebook_osint():
    username = Prompt.ask("[cyan]Enter Facebook username[/cyan]")
    print(check_platform(f"https://www.facebook.com/{username}", "Facebook"))
    input("Press Enter...")

TOOLS = {
    "Twitter OSINT": twitter_osint,
    "Instagram OSINT": instagram_osint,
    "Facebook OSINT": facebook_osint,
}