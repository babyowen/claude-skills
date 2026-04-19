#!/usr/bin/env python3
"""
并发抓取所有站点的候选新闻

- 有专用脚本的站点（collector_entry）：脚本直接提取 → items
- 无专用脚本的站点：jina-reader 抓原始 markdown → data/raw_{site_id}.md（由 agent 后续处理）

输出：data/candidates_all.json（仅包含脚本站点的结果）
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

SITES_JSON = "sites.json"
DATA_DIR = "data"
MAX_WORKERS = 6


def load_sites():
    with open(SITES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_with_script(site):
    """用专用脚本采集"""
    site_id = site['id']
    site_name = site['site_name']

    try:
        output_file = f"{DATA_DIR}/candidates_{site_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        cmd = f"python3 scripts/collect_site_candidates.py --site-id {site_id} --output {output_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)

        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 清理中间文件
            os.remove(output_file)
            print(f"✅ {site_name}: {data.get('count', 0)}条（脚本）")
            return data
        else:
            print(f"❌ {site_name}: 脚本失败")
            return {"site_id": site_id, "source": site_name, "count": 0, "items": []}

    except Exception as e:
        print(f"❌ {site_name}: 异常 - {str(e)}")
        return {"site_id": site_id, "source": site_name, "count": 0, "items": [], "error": str(e)}


def fetch_raw_markdown(site):
    """用 jina-reader 抓原始 markdown，保存到文件，由 agent 后续处理"""
    site_id = site['id']
    site_name = site['site_name']
    url = site['url']

    try:
        print(f"⏳ {site_name}: 抓取原始页面...")

        cmd = f'curl -s "https://r.jina.ai/{url}" --max-time 30'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

        if result.returncode == 0 and len(result.stdout) > 100:
            raw_path = f"{DATA_DIR}/raw_{site_id}.md"
            with open(raw_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"✅ {site_name}: 原始页面已保存（{len(result.stdout)}字符）")
            return {"site_id": site_id, "source": site_name, "raw_file": raw_path}
        else:
            print(f"❌ {site_name}: jina-reader失败")
            return {"site_id": site_id, "source": site_name, "count": 0, "items": [], "error": "抓取失败"}

    except Exception as e:
        print(f"❌ {site_name}: 异常 - {str(e)}")
        return {"site_id": site_id, "source": site_name, "count": 0, "items": [], "error": str(e)}


def main():
    sites = load_sites()

    script_sites = [s for s in sites if s.get('collector_entry')]
    raw_sites = [s for s in sites if not s.get('collector_entry')]

    print(f"共 {len(sites)} 个站点：{len(script_sites)} 个有脚本，{len(raw_sites)} 个需 LLM 提取")
    print()

    all_candidates = []
    raw_files = []

    # 并发抓取所有站点
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for site in script_sites:
            futures[executor.submit(collect_with_script, site)] = site
        for site in raw_sites:
            futures[executor.submit(fetch_raw_markdown, site)] = site

        for future in as_completed(futures):
            try:
                result = future.result()
                if 'raw_file' in result:
                    raw_files.append(result)
                else:
                    all_candidates.append(result)
            except Exception as e:
                print(f"❌ 抓取异常: {str(e)}")

    # 合并脚本站点的结果
    merged = {
        "source": "all_sites",
        "count": sum(item.get('count', 0) for item in all_candidates),
        "sites": len(all_candidates),
        "timestamp": datetime.now().isoformat(),
        "items": []
    }

    for item in all_candidates:
        merged['items'].extend(item.get('items', []))

    # 记录需要 LLM 处理的原始文件
    if raw_files:
        merged["pending_llm_files"] = [
            {"site_id": r["site_id"], "source": r["source"], "raw_file": r["raw_file"]}
            for r in raw_files
        ]

    # 保存
    output_file = f"{DATA_DIR}/candidates_all.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print()
    print(f"✅ 脚本站点抓取完成！候选数: {merged['count']} 条")
    if raw_files:
        print(f"   待 LLM 提取: {len(raw_files)} 个站点")
        for r in raw_files:
            print(f"     - {r['source']}: {r['raw_file']}")
    print(f"   输出文件: {output_file}")


if __name__ == "__main__":
    main()
