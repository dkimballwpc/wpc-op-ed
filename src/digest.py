import os
from pathlib import Path
from src.config import Settings
from src.collect_news import load_rss_from_yaml, load_rss
from src.score import cluster_by_topic, match_to_wpc_topics, generate_explanation

NEWS_FEEDS_YAML = "config/news_sources.yaml"

def render_digest(topics):
    lines = [
        "📰 WPC Daily Op-Ed Opportunities",
        f"Top trends matched to WPC research",
        "",
    ]
    
    for i, topic in enumerate(topics[:5], 1):
        title = topic["items"][0]["title"][:70]
        topic_name = topic["wpc_topic"].replace("_", " ").title()
        
        lines.append(f"{i}. {topic_name}: {title}")
        lines.append("")
        lines.append(generate_explanation(topic))
        lines.append("")
        lines.append("---")
        lines.append("")
    
    if not topics:
        lines.append("No strong topic matches found today.")
    
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
    
    wa_feeds, nat_feeds = load_rss_from_yaml(NEWS_FEEDS_YAML)
    
    wa_news = load_rss(wa_feeds, source_type="washington")
    nat_news = load_rss(nat_feeds, source_type="national")
    all_news = wa_news + nat_news
    
    print(f"Collected {len(wa_news)} WA news, {len(nat_news)} national news")
    
    clusters = cluster_by_topic(all_news)
    print(f"Clustered into {len(clusters)} topics")
    
    ranked = match_to_wpc_topics(clusters)
    print(f"Matched {len(ranked)} topics to WPC research")
    
    text = render_digest(ranked)
    
    Path("data").mkdir(exist_ok=True)
    Path("data/daily_digest.txt").write_text(text, encoding="utf-8")
    
    success = send_discord(settings.discord_webhook_url, text)
    
    if success:
        print("Discord message sent successfully")
    else:
        print("Failed to send Discord message")

if __name__ == "__main__":
    main()
