#!/usr/bin/env python3
"""Archive intermediate pipeline files with date prefix for historical viewing."""

import json
import shutil
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
today = date.today().isoformat()

MAPPINGS = [
    ("candidates_all.json", f"{today}-candidates.json"),
    ("first_round_filtered.json", f"{today}-first_round.json"),
    ("incremental_candidates.json", f"{today}-incremental.json"),
    ("second_round_filtered.json", f"{today}-second_round.json"),
]

for src_name, dst_name in MAPPINGS:
    src = DATA_DIR / src_name
    dst = DATA_DIR / dst_name
    if src.exists() and src.stat().st_size > 0:
        shutil.copy2(src, dst)
