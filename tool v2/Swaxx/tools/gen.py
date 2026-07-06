"""
GEN category tools – generators for usernames, passwords, etc.
"""
import time
import random
import string
from rich.prompt import IntPrompt

def username_generator():
    length = IntPrompt.ask("[cyan]Enter length[/cyan]", default=8)
    print(f"[yellow]Generating username of length {length}...[/yellow]")
    time.sleep(0.5)
    chars = string.ascii_lowercase + string.digits
    print(f"[green]Generated: {''.join(random.choices(chars, k=length))}[/green]")
    input("Press Enter to return...")

def password_generator():
    length = IntPrompt.ask("[cyan]Enter length[/cyan]", default=12)
    print(f"[yellow]Generating password of length {length}...[/yellow]")
    time.sleep(0.5)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    print(f"[green]Generated: {''.join(random.choices(chars, k=length))}[/green]")
    input("Press Enter to return...")

def email_generator():
    print("[yellow]Generating email...[/yellow]")
    time.sleep(0.5)
    chars = string.ascii_lowercase + string.digits
    print(f"[green]Generated: {''.join(random.choices(chars, k=10))}@example.com[/green]")
    input("Press Enter to return...")

def proxy_generator():
    count = IntPrompt.ask("[cyan]Number of proxies[/cyan]", default=5)
    print(f"[yellow]Generating {count} proxies...[/yellow]")
    time.sleep(0.5)
    for _ in range(count):
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        port = random.randint(1000, 9999)
        print(f"[green]{ip}:{port}[/green]")
    input("Press Enter to return...")

TOOLS = {
    "Username Generator": username_generator,
    "Password Generator": password_generator,
    "Email Generator": email_generator,
    "Proxy Generator": proxy_generator,
}