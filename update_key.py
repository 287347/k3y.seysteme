import requests
import base64
import random
import string
import os
import time

# Recupera i dati dai Secrets di GitHub
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
REPO = "287347/k3y.seysteme"
FILE_PATH = "key.txt"

def genera_chiave(length=10):
    # Genera una chiave alfanumerica professionale
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def update_github():
    nuova_k = genera_chiave()
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Recupera lo SHA attuale per sovrascrivere il file
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha", "")
    
    content_b64 = base64.b64encode(nuova_k.encode()).decode()
    
    # Aggiorna il file su GitHub
    requests.put(url, json={
        "message": "System: Automated Key Rotation",
        "content": content_b64, 
        "sha": sha
    }, headers=headers)
    
    # CALCOLO TIMESTAMP: Ora attuale + 5 minuti (300 secondi)
    # <t:timestamp:R> mostra il countdown relativo su Discord (es. "in 5 minutes")
    next_update = int(time.time()) + 300 
    discord_timestamp = f"<t:{next_update}:R>"

    # Invia a Discord con look professionale
    payload = {
        "content": "@here",
        "embeds": [{
            "title": "🔒 | Key Updated!",
            "description": f"**New Freemium Key:**\n```\n{nuova_k}\n```",
            "color": 0x2b2d31, # Colore scuro professionale (Dark Theme Discord)
            "fields": [
                {
                    "name": "⏳ Next Rotation",
                    "value": f"Key expires {discord_timestamp}",
                    "inline": True
                },
                {
                    "name": "🛡️ Status",
                    "value": "🟢 Operational",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Automated Security System • k3y.seysteme",
                "icon_url": "https://i.imgur.com/8nLFC9S.png" # Icona opzionale
            },
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    update_github()
