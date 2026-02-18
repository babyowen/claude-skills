#!/usr/bin/env python3
"""
OpenClaw Skill Validator
Validates OpenClaw skills against official documentation requirements.
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SkillValidator:
    """Validates OpenClaw skill structure and content."""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path).resolve()
        self.skill_dir = self.skill_path if self.skill_path.is_dir() else self.skill_path.parent
        self.skill_md = self.skill_dir / "SKILL.md"
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_all(self) -> bool:
        """Run all validation checks."""
        print(f"🔍 Validating OpenClaw skill: {self.skill_dir}\n")

        # Structure checks
        self._check_skill_md_exists()

        if not self.skill_md.exists():
            self._print_results()
            return False

        # Parse frontmatter and body
        frontmatter, body = self._parse_skill_md()
        if frontmatter is None:
            self._print_results()
            return False

        # Required fields
        self._check_required_fields(frontmatter)

        # Optional fields
        self._check_optional_fields(frontmatter)

        # metadata.openclaw validation
        if 'metadata' in frontmatter:
            self._validate_metadata_openclaw(frontmatter['metadata'])

        # Body content
        self._check_body_content(body)

        self._print_results()
        return len(self.errors) == 0

    def _check_skill_md_exists(self):
        """Check if SKILL.md exists."""
        if self.skill_md.exists():
            self.info.append("✅ SKILL.md found")
        else:
            self.errors.append("❌ SKILL.md not found. Each skill must have a SKILL.md file.")

    def _parse_skill_md(self) -> Tuple[Optional[dict], Optional[str]]:
        """Parse YAML frontmatter and markdown body."""
        try:
            with open(self.skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split frontmatter and body
            if not content.startswith('---'):
                self.errors.append("❌ SKILL.md must start with YAML frontmatter (---)")
                return None, None

            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append("❌ Invalid frontmatter format. Must start and end with ---")
                return None, None

            frontmatter_text = parts[1].strip()
            body = parts[2].strip() if len(parts) > 2 else ""

            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_text)

            if frontmatter is None:
                frontmatter = {}

            self.info.append("✅ YAML frontmatter parsed successfully")
            return frontmatter, body

        except yaml.YAMLError as e:
            self.errors.append(f"❌ YAML parsing error: {e}")
            return None, None
        except Exception as e:
            self.errors.append(f"❌ Error reading SKILL.md: {e}")
            return None, None

    def _check_required_fields(self, frontmatter: dict):
        """Check required fields in frontmatter."""
        required = ['name', 'description']

        for field in required:
            if field in frontmatter and frontmatter[field]:
                self.info.append(f"✅ Required field '{field}' present")
            else:
                self.errors.append(f"❌ Missing required field: '{field}'")

    def _check_optional_fields(self, frontmatter: dict):
        """Check optional fields and provide guidance."""
        optional_fields = {
            'user-invocable': 'bool',
            'disable-model-invocation': 'bool',
            'command-dispatch': 'tool',
            'command-tool': 'str',
        }

        for field, expected_type in optional_fields.items():
            if field in frontmatter:
                value = frontmatter[field]
                self.info.append(f"✅ Optional field '{field}' present (value: {value})")

                # Type validation
                if expected_type == 'bool' and not isinstance(value, bool):
                    self.warnings.append(f"⚠️  '{field}' should be boolean (true/false), got: {value}")
                elif expected_type == 'str' and not isinstance(value, str):
                    self.warnings.append(f"⚠️  '{field}' should be string, got: {type(value).__name__}")

    def _validate_metadata_openclaw(self, metadata: dict):
        """Validate metadata.openclaw structure."""
        if not isinstance(metadata, dict):
            self.errors.append(f"❌ metadata must be a JSON object, got: {type(metadata).__name__}")
            return

        if 'openclaw' not in metadata:
            self.warnings.append("⚠️  No metadata.openclaw found. Skill is always eligible (no gating).")
            return

        openclaw = metadata['openclaw']

        if not isinstance(openclaw, dict):
            self.errors.append(f"❌ metadata.openclaw must be a JSON object, got: {type(openclaw).__name__}")
            return

        self.info.append("✅ metadata.openclaw found")

        # Check fields
        self._check_openclaw_fields(openclaw)

    def _check_openclaw_fields(self, openclaw: dict):
        """Check specific metadata.openclaw fields."""
        # Optional fields
        optional_simple = ['emoji', 'homepage', 'primaryEnv', 'skillKey']
        for field in optional_simple:
            if field in openclaw:
                self.info.append(f"✅ metadata.openclaw.{field} present")

        # requires field
        if 'requires' in openclaw:
            self._validate_requires(openclaw['requires'])

        # os field
        if 'os' in openclaw:
            self._validate_os_field(openclaw['os'])

        # install field
        if 'install' in openclaw:
            self._validate_install(openclaw['install'])

    def _validate_requires(self, requires: dict):
        """Validate requires gating rules."""
        if not isinstance(requires, dict):
            self.errors.append(f"❌ metadata.openclaw.requires must be a JSON object")
            return

        self.info.append("✅ metadata.openclaw.requires present")

        # Check sub-fields
        valid_subfields = ['bins', 'anyBins', 'env', 'config']
        for field in requires:
            if field in valid_subfields:
                value = requires[field]
                if not isinstance(value, list):
                    self.errors.append(f"❌ requires.{field} must be a list, got: {type(value).__name__}")
                else:
                        self.info.append(f"✅ requires.{field} defined ({len(value)} items)")
            else:
                self.warnings.append(f"⚠️  Unknown requires field: '{field}'")

    def _validate_os_field(self, os_field):
        """Validate os field."""
        if not isinstance(os_field, list):
            self.errors.append(f"❌ metadata.openclaw.os must be a list, got: {type(os_field).__name__}")
            return

        valid_os = ['darwin', 'linux', 'win32']
        for os_val in os_field:
            if os_val in valid_os:
                self.info.append(f"✅ os filter: {os_val}")
            else:
                self.errors.append(f"❌ Invalid OS value: '{os_val}'. Valid: {valid_os}")

    def _validate_install(self, install: list):
        """Validate install specifications."""
        if not isinstance(install, list):
            self.errors.append(f"❌ metadata.openclaw.install must be a list, got: {type(install).__name__}")
            return

        self.info.append(f"✅ metadata.openclaw.install defined ({len(install)} installers)")

        valid_kinds = ['brew', 'node', 'go', 'download']

        for idx, installer in enumerate(install):
            if not isinstance(installer, dict):
                self.errors.append(f"❌ install[{idx}] must be a JSON object")
                continue

            if 'kind' not in installer:
                self.errors.append(f"❌ install[{idx}] missing 'kind' field")
                continue

            kind = installer['kind']
            if kind in valid_kinds:
                self.info.append(f"✅ install[{idx}] kind: {kind}")
                self._validate_installer_fields(kind, installer, idx)
            else:
                self.errors.append(f"❌ install[{idx}] invalid kind: '{kind}'. Valid: {valid_kinds}")

    def _validate_installer_fields(self, kind: str, installer: dict, idx: int):
        """Validate installer-specific fields."""
        if kind == 'brew':
            required = ['formula', 'bins', 'label']
            for field in required:
                if field in installer:
                    self.info.append(f"✅ brew install[{idx}].{field} present")
                else:
                    self.errors.append(f"❌ brew install[{idx}] missing required field: '{field}'")

        elif kind == 'node':
            if 'bins' in installer:
                self.info.append(f"✅ node install[{idx}].bins present")

        elif kind == 'go':
            if 'bins' in installer:
                self.info.append(f"✅ go install[{idx}].bins present")

        elif kind == 'download':
            if 'url' in installer:
                self.info.append(f"✅ download install[{idx}].url present")
            else:
                self.warnings.append(f"⚠️  download install[{idx}] missing 'url' field")

    def _check_body_content(self, body: str):
        """Check SKILL.md body content."""
        if not body:
            self.warnings.append("⚠️  SKILL.md body is empty. Add instructions for using this skill.")
        else:
            word_count = len(body.split())
            self.info.append(f"✅ SKILL.md body has {word_count} words")

            # Check for TODO placeholders
            if 'TODO' in body.upper():
                self.warnings.append("⚠️  SKILL.md contains TODO items. Complete before publishing.")

    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*60)

        if self.info:
            print("\n📋 Information:")
            for item in self.info:
                print(f"  {item}")

        if self.warnings:
            print("\n⚠️  Warnings:")
            for item in self.warnings:
                print(f"  {item}")

        if self.errors:
            print("\n❌ Errors:")
            for item in self.errors:
                print(f"  {item}")

        print("\n" + "="*60)

        # Summary
        total = len(self.info) + len(self.warnings) + len(self.errors)
        print(f"\nSummary: {len(self.info)} info, {len(self.warnings)} warnings, {len(self.errors)} errors")

        if len(self.errors) == 0:
            print("✅ Skill validation PASSED!")
        else:
            print("❌ Skill validation FAILED. Fix errors and re-validate.")

        # Suggestions
        if self.errors or self.warnings:
            print("\n💡 See references/common_issues.md for help with common issues.")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <path-to-skill>")
        print("  path-to-skill: Path to skill directory or SKILL.md")
        print("\nExample:")
        print("  python validate_skill.py ./skills/my-skill")
        print("  python validate_skill.py ./skills/my-skill/SKILL.md")
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path)

    if validator.validate_all():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
