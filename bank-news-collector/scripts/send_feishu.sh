#!/bin/bash
export PATH="/Users/babyowen/.nvm/versions/node/v24.11.0/bin:$PATH"
export LARK_CLI_BIN="/Users/babyowen/.nvm/versions/node/v24.11.0/bin/lark-cli"

TEXT=$(cat /tmp/feishu_report.txt)

"$LARK_CLI_BIN" im +messages-send \
  --as bot \
  --user-id ou_e9bf22aaaeae8652f04b87ec28fb6bd9 \
  --text "$TEXT"
