/**
 * 模板映射器
 * 定义 Markdown 元素到 HTML/PPTX 模板的映射规则
 */

import DESIGN_TOKENS from './design-tokens.js';

/**
 * 模板类型枚举
 */
export const TEMPLATE_TYPES = {
  TITLE_SLIDE: 'title-slide',
  STATS_CARDS: 'stats-cards',
  PROCESS_STEPS: 'process-steps',
  COMPARISON: 'comparison',
  TIMELINE: 'timeline',
  MEDIA_TEXT: 'media-text',
  TAGS_CLOUD: 'tags-cloud',
  TEAM_MEMBERS: 'team-members',
  QUOTE_HIGHLIGHT: 'quote-highlight',
  PROGRESS_BARS: 'progress-bars',
  CONTENT_SIMPLE: 'content-simple'
};

/**
 * 模板配置映射
 */
export const TEMPLATE_CONFIG = {
  [TEMPLATE_TYPES.TITLE_SLIDE]: {
    name: '封面页',
    description: '演示文稿开场页',
    maxItems: null,
    layout: 'full'
  },
  [TEMPLATE_TYPES.STATS_CARDS]: {
    name: '统计数据卡片',
    description: '展示关键指标和KPI数据',
    maxItems: 6,
    layout: 'grid-4'
  },
  [TEMPLATE_TYPES.PROCESS_STEPS]: {
    name: '流程步骤',
    description: '展示工作流程和操作步骤',
    maxItems: 6,
    layout: 'horizontal'
  },
  [TEMPLATE_TYPES.COMPARISON]: {
    name: '对比列表',
    description: '方案对比和优劣势分析',
    maxItems: 8,
    layout: 'two-column'
  },
  [TEMPLATE_TYPES.TIMELINE]: {
    name: '时间线',
    description: '项目进度和发展历程',
    maxItems: 8,
    layout: 'vertical'
  },
  [TEMPLATE_TYPES.MEDIA_TEXT]: {
    name: '图文混排',
    description: '产品介绍和功能说明',
    maxItems: 4,
    layout: 'media-text'
  },
  [TEMPLATE_TYPES.TAGS_CLOUD]: {
    name: '标签云',
    description: '技术栈和关键词展示',
    maxItems: 12,
    layout: 'flow'
  },
  [TEMPLATE_TYPES.TEAM_MEMBERS]: {
    name: '人物介绍',
    description: '团队成员和讲师介绍',
    maxItems: 8,
    layout: 'grid-4'
  },
  [TEMPLATE_TYPES.QUOTE_HIGHLIGHT]: {
    name: '引用强调',
    description: '重要声明和核心价值观',
    maxItems: 1,
    layout: 'center'
  },
  [TEMPLATE_TYPES.PROGRESS_BARS]: {
    name: '进度指示器',
    description: '目标达成和进度汇报',
    maxItems: 6,
    layout: 'vertical'
  },
  [TEMPLATE_TYPES.CONTENT_SIMPLE]: {
    name: '基础内容',
    description: '简单的列表内容',
    maxItems: 8,
    layout: 'vertical'
  }
};

/**
 * 将列表项转换为统计卡片数据
 */
export function mapToStatsCards(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;

    // 尝试提取数字、标签和趋势
    const numberMatch = text.match(/[\d,]+\.?\d*\s*[%万千百亿]?/);
    const labelMatch = text.match(/[^\d,]+/);
    const trendMatch = text.match(/[↑↓↗↘]/);

    return {
      id: index,
      number: numberMatch ? numberMatch[0].trim() : '—',
      label: labelMatch ? labelMatch[0].replace(/[():：]/g, '').trim() : text,
      trend: trendMatch ? trendMatch[0] : null,
      trendType: trendMatch && trendMatch[0] === '↑' ? 'up' : 'down',
      originalText: text
    };
  });
}

/**
 * 将列表项转换为流程步骤数据
 */
export function mapToProcessSteps(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;
    const parts = text.split(/[-–—:：]/).map(s => s.trim());

    return {
      id: index + 1,
      title: parts[0] || `步骤 ${index + 1}`,
      description: parts[1] || text,
      originalText: text
    };
  });
}

/**
 * 将列表项转换为对比数据
 */
export function mapToComparison(listItems) {
  const mid = Math.ceil(listItems.length / 2);
  const left = listItems.slice(0, mid);
  const right = listItems.slice(mid);

  return {
    leftTitle: '方案 A',
    rightTitle: '方案 B',
    leftItems: left.map(item => item.text || item),
    rightItems: right.map(item => item.text || item)
  };
}

