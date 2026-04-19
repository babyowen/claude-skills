#!/usr/bin/env python3
"""
验证输出格式是否符合模板要求

只允许输出表格和标题列表，不允许任何额外内容
"""

import re
import sys

def validate_output(output):
    """验证输出格式"""

    # 必须包含表格头
    required_pattern = r'^\| 站点 \| 初筛入选 \| 二轮入选 \|'
    if not re.search(required_pattern, output, re.MULTILINE):
        return False, "缺少必需的表格头"

    # 禁止内容列表
    forbidden_words = [
        '采集完成',
        '本次运行',
        '运行结束',
        '说明：',
        '注意：',
        '提示：',
        '总结：',
        '共计',
        '一共',
        '本次',
        '以下',
        '接下来'
    ]

    for word in forbidden_words:
        if word in output:
            return False, f"包含禁止词汇: {word}"

    # 检查行数（表格6行 + 标题列表，合理范围5-30行）
    lines = output.strip().split('\n')
    if len(lines) < 5 or len(lines) > 30:
        return False, f"输出行数异常: {len(lines)} 行"

    return True, "格式正确"

if __name__ == '__main__':
    output = sys.stdin.read()

    is_valid, message = validate_output(output)

    if is_valid:
        # 格式正确，输出原内容
        print(output, end='')
        sys.exit(0)
    else:
        # 格式错误，输出错误信息
        print(f"输出格式验证失败: {message}", file=sys.stderr)
        sys.exit(1)
