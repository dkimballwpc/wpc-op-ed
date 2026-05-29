import os
import yaml
from pathlib import Path
from src.config import Settings
from src.collect_news import load_rss_from_yaml, load_rss
from src.score import rank_topics

NEWS_FEEDS_YAML = "config/news_sources.yaml"

WPC_DOCS = [
    {"title": "WPC budget and taxes research", "text": "Washington Policy Center research on budget taxes government reform"},
    {"title": "WPC education policy", "text": "Washington Policy Center research on education schools policy"},
    {"title": "WPC environment energy", "text": "Washington Policy Center research on environment energy data centers energy costs"},
    {"title": "WPC health care", "text": "Washington Policy Center research on health care insurance policy"},
    {"title": "WPC transportation", "text": "Washington Policy Center research on transportation roads traffic"},
    {"title": "WPC labor workforce", "text": "Washington Policy Center research on labor workforce worker rights"},
    {"title": "WPC tech telecom", "text": "Washington Policy Center research on technology telecom"},
]

def render_digest(items):
    lines = [
        "📰 WPC Daily Op-Ed Opportunities",
        "",
    ]
    for i, x in enumerate(items[:8], 1):
        lines.append(f"{i}. {x.get('title', 'Untitled')[:80]}")
        lines.append(f"   Fit score: {x.get('fit_score', 0):.2f}")
        lines.append(f"   Link: {x.get('link', '')}")
        lines.append("")
    return "\n".join(lines)

def send_discord(webhook_url, text):
    if not webhook_url:
        return False
    import httpx
    try:
        r = httpx.post(webhook_url, json={"content": text[:1900]}, timeout=20)
        return r.status_code == 204 or r.status_code == 200
    except Exception as ex:
        print(f"Discord error: {ex}")
        return False

def main():
    settings = Settings()
    
    # Load feeds
    feed_urls = load_rss_from_yaml(NEWS_FEEDS_YAML)
    
    # Collect news
    news = load_rss(feed_urls)
    print(f"Collected {len(news)} news items")
    
    # Extract WPC text
    wpc_texts = [f"{x.get('title','')} {x.get('text','')}" for x in WPC_DOCS]
    
    # Score
    ranked = rank_topics(news, wpc_texts)
    print(f"Ranked {len(ranked)} topics")
    
    # Render
    text = render_digest(ranked)
    
    # Save
    Path("data").mkdir(exist_ok=True)
    Path("data/daily_digest.txt").write_text(text, encoding="utf-8")
    
    # Send
    success = send_discord(settings.discord_webhook_url, text)
    
    if success:
        print("Discord message sent successfully")
    else:
        print("Failed to send Discord message")

if __name__ == "__main__":
    main()
