#!/usr/bin/env python3
"""Step 5: Fetch article content for incremental candidates"""
import json
import subprocess
import re
import html as html_module
import sys

with open('data/incremental_candidates.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

results = []
for i, item in enumerate(candidates):
    url = item['url']
    source = item.get('source', '')
    title = item.get('title', '')
    print(f"\n--- [{i+1}/{len(candidates)}] {title[:50]} ---", file=sys.stderr)

    if 'yicai.com' in url:
        # 第一财经：直接抓HTML
        cmd = f'curl -s "{url}" --max-time 30'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and result.stdout:
            m = re.search(r'<div id="multi-text"[^>]*>(.*?)</div>', result.stdout, re.DOTALL)
            if m:
                text = re.sub(r'<[^>]*>', '', m.group(1))
                text = html_module.unescape(text)
                text = re.sub(r'\s+', ' ', text).strip()
                results.append({"title": title, "url": url, "source": source, "content": text[:5000]})
                print(f"  OK (yicai HTML) {len(text)} chars", file=sys.stderr)
            else:
                # fallback to jina
                cmd2 = f'curl -s "https://r.jina.ai/{url}" --max-time 30'
                result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=60)
                if result2.returncode == 0 and len(result2.stdout) > 100:
                    results.append({"title": title, "url": url, "source": source, "content": result2.stdout[:5000]})
                    print(f"  OK (jina fallback) {len(result2.stdout)} chars", file=sys.stderr)
                else:
                    results.append({"title": title, "url": url, "source": source, "content": ""})
                    print(f"  FAILED", file=sys.stderr)
        else:
            results.append({"title": title, "url": url, "source": source, "content": ""})
            print(f"  FAILED", file=sys.stderr)
    else:
        # 通用：jina-reader
        cmd = f'curl -s "https://r.jina.ai/{url}" --max-time 30'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and len(result.stdout) > 100:
            results.append({"title": title, "url": url, "source": source, "content": result.stdout[:5000]})
            print(f"  OK (jina) {len(result.stdout)} chars", file=sys.stderr)
        else:
            results.append({"title": title, "url": url, "source": source, "content": ""})
            print(f"  FAILED", file=sys.stderr)

with open('data/incremental_with_content.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone: {len(results)} articles fetched", file=sys.stderr)
ok = sum(1 for r in results if r['content'])
print(f"  Success: {ok}, Failed: {len(results)-ok}", file=sys.stderr)
