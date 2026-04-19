# 理杏仁 A 股接口详细文档

> 本文档包含所有 A 股公司接口的详细参数和返回说明。
> 基础 URL: `https://open.lixinger.com/api`
> 请求方式: **POST**
> Headers: `Content-Type: application/json`, `Accept-Encoding: gzip, deflate, br`

---

## 通用返回格式

所有接口返回统一格式：

```json
{
  "code": 1,
  "message": "success",
  "data": []
}
```

- `code`: `1` 表示成功，其他值表示失败
- `message`: 状态描述
- `data`: 业务数据数组

---

## 一、公司接口 — 基础信息（基本面数据）

### 1.1 非金融基本面

**Endpoint**: `cn/company/fundamental/non_financial`

**说明**: 获取非金融行业公司的基本面指标，如 PE、PB、市值、ROE 等。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCodes | Yes | Array[String] | 股票代码数组，1-100个 |
| date | Yes | String | 日期，格式 `YYYY-MM-DD` |
| metricsList | Yes | Array[String] | 指标代码列表 |

**常用指标**（估值类）：

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

> **注意**：`roe`、`roa`、`毛利率`、`净利率`、`资产负债率` 等财务指标**不在** `fundamental` 接口中，需通过 `fs/*` 财务报表接口查询（如 `q.m.roe.t`、`q.m.gp_m.t` 等）。

**请求示例**:

```json
{
  "date": "2026-03-10",
  "stockCodes": ["300750", "600519", "600157"],
  "metricsList": ["pe_ttm", "mc", "pe_ttm.y3.cvpos"],
  "token": "your-token"
}
```

**返回示例**:

```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "date": "2026-03-10T00:00:00+08:00",
      "mc": 1717383888142.8,
      "pe_ttm": 23.7861,
      "stockCode": "300750",
      "pe_ttm.y3.cvpos": 0.6238
    },
    {
      "date": "2026-03-10T00:00:00+08:00",
      "mc": 1755532569004.2002,
      "pe_ttm": 19.5,
      "stockCode": "600519",
      "pe_ttm.y3.cvpos": 0.0263
    }
  ]
}
```

### 1.2 银行基本面

**Endpoint**: `cn/company/fundamental/bank`

**说明**: 银行行业专用基本面指标。参数格式同非金融，但可用指标不同（如 `npl_ratio` 不良贷款率、`nim` 净息差等）。

### 1.3 证券基本面

**Endpoint**: `cn/company/fundamental/security`

### 1.4 保险基本面

**Endpoint**: `cn/company/fundamental/insurance`

### 1.5 其他金融基本面

**Endpoint**: `cn/company/fundamental/other_financial`

---

## 二、公司接口 — 公司概况

### 2.1 公司概况

**Endpoint**: `cn/company/profile`

**说明**: 获取公司基本信息，包括公司名称、所属城市/省份、实际控制人、历史更名记录等。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCodes | Yes | Array[String] | 股票代码数组，1-100个 |

**请求示例**:

```json
{
  "stockCodes": ["300750", "600519", "600157"],
  "token": "your-token"
}
```

**返回字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stockCode | String | 股票代码 |
| companyName | String | 公司全称 |
| city | String | 所在城市 |
| province | String | 所在省份 |
| actualControllerName | String | 实际控制人名称 |
| actualControllerTypes | Array[String] | 实际控制人类型 |
| historyStockNames | Array | 历史更名记录 |

**返回示例**:

```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "city": "宁德市",
      "province": "福建",
      "companyName": "宁德时代新能源科技股份有限公司",
      "historyStockNames": [],
      "stockCode": "300750",
      "actualControllerTypes": ["natural_person"],
      "actualControllerName": "曾毓群"
    }
  ]
}
```

---

## 三、公司接口 — 股本与股东

### 3.1 股本变动

**Endpoint**: `cn/company/equity-change`

**说明**: 获取公司股本变动历史记录，包括增发、配股、送转股等。

### 3.2 股东人数

**Endpoint**: `cn/company/shareholders-num`

**说明**: 获取公司股东人数变化数据。

### 3.3 高管增减持明细

