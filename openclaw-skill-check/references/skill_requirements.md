# OpenClaw Skill Requirements

Complete checklist of OpenClaw skill requirements based on official documentation.

## Skill Structure

```
skill-name/
├── SKILL.md (required)
└── [optional resources]
    ├── scripts/
    ├── references/
    └── assets/
```

## SKILL.md Format

### Required YAML Frontmatter

Every SKILL.md must include at minimum:

```yaml
---
name: skill-name
description: Brief description of what the skill does
---
```

**Fields:**
- `name` (required): The skill identifier
- `description` (required): Primary triggering mechanism - describe both what the skill does AND when to use it

### Optional YAML Frontmatter Fields

- `user-invocable`: `true|false` (default: true)
  - When true, skill is exposed as a user slash command
  - When false, skill only available via direct model invocation

- `disable-model-invocation`: `true|false` (default: false)
  - When true, skill excluded from model prompt
  - Still available via user invocation

- `command-dispatch`: `tool` (optional)
  - When set to `tool`, slash command bypasses model and dispatches directly to a tool

- `command-tool`: tool name (required when command-dispatch: tool)
  - Tool name to invoke when using tool dispatch

- `command-arg-mode`: `raw` (default)
  - For tool dispatch, forwards raw args string to tool (no core parsing)

### metadata.openclaw (Optional Gating Configuration)

```yaml
---
metadata:
{
  "openclaw": {
    "always": true,  // optional: always include skill (skip other gates)
    "emoji": "🎯",  // optional: emoji for macOS Skills UI
    "homepage": "https://example.com",  // optional: website URL
    "skillKey": "custom-key",  // optional: override config key name
    "os": ["darwin", "linux"],  // optional: platform whitelist
    "primaryEnv": "API_KEY_NAME",  // optional: primary env var name
    "requires": {
      "bins": ["binary-name"],  // list: must exist on PATH
      "anyBins": ["opt1", "opt2"],  // list: at least one must exist
      "env": ["VAR_NAME"],  // list: env var must exist or be in config
      "config": ["config.path"]  // list: config paths must be truthy
    },
    "install": [  // optional: installer specifications
      {
        "id": "brew",
        "kind": "brew",
        "formula": "package-name",
        "bins": ["binary-name"],
        "label": "Install Package Name (brew)",
        "os": ["darwin"]  // optional: platform filter
      }
    ]
  }
}
---
```

#### metadata.openclaw Fields

**Simple fields:**
- `always`: `true` - always include skill (skip other gates)
- `emoji`: string - emoji for macOS Skills UI
- `homepage`: URL - shown as "Website" in macOS Skills UI
- `skillKey`: string - override config key name in skills.entries
- `primaryEnv`: string - env var name for skills.entries.*.apiKey
- `os`: list - platform filter (`darwin`, `linux`, `win32`)

**requires (gating rules):**
- `bins`: list - all must exist on PATH
- `anyBins`: list - at least one must exist on PATH
- `env`: list - env var must exist OR be provided in config
- `config`: list - openclaw.json paths that must be truthy

**install (installers):**
- `kind`: installer type - `brew`, `node`, `go`, or `download`
- `id`: identifier
- `label`: display label
- `os`: optional platform filter

**Brew installer:**
- `formula`: formula name
- `bins`: list of binaries installed

**Node installer:**
- `bins`: list of binaries

**Go installer:**
- `bins`: list of binaries

**Download installer:**
- `url`: required download URL
- `archive`: `tar.gz` | `tar.bz2` | `zip`
- `extract`: boolean (default: auto when archive detected)
- `stripComponents`: number
- `targetDir`: path (default: `~/.openclaw/tools/`)

## Skill Loading Locations

Skills load from three places (precedence highest to lowest):

1. **Workspace skills**: `/skills` (highest precedense)
2. **Managed/local skills**: `~/.openclaw/skills`
3. **Bundled skills**: shipped with install (lowest)

Same skill name in multiple locations: workspace wins.

## Config Overrides

Per-skill configuration in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "skill-name": {
        "enabled": true,
        "apiKey": "API_KEY_HERE",
        "env": {
          "API_VAR": "value"
        },
        "config": {
          "customField": "value"
        }
      }
    }
  }
}
```

**Fields:**
- `enabled`: `false` disables skill even if bundled/installed
- `env`: injected only if variable not already set
- `apiKey`: convenience for skills with `primaryEnv`
- `config`: optional bag for custom per-skill fields

## Common Patterns

### User-Invocable Skills (Slash Commands)

Skills with `user-invocable: true` (default) are exposed as slash commands:
- Names sanitized to `a-z0-9_` (max 32 chars)
- Collisions get numeric suffixes (e.g., `_2`)

### Tool-Dispatched Commands

Set `command-dispatch: tool` + `command-tool` to route directly to tool:
- Bypasses model (deterministic, no model invocation)
- Tool invoked with params: `{ command: "", commandName: "", skillName: "" }`

### Environment Injection

When agent run starts:
1. Reads skill metadata
2. Applies `skills.entries.*.env` or `skills.entries.*.apiKey` to process.env
3. Builds system prompt with eligible skills
4. Restores original environment after run ends

Scoped to agent run, not global shell environment.

## Token Impact

Skills list injected into system prompt:
- **Base overhead** (only when ≥1 skill): 195 characters
- **Per skill**: 97 characters + length of XML-escaped name, description, location

Formula: `total = 195 + Σ (97 + len(name) + len(description) + len(location))`

Rough estimate: ~4 chars/token, so 97 chars ≈ 24 tokens per skill plus field lengths.

## Security Notes

- Treat third-party skills as **untrusted code** - read before enabling
- Prefer sandboxed runs for untrusted inputs
- `skills.entries.*.env` and `skills.entries.*.apiKey` inject secrets into host process
- Keep secrets out of prompts and logs

## Validation Checklist

- ✅ SKILL.md exists
- ✅ YAML frontmatter present (starts with `---`)
- ✅ `name` field present
- ✅ `description` field present
- ✅ metadata.openclaw is valid JSON object (if present)
- ✅ `user-invocable` is boolean (if present)
- ✅ `requires.*` fields are lists (if present)
- ✅ `os` values are valid platforms
- ✅ `install[*].kind` is valid installer type
- ✅ brew installers have required fields (formula, bins, label)
- ✅ download installers have url field
- ✅ Body content present (not just TODO placeholders)
