import pandas as pd
import os
import json

def save_to_csv(data, country):
    if not data:
        return

    filename = f"data/{country.lower().replace(' ', '_')}_news.csv"
    new_df = pd.DataFrame(data)

    if os.path.exists(filename):
        old_df = pd.read_csv(filename)
        combined = pd.concat([old_df, new_df], ignore_index=True)
        combined.drop_duplicates(subset=["title", "link"], inplace=True)
    else:
        combined = new_df

    combined.to_csv(filename, index=False, encoding='utf-8')
    print(f"[+] Appended {len(new_df)} articles to {filename}")

def save_to_json(data, country):
    if not data:
        return

    filename = f"data/{country.lower().replace(' ', '_')}_news.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as f:
            old_data = json.load(f)
        combined = {a['link']: a for a in old_data + data}.values()
    else:
        combined = data

    with open(filename, "w", encoding='utf-8') as f:
        json.dump(list(combined), f, ensure_ascii=False, indent=4)
    print(f"[+] Appended {len(data)} articles to {filename}")