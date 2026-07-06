"""
IP/WEB – IP geolocation, DNS, WHOIS, website info.
"""
import time
import socket
import requests
from rich.prompt import Prompt

def ip_geolocation():
    target = Prompt.ask("[cyan]Enter IP[/cyan]")
    try:
        resp = requests.get(f"http://ip-api.com/json/{target}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,query,proxy,hosting,mobile", timeout=5)
        if resp.status_code == 200 and resp.json().get('status') == 'success':
            data = resp.json()
            print(f"[green]IP: {data['query']}\nCountry: {data['country']} ({data['countryCode']})\nCity: {data['city']}\nISP: {data['isp']}\nProxy: {data['proxy']}\nHosting: {data['hosting']}[/green]")
        else:
            print("[red]Failed to fetch IP info.[/red]")
    except:
        print("[red]Request failed.[/red]")
    input("Press Enter...")

def website_info():
    url = Prompt.ask("[cyan]Enter URL (http:// or https://)[/cyan]")
    try:
        resp = requests.get(url, timeout=5, allow_redirects=True)
        print(f"[green]Status: {resp.status_code}\nServer: {resp.headers.get('Server', 'Unknown')}\nContent-Type: {resp.headers.get('Content-Type', 'Unknown')}\nContent-Length: {resp.headers.get('Content-Length', 'Unknown')}[/green]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
    input("Press Enter...")

def dns_lookup():
    import dns.resolver
    domain = Prompt.ask("[cyan]Enter domain[/cyan]")
    try:
        answers = dns.resolver.resolve(domain, 'A')
        print("[green]A Records:[/green]")
        for r in answers:
            print(f"  {r.address}")
    except Exception as e:
        print(f"[red]DNS lookup failed: {e}[/red]")
    input("Press Enter...")

def whois_lookup():
    import whois
    domain = Prompt.ask("[cyan]Enter domain[/cyan]")
    try:
        w = whois.whois(domain)
        print(f"[green]Registrar: {w.registrar}\nCreation: {w.creation_date}\nExpiration: {w.expiration_date}\nName Servers: {w.name_servers}[/green]")
    except Exception as e:
        print(f"[red]WHOIS failed: {e}[/red]")
    input("Press Enter...")

TOOLS = {
    "IP Geolocation": ip_geolocation,
    "Website Info": website_info,
    "DNS Lookup": dns_lookup,
    "WHOIS": whois_lookup,
}