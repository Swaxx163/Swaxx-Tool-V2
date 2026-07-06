"""
ROBLOX – Real Roblox API with enhanced error handling and more info.
"""
import time
import requests
from rich.prompt import Prompt

def roblox_user():
    username = Prompt.ask("[cyan]Enter Roblox username[/cyan]")
    try:
        # User lookup
        resp = requests.get(f"https://api.roblox.com/users/get-by-username?username={username}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            user_id = data.get('Id')
            print(f"[green]User: {data['Username']}\nID: {user_id}\nCreated: {data.get('Created', 'N/A')}[/green]")
            if user_id:
                # Fetch more details
                resp2 = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5)
                if resp2.status_code == 200:
                    details = resp2.json()
                    print(f"[green]Display Name: {details.get('displayName', 'N/A')}\nDescription: {details.get('description', 'N/A')[:200]}\nProfile: https://www.roblox.com/users/{user_id}/profile[/green]")
                # Fetch followers count
                resp3 = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=5)
                if resp3.status_code == 200:
                    print(f"Followers: {resp3.json().get('count', '?')}")
        else:
            print("[red]User not found.[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

def roblox_game():
    game_id = Prompt.ask("[cyan]Enter Roblox universe ID[/cyan]")
    try:
        resp = requests.get(f"https://games.roblox.com/v1/games?universeIds={game_id}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                game = data['data'][0]
                print(f"[green]Game: {game.get('name', 'N/A')}\nVisits: {game.get('visits', 'N/A')}\nCreated: {game.get('created', 'N/A')}\nFavorites: {game.get('favoritedCount', 'N/A')}\nPlayers: {game.get('playing', 'N/A')}[/green]")
            else:
                print("[red]Game not found.[/red]")
        else:
            print(f"[red]API error: {resp.status_code}[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

def roblox_group():
    group_id = Prompt.ask("[cyan]Enter Roblox group ID[/cyan]")
    try:
        resp = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[green]Group: {data.get('name', 'N/A')}\nMembers: {data.get('memberCount', 'N/A')}\nOwner: {data.get('owner', {}).get('username', 'N/A')}\nDescription: {data.get('description', 'N/A')[:200]}[/green]")
            # Fetch group icon
            resp2 = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/icon", timeout=5)
            if resp2.status_code == 200:
                icon = resp2.json().get('imageUrl', 'N/A')
                print(f"Icon: {icon}")
        else:
            print("[red]Group not found.[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

def roblox_avatar():
    user_id = Prompt.ask("[cyan]Enter Roblox user ID[/cyan]")
    try:
        resp = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=150x150&format=Png", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                url = data['data'][0].get('imageUrl')
                print(f"[green]Avatar URL: {url}[/green]")
            else:
                print("[red]No avatar found.[/red]")
        else:
            print("[red]Failed to fetch avatar.[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

TOOLS = {
    "Roblox User": roblox_user,
    "Roblox Game": roblox_game,
    "Roblox Group": roblox_group,
    "Roblox Avatar": roblox_avatar,
}