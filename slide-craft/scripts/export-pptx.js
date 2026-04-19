#!/usr/bin/env node

/**
 * PPTX Export Script (Enhanced)
 * Generates PowerPoint presentation using the new PPTXExporter
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { PresentationBuilder } from '../src/lib/presentation-builder.js';
import { PPTXExporter } from '../src/lib/pptx-exporter.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const inputPath = process.argv[2] || path.join(__dirname, '../presentation.md');
const outputPath = process.argv[3] || path.join(__dirname, '../dist/presentation.pptx');

async function main() {
  try {
    console.log('🚀 开始生成 PPTX 演示文稿...\n');

    // 检查输入文件
    if (!fs.existsSync(inputPath)) {
      console.error(`❌ 错误: 找不到输入文件 ${inputPath}`);
      console.log('\n使用方法:');
      console.log('  node scripts/export-pptx.js [输入文件] [输出文件]');
      console.log('\n示例:');
      console.log('  node scripts/export-pptx.js presentation.md dist/presentation.pptx');
      process.exit(1);
    }

    // 读取输入内容
    console.log(`📖 读取输入文件: ${inputPath}`);
    const content = fs.readFileSync(inputPath, 'utf-8');

    // 创建演示文稿构建器
    const builder = new PresentationBuilder();

    // 构建演示文稿数据
    console.log('🔧 解析内容并选择模板...');
    const presentationData = await builder.buildFromText(content);

    // 验证演示文稿
    console.log('✅ 验证演示文稿...');
    const validation = builder.validate(presentationData);

    if (!validation.valid) {
      console.error('❌ 演示文稿验证失败:');
      validation.errors.forEach(error => console.error(`  - ${error}`));
      process.exit(1);
    }

    // 获取统计信息
    const stats = builder.getStats(presentationData);
    console.log('\n📊 演示文稿统计:');
    console.log(`  总幻灯片数: ${stats.totalSlides}`);
    console.log(`  总列表项数: ${stats.totalListItems}`);
    console.log(`  包含图片: ${stats.hasImages ? '是' : '否'}`);
    console.log('\n  模板使用情况:');
    Object.entries(stats.templateUsage).forEach(([template, count]) => {
      console.log(`    - ${template}: ${count} 张`);
    });

    // 创建 PPTX 导出器
    const exporter = new PPTXExporter();

    // 导出 PPTX
    console.log(`\n📝 生成 PPTX 文件: ${outputPath}`);
    await exporter.export(presentationData, outputPath);

    console.log('\n✅ PPTX 导出成功!');
    console.log(`📁 输出文件: ${outputPath}`);

  } catch (error) {
    console.error('\n❌ 导出失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
