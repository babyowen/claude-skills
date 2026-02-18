---
name: openclaw-skill-check
description: Validate OpenClaw skills against official documentation requirements. Use when checking SKILL.md format, validating metadata.openclaw structure, verifying skill gating rules, checking installer specifications, or ensuring OpenClaw best practices
---

# OpenClaw Skill Validator

Validate OpenClaw skills against official documentation to ensure compliance and best practices.

## Quick Start

Use the validation script for automated checking:

```bash
python /path/to/openclaw-skill-check/scripts/validate_skill.py /path/to/skill
```

Example:
```bash
python ~/.claude/skills/openclaw-skill-check/scripts/validate_skill.py ./skills/my-skill
```

## What Gets Validated

### Structure
- ✅ SKILL.md exists
- ✅ YAML frontmatter format (`---` delimiters)
- ✅ Folder structure (scripts/, references/, assets/)

### Required Fields
- ✅ `name` present
- ✅ `description` present

### Optional Fields
- ✅ `user-invocable` (boolean check)
- ✅ `disable-model-invocation` (boolean check)
- ✅ `command-dispatch` (must be `tool` if set)
- ✅ `command-tool` (required when using tool dispatch)
- ✅ `command-arg-mode` (must be `raw` for tool dispatch)

### metadata.openclaw
- ✅ Metadata is valid JSON object
- ✅ `requires.bins` is a list of binary names
- ✅ `requires.anyBins` is a list (at least one must exist)
- ✅ `requires.env` is a list of env var names
- ✅ `requires.config` is a list of config paths
- ✅ `os` contains valid platforms (`darwin`, `linux`, `win32`)
- ✅ `primaryEnv` is set (for apiKey config)
- ✅ `skillKey` is set (for custom config keys)

### Installers
- ✅ `install` is a list
- ✅ `install[*].kind` is valid (`brew`, `node`, `go`, `download`)
- ✅ `brew` installers have: `formula`, `bins`, `label`
- ✅ `download` installers have: `url`
- ✅ Installer `os` filters are valid platforms

### Content
- ✅ SKILL.md body is not empty
- ✅ No TODO placeholders in body
- ✅ Reasonable word count (<5k words for body)

## When to Use

Use this skill when:
- Creating a new OpenClaw skill and want to verify it's correct
- Downloading skills from ClawHub and want to check quality
- Debugging why a skill isn't loading or appearing
- Preparing to publish a skill to ClawHub
- Reviewing someone else's skill for compliance

## Common Issues

See [common_issues.md](references/common_issues.md) for:
- YAML syntax errors
- Missing required fields
- Invalid metadata structure
- Broken installer specs
- Config key problems
- Security considerations

## Complete Requirements

See [skill_requirements.md](references/skill_requirements.md) for:
- Full frontmatter field reference
- All metadata.openclaw options
- Gating rules (requires.*)
- Installer specifications
- Config override patterns
- Token impact calculations

## Manual Validation Checklist

If not using the script, verify manually:

1. **SKILL.md exists**
   - Located at skill root
   - Contains YAML frontmatter

2. **Frontmatter complete**
   - Has `name` field
   - Has `description` field
   - Description is specific and actionable

3. **metadata.openclaw valid** (if present)
   - Is JSON object
   - Fields are correct types
   - Installers have required fields

4. **Body content present**
   - Not just TODO placeholders
   - Contains actual instructions
   - Consider splitting if >5k words

## Fixing Validation Errors

The validation script provides specific error messages with line numbers where possible.

**YAML Errors**
- Check indentation (use spaces, not tabs)
- Verify `---` delimiters
- Ensure quotes around special characters

**Missing Fields**
- Add required `name` and `description`
- Include installer required fields (formula, bins, label for brew)

**Type Errors**
- Boolean fields: `true` or `false`
- Lists: use `[item1, item2]`
- Objects: use `{key: value}`

## Best Practices

### Description Quality
Good descriptions trigger the skill at the right time:

```yaml
# ❌ Too vague
description: A helper for images

# ✅ Specific and actionable
description: Image processing with rotation, resizing, and format conversion. Use when user needs to modify images (rotate, resize, convert formats, optimize) for: (1) Image rotation, (2) Resizing, (3) Format conversion, (4) Batch operations
```

### Progressive Disclosure
Keep SKILL.md lean by moving details to references:

```markdown
# Main Skill

## Overview
[Brief overview]

## Advanced Topics
See [ADVANCED.md](ADVANCED.md) for complex patterns.

## API Reference
See [API.md](API.md) for complete reference.
```

### Environment Variables
Document required env vars in metadata.openclaw:

```yaml
metadata:
{
  "openclaw":
  {
    "requires":
    {
      "env": ["MY_API_KEY"]
    },
    "primaryEnv": "MY_API_KEY"
  }
}
```

Then users can configure via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "apiKey": "actual-key-here"
      }
    }
  }
}
```

## Resources

### Scripts

- `validate_skill.py` - Automated validation script
  - Checks all requirements from official docs
  - Provides actionable error messages
  - Exit code: 0 (pass), 1 (fail)

### References

- `skill_requirements.md` - Complete requirements checklist
- `common_issues.md` - Problems and solutions

## Token Impact

Skills contribute to context window. Keep SKILL.md concise:
- Base overhead: ~195 characters (when ≥1 skill)
- Per skill: ~97 characters + field lengths
- Rough estimate: ~4 chars/token

Monitor token usage with `/context detail` command.

## Security

Treat third-party skills as untrusted code:
- Read skill code before enabling
- Prefer sandboxed runs for untrusted inputs
- Never commit API keys in skill files
- Use `skills.entries.*.apiKey` for user-provided secrets

## Getting Help

- **Official docs**: https://docs.openclaw.ai/tools/skills
- **ClawHub**: https://clawhub.com
- **Report issues**: https://github.com/anthropics/claude-code/issues
