# Common OpenClaw Skill Issues and Solutions

## YAML Frontmatter Issues

### Missing `---` delimiters

**Error**: "SKILL.md must start with YAML frontmatter"

**Solution**: Wrap YAML metadata with `---`:

```yaml
---
name: my-skill
description: My skill description
---
```

### Invalid YAML syntax

**Error**: "YAML parsing error"

**Common causes:**
- Incorrect indentation (use spaces, not tabs)
- Unquoted colons in strings
- Missing commas in lists
- Invalid boolean values (use `true`/`false`, not `True`/`False`)

**Example fix:**

```yaml
# ❌ Wrong
metadata: {openclaw: {emoji: 😀}}

# ✅ Correct
metadata:
{
  "openclaw":
  {
    "emoji": "😀"
  }
}
```

## Required Fields Missing

### Missing name or description

**Error**: "Missing required field: 'name'" or "'description'"

**Solution**: Add both required fields:

```yaml
---
name: my-skill
description: Clear description of when to use this skill and what it does
---
```

**Tip**: Keep description comprehensive - it's the primary triggering mechanism!

## metadata.openclaw Issues

### Not a JSON object

**Error**: "metadata must be a JSON object"

**Solution**: Ensure metadata is a JSON object:

```yaml
# ❌ Wrong
metadata: "just a string"

# ✅ Correct
metadata:
{
  "openclaw":
  {
    "emoji": "🎯"
  }
}
```

### Invalid requires fields

**Error**: "requires.bins must be a list"

**Solution**: Use lists for requires subfields:

```yaml
# ❌ Wrong
metadata:
{
  "openclaw":
  {
    "requires":
    {
      "bins": "single-binary"  # Must be a list
    }
  }
}

# ✅ Correct
metadata:
{
  "openclaw":
  {
    "requires":
    {
      "bins": ["binary1", "binary2"]
    }
  }
}
```

### Invalid OS values

**Error**: "Invalid OS value: 'macos'"

**Solution**: Use valid platform identifiers:

```yaml
# ❌ Wrong
"os": ["macos", "windows", "ubuntu"]

# ✅ Correct
"os": ["darwin", "win32", "linux"]
```

**Valid values**: `darwin`, `linux`, `win32`

## Installer Issues

### Missing required brew fields

**Error**: "brew install[0] missing required field: 'formula'"

**Solution**: Include all required brew installer fields:

```yaml
"install": [
  {
    "id": "brew",
    "kind": "brew",
    "formula": "package-name",      # Required
    "bins": ["binary-name"],        # Required
    "label": "Install Package (brew)"  # Required
  }
]
```

### Missing download URL

**Error**: "download install[0] missing 'url' field"

**Solution**: Add url to download installers:

```yaml
"install": [
  {
    "kind": "download",
    "url": "https://example.com/file.tar.gz",  # Required
    "archive": "tar.gz",
    "targetDir": "~/.openclaw/tools/"
  }
]
```

### Invalid installer kind

**Error**: "install[0] invalid kind: 'apt'"

**Solution**: Use valid installer types:

**Valid kinds**: `brew`, `node`, `go`, `download`

## Body Content Issues

### Empty body

**Warning**: "SKILL.md body is empty"

**Solution**: Add instructions for using the skill:

```markdown
---
name: my-skill
description: Description here
---

# My Skill

## When to use

Use this skill when...

## How to use

1. First step...
2. Second step...
```

### TODO placeholders

**Warning**: "SKILL.md contains TODO items"

**Solution**: Complete all TODO items before publishing:

```markdown
<!-- ❌ Incomplete -->
## TODO: Add usage examples

<!-- ✅ Complete -->
## Usage Examples

Example 1: Basic usage
Example 2: Advanced usage
```

## Config Key Issues

### Skill name with hyphens

**Problem**: Skill names with hyphens need quoted keys in config

**Solution**: Quote the key or use `skillKey`:

```json
// In openclaw.json

// ❌ Wrong (syntax error)
{
  "skills": {
    "entries": {
      "my-skill": {  // Syntax error!
        "enabled": true
      }
    }
  }
}

// ✅ Option 1: Quote the key
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true
      }
    }
  }
}

// ✅ Option 2: Use skillKey in skill
// In SKILL.md:
metadata: {"openclaw": {"skillKey": "my_skill"}}
// In config:
{
  "skills": {
    "entries": {
      "my_skill": {  // No hyphens!
        "enabled": true
      }
    }
  }
}
```

## Environment Variable Issues

### Secrets not injected in sandbox

**Problem**: `skills.entries.*.env` doesn't work in sandboxed sessions

**Solution**: Use sandbox-specific env vars:

```json
// ❌ Doesn't work in sandbox
{
  "skills": {
    "entries": {
      "my-skill": {
        "env": {
          "API_KEY": "secret"
        }
      }
    }
  }
}

// ✅ Use sandbox env vars
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "env": {
            "API_KEY": "secret"
          }
        }
      }
    }
  }
}
```

## Best Practice Violations

### Description too vague

**Problem**: "My skill" or "Helper tool" doesn't tell Claude when to use it

**Solution**: Include triggers and use cases:

```yaml
# ❌ Too vague
description: A helper tool for images

# ✅ Specific and actionable
description: Image processing with rotation, resizing, and format conversion. Use when user needs to modify images (rotate, resize, convert formats, optimize) for: (1) Image rotation, (2) Resizing, (3) Format conversion, (4) Batch operations
```

### Missing instructions

**Problem**: SKILL.md has metadata but no instructions

**Solution**: Always include body content with clear workflow:

```markdown
---
name: my-skill
description: Clear description
---

# Skill Name

## Quick start

[Fastest path to success]

## When to use

[Specific scenarios]

## How it works

[Technical details]

## Examples

[Concrete examples]
```

## Performance Issues

### Token bloat from verbose SKILL.md

**Problem**: SKILL.md too long (>5k words)

**Solution**: Move details to references:

```markdown
# Main Skill

## Overview

[Brief overview]

## Advanced Topics
See [ADVANCED.md](ADVANCED.md) for complex patterns.

## API Reference
See [API.md](API.md) for complete reference.
```

Then create `references/ADVANCED.md` and `references/API.md`.

### Loading unnecessary resources

**Problem**: Always loading large reference files

**Solution**: Load references conditionally:

```markdown
# Main Skill

## Quick start

[Basic usage]

## For X: See [X.md](X.md)
## For Y: See [Y.md](Y.md)
```

Claude only loads X.md or Y.md when needed.

## Debugging Tips

### Test skill locally

1. Place skill in workspace `/skills` or `~/.openclaw/skills`
2. Start new OpenClaw session
3. Check that skill appears in available skills list
4. Test slash command (if `user-invocable: true`)
5. Verify gating rules work (env vars, binaries, etc.)

### Validate before publishing

Use the validation script:

```bash
python /path/to/openclaw-skill-check/scripts/validate_skill.py /path/to/your/skill
```

### Check token usage

Use `/context` command to see skill token impact:
```
/context detail
```

Shows per-skill and per-file token counts.

### Enable verbose logging

Enable to see skill loading details:

```json
// In ~/.openclaw/openclaw.json
{
  "skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 250
    }
  }
}
```

Watch console for skill loading errors.

## Getting Help

- **Documentation**: https://docs.openclaw.ai/tools/skills
- **ClawHub**: Browse skills at https://clawhub.com
- **Validation**: Use `openclaw-skill-check` for automated validation
