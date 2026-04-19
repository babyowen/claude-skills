/**
 * 演示文稿构建器
 * 主构建流程编排
 */

import { parseInput } from './markdown-parser.js';
import { analyzeAndSelectTemplate } from './content-analyzer.js';
import { mapContentToTemplate, TEMPLATE_CONFIG } from './template-mapper.js';

/**
 * 演示文稿构建器类
 */
export class PresentationBuilder {
  constructor() {
    this.slides = [];
    this.metadata = {
      title: '',
      date: this.getCurrentDate(),
      author: ''
    };
  }

  /**
   * 从文本内容构建演示文稿
   */
  async buildFromText(input) {
    // Step 1: 解析输入
    const sections = parseInput(input);

    if (sections.length === 0) {
      throw new Error('无法解析输入内容');
    }

    // Step 2: 分析并选择模板
    const analyzed = sections.map(section => ({
      ...section,
      template: analyzeAndSelectTemplate(section),
      mappedData: null
    }));

    // Step 3: 映射内容到模板数据
    analyzed.forEach(section => {
      if (section.type === 'title') {
        // 提取元数据
        this.metadata.title = section.title;
        if (section.metadata.date) {
          this.metadata.date = section.metadata.date;
        }
        section.mappedData = {
          title: section.title,
          subtitle: section.content?.paragraphs?.[0] || section.subtitle || '',
          date: section.metadata.date || this.metadata.date
        };
      } else {
        // 映射内容到模板
        section.mappedData = mapContentToTemplate(section.template, section);
      }
    });

    // Step 4: 优化内容（确保完整性）
    const optimized = this.optimizeContent(analyzed);

    this.slides = optimized;

    return {
      slides: optimized,
      metadata: this.metadata
    };
  }

  /**
   * 优化内容
   * - 确保所有内容都被包含
   * - 智能拆分过长内容
   */
  optimizeContent(sections) {
    return sections.flatMap(section => {
      // 检查是否需要拆分
      const config = TEMPLATE_CONFIG[section.template];

      if (!config || !config.maxItems) {
        return [section];
      }

      const items = section.content?.listItems || [];

      // 如果内容超过最大项数，拆分为多张幻灯片
      if (items.length > config.maxItems) {
        return this.splitSlide(section, config.maxItems);
      }

      return [section];
    });
  }

  /**
   * 拆分幻灯片
   */
  splitSlide(section, maxItems) {
    const items = section.content.listItems;
    const chunks = [];

    for (let i = 0; i < items.length; i += maxItems) {
      const chunk = items.slice(i, i + maxItems);
      const chunkSection = {
        ...section,
        index: section.index + (i / maxItems) * 0.1,
        content: {
          ...section.content,
          listItems: chunk
        },
        mappedData: mapContentToTemplate(section.template, {
          ...section,
          content: {
            ...section.content,
            listItems: chunk
          }
        })
      };

      // 为后续幻灯片添加编号
      if (i > 0) {
        chunkSection.title = `${section.title} (${Math.floor(i / maxItems) + 1})`;
      }

      chunks.push(chunkSection);
    }

    return chunks;
  }

  /**
   * 生成 HTML
   */
  async generateHTML(presentationData) {
    // 这个方法将在 html-generator.js 中实现
    // 这里只是接口定义
    throw new Error('generateHTML 方法需要在 html-generator.js 中实现');
  }

  /**
   * 生成 PPTX 数据
   */
  generatePPTXData(presentationData) {
    // 这个方法将在 pptx-exporter.js 中实现
    // 这里只是接口定义
    throw new Error('generatePPTXData 方法需要在 pptx-exporter.js 中实现');
  }

  /**
   * 获取当前日期
   */
  getCurrentDate() {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const day = now.getDate();

    return `${year}年${month}月${day}日`;
  }

  /**
   * 验证演示文稿数据
   */
  validate(presentationData) {
    const errors = [];

    // 检查是否有幻灯片
    if (!presentationData.slides || presentationData.slides.length === 0) {
      errors.push('演示文稿必须包含至少一张幻灯片');
    }

    // 检查第一张是否为标题页
    if (presentationData.slides.length > 0 && presentationData.slides[0].type !== 'title') {
      errors.push('第一张幻灯片必须是标题页');
    }

    // 检查每张幻灯片的内容
    presentationData.slides.forEach((slide, index) => {
      if (!slide.title && slide.type !== 'title') {
        errors.push(`幻灯片 ${index + 1} 缺少标题`);
      }

      if (!slide.template) {
        errors.push(`幻灯片 ${index + 1} 缺少模板类型`);
      }
    });

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * 获取演示文稿统计信息
   */
  getStats(presentationData) {
    const stats = {
      totalSlides: presentationData.slides.length,
      templateUsage: {},
      hasImages: false,
      totalListItems: 0
    };

    presentationData.slides.forEach(slide => {
      // 统计模板使用情况
      const template = slide.template || 'unknown';
      stats.templateUsage[template] = (stats.templateUsage[template] || 0) + 1;

      // 检查是否有图片
      if (slide.images && slide.images.length > 0) {
        stats.hasImages = true;
      }

      // 统计列表项数量
      if (slide.content?.listItems) {
        stats.totalListItems += slide.content.listItems.length;
      }
    });

    return stats;
  }
}

export default PresentationBuilder;
