import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href")
        url = urljoin(base_url, href)
        text = " ".join(a.get_text(" ", strip=True).split())
        if url.startswith(base_url) and text:
            links.append({"url": url, "text": text})
    return links

def crawl_seed(urls, base_url="https://www.washingtonpolicy.org"):
    pages = []
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for url in urls:
            r = client.get(url)
            r.raise_for_status()
            pages.append({
                "url": url,
                "html": r.text,
                "links": extract_links(r.text, base_url)
            })
    return pages
