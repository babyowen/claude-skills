---
name: lixinger
description: "理杏仁开放平台 A 股金融数据查询 Skill。提供 A 股公司基本面、财务报表、K 线、股东信息、龙虎榜、热度数据、资金流向等 40+ 个接口的统一查询能力。内置限流和重试机制。当用户需要查询 A 股股票数据、财务指标、行情数据、股东变动、公告信息、监管信息、分红配送等时使用。支持自然语言描述需求，由本 Skill 翻译成具体的 API 调用。"
---

# lixinger — 理杏仁 A 股数据查询

## 触发条件

当用户提到以下场景时触发本 Skill：
- 查询 A 股股票数据（PE、PB、市值、K 线等）
- 查询公司基本面、财务报表
- 查询股东信息、增减持、龙虎榜
- 查询公告、监管措施、问讯函
- 查询分红配送、营收构成
- 查询热度数据（换手率、融资融券、互联互通等）
- 查询资金流向

## 前置要求

### Token 配置

API Token 通过环境变量传入，**不要硬编码在代码或配置中**：

```bash
export LIXINGER_TOKEN="your-token-here"
```

### 脚本路径

核心调用脚本位于：`scripts/lixinger.py`

## 核心工作流

### 步骤 1：理解用户需求

用户通常用自然语言表达需求，如：
- "查一下茅台和宁德时代的 PE、PB"
- "我想看 600519 最近一年的 K 线"
- "看看 300750 的前十大股东"

将自然语言需求拆解为：
1. **目标数据类型** → 对应 API endpoint
2. **股票代码** → stockCodes / stockCode
3. **时间范围** → date / startDate / endDate
4. **具体指标** → metricsList（仅基本面/热度数据需要）

### 步骤 2：确定 Endpoint

根据数据类型选择接口路径：

| 需求类型 | Endpoint | 关键参数 |
|----------|----------|----------|
| 基本面指标（PE、PB、市值等） | `cn/company/fundamental/non_financial` | `stockCodes`, `date`, `metricsList` |
| 公司概况 | `cn/company/profile` | `stockCodes` |
| K 线数据 | `cn/company/candlestick` | `stockCode`, `startDate`, `endDate`, `type` |
| 前十大股东 | `cn/company/majority-shareholders` | `stockCode` (单数) |
| 前十大流通股东 | `cn/company/nolimit-shareholders` | `stockCode` (单数) |
| 龙虎榜明细 | `cn/company/trading-abnormal` | `date` |
| 公告 | `cn/company/announcement` | `stockCode` (单数), `date` |
| 财务报表 | `cn/company/fs/non_financial` | `stockCodes`, `date`, `metricsList` |
| 热度汇总指标 | `cn/company/hot/...` | `stockCodes` |
| 股权质押明细 | `cn/company/pledge` | `stockCode` (单数) |
| 大宗交易 | `cn/company/block-deal` | `date` |
| 营收构成 | `cn/company/operation-revenue-constitution` | `stockCode` (单数) |
| 资金流向-互联互通 | `cn/company/mutual-market` | `date` |
| 资金流向-融资融券 | `cn/company/margin-trading-and-securities-lending` | `stockCode` (单数) |

> 完整接口列表见 `scripts/lixinger.py list-endpoints` 或 [`references/api_endpoints.md`](references/api_endpoints.md)

### 步骤 3：构造请求并调用

**单接口调用（推荐）**：

```bash
python scripts/lixinger.py call \
  --endpoint cn/company/fundamental/non_financial \
  --data '{"stockCodes":["600519"],"date":"2026-03-10","metricsList":["pe_ttm","pb"]}' \
  --pretty
```

**批量调用**：

```bash
python scripts/lixinger.py batch \
  --endpoint cn/company/fundamental/non_financial \
  --data-file requests.json \
  --pretty
```

其中 `requests.json` 格式为 JSON 数组：
```json
[
  {"stockCodes": ["600519"], "date": "2026-03-10", "metricsList": ["pe_ttm"]},
  {"stockCodes": ["300750"], "date": "2026-03-10", "metricsList": ["pe_ttm"]}
]
```

