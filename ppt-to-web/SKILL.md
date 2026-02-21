---
name: ppt-to-web
description: "Generate animated web presentations from PPT outlines using GSAP. Use when users want to create HTML presentations, convert PPT outlines to web pages, or build slide-based presentations. Supports 9 content templates including Stats Cards, Process Steps, Comparison, Timeline, Media-Text, Tags Cloud, Team Members, Quote Highlight, and Progress Bars. Analyze content type to select appropriate template."
---

# PPT to Web Presentation Generator

Generate beautiful, animated web presentations from PPT outlines using GSAP animation library.

## Overview

This skill transforms structured PPT outlines into fully functional HTML presentations with smooth animations and professional styling.

## CRITICAL REQUIREMENT: Single HTML File Output

**The output MUST be a single, self-contained HTML file.**

- All CSS and JavaScript are automatically inlined by Vite build process
- GSAP library is bundled inline (no CDN required, works offline)
- **Images**: Automatically converted to Base64 and embedded during build
- The HTML file works when opened directly in any browser without internet
- This ensures the file can be easily copied and shared

## Build Process

**IMPORTANT: The final HTML is generated using Vite.**

```bash
# Install dependencies (first time only)
npm install

# Build the single HTML file
npm run build
```

The build process:
1. Bundles all JavaScript (including GSAP) inline
2. Inlines all CSS
3. Converts all images to Base64 and embeds them
4. Outputs a single `dist/index.html` file that works offline

**For development:**
```bash
npm run dev  # Start dev server with hot reload
```

## CRITICAL REQUIREMENT: Color Scheme (FIXED - Do NOT Change)

**All presentations must use the following CITIC color palette:**

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| **中信红 (Primary Red)** | `#D20A10` | rgb(210, 10, 16) | 强调色、标题、重要元素、按钮 |
| **标准灰五 (Gray 5)** | `#575757` | rgb(87, 87, 87) | 深色文字、重要内容 |
| **标准灰四 (Gray 4)** | `#898989` | rgb(137, 137, 137) | 次要文字、说明文字 |
| **标准灰三 (Gray 3)** | `#B5B5B5` | rgb(181, 181, 181) | 边框、分割线、禁用状态 |
| **标准灰二 (Gray 2)** | `#CACACA` | rgb(202, 202, 202) | 卡片背景、浅色边框 |
| **标准灰一 (Gray 1)** | `#DDDDDD` | rgb(221, 221, 221) | 页面背景、最浅色 |

**Color Usage Guidelines:**
- 主标题、强调内容：中信红 `#D20A10`
- 正文内容：标准灰五 `#575757`
- 次要说明：标准灰四 `#898989`
- 分割线、边框：标准灰三 `#B5B5B5`
- 卡片背景、hover状态：标准灰二 `#CACACA`
- 页面背景：标准灰一 `#DDDDDD` 或 `#F0F0F0`

**Core workflow:**
1. Parse user-provided PPT outline
2. Modify `src/index.html` with slide content
3. Add images to `src/assets/` directory
4. Run `npm run build` to generate single HTML file
5. Output: `dist/index.html` - self-contained, works offline

## Quick Start

**Example usage:**
```
User: "帮我生成一个关于产品介绍的演示，包含标题页、核心特性、技术架构和总结"
```

Claude will:
1. Parse the request into slide structure
2. Modify `src/index.html` with the slide content
3. Run `npm run build` to generate the single HTML file
4. Output file: `dist/index.html`

## Content Slide Templates - Choose Based on Content Type

**When generating slides, analyze the content and select the most appropriate template:**

### Template 1: 统计数据卡片 (Stats Cards)
- **Use when:** 展示关键指标、KPI数据、业绩概览
- **Features:** 4列网格布局，每个卡片包含图标、数字、标签、变化趋势
- **Best for:** "月度数据"、"业绩报告"、"关键指标"

### Template 2: 流程步骤 (Process Steps)
- **Use when:** 展示工作流程、操作步骤、实施阶段
- **Features:** 横向步骤展示，带编号圆形、连接线、标题和描述
- **Best for:** "实施流程"、"开发步骤"、"项目阶段"

### Template 3: 对比列表 (Comparison)
- **Use when:** 方案对比、优劣势分析、新旧对比
- **Features:** 左右两栏对比，中间VS分隔，列表形式展示要点
- **Best for:** "方案对比"、"优劣势分析"、"新旧比较"

### Template 4: 时间线 (Timeline)
- **Use when:** 展示项目进度、历史事件、发展历程
- **Features:** 垂直时间线，左侧日期标签，右侧内容卡片
- **Best for:** "项目进度"、"发展历程"、"里程碑"

### Template 5: 图文混排 (Media-Text)
- **Use when:** 产品介绍、功能说明、案例展示
- **Features:** 左图右文或左文右图，图片+标题+描述+特性列表
- **Best for:** "产品介绍"、"功能说明"、"案例展示"

