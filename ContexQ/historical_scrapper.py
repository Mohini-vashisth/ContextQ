
# Ensure project root is in sys.path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ContexQ.settings")
django.setup()

from articles.models import Article
from src.utils import detect_language

def save_article_if_new(title, link, published, source, country, summary=""):
    if not Article.objects.filter(link=link).exists():
        Article.objects.create(
            title=title,
            published=published,
            source=source,
            summary=summary,
            link=link,
            country=country,
            language=detect_language(title)
        )

# ---------- 🇮🇳 INDIA: Times of India ----------
def fetch_india_toi_articles(date_obj):
    day_number = (date_obj - datetime(1899, 12, 30)).days
    url = f"https://timesofindia.indiatimes.com/{date_obj.year}/{date_obj.month}/{date_obj.day}/archivelist/year-{date_obj.year},month-{date_obj.month},starttime-{day_number}.cms"
    print(f"[India - TOI] {url}")

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select(".content a")

        for link in links:
            href = link.get("href")
            title = link.text.strip()
            if href and title:
                full_link = "https://timesofindia.indiatimes.com" + href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "TOI", "India")
    except Exception as e:
        print(f"[!] TOI Error: {e}")

# ---------- 🇬🇧 UK: The Guardian ----------
def fetch_uk_guardian_articles(date_obj):
    date_str = date_obj.strftime('%Y/%b/%d').lower()
    page = 1
    print(f"[UK - Guardian] Searching for {date_obj.strftime('%Y-%m-%d')}")
    while True:
        url = f"https://www.theguardian.com/world/{date_str}/all?page={page}"
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.select('a.u-faux-block-link__overlay')
            if not articles:
                break

            for a in articles:
                link = a['href']
                title = a.text.strip()
                if title and link:
                    save_article_if_new(title, link, date_obj.strftime('%Y-%m-%d'), "The Guardian", "UK")
            page += 1
        except Exception as e:
            print(f"[!] Guardian Error: {e}")
            break

# ---------- 🇺🇸 USA: CNN ----------
def fetch_us_cnn_articles(date_obj):
    date_str = date_obj.strftime('%Y-%m-%d')
    print(f"[USA - CNN] Searching for {date_str}")
    try:
        url = "https://edition.cnn.com/world"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select('h3.cd__headline a')

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if href and title and href.startswith("/"):
                full_link = "https://edition.cnn.com" + href
                save_article_if_new(title, full_link, date_str, "CNN", "USA")
    except Exception as e:
        print(f"[!] CNN Error: {e}")

# ---------- 🇩🇪 Germany: DW ----------
def fetch_germany_dw_articles(date_obj):
    print(f"[Germany - DW] Searching for {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.dw.com/en/top-stories/s-9097"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.link")

        for a in articles:
            title = a.get("title")
            href = a.get("href")
            if title and href and href.startswith("/"):
                full_link = "https://www.dw.com" + href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "DW", "Germany")
    except Exception as e:
        print(f"[!] DW Error: {e}")

# ---------- 🇫🇷 France: France 24 ----------
def fetch_france_france24_articles(date_obj):
    print(f"[France - France24] Searching {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.france24.com/en/tag/world/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.article__title-link")

        for a in articles:
            title = a.text.strip()
            href = a.get("href")
            if title and href:
                full_link = "https://www.france24.com" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "France24", "France")
    except Exception as e:
        print(f"[!] France24 Error: {e}")

# ---------- 🇯🇵 Japan: NHK World ----------
def fetch_japan_nhk_articles(date_obj):
    print(f"[Japan - NHK] Searching {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www3.nhk.or.jp/nhkworld/en/news/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.c-newsList_item_link")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www3.nhk.or.jp" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "NHK", "Japan")
    except Exception as e:
        print(f"[!] NHK Error: {e}")

# ---------- 🇦🇺 Australia: ABC News ----------
def fetch_aus_abc_articles(date_obj):
    print(f"[Australia - ABC] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.abc.net.au/news/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a._3e_2")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.abc.net.au" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "ABC News", "Australia")
    except Exception as e:
        print(f"[!] ABC Error: {e}")

# ---------- 🇨🇦 Canada: CBC ----------
def fetch_canada_cbc_articles(date_obj):
    print(f"[Canada - CBC] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.cbc.ca/news"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.card")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.cbc.ca" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "CBC", "Canada")
    except Exception as e:
        print(f"[!] CBC Error: {e}")

