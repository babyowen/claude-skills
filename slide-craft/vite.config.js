import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { resolve } from 'path'

export default defineConfig({
  plugins: [viteSingleFile()],
  root: 'src',
  publicDir: false,
  build: {
    // 所有资源都内联为 Base64
    assetsInlineLimit: Infinity,
    // 不分割代码
    cssCodeSplit: false,
    // 输出目录
    outDir: '../dist',
    // 目标浏览器
    target: 'es2015',
    // 清空输出目录
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'src/index.html')
    }
  }
})
