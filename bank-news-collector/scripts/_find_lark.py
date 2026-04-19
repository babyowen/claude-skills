import subprocess, os, sys

paths_to_check = [
    "lark-cli",
    os.path.expanduser("~/.npm-global/bin/lark-cli"),
    "/usr/local/bin/lark-cli",
    "/opt/homebrew/bin/lark-cli",
]

for p in paths_to_check:
    exists = os.path.isfile(p)
    print(f"{p}: exists={exists}")

try:
    npm_prefix = subprocess.check_output(["npm", "prefix", "-g"], stderr=subprocess.DEVNULL).decode().strip()
    print(f"npm global prefix: {npm_prefix}")
    bin_path = os.path.join(npm_prefix, "bin", "lark-cli")
    print(f"npm bin path: {bin_path}, exists={os.path.isfile(bin_path)}")
    entries = os.listdir(os.path.join(npm_prefix, "bin"))
    print(f"npm bin entries: {entries[:20]}")
except Exception as e:
    print(f"npm check failed: {e}")

try:
    result = subprocess.run(["npx", "lark-cli", "--version"], capture_output=True, text=True, timeout=15)
    print(f"npx exit: {result.returncode}")
    if result.stdout:
        print(f"npx stdout: {result.stdout[:200]}")
    if result.stderr:
        print(f"npx stderr: {result.stderr[:200]}")
except Exception as e:
    print(f"npx failed: {e}")