**Endpoint**: `cn/company/senior-executive-shares-change`

**说明**: 获取高管增减持的具体交易记录。

### 3.4 大股东增减持明细

**Endpoint**: `cn/company/major-shareholders-shares-change`

**说明**: 获取大股东增减持的具体交易记录。

---

## 四、公司接口 — 交易信息

### 4.1 K 线数据

**Endpoint**: `cn/company/candlestick`

**说明**: 获取指定股票在指定时间范围内的 K 线数据。复权计算仅对所选时间段的价格进行复权，成交量不进行复权。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCode | Yes | String | 单只股票代码 |
| startDate | Yes | String | 开始日期 `YYYY-MM-DD` |
| endDate | Yes | String | 结束日期 `YYYY-MM-DD` |
| type | Yes | String | 复权类型 |

**type 取值**:

| 值 | 说明 |
|----|------|
| `lxr_fc_rights` | 前复权 |
| `lxr_bc_rights` | 后复权 |
| `none` | 不复权 |

**请求示例**:

```json
{
  "type": "lxr_fc_rights",
  "startDate": "2025-03-20",
  "endDate": "2026-03-20",
  "stockCode": "300750",
  "token": "your-token"
}
```

**返回字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| date | Date | 交易日期 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量（股） |
| amount | Number | 成交额（元） |
| change | Number | 涨跌幅 |
| stockCode | String | 股票代码 |
| to_r | Number | 换手率 |

### 4.2 龙虎榜明细

**Endpoint**: `cn/company/trading-abnormal`

**说明**: 获取某一天的龙虎榜详细数据，包括买卖前五营业部、机构买卖金额等。**按日期查询**，返回当日所有上榜股票。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| date | Yes | String | 日期 `YYYY-MM-DD` |

**返回字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| date | Date | 上榜日期 |
| stockCode | String | 股票代码 |
| reasonForDisclosure | String | 上榜原因 |
| totalPurchaseAmount | Number | 总买入金额 |
| totalSellAmount | Number | 总卖出金额 |
| totalNetPurchaseAmount | Number | 总净买入金额 |
| institutionBuyAmount | Number | 机构买入金额 |
| institutionSellAmount | Number | 机构卖出金额 |
| institutionNetPurchaseAmount | Number | 机构净买入金额 |
| institutionBuyCount | Number | 机构买入家数 |
| institutionSellCount | Number | 机构卖出家数 |
| buyList | Array | 买入前五营业部 |
| sellList | Array | 卖出前五营业部 |

**buyList / sellList 元素字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| branchName | String | 营业部名称 |
| buyAmount | Number | 买入金额 |
| sellAmount | Number | 卖出金额 |
| isInstitution | Boolean | 是否为机构专用 |

### 4.3 大宗交易

**Endpoint**: `cn/company/block-deal`

**说明**: 获取大宗交易记录。

### 4.4 股权质押明细

**Endpoint**: `cn/company/pledge`

**说明**: 获取股权质押的具体记录。

---

## 五、公司接口 — 经营信息

### 5.1 营收构成

**Endpoint**: `cn/company/operation-revenue-constitution`

**说明**: 获取公司营收构成明细，按产品/地区/行业等维度拆分。

### 5.2 经营数据

**Endpoint**: `cn/company/operating-data`

**说明**: 获取公司经营数据。

---

## 六、公司接口 — 分类信息

### 6.1 股票所属指数

**Endpoint**: `cn/company/indices`

**说明**: 查询股票所属的指数成分股信息。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCode | Yes | String | 单只股票代码 |

### 6.2 股票所属行业

**Endpoint**: `cn/company/industries`

**说明**: 查询股票所属的行业分类（申万、中信等）。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCode | Yes | String | 单只股票代码 |

---

## 七、公司接口 — 公告

### 7.1 公告

**Endpoint**: `cn/company/announcement`

**说明**: 获取公司公告列表。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCode | Yes | String | 单只股票代码 |
| date | No | String | 日期 `YYYY-MM-DD` |

---

## 八、监管信息

### 8.1 监管措施

**Endpoint**: `cn/company/measures`

**说明**: 获取公司收到的监管措施信息。

### 8.2 问讯函

