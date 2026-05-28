from pathlib import Path
from src.config import Settings

def send_discord(webhook_url, text):
    if not webhook_url:
        return False
    import httpx
    try:
        r = httpx.post(webhook_url, json={"content": text[:1900]}, timeout=20)
        return r.status_code == 204 or r.status_code == 200
    except Exception:
        return False

def main():
    settings = Settings()
    text = "WPC Op-Ed Engine test message\n\nThe app is working and sending messages to Discord."
    
    Path("data").mkdir(exist_ok=True)
    Path("data/daily_digest.txt").write_text(text, encoding="utf-8")
    
    success = send_discord(settings.discord_webhook_url, text)
    
    if success:
        print("Discord message sent successfully")
    else:
        print("Failed to send Discord message")

if __name__ == "__main__":
    main()
