# Claude Skills

我的 Claude Code Skills 集合，用于扩展 Claude Code 的能力。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [deepthink](./deepthink) | 深度思考辅助工具，采用多 agent 协作模式帮助用户澄清目标、收集背景、设计方案、批判审视 |
| [openclaw-skill-check](./openclaw-skill-check) | OpenClaw skill 验证器，检查 SKILL.md 格式和 metadata.openclaw 结构 |
| [skill-creator](./skill-creator) | Skill 创建向导，帮助创建新的 skill |
| [ui-ux-pro-max](./ui-ux-pro-max) | UI/UX 设计智能助手，支持多种框架和设计风格 |

## 安装方法

### 方法 1：克隆到 skills 目录

```bash
# 进入 Claude Code skills 目录
cd ~/.claude/skills

# 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-skills.git .
```

### 方法 2：复制单个 skill

如果你只需要某个特定的 skill：

```bash
# 复制单个 skill 到你的 skills 目录
cp -r claude-skills/deepthink ~/.claude/skills/
```

## 使用方法

安装后，在 Claude Code 中可以通过以下方式使用：

- **自动触发**：根据 skill 的 description 自动匹配
- **手动调用**：使用 `/skill-name` 命令，如 `/deepthink`

## 目录结构

```
claude-skills/
├── deepthink/              # 深度思考 skill
│   ├── SKILL.md
│   └── agents/
├── openclaw-skill-check/   # Skill 验证器
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── skill-creator/          # Skill 创建工具
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── ui-ux-pro-max/          # UI/UX 设计工具
    ├── SKILL.md
    ├── scripts/
    └── data/
```

## 创建新 Skill

使用 skill-creator 来创建新的 skill：

```
/skill-creator
```

或参考 [OpenClaw Skills 文档](https://docs.openclaw.ai/tools/skills) 了解更多。

## License

MIT
