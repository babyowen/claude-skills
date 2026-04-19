# Slide Craft

**智能演示文稿生成器** - 将 Markdown、文本或 YAML 转换为精美的 HTML 和 PowerPoint 演示文稿。

## 名称含义

**Slide Craft** = **Slide** (幻灯片) + **Craft** (工艺/精心制作)

体现了这个工具的核心理念：精心制作每一张幻灯片，通过智能分析内容，自动选择最佳模板，生成专业级的演示文稿。

## 为什么选择这个名称?

1. **简洁有力** - 易于记忆和输入
2. **不局限于格式** - 既支持 HTML 也支持 PPTX，不叫 "PPT-to-Web" 这种单向转换的名称
3. **体现专业性** - "Craft" 暗示精心制作、工艺精湛
4. **可扩展性** - 未来可以添加更多输出格式（PDF、视频等）
5. **国际化友好** - 英文名称，适合中英文环境

## 核心特性

- ✅ **多格式输入** - Markdown、纯文本、YAML
- ✅ **智能模板匹配** - AI 自动分析内容，选择最佳展示方式
- ✅ **双输出格式** - HTML（GSAP 动画）+ PPTX（PowerPoint）
- ✅ **9 种内容模板** - 统计卡片、流程步骤、对比列表、时间线等
- ✅ **固定封面设计** - 遵循公司品牌规范
- ✅ **视觉一致性** - HTML 和 PPTX 保持高度一致

## 快速开始

```bash
# 创建演示文稿
echo "# 我的演示
2025年2月

## 核心数据
- 用户: 10,000 (↑ 20%)
- 收入: ¥500万
" > my-presentation.md

# AI 会自动分析并生成
# 然后构建
npm run build        # 生成 HTML
npm run build:pptx   # 生成 PPTX
```

## 技术栈

- **GSAP** - 流畅的 HTML 动画
- **PptxGenJS** - PowerPoint 生成
- **marked** - Markdown 解析
- **Vite** - 快速构建

## 文档

- [完整文档](./SKILL.md)
- [商务 PPT 设计指南](./references/business-ppt-design-guide.md)
- [实施总结](./IMPLEMENTATION_SUMMARY.md)

## 许可证

MIT

---

**从 PPT-to-Web 到 Slide Craft 的升级** - 更专业、更智能、更强大的演示文稿生成工具 🚀
