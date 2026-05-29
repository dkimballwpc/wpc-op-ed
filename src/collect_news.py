import feedparser

def load_rss_from_yaml(yaml_path):
    import yaml
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])

def load_rss(feed_urls):
    items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:30]:
                items.append({
                    "source_feed": url,
                    "title": getattr(e, "title", ""),
                    "link": getattr(e, "link", ""),
                    "summary": getattr(e, "summary", "")[:500],
                    "published": getattr(e, "published", "")
                })
        except Exception as ex:
            print(f"Error parsing {url}: {ex}")
    return items
