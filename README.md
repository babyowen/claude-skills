# Claude Skills

我的 Claude Code Skills 集合，用于扩展 Claude Code 的能力。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [think-think](./think-think) | 深度思考辅助工具，采用多 agent 协作模式帮助用户澄清目标、收集背景、设计方案、批判审视 |
| [openclaw-skill-check](./openclaw-skill-check) | OpenClaw skill 验证器，检查 SKILL.md 格式和 metadata.openclaw 结构 |
| [ppt-to-web](./ppt-to-web) | PPT 转 Web 演示工具，使用 GSAP 动画库将 PPT 大纲转换为精美的 HTML 演示文稿 |
| [skill-creator](./skill-creator) | Skill 创建向导，帮助创建新的 skill |

> **注意**: `ui-ux-pro-max` 是第三方 skill，需要单独安装，参见下方说明。

## 安装方法

### 方法 1：克隆到 skills 目录

```bash
# 进入 Claude Code skills 目录
cd ~/.claude/skills

# 克隆仓库
git clone https://github.com/babyowen/claude-skills.git .
```

### 方法 2：复制单个 skill

如果你只需要某个特定的 skill：

```bash
# 复制单个 skill 到你的 skills 目录
cp -r claude-skills/think-think ~/.claude/skills/
```

### UI/UX Pro Max（第三方）

这个 skill 来自 [uupm.cc](https://uupm.cc)，需要单独安装：

```bash
# 首次安装
npm install -g uipro-cli
uipro init --ai claude

# 升级到最新版本
uipro update                    # 更新 CLI
uipro init --ai claude --force  # 重新安装 skill
```

更多选项：`uipro --help`

## 使用方法

安装后，在 Claude Code 中可以通过以下方式使用：

- **自动触发**：根据 skill 的 description 自动匹配
- **手动调用**：使用 `/skill-name` 命令，如 `/think-think`

## 目录结构

```
claude-skills/
├── think-think/            # 深度思考 skill
│   ├── SKILL.md
│   └── agents/
├── openclaw-skill-check/   # Skill 验证器
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── ppt-to-web/             # PPT 转 Web 演示
│   ├── SKILL.md
│   ├── src/
│   ├── dist/
│   └── demos/
└── skill-creator/          # Skill 创建工具
    ├── SKILL.md
    ├── scripts/
    └── references/
```

## 创建新 Skill

使用 skill-creator 来创建新的 skill：

```
/skill-creator
```

或参考 [OpenClaw Skills 文档](https://docs.openclaw.ai/tools/skills) 了解更多。

## License

MIT
