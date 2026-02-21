# PPT 大纲结构规范

## 标题幻灯片
```yaml
type: title
title: "演示标题"
subtitle: "副标题或描述"
author: "作者姓名"
date: "日期"
```

## 内容幻灯片（列表）
```yaml
type: content
title: "幻灯片标题"
points:
  - "要点一"
  - "要点二"
  - "要点三"
```

## 双栏幻灯片
```yaml
type: two-column
title: "幻灯片标题"
left_column:
  title: "左栏标题"
  content: "左栏内容文本"
right_column:
  title: "右栏标题"
  content: "右栏内容文本"
```

## 图片幻灯片
```yaml
type: image
title: "幻灯片标题"
image_url: "图片URL或本地路径"
caption: "图片说明（可选）"
```

## 引用幻灯片
```yaml
type: quote
quote: "引用的内容文本"
author: "引用来源"
```

## 代码幻灯片
```yaml
type: code
title: "幻灯片标题"
language: "编程语言"
code: |
  代码内容
  可以是多行
```

## 完整示例

```yaml
slides:
  - type: title
    title: "产品介绍"
    subtitle: "打造下一代用户体验"
    author: "产品团队"

  - type: content
    title: "核心特性"
    points:
      - "高性能 - 毫秒级响应"
      - "易用性 - 零学习曲线"
      - "可扩展 - 灵活的插件系统"

  - type: two-column
    title: "技术架构"
    left_column:
      title: "前端"
      content: "React + TypeScript 构建的用户界面"
    right_column:
      title: "后端"
      content: "Node.js + GraphQL API 服务"

  - type: quote
    quote: "简单是复杂的终极形式"
    author: "Leonardo da Vinci"

  - type: code
    title: "快速开始"
    language: "javascript"
    code: |
      import { App } from 'my-app';

      const app = new App();
      app.start();
```

## 设计建议

### 颜色方案
- 主色: #667eea (紫蓝渐变)
- 强调色: #764ba2
- 背景色: #1a1a2e
- 文字色: #ffffff, #d0d0e0

### 动画效果
- 标题: scaleIn 缩放进入
- 列表项: slideInLeft 左侧滑入
- 图片: fadeInUp 上移淡入

### 布局原则
- 每张幻灯片最多 5-7 个要点
- 保持足够的留白
- 使用一致的间距和对齐
