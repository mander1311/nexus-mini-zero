from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_FILE = BASE_DIR / "app.py"
URL = "http://127.0.0.1:5000"


def is_port_open(host: str = "127.0.0.1", port: int = 5000) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0


def ensure_requirements():
    req_path = BASE_DIR / "requirements.txt"
    if req_path.exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)], check=False)


def start_backend():
    if is_port_open():
        return
    log_path = BASE_DIR / "logs" / "nexus_launcher.log"
    log_path.parent.mkdir(exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log_file:
        subprocess.Popen(
            [sys.executable, str(APP_FILE)],
            cwd=str(BASE_DIR),
            stdout=log_file,
            stderr=log_file,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            start_new_session=True,
        )


def open_browser() -> None:
    if not is_port_open():
        for _ in range(30):
            time.sleep(0.5)
            if is_port_open():
                break
    webbrowser.open(URL)


def main() -> None:
    ensure_requirements()
    start_backend()
    open_browser()
    print(f"NEXUS MINI ZERO pronto em {URL}")


if __name__ == "__main__":
    main()
