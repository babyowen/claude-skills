#!/usr/bin/env python3
"""Fetch article content for second-round filtering."""
import subprocess, json, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
incremental_path = ROOT / "data" / "incremental_candidates.json"
output_path = ROOT / "data" / "second_round_filtered.json"

with open(incremental_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

results = []
today_str = "2026-03-30"
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

for item in items:
    url = item.get('url', '').strip()
    title = item.get('title', '').strip()
    source = item.get('source', item.get('listed_from', ''))

    if not url:
        continue

    # Fetch content
    content = ""
    is_yicai = 'yicai.com' in url

    if is_yicai:
        # Special handling for yicai - direct HTML extraction
        try:
            result = subprocess.run(
                ['curl', '-s', url, '--max-time', '15'],
                capture_output=True, text=True, timeout=20
            )
            html = result.stdout
            # Extract date
            dm = re.search(r'(\d{4})年(\d{2})月(\d{2})日', html)
            date_str = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else ""
            # Extract body
            m = re.search(r'id="multi-text"[^>]*>(.*?)</div>', html, re.S)
            if m:
                text = re.sub(r'<[^>]*>', '', m.group(1))
                for old, new in [('&ldquo;','"'), ('&rdquo;','"'), ('&nbsp;',' '),
                                 ('&lt;','<'), ('&gt;','>'), ('&quot;','"'), ('&amp;','&')]:
                    text = text.replace(old, new)
                content = text[:3000]
        except Exception as e:
            date_str = ""
            content = f"FETCH_ERROR: {e}"
    else:
        # Use jina-reader
        try:
            result = subprocess.run(
                ['curl', '-s', f'https://r.jina.ai/{url}', '--max-time', '30'],
                capture_output=True, text=True, timeout=35
            )
            text = result.stdout
            # Extract date from jina-reader output
            dm = re.search(r'Published Time:\s*(.+)', text)
            date_str = dm.group(1).strip()[:10] if dm else ""
            # Extract body after "Markdown Content:"
            body_match = re.search(r'Markdown Content:\n(.*)', text, re.S)
            content = body_match.group(1)[:3000] if body_match else text[:3000]
        except Exception as e:
            date_str = ""
            content = f"FETCH_ERROR: {e}"

    # Check date
    is_today = today_str in date_str or today_str.replace('-', '') in date_str.replace('-', '')

    # Also check content for date hints
    if not is_today and content:
        # Check for "3月30日" or "03-30" in content
        if '3月30日' in content or '03-30' in content or '03月30日' in content:
            is_today = True
            date_str = today_str

    if not is_today:
        # For CLS articles, check if the URL contains 20260330
        if '20260330' in url:
            is_today = True
            date_str = today_str

    print(f"[{'✓' if is_today else '✗'}] {date_str} | {title[:60]} | {url[:60]}")

    if is_today and content and 'FETCH_ERROR' not in content:
        # Store for LLM processing
        results.append({
            "title": title,
            "url": url,
            "source": source,
            "published_at": date_str,
            "content_preview": content[:2000],
            "collected_at": now_iso
        })

print(f"\n=== {len(results)} articles with today's date ===")
with open(ROOT / "data" / "today_candidates.json", 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
