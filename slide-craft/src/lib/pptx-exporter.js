/**
 * PPTX 导出器
 * 支持所有模板的 PPTX 生成，确保与 HTML 视觉一致性
 */

import PptxGenJS from 'pptxgenjs';
import {
  DESIGN_TOKENS,
  getPPTXColor,
  getPPTXFontSize,
  pptxUnit
} from './design-tokens.js';

/**
 * PPTX 导出器类
 */
export class PPTXExporter {
  constructor() {
    this.pres = new PptxGenJS();

    // 设置演示文稿属性
    this.pres.layout = 'LAYOUT_16x9';
    this.pres.title = '演示文稿';
    this.pres.author = 'Claude';

    // 图片路径
    this.logoPath = './src/assets/logo.png';
    this.sloganPath = './src/assets/slogon.png';
    this.backgroundPath = './src/assets/fm-background.png';
  }

  /**
   * 导出演示文稿
   */
  async export(presentationData, outputPath = './dist/presentation.pptx') {
    const { slides, metadata } = presentationData;

    // 设置标题
    if (metadata.title) {
      this.pres.title = metadata.title;
    }

    // 生成所有幻灯片
    for (const slide of slides) {
      await this.addSlide(slide);
    }

    // 保存文件
    await this.pres.writeFile({ fileName: outputPath });

    return outputPath;
  }

  /**
   * 添加幻灯片
   */
  async addSlide(slide) {
    const pptxSlide = this.pres.addSlide();

    switch (slide.template) {
      case 'title-slide':
        await this.addTitleSlide(pptxSlide, slide);
        break;

      case 'stats-cards':
        await this.addStatsCards(pptxSlide, slide);
        break;

      case 'process-steps':
        await this.addProcessSteps(pptxSlide, slide);
        break;

      case 'comparison':
        await this.addComparison(pptxSlide, slide);
        break;

      case 'timeline':
        await this.addTimeline(pptxSlide, slide);
        break;

      case 'media-text':
        await this.addMediaText(pptxSlide, slide);
        break;

      case 'tags-cloud':
        await this.addTagsCloud(pptxSlide, slide);
        break;

      case 'team-members':
        await this.addTeamMembers(pptxSlide, slide);
        break;

      case 'quote-highlight':
        await this.addQuoteHighlight(pptxSlide, slide);
        break;

      case 'progress-bars':
        await this.addProgressBars(pptxSlide, slide);
        break;

      case 'content-simple':
      default:
        await this.addContentSimple(pptxSlide, slide);
    }
  }

  /**
   * 添加封面页 (固定设计)
   */
  async addTitleSlide(pptxSlide, slide) {
    const data = slide.mappedData || {};

    // 1. 背景图片 - 全屏，半透明
    try {
      pptxSlide.addImage({
        path: this.backgroundPath,
        x: 0,
        y: 0,
        w: '100%',
        h: '100%',
        transparency: 50
      });
    } catch (error) {
      console.warn('背景图片加载失败，使用纯色背景');
      pptxSlide.background = { color: getPPTXColor('gray1') };
    }

    // 2. Logo - 左上角
    try {
      pptxSlide.addImage({
        path: this.logoPath,
        x: 0.5,
        y: 0.35,
        w: 1.5,
        h: 0.6,
        sizing: { type: 'contain', w: 1.5, h: 0.6 }
      });
    } catch (error) {
      console.warn('Logo 加载失败');
    }

    // 3. Slogan - 右上角
    try {
      pptxSlide.addImage({
        path: this.sloganPath,
        x: 7.5,
        y: 0.35,
        w: 2,
        h: 0.6,
        sizing: { type: 'contain', w: 2, h: 0.6 }
      });
    } catch (error) {
      console.warn('Slogan 加载失败');
    }

    // 4. 主标题 - 楷体，4rem（约48pt）
    pptxSlide.addText(data.title || slide.title, {
      x: 1.0,
      y: 2.4,
      w: 8,
      h: 0.8,
      fontSize: 48,
      fontFace: 'KaiTi, 楷体',
      bold: true,
      color: getPPTXColor('black'),
      align: 'left'
    });

    // 5. 副标题 - 楷体，1.8rem（约22pt）
    if (data.subtitle) {
      pptxSlide.addText(data.subtitle, {
        x: 1.0,
        y: 3.3,
        w: 8,
        h: 0.5,
        fontSize: 22,
        fontFace: 'KaiTi, 楷体',
        color: getPPTXColor('black'),
        align: 'left'
      });
    }

    // 6. 日期 - 楷体，1.5rem（约18pt）
    pptxSlide.addText(data.date || '', {
      x: 1.0,
      y: 4.0,
      w: 8,
      h: 0.4,
      fontSize: 18,
      fontFace: 'KaiTi, 楷体',
      color: getPPTXColor('black'),
      align: 'left'
    });
  }

