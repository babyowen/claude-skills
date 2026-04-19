/**
 * HTML 生成器
 * 动态生成 HTML 代码，支持所有模板
 */

import { getWebColor, getWebFontSize } from './design-tokens.js';

/**
 * HTML 生成器类
 */
export class HTMLGenerator {
  constructor() {
    this.sloganPath = './assets/slogon.png';
    this.logoPath = './assets/logo.png';
    this.backgroundPath = './assets/fm-background.png';
  }

  /**
   * 生成完整的 HTML 文档
   */
  generate(presentationData) {
    const { slides, metadata } = presentationData;

    const slidesHTML = slides.map(slide => {
      return this.generateSlide(slide);
    }).join('\n\n');

    return this.wrapInTemplate(slidesHTML, metadata);
  }

  /**
   * 生成单个幻灯片
   */
  generateSlide(slide) {
    switch (slide.template) {
      case 'title-slide':
        return this.generateTitleSlide(slide);

      case 'stats-cards':
        return this.generateStatsCards(slide);

      case 'process-steps':
        return this.generateProcessSteps(slide);

      case 'comparison':
        return this.generateComparison(slide);

      case 'timeline':
        return this.generateTimeline(slide);

      case 'media-text':
        return this.generateMediaText(slide);

      case 'tags-cloud':
        return this.generateTagsCloud(slide);

      case 'team-members':
        return this.generateTeamMembers(slide);

      case 'quote-highlight':
        return this.generateQuoteHighlight(slide);

      case 'progress-bars':
        return this.generateProgressBars(slide);

      case 'content-simple':
      default:
        return this.generateContentSimple(slide);
    }
  }

  /**
   * 生成封面页 (固定设计)
   */
  generateTitleSlide(slide) {
    const data = slide.mappedData || {};

    return `<div class="slide title-slide active">
    <img class="bg-pattern" src="${this.backgroundPath}" alt="">
    <div class="header">
        <div class="logo-container">
            <img src="${this.logoPath}" alt="Logo">
        </div>
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>
    <div class="main-content">
        <h1>${data.title || slide.title}</h1>
        <div class="subtitle">${data.subtitle || ''}</div>
        <div class="date">${data.date || ''}</div>
    </div>
</div>`;
  }

