/**
 * 图片处理器
 * 处理本地和远程图片，转换为 Base64
 */

import fs from 'fs/promises';
import path from 'path';

/**
 * 检查是否为远程 URL
 */
function isRemoteUrl(url) {
  return url.startsWith('http://') || url.startsWith('https://');
}

/**
 * 检查是否为 Data URL
 */
function isDataUrl(url) {
  return url.startsWith('data:');
}

/**
 * 下载远程图片
 * 注意：在浏览器环境中需要使用 fetch
 */
async function downloadRemoteImage(url) {
  try {
    // 在 Node.js 环境中
    if (typeof window === 'undefined') {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`下载图片失败: ${response.statusText}`);
      }
      const arrayBuffer = await response.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      return buffer;
    } else {
      // 浏览器环境
      const response = await fetch(url);
      const blob = await response.blob();
      return blob;
    }
  } catch (error) {
    console.error('下载远程图片失败:', error);
    throw error;
  }
}

/**
 * 读取本地图片
 */
async function readLocalImage(imagePath, basePath = './src') {
  try {
    const fullPath = path.resolve(basePath, imagePath);
    const buffer = await fs.readFile(fullPath);
    return buffer;
  } catch (error) {
    console.error('读取本地图片失败:', error);
    throw error;
  }
}

/**
 * Buffer 转 Base64
 */
function bufferToBase64(buffer, mimeType = 'image/png') {
  if (Buffer.isBuffer(buffer)) {
    return `data:${mimeType};base64,${buffer.toString('base64')}`;
  } else if (buffer instanceof Blob) {
    // 浏览器环境
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(buffer);
    });
  }
  throw new Error('不支持的 buffer 类型');
}

/**
 * 获取图片 MIME 类型
 */
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp'
  };
  return mimeTypes[ext] || 'image/png';
}

/**
 * 处理单个图片
 */
export async function processImage(imageSource, options = {}) {
  const {
    basePath = './src',
    convertToBase64 = true,
    maxSize = 10 * 1024 * 1024 // 10MB
  } = options;

  try {
    // 如果已经是 Data URL，直接返回
    if (isDataUrl(imageSource)) {
      return {
        success: true,
        data: imageSource,
        isBase64: true
      };
    }

    let buffer;
    let mimeType = 'image/png';

    // 远程图片
    if (isRemoteUrl(imageSource)) {
      buffer = await downloadRemoteImage(imageSource);
      // 尝试从 URL 获取 MIME 类型
      const urlPath = new URL(imageSource).pathname;
      mimeType = getMimeType(urlPath);
    }
    // 本地图片
    else {
      buffer = await readLocalImage(imageSource, basePath);
      mimeType = getMimeType(imageSource);
    }

    // 检查文件大小
    if (buffer.length > maxSize) {
      console.warn(`图片过大 (${(buffer.length / 1024 / 1024).toFixed(2)}MB)，建议压缩`);
    }

    // 转换为 Base64
    if (convertToBase64) {
      const base64 = await bufferToBase64(buffer, mimeType);
      return {
        success: true,
        data: base64,
        isBase64: true,
        mimeType,
        size: buffer.length
      };
    }

    return {
      success: true,
      data: buffer,
      isBase64: false,
      mimeType,
      size: buffer.length
    };
  } catch (error) {
    console.error('处理图片失败:', error);
    return {
      success: false,
      error: error.message,
      data: null
    };
  }
}

/**
 * 批量处理图片
 */
export async function processImages(imageSources, options = {}) {
  const results = await Promise.all(
    imageSources.map(src => processImage(src, options))
  );

  return results;
}

/**
 * 提取幻灯片中的所有图片 URL
 */
export function extractImageUrls(slides) {
  const urls = new Set();

  slides.forEach(slide => {
    // 封面页背景
    if (slide.type === 'title' && slide.background) {
      urls.add(slide.background);
    }

    // 图片数组
    if (slide.images && Array.isArray(slide.images)) {
      slide.images.forEach(img => {
        if (img.url) {
          urls.add(img.url);
        }
      });
    }

    // 图文混排模板
    if (slide.template === 'media-text' && slide.mappedData?.image?.url) {
      urls.add(slide.mappedData.image.url);
    }
  });

  return Array.from(urls);
}

/**
 * 预处理演示文稿中的所有图片
 */
export async function preprocessPresentationImages(presentationData, options = {}) {
  const imageUrls = extractImageUrls(presentationData.slides);
  const imageMap = new Map();

  // 并发处理所有图片
  const results = await processImages(imageUrls, options);

  imageUrls.forEach((url, index) => {
    if (results[index].success) {
      imageMap.set(url, results[index].data);
    }
  });

  return imageMap;
}

/**
 * 图片压缩 (简单实现)
 * 注意：需要安装 sharp 库来实现真正的压缩
 */
export async function compressImage(buffer, options = {}) {
  const {
    quality = 80,
    maxWidth = 1920,
    maxHeight = 1080
  } = options;

  // 这里只是占位符
  // 实际实现需要使用 sharp 或 jimp 库
  console.warn('图片压缩功能需要安装 sharp 库');
  return buffer;
}

export default {
  processImage,
  processImages,
  extractImageUrls,
  preprocessPresentationImages,
  compressImage,
  isRemoteUrl,
  isDataUrl,
  bufferToBase64,
  getMimeType
};
