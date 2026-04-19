/**
 * Markdown/文本解析器
 * 支持 Markdown、纯文本和 YAML 格式的输入解析
 */

import yaml from 'js-yaml';

/**
 * 检测输入格式
 */
export function detectFormat(content) {
  const trimmed = content.trim();

  // 检测 YAML 格式 (以 --- 开始)
  if (trimmed.startsWith('---') && trimmed.indexOf('---', 3) > 0) {
    return 'yaml';
  }

  // 检测 Markdown 格式 (包含 # 标题、- 列表等)
  if (/^#{1,6}\s/m.test(trimmed) || /^[-*+]\s/m.test(trimmed) || /^\d+\.\s/m.test(trimmed)) {
    return 'markdown';
  }

  // 默认为纯文本
  return 'text';
}

/**
 * 解析输入内容
 */
export function parseInput(content) {
  const format = detectFormat(content);

  switch (format) {
    case 'yaml':
      return parseYAML(content);
    case 'markdown':
      return parseMarkdown(content);
    case 'text':
      return parseText(content);
    default:
      return parseText(content);
  }
}

/**
 * 解析 YAML 格式
 */
function parseYAML(content) {
  try {
    const data = yaml.load(content);

    if (data.slides && Array.isArray(data.slides)) {
      return data.slides.map((slide, index) => ({
        index,
        type: detectSlideType(slide),
        template: slide.template || null,
        title: slide.title || '',
        subtitle: slide.subtitle || '',
        content: extractSlideContent(slide),
        images: slide.images || [],
        metadata: {
          date: slide.date || null,
          author: slide.author || null
        }
      }));
    }

    return [];
  } catch (error) {
    console.error('YAML 解析错误:', error);
    return [];
  }
}

/**
 * 解析 Markdown 格式
 */
function parseMarkdown(content) {
  // 按 --- 分割幻灯片
  const sections = content.split(/^---+\s*$/m).filter(s => s.trim());

  if (sections.length === 0) {
    sections.push(content);
  }

  return sections.map((section, index) => {
    const lines = section.trim().split('\n');

    // 提取标题
    let title = '';
    let titleLevel = 0;
    const contentLines = [];
    const images = [];
    const metadata = { date: null, author: null };

    lines.forEach(line => {
      const trimmed = line.trim();

      // 一级标题 - 主标题
      if (trimmed.startsWith('# ')) {
        title = trimmed.substring(2).trim();
        titleLevel = 1;
      }
      // 二级标题 - 内容页标题
      else if (trimmed.startsWith('## ')) {
        title = trimmed.substring(3).trim();
        titleLevel = 2;
      }
      // 图片
      else if (trimmed.match(/^!\[.*?\]\(.*?\)$/)) {
        const match = trimmed.match(/^!\[(.*?)\]\((.*?)\)$/);
        if (match) {
          images.push({
            alt: match[1],
            url: match[2]
          });
        }
      }
      // 日期识别
      else if (trimmed.match(/^\d{4}年\d{1,2}月\d{1,2}日?$/) ||
               trimmed.match(/^\d{4}[\/-]\d{1,2}[\/-]\d{1,2}$/)) {
        metadata.date = trimmed;
      }
      // 其他内容
      else {
        contentLines.push(line);
      }
    });

    // 提取列表项
    const listItems = extractListItems(contentLines.join('\n'));

    // 检测幻灯片类型
    const slideData = {
      index,
      title,
      titleLevel,
      type: titleLevel === 1 ? 'title' : 'content',
      template: null, // 将由 content-analyzer 决定
      content: {
        raw: contentLines.join('\n').trim(),
        listItems,
        paragraphs: extractParagraphs(contentLines.join('\n'))
      },
      images,
      metadata
    };

    return slideData;
  });
}

/**
 * 解析纯文本格式
 */
function parseText(content) {
  // 按空行分割段落
  const paragraphs = content.split(/\n\s*\n/).filter(p => p.trim());

  return paragraphs.map((para, index) => {
    const lines = para.trim().split('\n');
    const title = lines[0].trim();
    const content = lines.slice(1).join('\n').trim();

    // 尝试提取列表项
    const listItems = extractListItems(content);

    return {
      index,
      type: index === 0 ? 'title' : 'content',
      title,
      template: null,
      content: {
        raw: content,
        listItems,
        paragraphs: [content]
      },
      images: [],
      metadata: {
        date: extractDate(content)
      }
    };
  });
}

/**
 * 提取列表项
 */
function extractListItems(text) {
  const items = [];
  const lines = text.split('\n');

  lines.forEach(line => {
    const trimmed = line.trim();

    // 无序列表 (- 或 * 或 •)
    if (trimmed.match(/^[-*•]\s+/)) {
      items.push({
        type: 'bullet',
        text: trimmed.replace(/^[-*•]\s+/, ''),
        level: getIndentLevel(line)
      });
    }
    // 有序列表 (1. 2. 3.)
    else if (trimmed.match(/^\d+\.\s+/)) {
      const match = trimmed.match(/^(\d+)\.\s+(.*)$/);
      if (match) {
        items.push({
          type: 'number',
          number: parseInt(match[1]),
          text: match[2],
          level: getIndentLevel(line)
        });
      }
    }
  });

  return items;
}

/**
 * 提取段落
 */
function extractParagraphs(text) {
  return text
    .split(/\n\s*\n/)
    .map(p => p.trim())
    .filter(p => p.length > 0 && !p.match(/^[-*•\d]/));
}

/**
 * 提取日期
 */
function extractDate(text) {
  const patterns = [
    /\d{4}年\d{1,2}月\d{1,2}日?/,
    /\d{4}[\/-]\d{1,2}[\/-]\d{1,2}/,
    /\d{1,2}月\d{1,2}日/
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[0];
    }
  }

  return null;
}

/**
 * 检测幻灯片类型
 */
function detectSlideType(slide) {
  if (slide.type) {
    return slide.type;
  }

  // 如果是第一张，默认为标题页
  if (slide.index === 0) {
    return 'title';
  }

  return 'content';
}

/**
 * 提取幻灯片内容
 */
function extractSlideContent(slide) {
  const content = {
    raw: '',
    listItems: [],
    paragraphs: []
  };

  // 如果有 points 字段
  if (slide.points && Array.isArray(slide.points)) {
    content.listItems = slide.points.map((point, idx) => ({
      type: 'bullet',
      text: point,
      level: 0,
      number: idx + 1
    }));
    content.raw = slide.points.join('\n');
  }

  // 如果有 content 字段
  if (slide.content) {
    content.raw = slide.content;
    content.paragraphs = [slide.content];
  }

  // 如果有 stats 字段
  if (slide.stats && Array.isArray(slide.stats)) {
    content.stats = slide.stats;
  }

  // 如果有 steps 字段
  if (slide.steps && Array.isArray(slide.steps)) {
    content.steps = slide.steps;
  }

  return content;
}

/**
 * 获取缩进层级
 */
function getIndentLevel(line) {
  const match = line.match(/^(\s*)/);
  if (!match) return 0;

  const spaces = match[1].length;
  return Math.floor(spaces / 2);
}

export default {
  detectFormat,
  parseInput,
  parseYAML,
  parseMarkdown,
  parseText,
  extractListItems,
  extractParagraphs,
  extractDate
};