  /**
   * 生成统计卡片
   */
  generateStatsCards(slide) {
    const stats = slide.mappedData || [];

    const cardsHTML = stats.map((stat, index) => `
        <div class="stat-card fade-in-up" style="animation-delay: ${index * 0.1}s">
            <div class="stat-number">${stat.number}</div>
            <div class="stat-label">${stat.label}</div>
            ${stat.trend ? `<div class="stat-trend trend-${stat.trendType}">${stat.trend}</div>` : ''}
        </div>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="stats-grid">
        ${cardsHTML}
    </div>
</div>`;
  }

  /**
   * 生成流程步骤
   */
  generateProcessSteps(slide) {
    const steps = slide.mappedData || [];

    const stepsHTML = steps.map((step, index) => `
        <div class="process-step fade-in-left" style="animation-delay: ${index * 0.15}s">
            <div class="step-number">${step.id}</div>
            <div class="step-content">
                <h3 class="step-title">${step.title}</h3>
                <p class="step-description">${step.description}</p>
            </div>
        </div>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="process-container">
        ${stepsHTML}
    </div>
</div>`;
  }

  /**
   * 生成对比列表
   */
  generateComparison(slide) {
    const data = slide.mappedData || { leftItems: [], rightItems: [] };

    const leftHTML = data.leftItems.map(item => `<li>${item}</li>`).join('\n');
    const rightHTML = data.rightItems.map(item => `<li>${item}</li>`).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="comparison-container">
        <div class="comparison-column fade-in-left">
            <h3 class="column-title">${data.leftTitle}</h3>
            <ul class="comparison-list">
                ${leftHTML}
            </ul>
        </div>

        <div class="comparison-divider">
            <span class="vs-badge">VS</span>
        </div>

        <div class="comparison-column fade-in-right">
            <h3 class="column-title">${data.rightTitle}</h3>
            <ul class="comparison-list">
                ${rightHTML}
            </ul>
        </div>
    </div>
</div>`;
  }

  /**
   * 生成时间线
   */
  generateTimeline(slide) {
    const events = slide.mappedData || [];

    const eventsHTML = events.map((event, index) => `
        <div class="timeline-item fade-in-up" style="animation-delay: ${index * 0.2}s">
            <div class="timeline-date">${event.date}</div>
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <h3 class="timeline-title">${event.title}</h3>
                ${event.description ? `<p class="timeline-description">${event.description}</p>` : ''}
            </div>
        </div>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="timeline-container">
        ${eventsHTML}
    </div>
</div>`;
  }

  /**
   * 生成图文混排
   */
  generateMediaText(slide) {
    const data = slide.mappedData || {};
    const featuresHTML = (data.features || []).map(f => `<li>${f}</li>`).join('\n');
    const imageSrc = data.image?.url || './assets/placeholder.png';

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="media-text-container">
        <div class="media-image fade-in-left">
            <img src="${imageSrc}" alt="${data.title}">
        </div>
        <div class="media-content fade-in-right">
            ${data.description ? `<p class="media-description">${data.description}</p>` : ''}
            ${featuresHTML ? `
            <ul class="media-features">
                ${featuresHTML}
            </ul>
            ` : ''}
        </div>
    </div>
</div>`;
  }

  /**
   * 生成标签云
   */
  generateTagsCloud(slide) {
    const tags = slide.mappedData || [];

    const tagsHTML = tags.map((tag, index) => `
        <span class="tag ${tag.isPrimary ? 'tag-primary' : ''} pop-in" style="animation-delay: ${index * 0.05}s">
            ${tag.label}
        </span>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="tags-container">
        ${tagsHTML}
    </div>
</div>`;
  }

  /**
   * 生成人物介绍
   */
  generateTeamMembers(slide) {
    const members = slide.mappedData || [];

    const membersHTML = members.map((member, index) => `
        <div class="team-card rise-up" style="animation-delay: ${index * 0.1}s">
            <div class="team-avatar">
                <div class="avatar-placeholder">${member.name[0]}</div>
            </div>
            <h3 class="team-name">${member.name}</h3>
            <p class="team-title">${member.title}</p>
            ${member.bio ? `<p class="team-bio">${member.bio}</p>` : ''}
        </div>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="team-grid">
        ${membersHTML}
    </div>
</div>`;
  }

  /**
   * 生成引用强调
   */
  generateQuoteHighlight(slide) {
    const data = slide.mappedData || {};

    return `<div class="slide content-slide quote-slide">
    <div class="quote-container scale-in">
        <div class="quote-mark">"</div>
        <blockquote class="quote-text">
            ${data.text}
        </blockquote>
        ${data.author ? `<cite class="quote-author">— ${data.author}</cite>` : ''}
    </div>
</div>`;
  }

  /**
   * 生成进度条
   */
  generateProgressBars(slide) {
    const items = slide.mappedData || [];

    const barsHTML = items.map((item, index) => `
        <div class="progress-item fade-in-up" style="animation-delay: ${index * 0.15}s">
            <div class="progress-header">
                <span class="progress-label">${item.label}</span>
                <span class="progress-percent">${item.percent}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 0%" data-width="${item.percent}%"></div>
            </div>
        </div>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="progress-container">
        ${barsHTML}
    </div>
</div>`;
  }

  /**
   * 生成基础内容
   */
  generateContentSimple(slide) {
    const items = slide.mappedData || [];

    const itemsHTML = items.map((item, index) => `
        <li class="fade-in-up" style="animation-delay: ${index * 0.1}s">
            ${item.type === 'number' ? `<span class="list-number">${item.number}.</span>` : ''}
            ${item.text}
        </li>
    `).join('\n');

    return `<div class="slide content-slide">
    <div class="global-header">
        <div class="slogan-container">
            <img src="${this.sloganPath}" alt="Slogan">
        </div>
    </div>

    <div class="page-header">
        <h1 class="main-title">${slide.title}</h1>
    </div>
    <div class="divider"></div>

    <div class="content-container">
        <ul class="content-list">
            ${itemsHTML}
        </ul>
    </div>
</div>`;
  }

  /**
   * 包装到完整 HTML 模板
   */
  wrapInTemplate(slidesHTML, metadata) {
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${metadata.title || '演示文稿'}</title>
</head>
<body>
    <div class="presentation">
        ${slidesHTML}
    </div>

    <!-- Navigation Arrows -->
    <div class="nav-arrows">
        <button class="nav-arrow nav-prev" aria-label="上一页">❮</button>
        <button class="nav-arrow nav-next" aria-label="下一页">❯</button>
    </div>

    <script type="module" src="./main.js"></script>
</body>
</html>`;
  }
}

export default HTMLGenerator;
