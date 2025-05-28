# 📰 Web Scraping News from Different Countries using RSS Feeds

## 📌 Title: Web Scraping and Data Extraction

## 🚀 Objective
This project demonstrates the ability to:
- Extract structured news data from RSS feeds across different countries.
- Parse and process RSS feeds using Python.
- Store the data in both CSV and SQLite formats.
- Handle encoding, deduplication, and missing field issues.
- Provide an API to query stored news articles.

---

## 📁 Project Structure
```
rss-news-scraper/
├── ContexQ/                  # Django project settings
│   ├── settings.py
│   └── ...
├── articles/                 # Django app for news
│   ├── models.py
│   ├── views.py
│   └── ...
├── src/                      # Parsing logic
├── feeds/rss_feeds.json      # RSS feed URLs
├── data/                     # CSV output
├── run_scraper.sh            # Cron script
├── main.py                   # Scraper entry point
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📥 Data Collection
- 20+ RSS feeds from countries including UK, US, Japan, India, Germany, etc.
- Fields extracted:
  - Title
  - Published Date
  - Source
  - Country
  - Summary
  - URL
  - Language (detected)

---

## 💾 Data Storage
- Articles saved to:
  - CSV (`/data/*.csv`)
  - SQLite via Django ORM (`Article` model)

---

## 🧠 Code Features
- Modularized with `src/`
- Uses `feedparser`, `langdetect`, `pandas`
- Error handling and deduplication
- Fully commented and class/function-based design

---

## ⚙️ Django API Endpoint
### Base URL:
```
http://127.0.0.1:8000/api/news/
```

### Filters:
- `?country=India`
- `?lang=en`
- `?country=France&lang=fr`

### Example:
```
http://127.0.0.1:8000/api/news/?country=India&lang=en
```

---

## 🕒 Automation
Scheduled using cron:
```bash
0 7 * * * /absolute/path/run_scraper.sh >> /absolute/path/log.txt 2>&1
```

---

## 🔧 Usage

### Install:
```bash
pip install -r requirements.txt
```

### Scrape & Store:
```bash
python main.py
```

### Run Django API:
```bash
python manage.py runserver
```


---

## 📊 Summary Sheet 
Download summary: [`news_scraper_summary.csv`](./news_scraper_summary.csv)


---

## ✅ Completed Features
- ✅ 20+ countries
- ✅ RSS parsing + error handling
- ✅ CSV & SQLite storage
- ✅ Django API with filters
- ✅ Language detection
- ✅ Cron automation

---

## 📎 Submission Bundle
- `main.py`
- `feeds/rss_feeds.json`
- `data/*.csv`
- `run_scraper.sh`
- Django project
- `README.md`

---


