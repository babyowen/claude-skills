#!/bin/bash
# Try to find and execute lark-cli
for candidate in \
  /usr/local/bin/lark-cli \
  /opt/homebrew/bin/lark-cli \
  "$HOME/.npm-global/bin/lark-cli" \
  "$HOME/.local/bin/lark-cli" \
  "$(npm root -g 2>/dev/null)/../bin/lark-cli" \
  "$(npm prefix -g 2>/dev/null)/bin/lark-cli"; do
  if [ -x "$candidate" ] 2>/dev/null; then
    exec "$candidate" "$@"
  fi
done

# Try npx as fallback
if command -v npx >/dev/null 2>&1; then
  exec npx lark-cli "$@"
fi

echo "ERROR: lark-cli not found" >&2
exit 127