  /**
   * 添加统计卡片
   */
  async addStatsCards(pptxSlide, slide) {
    // 添加页眉 Slogan
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    // 统计卡片 - 4列布局
    const stats = slide.mappedData || [];
    const cols = 4;
    const cardWidth = 2;
    const cardHeight = 1.5;
    const startX = 0.5;
    const startY = 1.8;
    const gapX = 0.3;
    const gapY = 0.3;

    stats.forEach((stat, index) => {
      const col = index % cols;
      const row = Math.floor(index / cols);
      const x = startX + col * (cardWidth + gapX);
      const y = startY + row * (cardHeight + gapY);

      // 卡片背景
      pptxSlide.addShape('rect', {
        x,
        y,
        w: cardWidth,
        h: cardHeight,
        fill: { color: getPPTXColor('white') },
        shadow: { type: 'outer', blur: 8, offset: 2, angle: 45, opacity: 0.1 }
      });

      // 数字
      pptxSlide.addText(stat.number, {
        x,
        y: y + 0.2,
        w: cardWidth,
        h: 0.6,
        fontSize: 36,
        fontFace: 'Arial',
        bold: true,
        color: getPPTXColor('primary'),
        align: 'center'
      });

      // 标签
      pptxSlide.addText(stat.label, {
        x,
        y: y + 0.9,
        w: cardWidth,
        h: 0.4,
        fontSize: 14,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray5'),
        align: 'center'
      });

      // 趋势
      if (stat.trend) {
        pptxSlide.addText(stat.trend, {
          x,
          y: y + 1.2,
          w: cardWidth,
          h: 0.3,
          fontSize: 12,
          fontFace: 'Arial',
          color: stat.trendType === 'up' ? getPPTXColor('success') : getPPTXColor('danger'),
          align: 'center'
        });
      }
    });
  }

  /**
   * 添加流程步骤
   */
  async addProcessSteps(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const steps = slide.mappedData || [];
    const stepWidth = 1.5;
    const totalWidth = steps.length * stepWidth + (steps.length - 1) * 0.3;
    const startX = (10 - totalWidth) / 2;
    const y = 2.5;

    steps.forEach((step, index) => {
      const x = startX + index * (stepWidth + 0.3);

      // 圆形编号
      pptxSlide.addShape('ellipse', {
        x: x + (stepWidth - 0.6) / 2,
        y: y,
        w: 0.6,
        h: 0.6,
        fill: { color: getPPTXColor('primary') }
      });

      pptxSlide.addText(step.id.toString(), {
        x: x + (stepWidth - 0.6) / 2,
        y: y,
        w: 0.6,
        h: 0.6,
        fontSize: 20,
        fontFace: 'Arial',
        bold: true,
        color: getPPTXColor('white'),
        align: 'center',
        valign: 'middle'
      });

      // 标题
      pptxSlide.addText(step.title, {
        x,
        y: y + 0.8,
        w: stepWidth,
        h: 0.4,
        fontSize: 16,
        fontFace: 'Microsoft YaHei',
        bold: true,
        color: getPPTXColor('gray5'),
        align: 'center'
      });

      // 描述
      pptxSlide.addText(step.description, {
        x,
        y: y + 1.3,
        w: stepWidth,
        h: 0.6,
        fontSize: 12,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray4'),
        align: 'center'
      });

      // 连接线
      if (index < steps.length - 1) {
        pptxSlide.addShape('line', {
          x: x + stepWidth + 0.05,
          y: y + 0.3,
          w: 0.2,
          h: 0,
          line: { color: getPPTXColor('gray3'), width: 2 }
        });
      }
    });
  }

  /**
   * 添加对比列表
   */
  async addComparison(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const data = slide.mappedData || { leftItems: [], rightItems: [] };

    // 左栏
    pptxSlide.addText(data.leftTitle, {
      x: 0.5,
      y: 1.8,
      w: 4,
      h: 0.5,
      fontSize: 20,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('gray5')
    });

    const leftText = data.leftItems.map(item => `• ${item}`).join('\n');
    pptxSlide.addText(leftText, {
      x: 0.5,
      y: 2.4,
      w: 4,
      h: 2.5,
      fontSize: 16,
      fontFace: 'Microsoft YaHei',
      color: getPPTXColor('gray5'),
      valign: 'top'
    });

    // VS 分隔
    pptxSlide.addShape('ellipse', {
      x: 4.6,
      y: 2.8,
      w: 0.8,
      h: 0.8,
      fill: { color: getPPTXColor('gray2') }
    });

    pptxSlide.addText('VS', {
      x: 4.6,
      y: 2.8,
      w: 0.8,
      h: 0.8,
      fontSize: 18,
      fontFace: 'Arial',
      bold: true,
      color: getPPTXColor('gray5'),
      align: 'center',
      valign: 'middle'
    });

    // 右栏
    pptxSlide.addText(data.rightTitle, {
      x: 5.5,
      y: 1.8,
      w: 4,
      h: 0.5,
      fontSize: 20,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('gray5')
    });

    const rightText = data.rightItems.map(item => `• ${item}`).join('\n');
    pptxSlide.addText(rightText, {
      x: 5.5,
      y: 2.4,
      w: 4,
      h: 2.5,
      fontSize: 16,
      fontFace: 'Microsoft YaHei',
      color: getPPTXColor('gray5'),
      valign: 'top'
    });
  }

