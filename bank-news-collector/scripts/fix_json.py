#!/usr/bin/env python3
"""Fix second_round_filtered.json - replace unescaped ASCII double quotes inside string values."""
import json, re

with open('data/second_round_filtered.json', 'r', encoding='utf-8') as f:
    raw = f.read()

# Strategy: find JSON string values and fix internal unescaped quotes
# Known problematic patterns (ASCII " inside values that should be Chinese quotes)
fixes = [
    ('\u5b9e\u73b0"\u626d\u4e8f\u4e3a\u76c8"', '\u5b9e\u73b0\u201c\u626d\u4e8f\u4e3a\u76c8\u201d'),  # 实现"扭亏为盈"
    ('\u65e0\u5f62\u8d44\u4ea7"\u6362"\u8d37\u6b3e', '\u65e0\u5f62\u8d44\u4ea7\u201c\u6362\u201d\u8d37\u6b3e'),  # 无形资产"换"贷款
    ('\u4ea4\u901a\u94f6\u884c"\u4e13\u7cbe\u7279\u65b0"\u4e2d\u5c0f\u4f01\u4e1a', '\u4ea4\u901a\u94f6\u884c\u201c\u4e13\u7cbe\u7279\u65b0\u201d\u4e2d\u5c0f\u4f01\u4e1a'),  # 交通银行"专精特新"中小企业
    ('\u5b9e\u73b0"\u7834\u51b0"', '\u5b9e\u73b0\u201c\u7834\u51b0\u201d'),  # 实现"破冰"
    ('\u6784\u5efa"\u5b58\u6b3e\u66ff\u4ee3+\u8d22\u5bcc\u589e\u503c"', '\u6784\u5efa\u201c\u5b58\u6b3e\u66ff\u4ee3+\u8d22\u5bcc\u589e\u503c\u201d'),  # 构建"存款替代+财富增值"
    ('\u6784\u5efa"\u4fe1\u8d37+\u8d22\u5bcc\u7ba1\u7406+\u589e\u503c\u670d\u52a1"', '\u6784\u5efa\u201c\u4fe1\u8d37+\u8d22\u5bcc\u7ba1\u7406+\u589e\u503c\u670d\u52a1\u201d'),  # 构建"信贷+财富管理+增值服务"
]

for old, new in fixes:
    raw = raw.replace(old, new)

# Validate
data = json.loads(raw)
print(f'Fixed JSON: {len(data)} items valid')

with open('data/second_round_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('File rewritten successfully')
