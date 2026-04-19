#!/usr/bin/env python3
"""
lixinger.py - 理杏仁开放平台 A 股数据查询工具

功能：
  - 统一封装理杏仁 API 调用
  - 内置限流（每秒36次 / 每分钟1000次）
  - 指数退避重试
  - 批量请求自动分批

环境变量：
  LIXINGER_TOKEN - API Token（必需）

用法：
  python lixinger.py call --endpoint cn/company/profile --data '{"stockCodes":["600519"]}'
  python lixinger.py batch --endpoint cn/company/fundamental/non_financial --data-file requests.json
  python lixinger.py list-endpoints
"""

import argparse
import json
import os
import ssl
import sys
import time
import gzip
from collections import deque
from datetime import datetime, timezone, timedelta
from typing import Any

import urllib.request
import urllib.error


# SSL context fallback for macOS/development environments
_ssl_context = None


def _get_ssl_context():
    """获取 SSL context，在证书验证失败时回退到不验证模式"""
    global _ssl_context
    if _ssl_context is not None:
        return _ssl_context
    try:
        return ssl.create_default_context()
    except Exception:
        return None


API_BASE = "https://open.lixinger.com/api"
DEFAULT_TIMEOUT = 60
MAX_RETRIES = 5

# Rate limits
PER_SECOND = 36
PER_MINUTE = 1000


class RateLimiter:
    """令牌桶 + 滑动窗口限流器"""

    def __init__(self, per_second: int = PER_SECOND, per_minute: int = PER_MINUTE):
        self.per_second = per_second
        self.per_minute = per_minute
        self._second_window = deque()
        self._minute_window = deque()
        self._lock_time = 0.0

    def acquire(self):
        """获取一个请求许可，必要时阻塞等待"""
        now = time.monotonic()

        # 清理过期记录
        cutoff_second = now - 1.0
        cutoff_minute = now - 60.0
        while self._second_window and self._second_window[0] < cutoff_second:
            self._second_window.popleft()
        while self._minute_window and self._minute_window[0] < cutoff_minute:
            self._minute_window.popleft()

        # 检查限流
        wait_time = 0.0
        if len(self._second_window) >= self.per_second:
            wait_time = max(wait_time, self._second_window[0] + 1.0 - now)
        if len(self._minute_window) >= self.per_minute:
            wait_time = max(wait_time, self._minute_window[0] + 60.0 - now)

        if wait_time > 0:
            time.sleep(wait_time)
            return self.acquire()  # 递归重试

        # 记录本次请求
        self._second_window.append(now)
        self._minute_window.append(now)


# 全局限流器实例
_limiter = RateLimiter()

# 公司类型缓存
_COMPANY_TYPE_CACHE: dict[str, str] = {}
_CACHE_DIR = os.path.expanduser("~/.cache/lixinger")
_CACHE_FILE = os.path.join(_CACHE_DIR, "company_types.json")

_TYPE_ENDPOINT_MAP = {
    "non_financial": "non_financial",
    "bank": "bank",
    "security": "security",
    "insurance": "insurance",
    "other_financial": "other_financial",
}


def _load_type_cache() -> dict[str, str]:
    """从磁盘加载公司类型缓存"""
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_type_cache(cache: dict[str, str]):
    """将公司类型缓存持久化到磁盘"""
    try:
        os.makedirs(_CACHE_DIR, exist_ok=True)
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _infer_type_from_industries(industries: list[dict]) -> str:
    """根据行业分类推断公司金融类型

    优先使用申万2021版分类，回退到任意行业名称匹配。
    """
    type_priority = [
        ("bank", ["银行"]),
        ("security", ["证券"]),
        ("insurance", ["保险"]),
        ("other_financial", ["多元金融", "信托", "期货", "租赁", "金融"]),
    ]

    # 收集所有行业名称和代码
    names = []
    codes = []
    for item in industries:
        if isinstance(item, dict):
            name = item.get("name", "")
            code = item.get("stockCode", "")
            if name:
                names.append(name)
            if code:
                codes.append(code)

    # 按优先级匹配
    for type_key, keywords in type_priority:
        for name in names:
            for kw in keywords:
                if kw in name:
                    return type_key

    return "non_financial"


