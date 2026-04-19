#!/usr/bin/env python3
"""Fix unescaped double quotes in first_round_filtered.json"""
import re

with open('data/first_round_filtered.json', 'r', encoding='utf-8') as f:
    raw = f.read()

# Fix: replace unescaped " inside JSON string values with \"
# Strategy: find all "title": "..." and "source": "..." patterns and escape inner quotes
def fix_json_string_values(raw):
    result = []
    i = 0
    while i < len(raw):
        # Look for "key": " pattern
        match = re.match(r'"((?:title|source|listed_from|url))"\s*:\s*"', raw[i:])
        if match:
            result.append(raw[i:i+match.end()])
            i += match.end()
            # Now read the string value, handling nested quotes
            value_chars = []
            while i < len(raw):
                c = raw[i]
                if c == '"':
                    # Check if this ends the value (next non-space is , or } or \n)
                    rest = raw[i+1:].lstrip()
                    if rest and rest[0] in (',', '}', '\n', '\r'):
                        # This is the closing quote
                        result.append(''.join(value_chars))
                        result.append('"')
                        i += 1
                        break
                    else:
                        # This is an unescaped inner quote - escape it
                        value_chars.append('\\"')
                        i += 1
                elif c == '\\':
                    # Already escaped character
                    value_chars.append(raw[i:i+2])
                    i += 2
                else:
                    value_chars.append(c)
                    i += 1
        else:
            result.append(raw[i])
            i += 1
    return ''.join(result)

fixed = fix_json_string_values(raw)

import json
# Validate
try:
    data = json.loads(fixed)
    with open('data/first_round_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Fixed and validated: {len(data)} items")
except json.JSONDecodeError as e:
    print(f"Still invalid: {e}")
    # Fallback: try line-by-line
    print("Trying alternative fix...")
