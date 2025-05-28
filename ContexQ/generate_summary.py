import csv
from pathlib import Path
from django.db.models import Count
from articles.models import Article

# Output path
output_file = Path("news_scraper_summary.csv")

# Query summary data
summary = (
    Article.objects
    .values('country', 'source')
    .annotate(total_articles=Count('id'))
    .order_by('country', 'source')
)

# Preprocess into country-wise grouped format
summary_dict = {}
for entry in summary:
    country = entry['country']
    source = entry['source']
    total = entry['total_articles']
    if country not in summary_dict:
        summary_dict[country] = {"News Agency": [], "Total": 0}
    summary_dict[country]["News Agency"].append(source)
    summary_dict[country]["Total"] += total

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Country", "News Agency", "Total articles downloaded", "Total historical data"])

    for country, info in summary_dict.items():
        writer.writerow([
            country,
            ", ".join(info["News Agency"]),
            info["Total"],
            "Since 2023"  # or use a dynamic cutoff if stored per article
        ])