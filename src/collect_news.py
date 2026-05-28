import feedparser

def load_rss(feed_urls):
    items = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for e in feed.entries[:50]:
            items.append({
                "source_feed": url,
                "title": getattr(e, "title", ""),
                "link": getattr(e, "link", ""),
                "summary": getattr(e, "summary", ""),
                "published": getattr(e, "published", "")
            })
    return items
