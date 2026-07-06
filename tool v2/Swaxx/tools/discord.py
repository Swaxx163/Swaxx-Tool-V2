"""
DISCORD – Tools that do NOT require a token for basic lookups.
Token checker still requires one for validation.
"""
import time
import requests
import urllib3
from rich.prompt import Prompt
from rich.console import Console

console = Console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def user_lookup():
    """Look up a Discord user by ID using public APIs (no token)."""
    uid = Prompt.ask("[cyan]Enter User ID[/cyan]")
    profile_link = f"https://discord.com/users/{uid}"
    
    # Try API 1: discord.id (HTTPS)
    try:
        resp = requests.get(f"https://discord.id/api/users/{uid}", timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('username'):
                username = data.get('username', 'Unknown')
                discriminator = data.get('discriminator', '0')
                display = f"{username}#{discriminator}" if discriminator != "0" else username
                avatar_url = data.get('avatar_url', 'N/A')
                banner_url = data.get('banner_url', 'N/A')
                created_at = data.get('created_at', 'N/A')
                print(f"[green]User: {display}\nID: {data.get('id', uid)}\nCreated: {created_at}\nAvatar: {avatar_url}\nBanner: {banner_url}\nProfile: {profile_link}[/green]")
                input("Press Enter...")
                return
    except Exception:
        pass

    # Try API 2: japi.rest
    try:
        resp = requests.get(f"https://japi.rest/discord/v1/user/{uid}", timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success') and 'data' in data:
                user_data = data['data']
                username = user_data.get('username', 'Unknown')
                discriminator = user_data.get('discriminator', '0')
                display = f"{username}#{discriminator}" if discriminator != "0" else username
                avatar_url = user_data.get('avatar_url', 'N/A')
                banner_url = user_data.get('banner_url', 'N/A')
                created_at = user_data.get('created_at', 'N/A')
                print(f"[green]User: {display}\nID: {user_data.get('id', uid)}\nCreated: {created_at}\nAvatar: {avatar_url}\nBanner: {banner_url}\nProfile: {profile_link}[/green]")
                input("Press Enter...")
                return
    except Exception:
        pass

    # Try API 3: discordlookup (HTTP)
    try:
        resp = requests.get(f"http://discordlookup.mesavirep.xyz/api/user/{uid}", timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('username'):
                username = data.get('username', 'Unknown')
                discriminator = data.get('discriminator', '0')
                display = f"{username}#{discriminator}" if discriminator != "0" else username
                avatar_url = data.get('avatar_url', 'N/A')
                banner_url = data.get('banner_url', 'N/A')
                created_at = data.get('created_at', 'N/A')
                print(f"[green]User: {display}\nID: {data.get('id', uid)}\nCreated: {created_at}\nAvatar: {avatar_url}\nBanner: {banner_url}\nProfile: {profile_link}[/green]")
                input("Press Enter...")
                return
    except Exception:
        pass

    # Final fallback: show snowflake info and profile link
    console.print("[yellow]Could not fetch user data from public APIs. Showing snowflake info:[/yellow]")
    try:
        snowflake_id = int(uid)
        timestamp_ms = (snowflake_id >> 22) + 1420070400000
        created = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(timestamp_ms/1000))
        print(f"[green]ID: {uid}\nCreated (approx): {created}\nProfile: {profile_link}[/green]")
    except:
        print(f"[green]ID: {uid}\nProfile: {profile_link}[/green]")
    input("Press Enter...")

def token_checker():
    """Validate a Discord token (requires token)."""
    token = Prompt.ask("[cyan]Enter Discord token[/cyan]")
    headers = {"Authorization": token}
    try:
        resp = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[green]Valid token!\nUser: {data['username']}#{data.get('discriminator', '0')}\nID: {data['id']}\nProfile: https://discord.com/users/{data['id']}[/green]")
        else:
            print("[red]Invalid token.[/red]")
    except:
        print("[red]Request failed.[/red]")
    input("Press Enter...")

def invite_resolver():
    """Resolve an invite code (no token needed)."""
    code = Prompt.ask("[cyan]Enter invite code[/cyan]")
    try:
        resp = requests.get(f"https://discord.com/api/v9/invites/{code}?with_counts=true", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            guild = data.get('guild', {})
            print(f"[green]Server: {guild.get('name', 'Unknown')}\nMembers: {data.get('approximate_member_count', '?')}\nOnline: {data.get('approximate_presence_count', '?')}\nChannel: {data.get('channel', {}).get('name', '?')}[/green]")
        else:
            print("[red]Invalid invite.[/red]")
    except:
        print("[red]Request failed.[/red]")
    input("Press Enter...")

def webhook_info():
    """Get info from a webhook URL (no token needed)."""
    url = Prompt.ask("[cyan]Enter webhook URL[/cyan]")
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[green]Webhook Name: {data.get('name', 'N/A')}\nChannel: {data.get('channel_id', 'N/A')}\nGuild: {data.get('guild_id', 'N/A')}[/green]")
        else:
            print("[red]Invalid webhook.[/red]")
    except:
        print("[red]Request failed.[/red]")
    input("Press Enter...")

TOOLS = {
    "User Lookup": user_lookup,
    "Token Checker": token_checker,
    "Invite Resolver": invite_resolver,
    "Webhook Info": webhook_info,
}