# simulate_send.py
import requests
import json
import time
from pathlib import Path

URL = "http://localhost:3000/webhook"  # se usar ngrok, substitua aqui
HEADERS = {"Content-Type": "application/json", "X-Hook-Token": "token-teste-123"}

def send_file(path, retries=3):
    # abrir com utf-8-sig para lidar com arquivos que tenham BOM no início
    with open(path, "r", encoding="utf-8-sig") as f:
        payload = json.load(f)

    attempt = 0
    while attempt < retries:
        try:
            r = requests.post(URL, json=payload, headers=HEADERS, timeout=8)
            print(f"[{attempt+1}] {path} -> {r.status_code} {r.text}")
            if r.status_code == 200:
                return True
            else:
                attempt += 1
                time.sleep(1.5)
        except Exception as e:
            print("Erro:", e)
            attempt += 1
            time.sleep(1.5)
    print("Falha após retries")
    return False

if __name__ == "__main__":
    base = Path(__file__).parent
    files = ["lead_full.json", "lead_minimal.json", "lead_invalid.json"]
    for f in files:
        p = base / f
        if p.exists():
            send_file(str(p))
        else:
            print("Arquivo não encontrado:", p)
