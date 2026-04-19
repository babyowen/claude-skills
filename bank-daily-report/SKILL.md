---
name: bank-daily-report
description: 为银行管理层生成每日银行业综合分析报告。读取 bank-news-collector 采集的前一天新闻 JSON 数据，以省级股份制银行行长视角撰写包含综述、行业动态、经营启示的三部分精简日报。当用户提到银行日报、每日报告、日报生成、行业简报、daily report 时使用此技能。专为定时任务设计，支持无人值守自动运行。
---

# 银行业日报生成

## 数据源

路径：`/Users/babyowen/.claude/skills/bank-news-collector/data/{YYYY-MM-DD}.json`

**只读取此文件，不读取同目录下任何其他文件。**

## 工作流

### Step 1: 解析日期

```bash
date -v-1d +%Y-%m-%d
```

固定读取昨天的数据。

### Step 2: 读取数据

构造路径 `/Users/babyowen/.claude/skills/bank-news-collector/data/{date}.json`，用 Read 工具读取。

- 若文件不存在：报告"昨日无数据"，终止
- 若 JSON 为空数组 `[]`：生成"昨日无新闻"的简短报告
- 正常：记录条目总数 N

### Step 3: 加载参考文件

依次读取（路径相对于本 skill 目录）：
1. `references/report-template.md` — 报告结构、格式规范、字数限制
2. `references/persona-guide.md` — 人设、写作风格

### Step 4: 生成报告

按 report-template.md 生成三部分报告，**全文不超过1000字**：

1. **今日综述**（150-200字）：2-3句概括当天核心主题
2. **行业动态**（400-500字）：按主题分段归纳，段落式写作，不逐条列举
3. **经营启示**（250-350字）：自然流畅的分析和建议，像晨会备忘录而非填表

### Step 5: 发送到飞书

通过 `lark-im` 技能将报告发送到飞书对话 `oc_578717a43c0e5011765d9cada71d8218`。

使用 lark-im skill 的 `+send` 命令，`--markdown` 参数发送。

## 硬约束

1. **只读 JSON**：仅从 `{date}.json` 读取，不读同目录其他文件
2. **1000字以内**：全文（含标题落款）不超过1000字
3. **准确性**：不编造 JSON 中不存在的事实和数据
4. **无空话**：遵循 persona-guide.md 的反套话规则
5. **自然流畅**：Part 3 像正常报告，不用"发生了什么""意味着什么"等模板小标题

## Resources

### references/report-template.md
报告结构、格式规范、字数限制和写作示例。生成报告前必读。

### references/persona-guide.md
人设定义和写作风格。撰写前必读。