/**
 * 将列表项转换为时间线数据
 */
export function mapToTimeline(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;

    // 尝试提取日期
    const dateMatch = text.match(/\d{4}年|\d{1,2}月\d{1,2}日|\d{4}[\/-]\d{1,2}[\/-]\d{1,2}/);

    // 尝试分割标题和描述
    const parts = text.split(/[-–—:：]/).map(s => s.trim());

    return {
      id: index + 1,
      date: dateMatch ? dateMatch[0] : `节点 ${index + 1}`,
      title: parts[0] || text.substring(0, 30),
      description: parts[1] || '',
      originalText: text
    };
  });
}

/**
 * 将内容转换为图文混排数据
 */
export function mapToMediaText(section) {
  const images = section.images || [];
  const listItems = section.content?.listItems || [];

  return {
    image: images[0] || null,
    title: section.title,
    description: section.content?.paragraphs?.[0] || '',
    features: listItems.map(item => item.text || item)
  };
}

/**
 * 将列表项转换为标签云数据
 */
export function mapToTagsCloud(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;

    return {
      id: index + 1,
      label: text,
      isPrimary: index < 3 // 前三个标签为主标签
    };
  });
}

/**
 * 将列表项转换为人物介绍数据
 */
export function mapToTeamMembers(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;

    // 尝试提取姓名、职位和简介
    const parts = text.split(/[-–—,，]/).map(s => s.trim());

    return {
      id: index + 1,
      name: parts[0] || '姓名',
      title: parts[1] || '职位',
      bio: parts[2] || '',
      avatar: null,
      originalText: text
    };
  });
}

/**
 * 将内容转换为引用数据
 */
export function mapToQuote(section) {
  const text = section.content?.raw || '';

  // 移除引用标记
  const quote = text.replace(/^>\s*/, '').trim();

  return {
    text: quote,
    author: section.title || ''
  };
}

/**
 * 将列表项转换为进度条数据
 */
export function mapToProgressBars(listItems) {
  return listItems.map((item, index) => {
    const text = item.text || item;

    // 尝试提取百分比
    const percentMatch = text.match(/(\d+(?:\.\d+)?)\s*%/);
    const percent = percentMatch ? parseFloat(percentMatch[1]) : 0;

    // 提取标签
    const label = text.replace(/\d+(?:\.\d+)?\s*%/, '').trim();

    return {
      id: index + 1,
      label: label || text,
      percent: Math.min(100, Math.max(0, percent)),
      originalText: text
    };
  });
}

/**
 * 通用内容映射
 */
export function mapToContentSimple(listItems) {
  return listItems.map(item => ({
    text: item.text || item,
    type: item.type || 'bullet'
  }));
}

/**
 * 根据模板类型选择映射函数
 */
export function mapContentToTemplate(templateType, section) {
  const listItems = section.content?.listItems || [];

  switch (templateType) {
    case TEMPLATE_TYPES.STATS_CARDS:
      return mapToStatsCards(listItems);

    case TEMPLATE_TYPES.PROCESS_STEPS:
      return mapToProcessSteps(listItems);

    case TEMPLATE_TYPES.COMPARISON:
      return mapToComparison(listItems);

    case TEMPLATE_TYPES.TIMELINE:
      return mapToTimeline(listItems);

    case TEMPLATE_TYPES.MEDIA_TEXT:
      return mapToMediaText(section);

    case TEMPLATE_TYPES.TAGS_CLOUD:
      return mapToTagsCloud(listItems);

    case TEMPLATE_TYPES.TEAM_MEMBERS:
      return mapToTeamMembers(listItems);

    case TEMPLATE_TYPES.QUOTE_HIGHLIGHT:
      return mapToQuote(section);

    case TEMPLATE_TYPES.PROGRESS_BARS:
      return mapToProgressBars(listItems);

    case TEMPLATE_TYPES.CONTENT_SIMPLE:
    default:
      return mapToContentSimple(listItems);
  }
}

export default {
  TEMPLATE_TYPES,
  TEMPLATE_CONFIG,
  mapToStatsCards,
  mapToProcessSteps,
  mapToComparison,
  mapToTimeline,
  mapToMediaText,
  mapToTagsCloud,
  mapToTeamMembers,
  mapToQuote,
  mapToProgressBars,
  mapToContentSimple,
  mapContentToTemplate
};
