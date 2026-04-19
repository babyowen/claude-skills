#!/usr/bin/env python3
"""Send Feishu message using lark-cli."""
import subprocess
import sys
import shutil
import os

def find_lark_cli():
    # Check common locations
    candidates = [
        shutil.which("lark-cli"),
        os.path.expanduser("~/.npm-global/bin/lark-cli"),
        "/usr/local/bin/lark-cli",
        "/opt/homebrew/bin/lark-cli",
    ]
    # Also try npm global prefix
    try:
        npm_prefix = subprocess.check_output(
            ["npm", "prefix", "-g"], stderr=subprocess.DEVNULL
        ).decode().strip()
        candidates.append(os.path.join(npm_prefix, "bin", "lark-cli"))
    except Exception:
        pass

    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None

def main():
    lark_cli = find_lark_cli()
    if not lark_cli:
        print("ERROR: lark-cli not found", file=sys.stderr)
        sys.exit(127)

    message = """银行新闻采集报告 2026-03-31

站点统计：
财联社-首页: 初筛 0 | 二轮 0
财联社-深度-1032: 初筛 19 | 二轮 2
界面新闻-金融频道: 初筛 9 | 二轮 1
东方财富-首页: 初筛 8 | 二轮 5
东方财富-银行频道: 初筛 21 | 二轮 2
第一财经-金融频道: 初筛 14 | 二轮 0

今日已收录新闻（12条）：
1. 逆回购发力 流动性平稳跨季无虞
2. 美联储4月维持利率不变的概率为97.4%
3. 3月官方制造业PMI为50.4% 经济回升向好
4. 债市早参3月31日：债市明显升温，30年国债收益率下行逾2bp
5. 稳中有进、进中提质 中原银行2025年报彰显高质量发展实力
6. 多家上市银行去年代销保险保费与收入双增
7. 2025年国有六大行合计净赚1.42万亿元
8. 部分银行净息差止跌 机构释放乐观预期
9. 浦发银行去年净利润超500亿
10. 代销首单频现！中小银行欲借中间业务破局
11. 民生银行2025年净利润305.63亿 同比下降5.37%
12. 鲍威尔：可暂时忽略油价冲击 倾向于维持利率不变"""

    cmd = [
        lark_cli, "im", "+messages-send",
        "--as", "bot",
        "--user-id", "ou_e9bf22aaaeae8652f04b87ec28fb6bd9",
        "--text", message,
    ]

    print(f"Found lark-cli at: {lark_cli}", file=sys.stderr)
    print(f"Running: {' '.join(cmd[:4])} ...", file=sys.stderr)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
