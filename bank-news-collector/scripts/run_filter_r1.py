import json, re
from datetime import datetime

INPUT = "/Users/babyowen/.claude/skills/bank-news-collector/data/candidates_all.json"
OUTPUT = "/Users/babyowen/.claude/skills/bank-news-collector/data/first_round_filtered.json"

with open(INPUT, "r", encoding="utf-8") as fh:
    data = json.load(fh)
items = data["items"]
print("Loaded", len(items), "items")
