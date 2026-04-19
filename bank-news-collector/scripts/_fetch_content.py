import json
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('data/incremental_candidates.json', 'r') as f:
    candidates = json.load(f)

def fetch_cls(url):
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://r.jina.ai/{url}', '--max-time', '30'],
            capture_output=True, text=True, timeout=35
        )
        return result.stdout[:8000] if result.stdout else ''
    except:
        return ''

def fetch_eastmoney(url):
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://r.jina.ai/{url}', '--max-time', '30'],
            capture_output=True, text=True, timeout=35
        )
        return result.stdout[:8000] if result.stdout else ''
    except:
        return ''

def fetch_yicai(url):
    try:
        result = subprocess.run(
            ['curl', '-s', url, '--max-time', '30'],
            capture_output=True, text=True, timeout=35
        )
        html = result.stdout or ''
        html_oneline = html.replace('\n', '')
        match = re.search(r'<div id="multi-text"[^>]*>(.*?)</div>', html_oneline)
        if match:
            text = match.group(1)
            text = re.sub(r'<[^>]*>', '', text)
            text = text.replace('&ldquo;', '"').replace('&rdquo;', '"')
            text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
            text = text.replace('&quot;', '"').replace('&amp;', '&')
            return text[:8000]
        return ''
    except:
        return ''

def fetch_jiemian(url):
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://r.jina.ai/{url}', '--max-time', '30'],
            capture_output=True, text=True, timeout=35
        )
        return result.stdout[:8000] if result.stdout else ''
    except:
        return ''

results = {}

def fetch_one(item):
    url = item['url']
    source = item.get('source', '')
    if 'yicai.com' in url:
        content = fetch_yicai(url)
    elif 'cls.cn' in url:
        content = fetch_cls(url)
    elif 'eastmoney.com' in url:
        content = fetch_eastmoney(url)
    elif 'jiemian.com' in url:
        content = fetch_jiemian(url)
    else:
        try:
            result = subprocess.run(
                ['curl', '-s', f'https://r.jina.ai/{url}', '--max-time', '30'],
                capture_output=True, text=True, timeout=35
            )
            content = result.stdout[:8000] if result.stdout else ''
        except:
            content = ''
    return url, content

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(fetch_one, item): item for item in candidates}
    for future in as_completed(futures):
        url, content = future.result()
        results[url] = content

output = []
for item in candidates:
    entry = dict(item)
    entry['content'] = results.get(item['url'], '')
    output.append(entry)

with open('data/incremental_with_content.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

success = sum(1 for v in results.values() if v)
print(success)
