import json
from src.rss_parser import parse_feed
from src.utils import save_to_csv

def load_feeds(path="feeds/rss_feeds.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run():
    feeds_by_country = load_feeds()

    for country, urls in feeds_by_country.items():
        print(f"\n[+] Processing country: {country}")
        all_articles = []
        for url in urls:
            try:
                print(f"  --> Parsing feed: {url}")
                articles = parse_feed(url)
                for a in articles:
                    a["country"] = country
                all_articles.extend(articles)
            except Exception as e:
                print(f"  [!] Error parsing {url}: {e}")

        save_to_csv(all_articles, country)

if __name__ == "__main__":
    run()