#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ["title", "url", "summary"]
OPTIONAL_FIELDS = ["published_at", "source", "why_relevant", "collected_at"]


def main():
    if len(sys.argv) < 2:
        print('Usage: validate_news_json.py <daily_json_path>')
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"ok": False, "error": "file not found", "path": str(path)}, ensure_ascii=False))
        sys.exit(2)

    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"invalid json: {e}", "path": str(path)}, ensure_ascii=False))
        sys.exit(3)

    if not isinstance(data, list):
        print(json.dumps({"ok": False, "error": "top-level JSON must be an array", "path": str(path)}, ensure_ascii=False))
        sys.exit(4)

    issues = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            issues.append({"index": idx, "error": "item must be an object"})
            continue
        missing = [field for field in REQUIRED_FIELDS if not str(item.get(field, '')).strip()]
        if missing:
            issues.append({"index": idx, "missing_required_fields": missing})

    print(json.dumps({
        "ok": len(issues) == 0,
        "path": str(path),
        "required_fields": REQUIRED_FIELDS,
        "optional_fields": OPTIONAL_FIELDS,
        "count": len(data),
        "issues": issues
    }, ensure_ascii=False, indent=2))

    if issues:
        sys.exit(5)


if __name__ == '__main__':
    main()
