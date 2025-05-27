import pandas as pd
import json
import os

def save_to_csv(data, country):
    if not data:
        return
    df = pd.DataFrame(data)
    filename = f"data/{country.lower().replace(' ', '_')}_news.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"[+] Saved {len(data)} articles to {filename}")

def save_to_json(data, country):
    if not data:
        return
    filename = f"data/{country.lower().replace(' ', '_')}_news.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[+] Saved {len(data)} articles to {filename}")