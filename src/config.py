import os
from dataclasses import dataclass

@dataclass
class Settings:
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    email_to: str = os.getenv("EMAIL_TO", "")
    email_from: str = os.getenv("EMAIL_FROM", "")
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_pass: str = os.getenv("SMTP_PASS", "")
    wpc_base_url: str = "https://www.washingtonpolicy.org"
