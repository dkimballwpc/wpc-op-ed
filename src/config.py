import os
from dataclasses import dataclass

@dataclass
class Settings:
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    wpc_base_url: str = "https://www.washingtonpolicy.org"
