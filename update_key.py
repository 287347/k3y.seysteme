import requests
import base64
import random
import string
import os

# Recupera i dati dai Secrets di GitHub
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
REPO = "287347/k3y.seysteme"
FILE_PATH = "key.txt"

def genera_chiave(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def update_github():
    nuova_k = genera_chiave()
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # Prendi lo SHA per aggiornare il file
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha", "")
    
    content_b64 = base64.b64encode(nuova_k.encode()).decode()
    
    # Carica su GitHub
    requests.put(url, json={"message": "Auto-update key", "content": content_b64, "sha": sha}, headers=headers)
    
    # Invia a Discord (Layout identico alla foto)
    payload = {
        "content": "@here",
        "embeds": [{
            "title": "🔒 | Key Updated!",
            "description": f"New Freemium Key:\n```\n{nuova_k}\n```\nKey changes automatically!",
            "color": 15158332 # Rosso/Arancio
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    update_github()
