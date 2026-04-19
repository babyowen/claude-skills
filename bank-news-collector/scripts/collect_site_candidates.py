#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SITES_PATH = ROOT / "sites.json"
LOG_DIR = ROOT / "logs"

# 多个 sign 参数尝试（财联社 API 签名可能有时效性）
CLS_SIGNS = [
    "9f8797a1f4de66c2370f7a03990d2737",  # 当前已知签名
    # 如果发现新签名，可以添加到这里
]

CLS_API_BASE = "https://www.cls.cn/v3/depth/home/assembled/1032?app=CailianpressWeb&os=web&sv=8.4.6"
CLS_HOME_ROLL_API = "https://www.cls.cn/v1/roll/get_roll_list?app=CailianpressWeb&os=web&sv=8.4.6"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}


def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_error(site_id: str, error_msg: str):
    """记录错误日志"""
    ensure_log_dir()
    log_file = LOG_DIR / f"errors-{datetime.now().strftime('%Y%m')}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{site_id}] {error_msg}\n")


def load_sites():
    return json.loads(SITES_PATH.read_text(encoding="utf-8"))


def get_site(site_id: str):
    for site in load_sites():
        if site.get("id") == site_id:
            return site
    raise SystemExit(f"site_id not found: {site_id}")


def fetch_json(url: str, timeout: int = 30):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def collect_cls_depth(site: dict):
    """采集财联社深度页候选文章"""
    items = []
    seen = set()
    last_error = None
    
    # 尝试多个 sign 参数
    for sign in CLS_SIGNS:
        api_url = f"{CLS_API_BASE}&sign={sign}"
        try:
            data = fetch_json(api_url)
            
            # 检查 API 返回是否正常
            if data.get("errno") != 0:
                last_error = f"API errno={data.get('errno')}, msg={data.get('msg')}"
                continue
            
            # 提取文章列表
            for key in ("top_article", "depth_list"):
                for article in data.get("data", {}).get(key, []) or []:
                    article_id = article.get("id")
                    title = (article.get("title") or "").strip()
                    if not article_id or not title:
                        continue
                    url = f"https://www.cls.cn/detail/{article_id}"
                    if url in seen:
                        continue
                    seen.add(url)
                    items.append({
                        "title": title,
                        "url": url,
                        "source": site.get("site_name"),
                        "listed_from": site.get("url"),
                    })
            
            # 成功获取数据，跳出循环
            if items:
                break
                
        except requests.exceptions.Timeout:
            last_error = "API request timeout"
            continue
        except requests.exceptions.RequestException as e:
            last_error = f"API request failed: {e}"
            continue
        except (json.JSONDecodeError, KeyError) as e:
            last_error = f"API response parse error: {e}"
            continue
    
    # 如果所有 sign 都失败，记录错误
    if not items and last_error:
        log_error("cls-depth-1032", last_error)
    
    return {
        "site_id": site.get("id"),
        "site": site.get("url"),
        "source": site.get("site_name"),
        "count": len(items),
        "items": items,
        "error": last_error if not items else None,
    }


def collect_cls_home(site: dict):
    """采集财联社首页候选文章（快讯流 + 深度文章混合）

    财联社 API 接口不受 418 反爬限制，无需 cookie/UA 预热。
    418 仅针对 HTML 页面。
    """
    items = []
    seen = set()
    last_error = None

    # 1) 调用快讯滚动 API（无需 cookie，直接调）
    for sign in CLS_SIGNS:
        api_url = f"{CLS_HOME_ROLL_API}&sign={sign}"
        try:
            data = fetch_json(api_url)

            if data.get("errno") != 0:
                last_error = f"Roll API errno={data.get('errno')}, msg={data.get('msg')}"
                continue

            roll_data = data.get("data", {}).get("roll_data") or []
            for article in roll_data:
                article_id = article.get("id")
                title = (article.get("title") or "").strip()
                brief = (article.get("brief") or "").strip()
                ctime = article.get("ctime", 0)
                # 过滤空标题、纯行情快讯
                if not article_id or not title:
                    continue
                if len(title) < 10 and not brief:
                    continue  # 跳过过短的空标题快讯
                url = f"https://www.cls.cn/detail/{article_id}"
                if url in seen:
                    continue
                seen.add(url)
                item = {
                    "title": title,
                    "url": url,
                    "source": site.get("site_name"),
                    "listed_from": site.get("url"),
                }
                # 附带 published_at（时间戳转 ISO）
                if ctime:
                    item["published_at"] = datetime.fromtimestamp(ctime, tz=None).strftime("%Y-%m-%dT%H:%M:%S+08:00")
                items.append(item)

            # 成功获取数据
            if items:
                last_error = None
                break

        except requests.exceptions.Timeout:
            last_error = "Roll API request timeout"
            continue
        except requests.exceptions.RequestException as e:
            last_error = f"Roll API request failed: {e}"
            continue
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            last_error = f"Roll API parse error: {e}"
            continue

    # 2) 再补充调用深度 1032 API（避免首页遗漏深度文章）
    for sign in CLS_SIGNS:
        api_url = f"{CLS_API_BASE}&sign={sign}"
        try:
            data = fetch_json(api_url)
            if data.get("errno") != 0:
                continue
            for key in ("top_article", "depth_list"):
                for article in data.get("data", {}).get(key, []) or []:
                    article_id = article.get("id")
                    title = (article.get("title") or "").strip()
                    if not article_id or not title:
                        continue
                    url = f"https://www.cls.cn/detail/{article_id}"
                    if url in seen:
                        continue
                    seen.add(url)
                    item = {
                        "title": title,
                        "url": url,
                        "source": site.get("site_name"),
                        "listed_from": site.get("url"),
                    }
                    ctime = article.get("ctime", 0)
                    if ctime:
                        item["published_at"] = datetime.fromtimestamp(ctime, tz=None).strftime("%Y-%m-%dT%H:%M:%S+08:00")
                    items.append(item)
            break  # 深度 API 只尝试一次（与 cls-depth-1032 共用签名）
        except Exception:
            continue

    if not items and last_error:
        log_error("cls-home", last_error)

    return {
        "site_id": site.get("id"),
        "site": site.get("url"),
        "source": site.get("site_name"),
        "count": len(items),
        "items": items,
        "error": last_error if not items else None,
    }


def collect_jiemian(site: dict, output_path=None):
    script = ROOT / "scripts" / "jiemian_finance_extractor.py"
    cmd = [
        sys.executable,
        str(script),
        "--url",
        site.get("url"),
        "--source",
        site.get("site_name"),
    ]
    if output_path:
        cmd.extend(["--output", output_path])
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    if output_path:
        return json.loads(Path(output_path).read_text(encoding="utf-8"))
    return json.loads(proc.stdout)


def main():
    parser = argparse.ArgumentParser(description="Collect candidate titles for one configured bank-news site")
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--output", help="Write JSON output to this file")
    args = parser.parse_args()

    site = get_site(args.site_id)
    site_id = site.get("id")

    if site_id == "jiemian-finance":
        payload = collect_jiemian(site, output_path=args.output)
    elif site_id == "cls-depth-1032":
        payload = collect_cls_depth(site)
        if args.output:
            Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif site_id == "cls-home":
        payload = collect_cls_home(site)
        if args.output:
            Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        raise SystemExit(f"site_id not yet wired to script entry: {site_id}")

    if not args.output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
