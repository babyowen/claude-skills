import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
today = datetime.now().strftime("%Y-%m-%d")

with open(DATA_DIR / "first_round_filtered.json", "r", encoding="utf-8") as f:
    first_round_data = json.load(f)
    first_round = first_round_data["items"] if isinstance(first_round_data, dict) and "items" in first_round_data else first_round_data

process_path = DATA_DIR / f"{today}-process.json"
processed_urls = set()
if process_path.exists():
    with open(process_path, "r", encoding="utf-8") as f:
        process_data = json.load(f)
        processed_urls = {item["url"] for item in process_data if isinstance(item, dict) and item.get("url")}

seen = set()
incremental = []
for item in first_round:
    url = item.get("url", "").strip()
    title = item.get("title", "").strip()
    key = url or f"title::{title}"
    if key in processed_urls or key in seen:
        continue
    seen.add(key)
    incremental.append(item)

with open(DATA_DIR / "incremental_candidates.json", "w", encoding="utf-8") as f:
    json.dump(incremental, f, ensure_ascii=False, indent=2)

all_process = processed_urls | {item.get("url", "").strip() for item in first_round if item.get("url")}
with open(process_path, "w", encoding="utf-8") as f:
    json.dump([{"url": url} for url in sorted(all_process)], f, ensure_ascii=False, indent=2)

print(f"first_round: {len(first_round)}, processed: {len(processed_urls)}, incremental: {len(incremental)}")