**Endpoint**: `cn/company/inquiry`

**说明**: 获取公司收到的问讯函信息。

---

## 九、股东信息

### 9.1 前十大股东

**Endpoint**: `cn/company/majority-shareholders`

**说明**: 获取公司前十大股东持股信息。

**参数**:

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| token | Yes | String | API Token |
| stockCode | Yes | String | 单只股票代码 |

### 9.2 前十大流通股东

**Endpoint**: `cn/company/nolimit-shareholders`

**说明**: 获取公司前十大流通股东持股信息。

**参数**: `stockCode` (String, 单只股票代码)

### 9.3 公募基金持股

**Endpoint**: `cn/company/fund-shareholders`

**说明**: 获取公募基金持仓信息。

### 9.4 基金公司持股

**Endpoint**: `cn/company/fund-collection-shareholders`

**说明**: 获取基金公司持仓信息。

---

## 十、分红送配

### 10.1 分红

**Endpoint**: `cn/company/dividend`

**说明**: 获取公司分红历史记录。

### 10.2 配送

**Endpoint**: `cn/company/allotment`

**说明**: 获取公司配股/送转历史记录。

---

## 十一、客户及供应商

### 11.1 客户

**Endpoint**: `cn/company/customers`

**说明**: 获取公司主要客户信息。

### 11.2 供应商

**Endpoint**: `cn/company/suppliers`

**说明**: 获取公司主要供应商信息。

---

## 十二、财务报表

> 按行业类型分为 5 个接口，参数和返回结构与基本面数据类似。

### 12.1 非金融财务报表

**Endpoint**: `cn/company/fs/non_financial`

### 12.2 银行财务报表

**Endpoint**: `cn/company/fs/bank`

### 12.3 证券财务报表

**Endpoint**: `cn/company/fs/security`

### 12.4 保险财务报表

**Endpoint**: `cn/company/fs/insurance`

### 12.5 其他金融财务报表

**Endpoint**: `cn/company/fs/other_financial`

---

## 十三、热度数据

> 热度数据接口提供汇总统计指标，**按 stockCodes 查询**，返回各时间段（最新/1月/3月/6月/1年/2年/3年）的汇总数据。

### 13.1 分红再投入收益率

**Endpoint**: `cn/company/hot/tr_dri`

### 13.2 互联互通（热度汇总）

**Endpoint**: `cn/company/hot/mm_ha`

**说明**: 各时间段互联互通资金流入流出汇总。

### 13.3 融资融券（热度汇总）

**Endpoint**: `cn/company/hot/mtasl`

**说明**: 各时间段融资融券余额变化汇总。

### 13.4 高管增减持（热度汇总）

**Endpoint**: `cn/company/hot/esc`

**说明**: 各时间段高管增减持金额汇总。

### 13.5 大股东增减持（热度汇总）

**Endpoint**: `cn/company/hot/mssc`

**说明**: 各时间段大股东增减持金额汇总。返回字段示例：

| 字段名 | 说明 |
|--------|------|
| last_data_date | 最新数据日期 |
| mssca_last | 最新增减持金额 |
| mssca_m6 | 近6月增减持金额 |
| mssca_y1 | 近1年增减持金额 |
| mssca_y2 | 近2年增减持金额 |
| mssca_y3 | 近3年增减持金额 |
| msscm_last | 最新增减持市值 |
| mssc_cap_rc_last | 最新占流通市值比 |

### 13.6 龙虎榜（热度汇总）

**Endpoint**: `cn/company/hot/t_a`

**说明**: 各时间段龙虎榜净买入汇总。

**返回字段**:

| 字段名 | 说明 |
|--------|------|
| last_data_date | 最新数据日期 |
| tatnpa_last | 最新龙虎榜总净买入金额 |
| tainpa_last | 最新龙虎榜机构净买入金额 |
| tatnpa_m1 | 过去1个月总净买入 |
| tatnpa_m3 | 过去3个月总净买入 |
| tatnpa_m6 | 过去6个月总净买入 |
| tatnpa_y1 | 过去1年总净买入 |
| tainpa_m1 | 过去1个月机构净买入 |
| tainpa_m3 | 过去3个月机构净买入 |
| tainpa_m6 | 过去6个月机构净买入 |
| tainpa_y1 | 过去1年机构净买入 |