### 步骤 4：处理返回结果

返回格式统一为：
```json
{
  "code": 1,
  "message": "success",
  "data": [...]
}
```

- `code == 1` 表示成功
- `data` 为数组，每个元素对应一只股票的数据
- 直接返回原始 JSON 给用户，不做额外格式化

## 关键约束

### 限流规则

- **每秒最多 36 次请求**
- **每分钟最多 1000 次请求**
- 超过返回 HTTP 429 (Too Many Requests)
- 脚本已内置限流器和指数退避重试，调用方无需额外处理

### 股票代码限制

- `stockCodes` 数组长度：**1 ≤ len ≤ 100**
- 超过 100 需分批调用

### 日期格式

- 统一使用 `YYYY-MM-DD`，如 `"2026-03-10"`

### 复权类型（K线）

| type 值 | 说明 |
|---------|------|
| `lxr_fc_rights` | 前复权（默认推荐） |
| `lxr_bc_rights` | 后复权 |
| `none` | 不复权 |

## 公司接口 vs 热度数据 的区别

**重要**：部分数据在两个分类下都有接口，但数据粒度不同：

| 数据主题 | 公司接口（明细） | 热度数据（汇总） |
|----------|------------------|------------------|
| 龙虎榜 | `trading-abnormal` — 某一天的买卖营业部明细 | `hot/t_a` — 各时间段净买入汇总统计 |
| 大股东增减持 | `major-shareholders-shares-change` — 具体增减持记录 | `hot/mssc` — 各时间段增减持金额汇总 |
| 高管增减持 | `senior-executive-shares-change` — 具体增减持记录 | `hot/esc` — 各时间段增减持金额汇总 |
| 融资融券 | `margin-trading-and-securities-lending` — 每日明细 | `hot/mtasl` — 各时间段汇总统计 |
| 互联互通 | `mutual-market` — 每日资金流向明细 | `hot/mm_ha` — 各时间段汇总统计 |
| 股权质押 | `pledge` — 具体质押记录 | `hot/ple` — 汇总统计 |

**选择建议**：
- 需要**具体事件/明细** → 用公司接口
- 需要**多时间段汇总对比** → 用热度数据

## 金融板块适配

理杏仁按行业类型提供不同的基本面和财务报表接口：

| 行业类型 | 基本面接口 | 财务报表接口 |
|----------|-----------|-------------|
| 非金融 | `fundamental/non_financial` | `fs/non_financial` |
| 银行 | `fundamental/bank` | `fs/bank` |
| 证券 | `fundamental/security` | `fs/security` |
| 保险 | `fundamental/insurance` | `fs/insurance` |
| 其他金融 | `fundamental/other_financial` | `fs/other_financial` |

查询前需确认目标股票所属行业类型，选择对应接口。

### 智能路由（自动识别行业类型）

脚本内置了智能路由功能，可自动根据股票的行业分类选择正确的子接口：

```bash
# 智能路由 - 基本面数据
python scripts/lixinger.py smart-fundamental \
  --data '{"stockCodes":["600519","600036"],"date":"2026-04-17","metricsList":["pe_ttm","pb"]}' \
  --pretty

# 智能路由 - 财务报表
python scripts/lixinger.py smart-fs \
  --data '{"stockCodes":["600519","600036"],"date":"2025-09-30","metricsList":["q.ps.toi.t","q.ps.np.t"]}' \
  --pretty
```

**工作原理**：
1. 首次查询某股票时，调用 `industries` 接口获取申万行业分类
2. 根据行业名称自动推断类型：银行 → `bank`、证券 → `security`、保险 → `insurance`、多元金融 → `other_financial`、其他 → `non_financial`
3. 按类型分组调用对应子接口，合并返回结果
4. 推断结果缓存到 `~/.cache/lixinger/company_types.json`，后续查询直接复用

