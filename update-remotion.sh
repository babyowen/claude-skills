#!/bin/bash
# 更新 Remotion skill

SKILL_DIR="$HOME/.claude/skills/remotion"
BASE_URL="https://raw.githubusercontent.com/remotion-dev/remotion/master/packages/skills/skills/remotion"

mkdir -p "$SKILL_DIR/rules/assets"

# 下载 SKILL.md
curl -fsSL -o "$SKILL_DIR/SKILL.md" "$BASE_URL/SKILL.md"

# 所有规则文件列表
RULES=(
  3d
  animations
  audio
  audio-visualization
  calculate-metadata
  can-decode
  charts
  compositions
  display-captions
  extract-frames
  ffmpeg
  fonts
  get-audio-duration
  get-video-dimensions
  get-video-duration
  gifs
  images
  import-srt-captions
  light-leaks
  lottie
  maps
  measuring-dom-nodes
  measuring-text
  parameters
  sequencing
  subtitles
  tailwind
  text-animations
  timing
  transcribe-captions
  transitions
  transparent-videos
  trimming
  videos
  voiceover
)

# 下载所有规则文件
cd "$SKILL_DIR/rules"
for file in "${RULES[@]}"; do
  curl -fsSL -o "${file}.md" "$BASE_URL/rules/${file}.md"
done

# 下载 assets
cd assets
curl -fsSL -o charts-bar-chart.tsx "$BASE_URL/rules/assets/charts-bar-chart.tsx"
curl -fsSL -o text-animations-typewriter.tsx "$BASE_URL/rules/assets/text-animations-typewriter.tsx"
curl -fsSL -o text-animations-word-highlight.tsx "$BASE_URL/rules/assets/text-animations-word-highlight.tsx"

echo "✅ Remotion skill updated!"
