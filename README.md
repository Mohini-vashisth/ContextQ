# 📰 RSS News Scraper

A Python-based news aggregator that extracts articles from RSS feeds of 20+ countries and stores them in structured CSV/JSON formats.

---

## 🌍 Supported Countries
- UK, US, Japan, India, Germany, France, Canada, Brazil, Australia, China,
  Russia, South Korea, Singapore, Malaysia, Indonesia, Italy, Spain, South Africa, Turkey, Mexico

---

## 🚀 How to Run

### 1. Clone and Setup

```bash
git clone https://github.com/your-username/rss-news-scraper.git
cd rss-news-scraper
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Run the Parser

```bash
python main.py
```

### 3. Output

- Saved to `data/COUNTRY_news.csv`
- One file per country

---

## 📦 Sample Output (Example)

| Title                           | Published          | Source | Country | Link                  |
|--------------------------------|--------------------|--------|---------|-----------------------|
| UK Inflation Falls              | 2025-05-27 10:00   | BBC    | UK      | https://bbc...        |
| Biden Speaks on AI             | 2025-05-27 09:45   | CNN    | US      | https://cnn...        |
| NHK Report on Earthquake       | 2025-05-27 08:30   | NHK    | Japan   | https://nhk...        |

---

## 📁 Project Structure

```
rss-news-scraper/
│
├── data/             # CSV/JSON outputs
├── feeds/            # RSS feed lists
├── src/              # Parsing and utility logic
├── main.py           # Entry point
├── README.md
├── requirements.txt
```