### Template 6: 标签云 (Tags Cloud)
- **Use when:** 技术栈展示、关键词汇总、能力矩阵
- **Features:** 流式标签布局，支持primary样式突出重点
- **Best for:** "技术栈"、"关键词"、"核心能力"

### Template 7: 人物介绍 (Team Members)
- **Use when:** 团队成员展示、讲师介绍、合作伙伴
- **Features:** 4列网格，每个卡片包含头像、姓名、职位、简介
- **Best for:** "团队成员"、"讲师介绍"、"组织架构"

### Template 8: 引用强调 (Quote Highlight)
- **Use when:** 重要声明、核心价值观、愿景使命
- **Features:** 大红色渐变背景，引号装饰，突出显示文字
- **Best for:** "企业使命"、"核心价值观"、"重要声明"

### Template 9: 进度指示器 (Progress Bars)
- **Use when:** 目标达成展示、进度汇报、完成率
- **Features:** 多个进度条，显示标签、百分比、动画填充
- **Best for:** "目标达成"、"进度汇报"、"完成情况"

### Template Selection Guidelines:

| Content Type | Recommended Template |
|-------------|---------------------|
| 数据指标 | Stats Cards |
| 流程/步骤 | Process Steps |
| 对比分析 | Comparison |
| 时间/历程 | Timeline |
| 产品/功能 | Media-Text |
| 关键词/标签 | Tags Cloud |
| 人物/团队 | Team Members |
| 重要声明 | Quote Highlight |
| 进度/目标 | Progress Bars |

## Legacy Slide Types (Basic)

These basic types are also available for simpler content:

### Title Slide (Basic)
- **Use for:** Simple opening slides
- **Structure:** Title, subtitle, author

### Content Slide (List)
- **Use for:** Bullet points, feature lists
- **Structure:** Title with animated bullet list items

### Two-Column Slide
- **Use for:** Side-by-side content
- **Structure:** Two equal columns with titles and content

### Image Slide
- **Use for:** Single image display
- **Structure:** Centered image with optional caption

### Quote Slide
- **Use for:** Simple quotes
- **Structure:** Quote text with author attribution

### Code Slide
- **Use for:** Code examples
- **Structure:** Code block with syntax highlighting

## Workflow

### Step 1: Gather Requirements

Ask the user for:
- Presentation topic/theme
- Number of slides desired
- Slide content (can be rough notes or detailed)
- Any specific images or visual elements
- Preferred style (formal, creative, minimal, etc.)

**If user provides incomplete outline:** Generate reasonable defaults based on the topic.

### Step 2: Structure the Outline

Create a YAML or structured outline following the format in `references/outline_format.md`:

```yaml
slides:
  - type: title
    title: "Presentation Title"
    subtitle: "Subtitle"
  - type: content
    title: "Key Points"
    points:
      - "Point 1"
      - "Point 2"
```

### Step 3: Generate HTML Source

Modify `src/index.html`:

