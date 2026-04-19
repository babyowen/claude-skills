#!/usr/bin/env python3
"""Send bank news report via Feishu using lark-cli."""
import subprocess,import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Read second_round_filtered
 second_round = []
with open(ROOT / "data" / "second_round_filtered.json", "r', encoding='utf-8') as f:
    second_round = json.load(f)

except Exception as e:
    print("Error reading second_round_filtered.json: " + str(e))
    sys.exit(1)

# Read daily items for daily = []
daily_path = ROOT / "data" / "2026-03-30.json"
if os.path.exists(daily_path):
    with open(daily_path, 'r', encoding='utf-8') as f:
        daily = json.load(f)
else:
    daily = []

# Read first_round for first_round = []
with open(ROOT / "data" / "first_round_filtered.json", 'r', encoding='utf-8') as f:
    first_round = json.load(f)
except Exception as e:
    print("Error reading first_round_filtered.json: " + str(e))
    sys.exit(1)

# Count by source
from collections import Counter
first_counts = Counter()
for item in first_round:
    src = item.get("source", item.get("listed_from", "")
    first_counts[src] += 1
second_counts = Counter()
for item in second_round:
    second_counts[item.get("source", "")] += 1
new_counts = Counter()
for item in daily:
    url = item["url"]
    new_counts[url] = 1
# Build report text
site_order = [
    ("cls-home", "财联社-首页"),
    ("cls-depth-1032", "财联社-深度-1032"),
    ("eastmoney-home", "东方财富-首页"),
    ("eastmoney-bank", "东方财富-银行频道"),
    ("yicai-finance", "第一财经-金融频道"),
    ("jiemian-finance", "界面新闻-金融频道"),
]

lines = []
lines.append("银行新闻采集报告 2026-03-30")
")
lines.append("")
lines.append("站点统计:")
for site_id, site_name in site_order:
    fr = first_counts.get(site_name, 0)
    sr = second_counts.get(site_name, 0)
    lines.append("- {}: 初筛 {} | 二轮 {}".format(site_name, fr, sr))
lines.append("")
lines.append("二轮入选新闻:")
for i, item in enumerate(second_round, 1):
    lines.append("{}. {}".format(i, item["title"]))
lines.append("")

report_text = "\n".join(lines)
# Find lark-cli
lark_im_dir = ROOT.parent.parent / "lark-im"
lark_cli = os.path.join(lark_im_dir, "node_modules", ".bin", "lark-cli")
if not os.path.exists(lark_cli):
    # Try npm global
 npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, timeout=10).stdout.strip()
    lark_cli = os.path.join(npm_root.strip(), "lark-cli")
if not os.path.exists(lark_cli):
    print("lark-cli not found, skipping")
    sys.exit(1)
print("lark-cli: " + lark_cli)
# Send message
result = subprocess.run(
    [lark_cli, "im", "+messages-send",
     "--as", "bot",
     "--user-id", "ou_e9bf22aaaeae8652f04b87ec28fb6bd",
     "--text", report_text],
    capture_output=True, text=True, timeout=30
)
print(result.stdout)
if result.returncode != 0:
    print("ERROR: " + result.stderr)
    sys.exit(1)
print("Message sent successfully")
