#!/usr/bin/env python3
"""Send Feishu message via direct API, reading secret from Keychain."""
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

CONFIG_PATH = os.path.expanduser("~/.lark-cli/config.json")
OPEN_API_BASE = "https://open.feishu.cn/open-apis"

def get_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_secret_from_keychain(key_id):
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", key_id, "-w"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Keychain access failed (exit {result.returncode}): {result.stderr.strip()}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Keychain access error: {e}", file=sys.stderr)
        return None

def get_tenant_token(app_id, app_secret):
    url = f"{OPEN_API_BASE}/auth/v3/tenant_access_token/internal"
    data = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if result.get("code") != 0:
        print(f"Failed to get tenant token: code={result.get('code')}, msg={result.get('msg')}", file=sys.stderr)
        sys.exit(1)
    return result["tenant_access_token"]

def send_message(token, user_id, text):
    url = f"{OPEN_API_BASE}/im/v1/messages?receive_id_type=open_id"
    body = json.dumps({
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    return result

def main():
    config = get_config()
    app = config["apps"][0]
    app_id = app["appId"]

    secret_info = app.get("appSecret", {})
    if isinstance(secret_info, dict) and secret_info.get("source") == "keychain":
        key_id = secret_info.get("id")
        app_secret = get_secret_from_keychain(key_id)
        if not app_secret:
            print("ERROR: Could not retrieve app_secret from Keychain", file=sys.stderr)
            sys.exit(1)
    elif isinstance(secret_info, str):
        app_secret = secret_info
    else:
        print(f"ERROR: Unknown secret format: {type(secret_info)}", file=sys.stderr)
        sys.exit(1)

    token = get_tenant_token(app_id, app_secret)

    message = (
        "银行新闻采集报告 2026-03-31\n"
        "\n"
        "站点统计：\n"
        "财联社-首页: 初筛 0 | 二轮 0\n"
        "财联社-深度-1032: 初筛 19 | 二轮 2\n"
        "界面新闻-金融频道: 初筛 9 | 二轮 1\n"
        "东方财富-首页: 初筛 8 | 二轮 5\n"
        "东方财富-银行频道: 初筛 21 | 二轮 2\n"
        "第一财经-金融频道: 初筛 14 | 二轮 0\n"
        "\n"
        "今日已收录新闻（12条）：\n"
        "1. 逆回购发力 流动性平稳跨季无虞\n"
        "2. 美联储4月维持利率不变的概率为97.4%\n"
        "3. 3月官方制造业PMI为50.4% 经济回升向好\n"
        "4. 债市早参3月31日：债市明显升温，30年国债收益率下行逾2bp\n"
        "5. 稳中有进、进中提质 中原银行2025年报彰显高质量发展实力\n"
        "6. 多家上市银行去年代销保险保费与收入双增\n"
        "7. 2025年国有六大行合计净赚1.42万亿元\n"
        "8. 部分银行净息差止跌 机构释放乐观预期\n"
        "9. 浦发银行去年净利润超500亿\n"
        "10. 代销首单频现！中小银行欲借中间业务破局\n"
        "11. 民生银行2025年净利润305.63亿 同比下降5.37%\n"
        "12. 鲍威尔：可暂时忽略油价冲击 倾向于维持利率不变"
    )

    result = send_message(token, "ou_e9bf22aaaeae8652f04b87ec28fb6bd9", message)

    if result.get("code") == 0:
        msg_id = result.get("data", {}).get("message_id", "")
        print(f"OK: message_id={msg_id}")
    else:
        print(f"Failed: code={result.get('code')}, msg={result.get('msg')}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
