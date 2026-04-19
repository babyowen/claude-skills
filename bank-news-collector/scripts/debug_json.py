#!/usr/bin/env python3
"""Fix and validate first_round_filtered.json"""
import json
import re

with open('data/first_round_filtered.json', 'r', encoding='utf-8') as f:
    raw = f.read()

# Find problematic characters
for i in range(30, min(80, len(raw))):
    c = raw[i]
    print(f'  [{i}] U+{ord(c):04X} {repr(c)}')
