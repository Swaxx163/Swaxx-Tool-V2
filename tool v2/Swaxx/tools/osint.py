"""
OSINT – Real intelligence gathering.
"""
import time
import socket
import requests
import json
from rich.prompt import Prompt

def ip_lookup():
    target = Prompt.ask("[cyan]Enter IP or domain[/cyan]")
    try:
        ip = socket.gethostbyname(target)
    except:
        print("[red]Could not resolve hostname.[/red]")
        input("Press Enter...")
        return
    resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,query,proxy,hosting,mobile", timeout=5)
    if resp.status_code == 200 and resp.json().get('status') == 'success':
        data = resp.json()
        print(f"[green]IP: {data['query']}\nCountry: {data['country']} ({data['countryCode']})\nCity: {data['city']}\nISP: {data['isp']}\nProxy: {data['proxy']}\nHosting: {data['hosting']}[/green]")
    else:
        print("[red]Failed to fetch IP info.[/red]")
    input("Press Enter...")

def domain_intel():
    import whois
    domain = Prompt.ask("[cyan]Enter domain[/cyan]")
    try:
        w = whois.whois(domain)
        print(f"[green]Domain: {w.domain_name}\nRegistrar: {w.registrar}\nCreation: {w.creation_date}\nExpiration: {w.expiration_date}\nName Servers: {w.name_servers}[/green]")
    except Exception as e:
        print(f"[red]WHOIS lookup failed: {e}[/red]")
    input("Press Enter...")

def email_search():
    import hashlib
    email = Prompt.ask("[cyan]Enter email[/cyan]")
    sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
    url = f"https://api.pwnedpasswords.com/range/{sha1[:5]}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            suffixes = [line.split(':') for line in resp.text.splitlines()]
            found = [s for s in suffixes if s[0] == sha1[5:]]
            if found:
                print(f"[red]Breach found! Count: {found[0][1]} occurrences.[/red]")
            else:
                print("[green]No breaches found.[/green]")
        else:
            print("[red]API error.[/red]")
    except:
        print("[red]Request failed.[/red]")
    input("Press Enter...")

def breach_check():
    email_search()  # same function

def exif_analysis():
    from PIL import Image
    from PIL.ExifTags import TAGS
    path = Prompt.ask("[cyan]Enter image file path[/cyan]")
    try:
        img = Image.open(path)
        exif = img.getexif()
        if not exif:
            print("[yellow]No EXIF data.[/yellow]")
        else:
            for tag, value in exif.items():
                print(f"{TAGS.get(tag, tag)}: {value}")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

TOOLS = {
    "IP Lookup": ip_lookup,
    "Domain Intel": domain_intel,
    "Email Search": email_search,
    "Breach Check": breach_check,
    "EXIF Analysis": exif_analysis,
}