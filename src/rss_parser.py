import feedparser

def parse_feed(url):
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        article = {
            "title": entry.get("title", ""),
            "published": entry.get("published", ""),
            "source": feed.feed.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", "")
        }
        articles.append(article)

    return articles