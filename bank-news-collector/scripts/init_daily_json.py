#!/usr/bin/env python3
import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main():
    today = date.today().isoformat()
    path = DATA_DIR / f"{today}.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        text = path.read_text(encoding='utf-8').strip()
        if not text:
            path.write_text('[]\n', encoding='utf-8')
            print(json.dumps({"created": False, "repaired_empty": True, "path": str(path)}, ensure_ascii=False))
            return
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "path": str(path), "error": f"invalid json: {e}"}, ensure_ascii=False))
            sys.exit(2)
        if not isinstance(data, list):
            print(json.dumps({"ok": False, "path": str(path), "error": "daily json must be a JSON array"}, ensure_ascii=False))
            sys.exit(3)
        print(json.dumps({"created": False, "repaired_empty": False, "path": str(path), "count": len(data)}, ensure_ascii=False))
        return

    path.write_text('[]\n', encoding='utf-8')
    print(json.dumps({"created": True, "repaired_empty": False, "path": str(path), "count": 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
