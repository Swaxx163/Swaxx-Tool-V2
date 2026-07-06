"""
MONITOR – System, network, webhook monitoring.
"""
import time
import subprocess
import platform
import requests
from rich.prompt import Prompt

def network_monitor():
    print("[yellow]Pinging Google DNS (8.8.8.8)...[/yellow]")
    param = '-n' if platform.system() == 'Windows' else '-c'
    try:
        out = subprocess.check_output(['ping', param, '4', '8.8.8.8'], text=True, timeout=10)
        print(f"[green]{out}[/green]")
    except Exception as e:
        print(f"[red]Ping failed: {e}[/red]")
    input("Press Enter...")

def webhook_monitor():
    url = Prompt.ask("[cyan]Enter webhook URL[/cyan]")
    try:
        resp = requests.post(url, json={"content": "🔔 Webhook test from Swaxx-Tools"}, timeout=5)
        if resp.status_code in (200, 204):
            print("[green]Webhook is active![/green]")
        else:
            print(f"[red]Webhook responded with {resp.status_code}[/red]")
    except:
        print("[red]Webhook unreachable.[/red]")
    input("Press Enter...")

def status_check():
    import psutil
    print(f"[green]CPU: {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%\nDisk: {psutil.disk_usage('/').percent}%[/green]")
    input("Press Enter...")

TOOLS = {
    "Network Monitor": network_monitor,
    "Webhook Monitor": webhook_monitor,
    "Status Check": status_check,
}