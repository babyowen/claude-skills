#!/bin/bash
# bank-news-collector 自动运行脚本
# 供 crontab / launchd 调度使用

# === 环境变量 ===
export PATH="/Users/babyowen/.local/bin:/Users/babyowen/.nvm/versions/node/v24.11.0/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/babyowen"

SKILL_DIR="/Users/babyowen/.claude/skills/bank-news-collector"
LOG_DIR="$SKILL_DIR/logs"
LOG_FILE="$LOG_DIR/auto_$(date +%Y%m%d_%H%M%S).log"
CLAUDE="/Users/babyowen/.local/bin/claude"

mkdir -p "$LOG_DIR"

echo "=== 开始运行 $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

cd "$SKILL_DIR"

"$CLAUDE" -p "请运行银行新闻采集skill，完成全部步骤1到9。" \
  --allowedTools \
    "Bash(python3 *)" \
    "Bash(curl *)" \
    "Bash(lark-cli *)" \
    "Bash(ls *)" \
    "Read(*)" \
    "Write(*)" \
    "Edit(*)" \
    "Glob(*)" \
    "Grep(*)" \
    "Agent(*)" \
    "Skill(*)" \
    "WebFetch(*)" \
    "mcp__web_reader__webReader(*)" \
  >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "=== 运行结束 exit=$EXIT_CODE $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 清理30天前的日志
find "$LOG_DIR" -name "auto_*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT_CODE
