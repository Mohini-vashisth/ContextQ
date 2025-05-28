import os
import django
import json

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ContexQ.settings")
django.setup()

import sys
sys.path.append(os.path.abspath(".."))

from src.rss_parser import parse_feed
from src.utils import detect_language
from articles.models import Article

def load_feeds(path=None):
    if not path:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "feeds", "rss_feeds.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run():
    feeds_by_country = load_feeds()

    for country, urls in feeds_by_country.items():
        print(f"\n[+] Processing country: {country}")
        for url in urls:
            try:
                print(f"  --> Parsing feed: {url}")
                articles = parse_feed(url)
                for a in articles:
                    a["country"] = country
                    a["language"] = detect_language(a["title"] + " " + a.get("summary", ""))

                    if not Article.objects.filter(link=a["link"]).exists():
                        Article.objects.create(
                            title=a["title"],
                            published=a["published"],
                            source=a["source"],
                            summary=a["summary"],
                            link=a["link"],
                            country=a["country"],
                            language=a["language"]
                        )
            except Exception as e:
                print(f"  [!] Error: {e}")

if __name__ == "__main__":
    run()