#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def load_items(path: Path):
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8').strip()
    if not text:
        return []
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f'{path} must contain a JSON array')
    return data


def key_of(item):
    url = (item.get('url') or '').strip()
    title = (item.get('title') or '').strip()
    return url or f'title::{title}'


def target_date_from_daily_path(daily_path: Path):
    m = DATE_RE.search(daily_path.stem)
    return m.group(1) if m else None


def published_date_of(item):
    value = (item.get('published_at') or '').strip()
    if not value:
        return None
    m = DATE_RE.search(value)
    return m.group(1) if m else None


def main():
    if len(sys.argv) < 3:
        print('Usage: merge_news_json.py <daily_json> <candidate_json>')
        sys.exit(1)

    daily_path = Path(sys.argv[1])
    candidate_path = Path(sys.argv[2])

    daily_items = load_items(daily_path)
    candidate_items = load_items(candidate_path)
    target_date = target_date_from_daily_path(daily_path)

    seen = {key_of(item) for item in daily_items if key_of(item)}
    added = []
    skipped_non_target_date = []
    skipped_missing_published_at = []

    for item in candidate_items:
        published_date = published_date_of(item)
        if not published_date:
            skipped_missing_published_at.append(item)
            continue
        if target_date and published_date != target_date:
            skipped_non_target_date.append({
                'title': item.get('title'),
                'published_at': item.get('published_at')
            })
            continue

        k = key_of(item)
        if not k or k in seen:
            continue
        item.setdefault('collected_at', datetime.now(ZoneInfo('Asia/Shanghai')).isoformat())
        daily_items.append(item)
        seen.add(k)
        added.append(item)

    daily_path.parent.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(json.dumps(daily_items, ensure_ascii=False, indent=2), encoding='utf-8')

    # 保存本次新增的URL列表（供generate_report.py使用）
    new_urls_path = daily_path.parent / f"{daily_path.stem}-new-urls.json"
    new_urls_path.write_text(json.dumps([item['url'] for item in added], ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({
        'daily_path': str(daily_path),
        'target_date': target_date,
        'existing_count': len(daily_items) - len(added),
        'added_count': len(added),
        'total_count': len(daily_items),
        'skipped_non_target_date_count': len(skipped_non_target_date),
        'skipped_missing_published_at_count': len(skipped_missing_published_at)
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
