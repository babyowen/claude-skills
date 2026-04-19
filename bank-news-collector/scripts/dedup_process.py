#!/usr/bin/env python3
"""
步骤4：与 process.json 去重，保留增量

输入：data/first_round_filtered.json（Agent步骤3的输出）
输出：data/incremental_candidates.json（增量候选）

用法：python3 scripts/dedup_process.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    first_round_path = DATA_DIR / "first_round_filtered.json"
    process_path = DATA_DIR / f"{today}-process.json"
    output_path = DATA_DIR / "incremental_candidates.json"

    # 读取第一轮筛选结果
    if not first_round_path.exists():
        print(json.dumps({"error": "first_round_filtered.json not found"}, ensure_ascii=False))
        sys.exit(1)

    with open(first_round_path, 'r', encoding='utf-8') as f:
        first_round_raw = json.load(f)

    # 兼容两种格式：纯列表 或 {"items": [...]} 字典
    if isinstance(first_round_raw, dict) and 'items' in first_round_raw:
        first_round = first_round_raw['items']
    elif isinstance(first_round_raw, list):
        first_round = first_round_raw
    else:
        first_round = []

    # 读取已处理URL
    processed_urls = set()
    if process_path.exists():
        with open(process_path, 'r', encoding='utf-8') as f:
            process_data = json.load(f)
            processed_urls = {
                item['url'] for item in process_data
                if isinstance(item, dict) and item.get('url')
            }

    # 去重：按URL，同时补充按title去重
    seen = set()
    incremental = []
    for item in first_round:
        url = item.get('url', '').strip()
        title = item.get('title', '').strip()
        key = url or f'title::{title}'

        if key in processed_urls or key in seen:
            continue
        seen.add(key)
        incremental.append(item)

    # 保存增量候选
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(incremental, f, ensure_ascii=False, indent=2)

    # 更新 process.json：追加本轮所有第一轮筛选的URL
    all_process = processed_urls | {item.get('url', '').strip() for item in first_round if item.get('url')}
    with open(process_path, 'w', encoding='utf-8') as f:
        json.dump([{"url": url} for url in sorted(all_process)], f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "first_round_count": len(first_round),
        "already_processed": len(processed_urls),
        "incremental_count": len(incremental)
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
