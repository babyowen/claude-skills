/**
 * 内容分析器
 * 分析内容特征并智能选择最合适的模板
 */

/**
 * 提取内容特征
 */
export function extractFeatures(section) {
  const text = typeof section.content === 'string'
    ? section.content
    : section.content.raw || '';

  const listItems = section.content?.listItems || [];
  const images = section.images || [];

  return {
    // 数字和百分比
    hasNumbers: /\d+[\d,.]*/.test(text),
    hasPercentages: /\d+(\.\d+)?%/.test(text),
    hasLargeNumbers: /\d+[万千百亿]/.test(text),

    // 步骤和流程
    hasSteps: /步骤|阶段|第[一二三四五六七八九十\d]+步|阶段[一二三四五六七八九十\d]+/.test(text),
    hasNumberedSequence: listItems.some(item => item.type === 'number'),
    hasProcessKeywords: /流程|实施|开发|执行|操作/.test(section.title || ''),

    // 对比
    hasComparison: /对比|VS|vs|优劣势|新旧|方案[AB]/.test(text),
    hasVersus: /VS|vs|对比|比较/.test(section.title || ''),

    // 时间线
    hasYears: /\d{4}年/.test(text),
    hasDates: /\d{4}[\/-]\d{1,2}[\/-]\d{1,2}/.test(text) || /\d{1,2}月\d{1,2}日/.test(text),
    hasTimelineKeywords: /里程碑|时间线|进度|历程|发展/.test(section.title || ''),

    // 图文
    hasImages: images.length > 0,
    hasMediaKeywords: /产品|功能|案例|展示|介绍/.test(section.title || ''),

    // 关键词/标签
    hasManyKeywords: listItems.length >= 5 && listItems.every(item => item.text.length < 20),
    hasTechStack: /技术栈|技术|框架|工具|语言/.test(section.title || ''),

    // 人物
    hasPersonNames: /[张王李赵刘陈杨黄周吴徐孙朱马胡郭林何高梁郑罗宋谢唐韩曹许邓萧冯曾程蔡彭潘袁于董余苏叶吕魏蒋田杜丁沈姜范江傅钟卢汪戴崔任陆廖姚方金邱夏谭韦贾邹石熊孟秦阎薛侯雷白龙段郝孔邵史毛常万顾赖武贺龚文]/.test(text),
    hasPersonTitles: /总监|经理|负责人|专家|设计师|工程师|主管|主任/.test(text),

    // 引用
    hasQuoteMarker: /^>/.test(text.trim()),
    hasMissionKeywords: /使命|愿景|价值观|宣言|理念/.test(section.title || ''),

    // 进度
    hasProgressKeywords: /完成率|达成|进度|目标|完成/.test(text),
    hasProgressMarkers: listItems.some(item => /\d+(\.\d+)?%/.test(item.text)),

    // 内容数量
    listItemCount: listItems.length,
    imageCount: images.length,

    // 原始文本
    text
  };
}

/**
 * 计算统计卡片模板分数
 */
function calculateStatsScore(features) {
  let score = 0;

  if (features.hasNumbers) score += 20;
  if (features.hasPercentages) score += 30;
  if (features.hasLargeNumbers) score += 25;

  // 如果有增长/下降关键词
  if (/增长|下降|提升|减少|上升|回落/.test(features.text)) {
    score += 15;
  }

  // 列表项数量适中 (4-6个最适合)
  if (features.listItemCount >= 4 && features.listItemCount <= 6) {
    score += 10;
  }

  return score;
}

/**
 * 计算流程步骤模板分数
 */
function calculateProcessScore(features) {
  let score = 0;

  if (features.hasSteps) score += 35;
  if (features.hasNumberedSequence) score += 25;
  if (features.hasProcessKeywords) score += 20;

  // 步骤数量 (3-6个最合适)
  if (features.listItemCount >= 3 && features.listItemCount <= 6) {
    score += 20;
  }

  return score;
}

/**
 * 计算对比模板分数
 */
function calculateComparisonScore(features) {
  let score = 0;

  if (features.hasComparison) score += 40;
  if (features.hasVersus) score += 30;

  // 列表项数量是偶数（左右对比）
  if (features.listItemCount > 0 && features.listItemCount % 2 === 0) {
    score += 15;
  }

  return score;
}

/**
 * 计算时间线模板分数
 */
function calculateTimelineScore(features) {
  let score = 0;

  if (features.hasYears) score += 35;
  if (features.hasDates) score += 25;
  if (features.hasTimelineKeywords) score += 25;

  // 3-8个时间点最合适
  if (features.listItemCount >= 3 && features.listItemCount <= 8) {
    score += 15;
  }

  return score;
}

/**
 * 计算图文混排模板分数
 */