# ---------- 🇧🇷 Brazil: Globo ----------
def fetch_brazil_globo_articles(date_obj):
    print(f"[Brazil - Globo] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://g1.globo.com/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.feed-post-link")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                save_article_if_new(title, href, date_obj.strftime('%Y-%m-%d'), "Globo", "Brazil")
    except Exception as e:
        print(f"[!] Globo Error: {e}")

# ---------- 🇹🇷 Turkey: Hurriyet ----------
def fetch_turkey_hurriyet_articles(date_obj):
    print(f"[Turkey - Hurriyet] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.hurriyetdailynews.com/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.main-news-link, a.news-title")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.hurriyetdailynews.com" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "Hurriyet", "Turkey")
    except Exception as e:
        print(f"[!] Hurriyet Error: {e}")

# ---------- 🇲🇾 Malaysia: The Star ----------
def fetch_malaysia_star_articles(date_obj):
    print(f"[Malaysia - The Star] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.thestar.com.my/news/nation"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.facet-title, h2 a")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.thestar.com.my" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "The Star", "Malaysia")
    except Exception as e:
        print(f"[!] The Star Error: {e}")

# ---------- 🇪🇸 Spain: El País ----------
def fetch_spain_elpais_articles(date_obj):
    print(f"[Spain - El País] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://english.elpais.com/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.c_t")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://english.elpais.com" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "El País", "Spain")
    except Exception as e:
        print(f"[!] El País Error: {e}")

# ---------- 🇮🇹 Italy: ANSA ----------
def fetch_italy_ansa_articles(date_obj):
    print(f"[Italy - ANSA] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.ansa.it/english/news/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("div.news-title a")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.ansa.it" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "ANSA", "Italy")
    except Exception as e:
        print(f"[!] ANSA Error: {e}")

# ---------- 🇷🇺 Russia: TASS ----------
def fetch_russia_tass_articles(date_obj):
    print(f"[Russia - TASS] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://tass.com/world"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("div.news-item a")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://tass.com" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "TASS", "Russia")
    except Exception as e:
        print(f"[!] TASS Error: {e}")

# ---------- 🇲🇽 Mexico: Mexico News Daily ----------
def fetch_mexico_mnd_articles(date_obj):
    print(f"[Mexico - MND] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://mexiconewsdaily.com/news/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.title-link")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                save_article_if_new(title, href, date_obj.strftime('%Y-%m-%d'), "Mexico News Daily", "Mexico")
    except Exception as e:
        print(f"[!] MND Error: {e}")

# ---------- 🇨🇳 China: Xinhua ----------
def fetch_china_xinhua_articles(date_obj):
    print(f"[China - Xinhua] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://english.news.cn/world/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href and "202" in href:  # crude filter to avoid junk
                full_link = "https://english.news.cn" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "Xinhua", "China")
    except Exception as e:
        print(f"[!] Xinhua Error: {e}")

# ---------- 🇿🇦 South Africa: News24 ----------
def fetch_sa_news24_articles(date_obj):
    print(f"[South Africa - News24] {date_obj.strftime('%Y-%m-%d')}")
    try:
        url = "https://www.news24.com/news24/world"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select("a.card__link")

        for a in articles:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                full_link = "https://www.news24.com" + href if href.startswith("/") else href
                save_article_if_new(title, full_link, date_obj.strftime('%Y-%m-%d'), "News24", "South Africa")
    except Exception as e:
        print(f"[!] News24 Error: {e}")



# ---------- 🔁 Controller ----------
def run_historical_scraping():
    start_date = datetime.now() - timedelta(days=365)
    for i in range(366):
        date = start_date + timedelta(days=i)
        fetch_india_toi_articles(date)
        fetch_uk_guardian_articles(date)
        fetch_us_cnn_articles(date)
        fetch_germany_dw_articles(date)
        fetch_france_france24_articles(date)
        fetch_japan_nhk_articles(date)
        fetch_aus_abc_articles(date)
        fetch_canada_cbc_articles(date)
        fetch_brazil_globo_articles(date)
        fetch_turkey_hurriyet_articles(date)
        fetch_malaysia_star_articles(date)
        fetch_spain_elpais_articles(date)
        fetch_italy_ansa_articles(date)
        fetch_russia_tass_articles(date)
        fetch_mexico_mnd_articles(date)
        fetch_china_xinhua_articles(date)
        fetch_sa_news24_articles(date)

if __name__ == "__main__":
    run_historical_scraping()