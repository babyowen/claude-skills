# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**Slide Craft** - 智能演示文稿生成器，将 Markdown/文本大纲转换为 HTML（GSAP动画）和 PowerPoint 双格式输出。

## 常用命令

```bash
# 开发模式
npm run dev

# 生成 HTML（输出到 dist/index.html）
npm run build

# 生成 PPTX（输出到 dist/presentation.pptx）
npm run build:pptx

# 同时生成 HTML 和 PPTX
npm run build:all

# 预览构建结果
npm run preview
```

## 架构设计

### 核心流程

```
输入（Markdown/文本）
  ↓
markdown-parser.js（解析输入）
  ↓
content-analyzer.js（分析内容特征）
  ↓
template-mapper.js（映射到6种核心模板）
  ↓
presentation-builder.js（构建流程编排）
  ↓
双输出：
  - html-generator.js → Vite构建 → dist/index.html
  - pptx-exporter.js → scripts/export-pptx.js → dist/presentation.pptx
```

### 6种核心布局模板

1. **封面页** (title-slide) - 固定设计，遵循品牌规范
2. **左右分栏** (left-right-split) - 项目介绍、对比
3. **三栏并列** (three-column) - 多维度展示、团队介绍
4. **中心辐射** (center-radial) - 核心能力、工作重点
5. **横向流程** (horizontal-process) - 项目进展、工作流程
6. **数据总结** (data-summary) - 成果汇报、年度总结

### 智能模板匹配策略

`content-analyzer.js` 通过以下特征自动选择模板：
- 步骤/流程关键词 → 横向流程
- 3个并列主题 → 三栏并列
- 5-6个子项围绕核心 → 中心辐射
- 数据+百分比 → 数据总结
- 背景图+多模块 → 左右分栏

### 混合生成策略

- **优先级1**: 匹配6种核心模板（覆盖率80%）
- **优先级2**: 特殊内容基于 `references/design-system.md` 自由生成
- 所有布局遵循统一的设计令牌系统（`design-tokens.js`）

## 关键文件说明

### `/src/lib/` 核心模块

- **markdown-parser.js**: 解析 Markdown 和纯文本，提取标题、列表、图片
- **content-analyzer.js**: 内容特征分析 + 模板匹配算法
- **template-mapper.js**: 将内容映射到模板数据结构，定义每种模板的配置
- **presentation-builder.js**: 主构建流程，协调解析→分析→映射→优化
- **html-generator.js**: 生成 HTML 代码（含 GSAP 动画）
- **pptx-exporter.js**: 生成 PPTX 文件（调用 PptxGenJS）
- **design-tokens.js**: 统一设计令牌（中信配色、字体、间距）
- **image-handler.js**: 图片处理和 Base64 转换

### `/scripts/export-pptx.js`

独立的 Node.js 脚本，读取 `presentation.md`，调用 PresentationBuilder 和 PPTXExporter 生成 PPTX。

### `/references/`

- **design-system.md**: 完整设计规范（颜色、字体、间距、组件）
- **professional-ppt-guide.md**: 商务PPT设计指南

## 设计系统约束

### 固定封面设计

封面页必须严格遵循以下规范（**不可更改**）：

- Logo（`assets/logo.png`）- 左上角，60px
- Slogan（`assets/slogon.png`）- 右上角，60px
- 背景图（`assets/fm-background.png`）- 全屏，opacity 0.5
- 主标题：楷体，4rem，加粗，黑色，左对齐，左缩进10%
- 副标题：楷体，1.8rem，常规
- 日期：楷体，1.5rem

### 中信配色方案（固定）

```
中信红 (Primary): #D20A10
标准灰五: #575757（深色文字）
标准灰四: #898989（次要文字）
标准灰三: #B5B5B5（边框）
标准灰二: #CACACA（卡片背景）
标准灰一: #DDDDDD（页面背景）
```

所有颜色定义在 `design-tokens.js` 中，确保 HTML 和 PPTX 视觉一致。

## 内容完整性原则

**必须包含所有用户提供的内容**：
- 不得省略或简化任何要点
- 内容过长时自动拆分为多张幻灯片
- 三栏并列：最多3个模块，超过则拆分
- 横向流程：最多6步，超过则拆分
- 列表内容：最多8项，超过则拆分

拆分逻辑在 `presentation-builder.js:optimizeContent()` 中实现。

## 图片处理

- 使用相对路径 `./assets/xxx.png`
- Vite 构建时自动转换为 Base64 嵌入 HTML
- 支持本地文件和远程 URL
- 推荐分辨率：≥1920×1080

## 技术栈

- **Vite** (^5.4.0) + vite-plugin-singlefile - 构建单个自包含 HTML
- **GSAP** (^3.12.5) - HTML 动画库
- **PptxGenJS** (^4.0.1) - PPTX 生成
- **marked** (^12.0.0) - Markdown 解析
- **js-yaml** (^4.1.0) - YAML 解析（可选）

## 输出格式对比

| 特性 | HTML | PPTX |
|-----|------|------|
| 用途 | 在线展示、网页嵌入 | 离线编辑、会议演示 |
| 动画 | GSAP 流畅动画 | PowerPoint 基础动画 |
| 文件 | 单个自包含 HTML | PowerPoint 文件 |
| 兼容性 | 任何浏览器 | PowerPoint 2016+ |

## 开发注意事项

1. **修改模板逻辑**: 主要编辑 `template-mapper.js` 和 `content-analyzer.js`
2. **调整设计令牌**: 修改 `design-tokens.js` 会同时影响 HTML 和 PPTX
3. **添加新模板**: 在 `template-mapper.js` 中添加配置，在 `content-analyzer.js` 中添加匹配逻辑
4. **测试构建**: 使用 `example-presentation.md` 进行测试
5. **PPTX 调试**: 查看 `scripts/export-pptx.js` 输出的统计信息

## 版本历史

- **v3.0.0**: 从9种模板精简为6种核心布局，引入混合生成策略
- **v2.0.0**: 支持 Markdown 输入，新增智能模板匹配和 PPTX 导出