  /**
   * 添加时间线
   */
  async addTimeline(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const events = slide.mappedData || [];
    const startY = 1.8;
    const itemHeight = 0.8;

    events.forEach((event, index) => {
      const y = startY + index * itemHeight;

      // 日期
      pptxSlide.addText(event.date, {
        x: 0.5,
        y,
        w: 1.5,
        h: 0.5,
        fontSize: 14,
        fontFace: 'Arial',
        bold: true,
        color: getPPTXColor('primary'),
        align: 'right'
      });

      // 标记点
      pptxSlide.addShape('ellipse', {
        x: 2.2,
        y: y + 0.1,
        w: 0.3,
        h: 0.3,
        fill: { color: getPPTXColor('primary') }
      });

      // 连接线
      if (index < events.length - 1) {
        pptxSlide.addShape('line', {
          x: 2.35,
          y: y + 0.4,
          w: 0,
          h: 0.5,
          line: { color: getPPTXColor('gray3'), width: 2 }
        });
      }

      // 标题
      pptxSlide.addText(event.title, {
        x: 2.7,
        y,
        w: 6.5,
        h: 0.4,
        fontSize: 16,
        fontFace: 'Microsoft YaHei',
        bold: true,
        color: getPPTXColor('gray5')
      });

      // 描述
      if (event.description) {
        pptxSlide.addText(event.description, {
          x: 2.7,
          y: y + 0.4,
          w: 6.5,
          h: 0.3,
          fontSize: 12,
          fontFace: 'Microsoft YaHei',
          color: getPPTXColor('gray4')
        });
      }
    });
  }

  /**
   * 添加图文混排
   */
  async addMediaText(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const data = slide.mappedData || {};

    // 图片（左侧）
    if (data.image?.url) {
      pptxSlide.addImage({
        path: data.image.url,
        x: 0.5,
        y: 1.8,
        w: 4.5,
        h: 3
      });
    }

    // 描述（右侧）
    if (data.description) {
      pptxSlide.addText(data.description, {
        x: 5.5,
        y: 1.8,
        w: 4,
        h: 1,
        fontSize: 16,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray5')
      });
    }

    // 特性列表
    if (data.features && data.features.length > 0) {
      const featuresText = data.features.map(f => `• ${f}`).join('\n');
      pptxSlide.addText(featuresText, {
        x: 5.5,
        y: 3,
        w: 4,
        h: 2,
        fontSize: 14,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray5'),
        valign: 'top'
      });
    }
  }

  /**
   * 添加标签云
   */
  async addTagsCloud(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const tags = slide.mappedData || [];
    let x = 0.5;
    let y = 2;
    const lineHeight = 0.6;

    tags.forEach((tag, index) => {
      const textWidth = tag.label.length * 0.15 + 0.3;

      // 换行检查
      if (x + textWidth > 9.5) {
        x = 0.5;
        y += lineHeight;
      }

      pptxSlide.addText(tag.label, {
        x,
        y,
        w: textWidth,
        h: 0.4,
        fontSize: 14,
        fontFace: 'Microsoft YaHei',
        bold: tag.isPrimary,
        color: tag.isPrimary ? getPPTXColor('primary') : getPPTXColor('gray5'),
        fill: { color: tag.isPrimary ? getPPTXColor('gray2') : getPPTXColor('gray1') },
        align: 'center',
        valign: 'middle'
      });

      x += textWidth + 0.2;
    });
  }