function calculateMediaTextScore(features) {
  let score = 0;

  if (features.hasImages) score += 40;
  if (features.hasMediaKeywords) score += 20;

  // 有描述性文字
  if (features.listItemCount > 0 && features.listItemCount <= 4) {
    score += 20;
  }

  return score;
}

/**
 * 计算标签云模板分数
 */
function calculateTagsScore(features) {
  let score = 0;

  if (features.hasManyKeywords) score += 35;
  if (features.hasTechStack) score += 25;

  // 关键词数量多
  if (features.listItemCount >= 6) {
    score += 25;
  }

  return score;
}

/**
 * 计算人物介绍模板分数
 */
function calculateTeamScore(features) {
  let score = 0;

  if (features.hasPersonNames) score += 30;
  if (features.hasPersonTitles) score += 30;

  // 2-8个人物
  if (features.listItemCount >= 2 && features.listItemCount <= 8) {
    score += 25;
  }

  return score;
}

/**
 * 计算引用模板分数
 */
function calculateQuoteScore(features) {
  let score = 0;

  if (features.hasQuoteMarker) score += 40;
  if (features.hasMissionKeywords) score += 35;

  return score;
}

/**
 * 计算进度条模板分数
 */
function calculateProgressScore(features) {
  let score = 0;

  if (features.hasProgressKeywords) score += 30;
  if (features.hasProgressMarkers) score += 35;

  // 3-6个进度项
  if (features.listItemCount >= 3 && features.listItemCount <= 6) {
    score += 20;
  }

  return score;
}

/**
 * 分析并选择最合适的模板
 */
export function analyzeAndSelectTemplate(section) {
  // 如果已经指定了模板，直接返回
  if (section.template) {
    return section.template;
  }

  // 标题页固定使用 title-slide
  if (section.type === 'title') {
    return 'title-slide';
  }

  const features = extractFeatures(section);

  // 计算每个模板的匹配分数
  const scores = {
    'stats-cards': calculateStatsScore(features),
    'process-steps': calculateProcessScore(features),
    'comparison': calculateComparisonScore(features),
    'timeline': calculateTimelineScore(features),
    'media-text': calculateMediaTextScore(features),
    'tags-cloud': calculateTagsScore(features),
    'team-members': calculateTeamScore(features),
    'quote-highlight': calculateQuoteScore(features),
    'progress-bars': calculateProgressScore(features)
  };

  // 找出得分最高的模板
  let maxScore = 0;
  let bestTemplate = 'content-simple'; // 默认使用简单内容模板

  Object.entries(scores).forEach(([template, score]) => {
    if (score > maxScore) {
      maxScore = score;
      bestTemplate = template;
    }
  });

  // 如果最高分太低，使用基础列表模板
  if (maxScore < 30) {
    return 'content-simple';
  }

  return bestTemplate;
}

/**
 * 获取模板的推荐动画配置
 */
export function getTemplateAnimationConfig(template) {
  const configs = {
    'stats-cards': {
      type: 'scale',
      duration: 0.6,
      stagger: 0.15,
      ease: 'back.out(1.7)'
    },
    'process-steps': {
      type: 'slideLeft',
      duration: 0.5,
      stagger: 0.2,
      ease: 'power2.out'
    },
    'comparison': {
      type: 'slideOpposite',
      duration: 0.6,
      stagger: 0.1,
      ease: 'power3.out'
    },
    'timeline': {
      type: 'fadeUp',
      duration: 0.5,
      stagger: 0.25,
      ease: 'power2.out'
    },
    'media-text': {
      type: 'slideCross',
      duration: 0.7,
      stagger: 0,
      ease: 'power3.out'
    },
    'tags-cloud': {
      type: 'pop',
      duration: 0.4,
      stagger: 0.08,
      ease: 'back.out(2)'
    },
    'team-members': {
      type: 'rise',
      duration: 0.6,
      stagger: 0.15,
      ease: 'power3.out'
    },
    'quote-highlight': {
      type: 'scaleCenter',
      duration: 0.8,
      stagger: 0,
      ease: 'power4.out'
    },
    'progress-bars': {
      type: 'fill',
      duration: 1.0,
      stagger: 0.2,
      ease: 'power2.out'
    },
    'content-simple': {
      type: 'fadeUp',
      duration: 0.5,
      stagger: 0.15,
      ease: 'power2.out'
    }
  };

  return configs[template] || configs['content-simple'];
}

export default {
  extractFeatures,
  analyzeAndSelectTemplate,
  getTemplateAnimationConfig,
  calculateStatsScore,
  calculateProcessScore,
  calculateComparisonScore,
  calculateTimelineScore,
  calculateMediaTextScore,
  calculateTagsScore,
  calculateTeamScore,
  calculateQuoteScore,
  calculateProgressScore
};