def detect_company_type(stock_code: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """通过 industries 接口检测公司金融类型

    Args:
        stock_code: 单只股票代码
        timeout: 请求超时秒数

    Returns:
        类型字符串: non_financial / bank / security / insurance / other_financial
    """
    result = make_request("cn/company/industries", {"stockCode": stock_code}, timeout)
    if result.get("code") != 1:
        return "non_financial"

    industries = result.get("data", [])
    return _infer_type_from_industries(industries)


def get_company_type(stock_code: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """获取公司金融类型（带缓存）

    查询顺序: 内存缓存 → 磁盘缓存 → API 检测 → 写入缓存
    """
    global _COMPANY_TYPE_CACHE

    # 内存缓存
    if stock_code in _COMPANY_TYPE_CACHE:
        return _COMPANY_TYPE_CACHE[stock_code]

    # 磁盘缓存
    disk_cache = _load_type_cache()
    if stock_code in disk_cache:
        _COMPANY_TYPE_CACHE[stock_code] = disk_cache[stock_code]
        return disk_cache[stock_code]

    # API 检测
    company_type = detect_company_type(stock_code, timeout)

    # 写入缓存
    _COMPANY_TYPE_CACHE[stock_code] = company_type
    disk_cache[stock_code] = company_type
    _save_type_cache(disk_cache)

    return company_type


def smart_request(
    endpoint_family: str,
    data: dict,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """智能路由请求：自动根据公司类型选择正确的子接口

    仅支持 endpoint_family 为 "fundamental" 或 "fs" 的场景。
    当 stockCodes 中存在多种类型时，自动分组并行调用对应子接口，
    最终合并返回结果。

    Args:
        endpoint_family: "fundamental" 或 "fs"
        data: 请求体（不含 token），必须包含 stockCodes 数组
        timeout: 单个请求超时秒数

    Returns:
        合并后的 API 返回数据，code=1 表示全部成功
    """
    stock_codes = data.get("stockCodes", [])
    if not stock_codes:
        raise ValueError("请求体中必须包含 stockCodes 数组")

    # 检测每个股票类型
    type_map: dict[str, list[str]] = {}
    for code in stock_codes:
        ctype = get_company_type(code, timeout)
        type_map.setdefault(ctype, []).append(code)

    # 按类型分组调用
    all_data = []
    has_error = False
    for ctype, codes in type_map.items():
        sub_endpoint = f"cn/company/{endpoint_family}/{ctype}"
        sub_data = {**data, "stockCodes": codes}
        result = make_request(sub_endpoint, sub_data, timeout)
        if result.get("code") != 1:
            has_error = True
        all_data.extend(result.get("data", []))

    return {
        "code": 0 if has_error else 1,
        "message": "success" if not has_error else "partial success",
        "data": all_data,
    }


def make_request(endpoint: str, data: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    发送单个 API 请求，内置限流和重试

    Args:
        endpoint: API 路径，如 "cn/company/profile"
        data: 请求体 JSON 数据
        timeout: 请求超时秒数

    Returns:
        API 返回的 JSON 数据

    Raises:
        urllib.error.HTTPError: 超过最大重试次数后仍失败
    """
    token = os.environ.get("LIXINGER_TOKEN", "")
    if not token:
        raise RuntimeError(
            "环境变量 LIXINGER_TOKEN 未设置。请设置: export LIXINGER_TOKEN=your_token"
        )

    url = f"{API_BASE}/{endpoint}"
    payload = {**data, "token": token}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "lixinger-skill/1.0",
    }

    req = urllib.request.Request(
        url, data=body, headers=headers, method="POST"
    )

    last_exception = None
    for attempt in range(MAX_RETRIES):
        # 限流等待
        _limiter.acquire()

        try:
            ssl_context = _get_ssl_context()
            kwargs = {"timeout": timeout}
            if ssl_context is not None:
                kwargs["context"] = ssl_context
            with urllib.request.urlopen(req, **kwargs) as resp:
                raw = resp.read()
                # 处理 gzip
                encoding = resp.headers.get("Content-Encoding", "").lower()
                if "gzip" in encoding:
                    raw = gzip.decompress(raw)
                result = json.loads(raw.decode("utf-8"))
                return result
        except urllib.error.HTTPError as e:
            last_exception = e
            if e.code == 429:
                # 触发限流，使用指数退避
                wait = min(2 ** attempt, 30) + (attempt * 0.5)
                print(f"[限流] 429 Too Many Requests，等待 {wait:.1f}s 后重试 ({attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
                time.sleep(wait)
                continue
            elif e.code >= 500:
                # 服务器错误，重试
                wait = min(2 ** attempt, 30)
                print(f"[服务端错误] HTTP {e.code}，等待 {wait:.1f}s 后重试 ({attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
                time.sleep(wait)
                continue
            else:
                # 客户端错误（4xx），不重试，尝试读取错误响应体
                try:
                    err_body = e.read().decode("utf-8")
                    err_data = json.loads(err_body)
                    return err_data
                except Exception:
                    raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_exception = e
            err_str = str(e)
            global _ssl_context
            # SSL 证书验证失败时回退到不验证模式
            if "CERTIFICATE_VERIFY_FAILED" in err_str and _ssl_context is None:
                _ssl_context = ssl._create_unverified_context()
                print("[SSL] 证书验证失败，已切换到不验证模式", file=sys.stderr)
                continue
            wait = min(2 ** attempt, 30)
            print(f"[网络错误] {e}，等待 {wait:.1f}s 后重试 ({attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
            time.sleep(wait)
            continue

    # 超过最大重试次数
    raise RuntimeError(f"请求失败，超过最大重试次数 {MAX_RETRIES}。最后错误: {last_exception}")


def batch_call(endpoint: str, items: list[dict], timeout: int = DEFAULT_TIMEOUT) -> list[dict]:
    """
    批量调用 API，自动处理分批和错误

    Args:
        endpoint: API 路径
        items: 每个元素是一个请求体 dict（不含 token）
        timeout: 单个请求超时

    Returns:
        每个请求对应的返回结果列表
    """
    results = []
    for i, item in enumerate(items):
        try:
            result = make_request(endpoint, item, timeout)
            results.append(result)
        except Exception as e:
            print(f"[批量请求 {i + 1}/{len(items)}] 失败: {e}", file=sys.stderr)
            results.append({"error": str(e), "index": i})
    return results


def split_stock_codes(stock_codes: list[str], batch_size: int = 100) -> list[list[str]]:
    """将股票代码列表按最大允许数量分批"""
    return [stock_codes[i:i + batch_size] for i in range(0, len(stock_codes), batch_size)]


def list_endpoints():
    """打印所有支持的 A 股接口速查表"""
    endpoints = {
        "公司接口 - 基础信息": [
            ("cn/company/fundamental/non_financial", "非金融基本面数据（PE、PB等）"),
            ("cn/company/fundamental/bank", "银行基本面数据"),
            ("cn/company/fundamental/security", "证券基本面数据"),
            ("cn/company/fundamental/insurance", "保险基本面数据"),
            ("cn/company/fundamental/other_financial", "其他金融基本面数据"),
        ],
        "公司接口 - 公司概况": [
            ("cn/company/profile", "公司概况"),
        ],
        "公司接口 - 股本与股东": [
            ("cn/company/equity-change", "股本变动"),
            ("cn/company/shareholders-num", "股东人数"),
            ("cn/company/senior-executive-shares-change", "高管增减持明细"),
            ("cn/company/major-shareholders-shares-change", "大股东增减持明细"),
        ],
        "公司接口 - 交易信息": [
            ("cn/company/candlestick", "K线数据"),
            ("cn/company/trading-abnormal", "龙虎榜明细（按日期）"),
            ("cn/company/block-deal", "大宗交易"),
            ("cn/company/pledge", "股权质押明细"),
        ],
        "公司接口 - 经营信息": [
            ("cn/company/operation-revenue-constitution", "营收构成"),
            ("cn/company/operating-data", "经营数据"),
        ],
        "公司接口 - 分类信息": [
            ("cn/company/indices", "股票所属指数"),
            ("cn/company/industries", "股票所属行业"),
        ],
        "公司接口 - 公告": [
            ("cn/company/announcement", "公告"),
        ],
        "监管信息": [
            ("cn/company/measures", "监管措施"),
            ("cn/company/inquiry", "问讯函"),
        ],
        "股东信息": [
            ("cn/company/majority-shareholders", "前十大股东"),
            ("cn/company/nolimit-shareholders", "前十大流通股东"),
            ("cn/company/fund-shareholders", "公募基金持股"),
            ("cn/company/fund-collection-shareholders", "基金公司持股"),
        ],
        "分红送配": [
            ("cn/company/dividend", "分红"),
            ("cn/company/allotment", "配送"),
        ],
        "客户及供应商": [
            ("cn/company/customers", "客户"),
            ("cn/company/suppliers", "供应商"),
        ],
        "财务报表": [
            ("cn/company/fs/non_financial", "非金融财务报表"),
            ("cn/company/fs/bank", "银行财务报表"),
            ("cn/company/fs/security", "证券财务报表"),
            ("cn/company/fs/insurance", "保险财务报表"),
            ("cn/company/fs/other_financial", "其他金融财务报表"),
        ],
        "热度数据 - 汇总指标": [
            ("cn/company/hot/tr_dri", "分红再投入收益率"),
            ("cn/company/hot/mm_ha", "互联互通（热度）"),
            ("cn/company/hot/mtasl", "融资融券（热度）"),
            ("cn/company/hot/esc", "高管增减持（热度汇总）"),
            ("cn/company/hot/mssc", "大股东增减持（热度汇总）"),
            ("cn/company/hot/t_a", "龙虎榜（热度汇总）"),
            ("cn/company/hot/elr", "限售解禁"),
            ("cn/company/hot/ple", "股权质押（热度汇总）"),
            ("cn/company/hot/capita", "人均指标"),
            ("cn/company/hot/shnc", "股东人数变化"),
            ("cn/company/hot/df", "分红融资"),
            ("cn/company/hot/npd", "派息"),
            ("cn/company/hot/tr", "换手率"),
        ],
        "资金流向": [
            ("cn/company/mutual-market", "互联互通（资金流向明细）"),
            ("cn/company/margin-trading-and-securities-lending", "融资融券（资金流向明细）"),
        ],
    }

    print("=" * 60)
    print("理杏仁 A 股接口速查表")
    print("=" * 60)
    for category, items in endpoints.items():
        print(f"\n【{category}】")
        for endpoint, desc in items:
            print(f"  {endpoint:<55} {desc}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="理杏仁开放平台 A 股数据查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单接口调用
  python lixinger.py call --endpoint cn/company/profile --data '{"stockCodes":["600519"]}'

  # 基本面数据（指定指标）
  python lixinger.py call --endpoint cn/company/fundamental/non_financial \\
      --data '{"stockCodes":["600519"],"date":"2026-03-10","metricsList":["pe_ttm","pb"]}'

  # K线数据
  python lixinger.py call --endpoint cn/company/candlestick \\
      --data '{"stockCode":"600519","startDate":"2025-03-20","endDate":"2026-03-20","type":"lxr_fc_rights"}'

  # 批量调用（从文件读取多个请求）
  python lixinger.py batch --endpoint cn/company/fundamental/non_financial --data-file reqs.json

  # 智能路由 - 基本面（自动识别银行/证券/保险/非金融）
  python lixinger.py smart-fundamental \
      --data '{"stockCodes":["600519","600036"],"date":"2026-03-10","metricsList":["pe_ttm","pb"]}'

  # 智能路由 - 财务报表（自动识别行业类型）
  python lixinger.py smart-fs \
      --data '{"stockCodes":["600519","600036"],"date":"2025-09-30","metricsList":["q.ps.toi.t","q.ps.np.t"]}'

  # 列出所有接口
  python lixinger.py list-endpoints
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # call 子命令
    call_parser = subparsers.add_parser("call", help="单接口调用")
    call_parser.add_argument("--endpoint", required=True, help="API 路径，如 cn/company/profile")
    call_parser.add_argument("--data", required=True, help="请求体 JSON 字符串")
    call_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    call_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数")

    # batch 子命令
    batch_parser = subparsers.add_parser("batch", help="批量接口调用（从文件读取）")
    batch_parser.add_argument("--endpoint", required=True, help="API 路径")
    batch_parser.add_argument("--data-file", required=True, help="JSON 文件路径，内容为请求体数组")
    batch_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    batch_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数")

    # list-endpoints 子命令
    subparsers.add_parser("list-endpoints", help="列出所有支持的接口")

    # smart-fundamental 子命令
    smart_fund_parser = subparsers.add_parser("smart-fundamental", help="智能路由基本面数据（自动识别行业类型）")
    smart_fund_parser.add_argument("--data", required=True, help='请求体 JSON 字符串，如 \'{"stockCodes":["600519"],"date":"2026-03-10","metricsList":["pe_ttm"]}\'')
    smart_fund_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    smart_fund_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数")

    # smart-fs 子命令
    smart_fs_parser = subparsers.add_parser("smart-fs", help="智能路由财务报表（自动识别行业类型）")
    smart_fs_parser.add_argument("--data", required=True, help='请求体 JSON 字符串，如 \'{"stockCodes":["600519"],"date":"2025-09-30","metricsList":["q.ps.toi.t"]}\'')
    smart_fs_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    smart_fs_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数")

    args = parser.parse_args()

    if args.command == "call":
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            result = make_request(args.endpoint, data, timeout=args.timeout)
            if args.pretty:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "batch":
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            if not isinstance(items, list):
                print("data-file 必须是 JSON 数组", file=sys.stderr)
                sys.exit(1)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"文件读取错误: {e}", file=sys.stderr)
            sys.exit(1)

        results = batch_call(args.endpoint, items, timeout=args.timeout)
        if args.pretty:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(results, ensure_ascii=False))

    elif args.command == "list-endpoints":
        list_endpoints()

    elif args.command == "smart-fundamental":
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            result = smart_request("fundamental", data, timeout=args.timeout)
            if args.pretty:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "smart-fs":
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            result = smart_request("fs", data, timeout=args.timeout)
            if args.pretty:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