  /**
   * 添加人物介绍
   */
  async addTeamMembers(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const members = slide.mappedData || [];
    const cols = 4;
    const cardWidth = 2;
    const cardHeight = 2.5;
    const startX = 0.5;
    const startY = 1.8;
    const gapX = 0.3;

    members.forEach((member, index) => {
      const col = index % cols;
      const x = startX + col * (cardWidth + gapX);
      const y = startY;

      // 头像占位符
      pptxSlide.addShape('ellipse', {
        x: x + (cardWidth - 0.8) / 2,
        y: y + 0.2,
        w: 0.8,
        h: 0.8,
        fill: { color: getPPTXColor('gray2') }
      });

      // 姓名首字母
      pptxSlide.addText(member.name[0], {
        x: x + (cardWidth - 0.8) / 2,
        y: y + 0.2,
        w: 0.8,
        h: 0.8,
        fontSize: 28,
        fontFace: 'Microsoft YaHei',
        bold: true,
        color: getPPTXColor('primary'),
        align: 'center',
        valign: 'middle'
      });

      // 姓名
      pptxSlide.addText(member.name, {
        x,
        y: y + 1.2,
        w: cardWidth,
        h: 0.4,
        fontSize: 16,
        fontFace: 'Microsoft YaHei',
        bold: true,
        color: getPPTXColor('gray5'),
        align: 'center'
      });

      // 职位
      pptxSlide.addText(member.title, {
        x,
        y: y + 1.6,
        w: cardWidth,
        h: 0.3,
        fontSize: 12,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray4'),
        align: 'center'
      });

      // 简介
      if (member.bio) {
        pptxSlide.addText(member.bio, {
          x,
          y: y + 2,
          w: cardWidth,
          h: 0.4,
          fontSize: 10,
          fontFace: 'Microsoft YaHei',
          color: getPPTXColor('gray4'),
          align: 'center'
        });
      }
    });
  }

  /**
   * 添加引用强调
   */
  async addQuoteHighlight(pptxSlide, slide) {
    const data = slide.mappedData || {};

    // 背景色
    pptxSlide.background = { color: getPPTXColor('primary') };

    // 引号
    pptxSlide.addText('"', {
      x: 1,
      y: 1.5,
      w: 8,
      h: 1,
      fontSize: 72,
      fontFace: 'Georgia',
      color: getPPTXColor('white'),
      transparency: 50
    });

    // 引用文本
    pptxSlide.addText(data.text, {
      x: 1,
      y: 2.2,
      w: 8,
      h: 2,
      fontSize: 28,
      fontFace: 'KaiTi, 楷体',
      color: getPPTXColor('white'),
      align: 'center',
      valign: 'middle'
    });

    // 作者
    if (data.author) {
      pptxSlide.addText(`— ${data.author}`, {
        x: 1,
        y: 4.5,
        w: 8,
        h: 0.5,
        fontSize: 18,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('white'),
        align: 'center'
      });
    }
  }

  /**
   * 添加进度条
   */
  async addProgressBars(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const items = slide.mappedData || [];
    const startY = 1.8;
    const itemHeight = 0.8;

    items.forEach((item, index) => {
      const y = startY + index * itemHeight;

      // 标签
      pptxSlide.addText(item.label, {
        x: 0.5,
        y,
        w: 7,
        h: 0.3,
        fontSize: 16,
        fontFace: 'Microsoft YaHei',
        color: getPPTXColor('gray5')
      });

      // 百分比
      pptxSlide.addText(`${item.percent}%`, {
        x: 7.5,
        y,
        w: 2,
        h: 0.3,
        fontSize: 16,
        fontFace: 'Arial',
        bold: true,
        color: getPPTXColor('primary'),
        align: 'right'
      });

      // 进度条背景
      pptxSlide.addShape('rect', {
        x: 0.5,
        y: y + 0.4,
        w: 9,
        h: 0.2,
        fill: { color: getPPTXColor('gray2') }
      });

      // 进度条填充
      const fillWidth = (item.percent / 100) * 9;
      pptxSlide.addShape('rect', {
        x: 0.5,
        y: y + 0.4,
        w: fillWidth,
        h: 0.2,
        fill: { color: getPPTXColor('primary') }
      });
    });
  }

  /**
   * 添加基础内容
   */
  async addContentSimple(pptxSlide, slide) {
    this.addGlobalHeader(pptxSlide);

    // 页面标题
    pptxSlide.addText(slide.title, {
      x: 0.5,
      y: 0.5,
      w: 9,
      h: 0.8,
      fontSize: 32,
      fontFace: 'Microsoft YaHei',
      bold: true,
      color: getPPTXColor('primary')
    });

    const items = slide.mappedData || [];
    const text = items.map(item => {
      const prefix = item.type === 'number' ? `${item.number}. ` : '• ';
      return `${prefix}${item.text}`;
    }).join('\n');

    pptxSlide.addText(text, {
      x: 0.5,
      y: 1.8,
      w: 9,
      h: 3.5,
      fontSize: 20,
      fontFace: 'Microsoft YaHei',
      color: getPPTXColor('gray5'),
      valign: 'top'
    });
  }

  /**
   * 添加全局页眉（Slogan）
   */
  addGlobalHeader(pptxSlide) {
    try {
      pptxSlide.addImage({
        path: this.sloganPath,
        x: 7.5,
        y: 0.3,
        w: 2,
        h: 0.5,
        sizing: { type: 'contain', w: 2, h: 0.5 }
      });
    } catch (error) {
      console.warn('Slogan 加载失败');
    }
  }
}

export default PPTXExporter;