**适用场景**：
- 混合查询多只股票（如同时查茅台和招商银行）
- 不确定股票所属行业类型时
- 自动化脚本中避免手动维护类型映射

## metricsList 常用指标速查

基本面和热度数据接口通过 `metricsList` 指定需要的指标字段。常见指标：

### `fundamental/*` 接口指标（估值类）

| 指标代码 | 含义 |
|----------|------|
| `pe_ttm` | 市盈率 TTM |
| `pb` | 市净率 |
| `ps_ttm` | 市销率 TTM |
| `pcf_ttm` | 市现率 TTM |
| `mc` | 总市值 |
| `pe_ttm.y3.cvpos` | PE 近3年历史分位 |
| `pe_ttm.y5.cvpos` | PE 近5年历史分位 |
| `pb.y3.cvpos` | PB 近3年历史分位 |
| `pb.y5.cvpos` | PB 近5年历史分位 |

### `fs/*` 接口指标（财务指标类）

需通过财务报表接口查询，格式为 `[粒度].[表名].[字段名].[计算类型]`：

| 指标代码 | 含义 |
|----------|------|
| `q.m.roe.t` | 季度净资产收益率 |
| `q.m.roic.t` | 季度投入资本回报率 |
| `q.m.gp_m.t` | 季度毛利率 |
| `q.m.np_s_r.t` | 季度净利率 |
| `q.bs.ta.t` | 季度资产总计 |
| `q.bs.tl.t` | 季度负债合计 |
| `q.ps.toi.t` | 季度营业总收入 |
| `q.ps.np.t` | 季度净利润 |

> 完整指标列表请参考 [`references/api_endpoints.md`](references/api_endpoints.md)

## 给其他 Skill 的调用指南

当其他 Skill 需要调用本 Skill 时：

1. **读取 SKILL.md** 理解接口分类和约束
2. **如需详细参数** → 读取 `references/api_endpoints.md`
3. **使用 Bash 调用脚本**：
   ```bash
   python /path/to/lixinger/scripts/lixinger.py call \
     --endpoint cn/company/profile \
     --data '{"stockCodes":["600519"]}'
   ```
4. **解析返回的 JSON**，提取所需数据
5. **Token 由调用方确保环境变量已设置**

**不要**直接用 curl 调用 API（会绕过脚本的限流保护）。

## 参数格式重要说明

**经实际测试验证**，以下接口的参数与官方文档标注不一致，以本 Skill 为准：

### 使用 `stockCode`（单数）的接口

以下接口实际接受单只股票代码，**不是** `stockCodes` 数组：

- `cn/company/candlestick`
- `cn/company/announcement`
- `cn/company/majority-shareholders`
- `cn/company/nolimit-shareholders`
- `cn/company/fund-shareholders`
- `cn/company/fund-collection-shareholders`
- `cn/company/dividend`
- `cn/company/allotment`
- `cn/company/customers`
- `cn/company/suppliers`
- `cn/company/indices`
- `cn/company/industries`
- `cn/company/pledge`
- `cn/company/shareholders-num`
- `cn/company/operating-data`
- `cn/company/operation-revenue-constitution`
- `cn/company/margin-trading-and-securities-lending`
- `cn/company/equity-change`
- `cn/company/senior-executive-shares-change`
- `cn/company/major-shareholders-shares-change`

### 使用 `date`（按日期查询）的接口

以下接口**按日期查询**，返回当日所有股票数据：

- `cn/company/trading-abnormal` — 龙虎榜明细
- `cn/company/block-deal` — 大宗交易
- `cn/company/mutual-market` — 互联互通资金流向

### 使用 `startDate` + `stockCode`（单数）的接口

以下接口**按股票+日期范围查询**，需同时提供 `stockCode` 和 `startDate`（可选 `endDate`）：

- `cn/company/measures` — 监管措施
- `cn/company/inquiry` — 问讯函

> 完整参数速查表见 [`references/api_endpoints.md` 附录A](references/api_endpoints.md#附录a接口参数格式速查表)
