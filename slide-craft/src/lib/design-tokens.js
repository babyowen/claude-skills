/**
 * 设计令牌系统
 * 确保 HTML 和 PPTX 使用相同的设计标准
 */

export const DESIGN_TOKENS = {
  // 中信配色方案
  colors: {
    primary: 'D20A10',      // 中信红 (无#号，用于PPTX)
    primaryHex: '#D20A10',  // 中信红 (带#号，用于CSS)
    gray5: '575757',        // 深灰
    gray5Hex: '#575757',
    gray4: '898989',        // 次要文字
    gray4Hex: '#898989',
    gray3: 'B5B5B5',        // 边框
    gray3Hex: '#B5B5B5',
    gray2: 'CACACA',        // 卡片背景
    gray2Hex: '#CACACA',
    gray1: 'DDDDDD',        // 页面背景
    gray1Hex: '#DDDDDD',
    white: 'FFFFFF',
    whiteHex: '#FFFFFF',
    black: '000000',
    blackHex: '#000000',

    // 辅助色
    success: '10B981',      // 绿色 - 正向趋势
    successHex: '#10B981',
    danger: 'EF4444',       // 红色 - 负向趋势
    dangerHex: '#EF4444',
    warning: 'F59E0B',      // 橙色
    warningHex: '#F59E0B',
    info: '3B82F6',         // 蓝色
    infoHex: '#3B82F6'
  },

  // 字体
  fonts: {
    // Web 字体
    primary: {
      web: '"KaiTi", "楷体", "STKaiti", serif',  // 楷体（封面专用）
      pptx: 'KaiTi'
    },
    secondary: {
      web: '"PingFang SC", "Microsoft YaHei", sans-serif',  // 平方/微软雅黑
      pptx: 'Microsoft YaHei'
    },
    data: {
      web: '"Roboto", "Arial", sans-serif',  // 数字字体
      pptx: 'Arial'
    }
  },

  // 字号标准 (PPTX 使用 pt，Web 使用 px)
  fontSizes: {
    // 封面
    coverTitle: { web: '4rem', pptx: 48 },      // 封面主标题
    coverSubtitle: { web: '1.8rem', pptx: 22 }, // 封面副标题
    coverDate: { web: '1.5rem', pptx: 18 },     // 封面日期

    // 内容页
    pageTitle: { web: '2rem', pptx: 32 },       // 页面主标题
    pageSubtitle: { web: '1.5rem', pptx: 24 },  // 页面副标题
    bodyText: { web: '1.25rem', pptx: 20 },     // 正文
    listText: { web: '1.125rem', pptx: 18 },    // 列表文字

    // 数据卡片
    statNumber: { web: '2.5rem', pptx: 40 },    // 统计数字
    statLabel: { web: '1rem', pptx: 16 },       // 统计标签

    // 其他
    caption: { web: '0.875rem', pptx: 14 },     // 说明文字
    footnote: { web: '0.75rem', pptx: 12 }      // 脚注
  },

  // 间距 (PPTX 单位: 英寸, Web 单位: px 或 %)
  spacing: {
    // 页边距
    pagePadding: { web: '5%', pptx: 0.5 },

    // 封面专用
    coverMainPadding: { web: '12% 5% 8% 10%', pptx: { t: 1.2, r: 0.5, b: 0.8, l: 1.0 } },
    coverLogoPadding: { web: '3.5% 5% 0 5%', pptx: { t: 0.35, r: 0.5, b: 0, l: 0.5 } },

    // 元素间距
    titleGap: { web: '40px', pptx: 0.4 },
    sectionGap: { web: '30px', pptx: 0.3 },
    itemGap: { web: '20px', pptx: 0.2 },
    cardGap: { web: '20px', pptx: 0.2 }
  },

  // 尺寸
  sizes: {
    // Logo
    logoHeight: { web: '60px', pptx: 0.6 },
    sloganHeight: { web: '60px', pptx: 0.6 },

    // 图标
    iconSmall: { web: '32px', pptx: 0.33 },
    iconMedium: { web: '48px', pptx: 0.5 },
    iconLarge: { web: '64px', pptx: 0.67 },

    // 卡片
    cardMinWidth: { web: '250px', pptx: 2.6 },
    cardMaxWidth: { web: '400px', pptx: 4.17 }
  },

  // 圆角
  borderRadius: {
    small: { web: '4px', pptx: 0.04 },
    medium: { web: '8px', pptx: 0.08 },
    large: { web: '12px', pptx: 0.12 }
  },

  // 阴影 (仅用于 Web)
  shadows: {
    small: '0 2px 8px rgba(0, 0, 0, 0.08)',
    medium: '0 4px 16px rgba(0, 0, 0, 0.1)',
    large: '0 8px 24px rgba(0, 0, 0, 0.12)'
  },

  // PPTX 画布尺寸 (16:9)
  pptxLayout: {
    width: 10,    // 英寸
    height: 5.625 // 英寸
  }
};

/**
 * PPTX 单位转换工具
 */
export const pptxUnit = {
  /**
   * 像素转英寸 (96 DPI)
   */
  pxToInch(px) {
    return px / 96;
  },

  /**
   * 百分比转英寸 (基于 10 英寸宽)
   */
  percentToInch(percent) {
    return (parseFloat(percent) / 100) * 10;
  },

  /**
   * pt 转英寸
   */
  ptToInch(pt) {
    return pt / 72;
  },

  /**
   * Rem 转英寸 (假设基准 16px)
   */
  remToInch(rem) {
    const px = parseFloat(rem) * 16;
    return this.pxToInch(px);
  }
};

/**
 * 获取 PPTX 颜色值 (无#号)
 */
export function getPPTXColor(colorKey) {
  return DESIGN_TOKENS.colors[colorKey] || DESIGN_TOKENS.colors.black;
}

/**
 * 获取 Web 颜色值 (带#号)
 */
export function getWebColor(colorKey) {
  return DESIGN_TOKENS.colors[colorKey + 'Hex'] || DESIGN_TOKENS.colors.blackHex;
}

/**
 * 获取 PPTX 字号 (pt)
 */
export function getPPTXFontSize(sizeKey) {
  const size = DESIGN_TOKENS.fontSizes[sizeKey];
  return size ? size.pptx : 18;
}

/**
 * 获取 Web 字号 (CSS 值)
 */
export function getWebFontSize(sizeKey) {
  const size = DESIGN_TOKENS.fontSizes[sizeKey];
  return size ? size.web : '1rem';
}

export default DESIGN_TOKENS;