1. **Preserve the structure:** The HTML imports `main.js` (includes GSAP) and `styles.css`
2. **Inject slides:** Replace the `<!-- Slides will be generated here -->` comment with actual slide HTML
3. **Add images:** Place images in `src/assets/` and reference them (they'll be converted to Base64 during build)
4. **Map slide types to HTML:**

### Step 4: Build and Output

Run `npm run build` to generate `dist/index.html` - the final single self-contained HTML file.

## Cover Page (Title Slide) - FIXED DESIGN SPECIFICATION

**IMPORTANT: The cover page design is FIXED and must NOT be modified.** Every presentation MUST start with this cover page design. See `demos/cover-page-demo.html` for the complete reference implementation.

### Cover Page HTML Structure:
```html
<div class="slide title-slide active">
    <img class="bg-pattern" src="[background-image-path]" alt="">
    <div class="header">
        <div class="logo-container">
            <img src="[logo-path]" alt="Logo">
        </div>
        <div class="slogan-container">
            <img src="[slogan-path]" alt="Slogan">
        </div>
    </div>
    <div class="main-content">
        <h1>[主标题]</h1>
        <div class="subtitle">[副标题/部门名称]</div>
    </div>
    <div class="footer">
        <div class="date">[日期]</div>
    </div>
</div>
```

### Cover Page Design Parameters (DO NOT CHANGE):

| Element | Specification |
|---------|---------------|
| **背景图片** | 全屏覆盖，opacity: 0.5，z-index: 0 |
| **Logo区域** | 左上角，padding: 3.5% 5% 0 5%，高度60px |
| **Slogan区域** | 右上角，与Logo同行，高度60px |
| **主标题** | 楷体，4rem，加粗，黑色，左对齐，letter-spacing: 0，padding-left: 10% |
| **副标题** | 楷体，1.8rem，常规，黑色，左对齐，letter-spacing: 0，padding-left: 10% |
| **日期** | 楷体，1.5rem，黑色，左对齐，bottom: 38%，padding-left: 10% |
| **主内容区** | padding: 12% 5% 8% 10%（上右下左） |

### Required Image Files:
- `src/assets/logo.png` - 公司Logo
- `src/assets/slogon.png` - 公司Slogan
- `src/assets/fm-background.png` - 背景装饰图

## Global Header - REQUIRED on ALL Content Slides

**IMPORTANT: Every content slide (except cover page) MUST include the Global Header with Slogan at the top right.**

### Global Header HTML Structure:
```html
<!-- Global Header with Slogan - REQUIRED -->
<div class="global-header">
    <div class="slogan-container">
        <img src="[slogan-path]" alt="Slogan">
    </div>
</div>
```

### Content Slide Structure with Global Header:
```html
<div class="slide content-slide">
    <!-- Global Header - REQUIRED -->
    <div class="global-header">
        <div class="slogan-container">
            <img src="[slogan-path]" alt="Slogan">
        </div>
    </div>

    <!-- Page Header -->
    <div class="page-header">
        <h1 class="main-title">[页面标题]</h1>
        <p class="sub-title">[页面副标题]</p>
    </div>
    <div class="divider"></div>

    <!-- Content Area -->
    <div class="card-container">
        <!-- Cards or other content -->
    </div>
</div>
```

## Core Design Principle: One-Key Navigation

**This is the most important principle - all other design decisions follow from this.**

The presentation must feel like a real PPT with keyboard-driven navigation:

- **One key = One slide transition** - Pressing a single key (arrow keys, space, or page up/down) navigates to the next/previous slide
- **Instant snap** - No smooth scrolling between slides; the view should snap directly to the next slide
- **Full-viewport slides** - Each slide occupies exactly 100% of the viewport height/width
- **Keyboard support:**
  - `↓` / `→` / `Space` / `Page Down` - Next slide
  - `↑` / `←` / `Page Up` - Previous slide
  - `Home` - First slide
  - `End` - Last slide
- **Optional touch/click:** Click navigation arrows or swipe on mobile

This creates a "slide deck" experience, not a scrolling webpage. Users should feel they are flipping through pages, not scrolling through content.

### Animations
GSAP animations are pre-configured in the template. Each template type has optimized animation settings:
- **Stats Cards:** Scale and fade in with stagger
- **Process Steps:** Sequential reveal from left
- **Comparison:** Left/right slide in effect
- **Timeline:** Progressive reveal with date highlight
- **Media-Text:** Image and content slide from opposite sides
- **Tags Cloud:** Pop-in effect with bounce
- **Team Members:** Cards rise up with shadow
- **Quote Highlight:** Scale and fade center reveal
- **Progress Bars:** Animated fill with delay stagger

### Responsive Design
The presentation adapts to:
- **Desktop:** Full layout with all features
- **Tablet:** Adjusted spacing and font sizes
- **Mobile:** Single column, larger touch targets

## Customization Options

When users request customizations:

### Changing Colors
Modify the CSS in the template:
```css
.slide.title-slide .slide-content h1 {
    background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
}
```

### Adding Custom Fonts
Insert Google Fonts link in `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

### Adjusting Animations
Modify timing in the JavaScript:
```javascript
gsap.fromTo(elements,
    { opacity: 0, y: 60 },
    {
        opacity: 1,
        y: 0,
        duration: 1.2,  // Adjust duration
        ease: "power4.out",  // Change easing
        stagger: 0.3  // Adjust stagger
    }
);
```

## Common Patterns

### Multi-section Presentation
For long presentations, organize into sections:
1. Create a section divider slide before each major topic
2. Use consistent styling for section headers
3. Consider adding a table of contents slide

### Image-heavy Slides
1. Use high-quality images (minimum 1920x1080 for full-bleed)
2. Optimize image file sizes for web
3. Consider lazy loading for large presentations
4. Use placeholder images from Unsplash if user doesn't provide images

### Data Visualization
For charts and graphs:
1. Generate static images of visualizations
2. Insert as image slides
3. Or embed interactive chart libraries (Chart.js, D3.js)

## Best Practices

1. **Keep slides focused:** One main idea per slide
2. **Limit text:** Use bullet points, not paragraphs
3. **Consistent styling:** Use same fonts, colors throughout
4. **Test in browser:** Always open the HTML file to verify animations work
5. **Optimize images:** Compress large images before embedding

## Resources

### Project Structure
```
ppt-to-web/
├── src/
│   ├── index.html          # Entry HTML template
│   ├── main.js             # Slide logic + GSAP animations
│   ├── styles.css          # All styles
│   └── assets/             # Images (converted to Base64 on build)
├── dist/
│   └── index.html          # Final single-file output (after build)
├── package.json            # Dependencies (Vite, GSAP)
└── vite.config.js          # Build configuration
```

### Files
- **Source Template:** `src/index.html` - Master HTML template
- **Styles:** `src/styles.css` - All CSS styles
- **Scripts:** `src/main.js` - Slide navigation and GSAP animations
- **Build Config:** `vite.config.js` - Vite + single-file plugin configuration
- **Demo Files:**
  - `demos/cover-page-demo.html` - **REQUIRED cover page template** - Every presentation MUST follow this exact design
  - `demos/templates.html` - Complete showcase of all 9 content templates with examples
