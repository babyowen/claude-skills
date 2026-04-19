import subprocess, json, os, re

with open('data/incremental_candidates.json') as f:
    items = json.load(f)
if isinstance(items, dict):
    items = items.get('items', [])

os.makedirs('data/articles', exist_ok=True)

for i, item in enumerate(items):
    url = item['url']
    out_path = f'data/articles/{i:02d}.txt'

    if 'yicai.com' in url:
        result = subprocess.run(['curl', '-s', url, '--max-time', '30'], capture_output=True, text=True)
        html = result.stdout.replace('\n', ' ')
        m = re.search(r'<div id="multi-text"[^>]*>(.*?)</div>', html, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]*>', '', m.group(1))
            text = text.replace('&ldquo;', '"').replace('&rdquo;', '"')
            text = text.replace('&nbsp;', ' ').replace('&lt;', '<')
            text = text.replace('&gt;', '>').replace('&quot;', '"')
            text = text.replace('&amp;', '&')
        else:
            text = result.stdout[:3000]
        with open(out_path, 'w') as fout:
            fout.write(text)
    else:
        jina_url = 'https://r.jina.ai/' + url
        result = subprocess.run(['curl', '-s', jina_url, '--max-time', '30'], capture_output=True, text=True)
        with open(out_path, 'w') as fout:
            fout.write(result.stdout[:5000])

    sz = os.path.getsize(out_path)
    print(f'{i}: {item["title"][:40]}... {sz} bytes')

print('All done')
