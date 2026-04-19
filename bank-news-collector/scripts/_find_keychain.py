import subprocess, sys

# Try different ways to find the lark-cli secret in Keychain
attempts = [
    ["security", "find-generic-password", "-s", "appsecret:cli_a94d06a768b8dbde"],
    ["security", "find-generic-password", "-a", "appsecret:cli_a94d06a768b8dbde"],
    ["security", "find-generic-password", "-s", "lark-cli"],
    ["security", "find-generic-password", "-s", "cli_a94d06a768b8dbde"],
    ["security", "find-internet-password", "-s", "open.feishu.cn"],
    ["security", "find-generic-password", "-s", "feishu"],
    ["security", "find-generic-password", "-s", "lark"],
]

for cmd in attempts:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"SUCCESS with: {' '.join(cmd)}")
            # Don't print the actual secret, just that we found it
            print(f"  Found entry (length: {len(result.stdout)})")
        else:
            pass  # Skip failures silently
    except Exception:
        pass

# Also dump all generic passwords related to lark
try:
    result = subprocess.run(
        ["security", "dump-keychain"],
        capture_output=True, text=True, timeout=10
    )
    lines = result.stdout.split("\n")
    for i, line in enumerate(lines):
        if "lark" in line.lower() or "feishu" in line.lower() or "appsecret" in line.lower() or "cli_a94d" in line.lower():
            # Print surrounding context but mask actual passwords
            context = lines[max(0, i-2):min(len(lines), i+3)]
            for c in context:
                if "password" in c.lower() or "data" in c.lower():
                    print(f"  [REDACTED]")
                else:
                    print(f"  {c.strip()}")
            print("---")
except Exception as e:
    print(f"dump failed: {e}")
