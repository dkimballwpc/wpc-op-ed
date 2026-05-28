from pathlib import Path
from src.config import Settings
from src.collect_news import load_rss
from src.score import rank_topics

NEWS_FEEDS = [
    "https://rss.cnn.com/rss/cnn_topstories.rss",
    "https://feeds.apnews.com/rss/apf-topnews",
    "https://www.npr.org/rss/rss.php?id=1001",
    "https://www.seattletimes.com/feed/",
    "https://www.wsj.com/xml/rss/3_7085.xml",
    "https://www.thecentersquare.com/search/?f=rss&t=article&l=50",
]

WPC_DOCS = [
    {"title": "WPC placeholder document", "text": "Replace with crawled WPC content."}
]

def render_digest(items):
    lines = ["WPC daily op-ed opportunities", ""]
    for i, x in enumerate(items[:10], 1):
        lines.append(f"{i}. {x.get('title','')} (fit {x.get('fit_score',0):.2f})")
        lines.append(f"   {x.get('link','')}")
    return "\n".join(lines)

def send_discord(webhook_url, text):
    if not webhook_url:
        return
    import httpx
    httpx.post(webhook_url, json={"content": text[:1900]}, timeout=20)

def main():
    settings = Settings()
    news = load_rss(NEWS_FEEDS)
    ranked = rank_topics(news, WPC_DOCS)
    text = render_digest(ranked)

    Path("data").mkdir(exist_ok=True)
    Path("data/daily_digest.txt").write_text(text, encoding="utf-8")

    send_discord(settings.discord_webhook_url, text)

if __name__ == "__main__":
    main()