### 13.7 限售解禁

**Endpoint**: `cn/company/hot/elr`

### 13.8 股权质押（热度汇总）

**Endpoint**: `cn/company/hot/ple`

### 13.9 人均指标

**Endpoint**: `cn/company/hot/capita`

### 13.10 股东人数变化

**Endpoint**: `cn/company/hot/shnc`

### 13.11 分红融资

**Endpoint**: `cn/company/hot/df`

### 13.12 派息

**Endpoint**: `cn/company/hot/npd`

### 13.13 换手率

**Endpoint**: `cn/company/hot/tr`

---

## 十四、资金流向

### 14.1 互联互通（资金流向明细）

**Endpoint**: `cn/company/mutual-market`

**说明**: 获取每日互联互通资金流向明细。**按日期查询**。

### 14.2 融资融券（资金流向明细）

**Endpoint**: `cn/company/margin-trading-and-securities-lending`

**说明**: 获取每日融资融券余额明细。**按日期查询**。

---

## 附录：接口分类总表

| 分类 | 接口数 | 说明 |
|------|--------|------|
| 基础信息（基本面） | 5 | 非金融/银行/证券/保险/其他金融 |
| 公司概况 | 1 | 公司基本信息 |
| 股本与股东 | 4 | 股本变动、股东人数、高管/大股东增减持 |
| 交易信息 | 4 | K线、龙虎榜明细、大宗交易、股权质押明细 |
| 经营信息 | 2 | 营收构成、经营数据 |
| 分类信息 | 2 | 所属指数、所属行业 |
| 公告 | 1 | 公司公告 |
| 监管信息 | 2 | 监管措施、问讯函 |
| 股东信息 | 4 | 前十大股东/流通股东、公募基金/基金公司持股 |
| 分红送配 | 2 | 分红、配送 |
| 客户及供应商 | 2 | 客户、供应商 |
| 财务报表 | 5 | 非金融/银行/证券/保险/其他金融 |
| 热度数据 | 13 | 各类汇总统计指标 |
| 资金流向 | 2 | 互联互通、融资融券明细 |
| **合计** | **43** | |

---

## 附录A：接口参数格式速查表

> 经实际测试验证的参数格式。部分接口与官方文档标注不一致，以下表为准。

### 使用 stockCodes（数组，可多股批量查询）

| 接口 | 额外必填参数 |
|------|-------------|
| `cn/company/fundamental/*` (5个) | `date`, `metricsList` |
| `cn/company/profile` | 无 |
| `cn/company/fs/*` (5个) | `date`, `metricsList` |
| `cn/company/hot/*` (13个) | 无 |

### 使用 stockCode（单数，仅查一只股票）

| 接口 | 额外必填参数 |
|------|-------------|
| `cn/company/candlestick` | `startDate`, `endDate`, `type` |
| `cn/company/announcement` | 无（可选 `date`） |
| `cn/company/majority-shareholders` | 无 |
| `cn/company/nolimit-shareholders` | 无 |
| `cn/company/fund-shareholders` | 无 |
| `cn/company/fund-collection-shareholders` | 无 |
| `cn/company/dividend` | 无 |
| `cn/company/allotment` | 无 |
| `cn/company/customers` | 无 |
| `cn/company/suppliers` | 无 |
| `cn/company/indices` | 无 |
| `cn/company/industries` | 无 |
| `cn/company/pledge` | 无 |
| `cn/company/shareholders-num` | 无 |
| `cn/company/operating-data` | 无 |
| `cn/company/operation-revenue-constitution` | 无 |
| `cn/company/margin-trading-and-securities-lending` | 无 |
| `cn/company/equity-change` | 无 |
| `cn/company/senior-executive-shares-change` | 无 |
| `cn/company/major-shareholders-shares-change` | 无 |

### 使用 startDate + stockCode（单数，按股票+日期范围查询）

| 接口 | 说明 |
|------|------|
| `cn/company/measures` | 监管措施 |
| `cn/company/inquiry` | 问讯函 |

