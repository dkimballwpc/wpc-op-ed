import feedparser
import yaml

def load_rss_from_yaml(yaml_path):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("washington_feeds", []), data.get("national_feeds", [])

def load_rss(feed_urls, source_type="national"):
    items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:40]:
                items.append({
                    "source_feed": url,
                    "source_type": source_type,
                    "title": getattr(e, "title", ""),
                    "link": getattr(e, "link", ""),
                    "summary": getattr(e, "summary", "")[:500],
                    "published": getattr(e, "published", "")
                })
        except Exception as ex:
            print(f"Error parsing {url}: {ex}")
    return items
