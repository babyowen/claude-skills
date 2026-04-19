#!/bin/bash
# bank-daily-report 自动运行脚本
# 供 launchd 调度使用，每天上午8点执行

# === 环境变量 ===
export PATH="/Users/babyowen/.local/bin:/Users/babyowen/.nvm/versions/node/v24.11.0/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/babyowen"

SKILL_DIR="/Users/babyowen/.claude/skills/bank-daily-report"
LOG_DIR="$SKILL_DIR/logs"
LOG_FILE="$LOG_DIR/auto_$(date +%Y%m%d_%H%M%S).log"
CLAUDE="/Users/babyowen/.local/bin/claude"

mkdir -p "$LOG_DIR"

echo "=== 开始运行 $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 预处理：获取昨天日期和JSON文件条目数，注入prompt确保完整性
YESTERDAY=$(date -v-1d +%Y-%m-%d)
DATA_FILE="/Users/babyowen/.claude/skills/bank-news-collector/data/${YESTERDAY}.json"
if [ -f "$DATA_FILE" ]; then
    TOTAL=$(python3 -c "import json; print(len(json.load(open('$DATA_FILE'))))")
    echo "数据文件: $DATA_FILE | 条目数: $TOTAL" >> "$LOG_FILE"
    PROMPT="请运行银行日报生成skill，完成全部步骤。昨天的日期是${YESTERDAY}，JSON文件中共有${TOTAL}条新闻，报告中必须覆盖全部${TOTAL}条，不得遗漏。"
else
    echo "数据文件不存在: $DATA_FILE" >> "$LOG_FILE"
    PROMPT="请运行银行日报生成skill，完成全部步骤。昨天的日期是${YESTERDAY}。"
fi

"$CLAUDE" -p "$PROMPT" \
  --allowedTools \
    "Bash(date *)" \
    "Bash(lark-cli im +messages-send *)" \
    "Read(*)" \
  >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "=== 运行结束 exit=$EXIT_CODE $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 清理30天前的日志
find "$LOG_DIR" -name "auto_*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT_CODE