### 使用 date（按日期查询，返回当日所有股票）

| 接口 | 说明 |
|------|------|
| `cn/company/trading-abnormal` | 龙虎榜明细 |
| `cn/company/block-deal` | 大宗交易 |
| `cn/company/mutual-market` | 互联互通资金流向 |

---

## 附录B：财务报表(fs)接口指标格式

### 指标命名格式

`[粒度].[表名].[字段名].[计算类型]`

**粒度 (granularity)**:
- `y` - 年报
- `hy` - 半年报
- `q` - 季报

**表名 (tableName)**:
- `bs` - 资产负债表 (Balance Sheet)
- `ps` - 利润表 (Profit Statement)
- `cfs` - 现金流量表 (Cash Flow Statement)
- `m` - 财务指标 (Metrics)

**计算类型 (expressionCalculateType)**:

资产负债表：
- `t` - 当期 / 年:当期, 半年:当期, 季度:当期
- `t_r` - 当期回溯值
- `t_y2y` - 当期同比
- `t_c2c` - 当期环比（官方定义存在，实测中年报及部分季报累积值不返回）
- `c` - 半年/单季（适用于 hy/q）
- `c_r` - 半年/单季回溯值
- `c_y2y` - 半年/单季同比
- `c_c2c` - 半年/单季环比

利润表：
- `t` - 累积（适用于 y/hy/q 年报/半年报/季报）
- `t_r` - 累积回溯值
- `t_y2y` - 累积同比
- `t_c2c` - 累积环比
- `c` - 半年/单季
- `c_r` - 半年/单季回溯值
- `c_y2y` - 半年/单季同比
- `c_c2c` - 半年/单季环比
- `c_2y` - 半年/单季年比
- `ttm` - TTM
- `ttm_y2y` - TTM同比
- `ttm_c2c` - TTM环比

现金流量表：同利润表

### 常用指标示例

| 指标代码 | 含义 |
|----------|------|
| `q.ps.toi.t` | 季度营业总收入(累积) |
| `q.ps.np.t` | 季度净利润(累积) |
| `q.ps.gp_m.t` | 季度毛利率 |
| `q.ps.op.t` | 季度营业利润(累积) |
| `q.ps.npatoshopc.t` | 季度归母净利润(累积) |
| `q.ps.beps.t` | 季度基本每股收益(累积) |
| `q.bs.ta.t` | 季度资产总计 |
| `q.bs.tl.t` | 季度负债合计 |
| `q.bs.toe.t` | 季度所有者权益合计 |
| `q.bs.cabb.t` | 季度货币资金 |
| `q.bs.sc.t` | 季度股本 |
| `q.cfs.ncffoa.t` | 季度经营活动现金流净额(累积) |
| `q.m.fcf.t` | 季度自由现金流量（财务指标表，非现金流量表） |
| `y.ps.toi.t` | 年报营业总收入 |
| `y.ps.np.t` | 年报净利润 |
| `y.bs.ta.t` | 年报资产总计 |
| `q.m.roe.t` | 季度ROE |
| `q.m.wroe.t` | 季度加权ROE |
| `q.m.roic.t` | 季度ROIC |
| `q.m.gp_m.t` | 季度毛利率(同上) |
| `q.m.np_s_r.t` | 季度净利润率 |

### 请求示例

```json
{
  "date": "2025-09-30",
  "stockCodes": ["600519"],
  "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.bs.ta.t"],
  "token": "your-token"
}
```

### 返回示例

```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "date": "2025-09-30T00:00:00+08:00",
      "currency": "CNY",
      "q": {
        "ps": {
          "toi": { "t": 130903889635 },
          "np": { "t": 60828385633 }
        },
        "bs": {
          "ta": { "t": 298934537683 }
        }
      },
      "reportDate": "2025-10-30T00:00:00+08:00",
      "reportType": "third_quarterly_report",
      "standardDate": "2025-09-30T00:00:00+08:00",
      "stockCode": "600519"
    }
  ]
}
```

**注意**: fs 接口返回数据为嵌套结构 `data[].q.bs.ta.t`，而非 `data[].total_assets` 等扁平字段。
