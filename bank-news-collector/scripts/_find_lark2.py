import subprocess, os, sys

# Try to source shell profile and find lark-cli
home = os.path.expanduser("~")
profiles = [
    os.path.join(home, ".zshrc"),
    os.path.join(home, ".bashrc"),
    os.path.join(home, ".zprofile"),
    os.path.join(home, ".bash_profile"),
]

for p in profiles:
    if os.path.isfile(p):
        print(f"Found profile: {p}")

# Try running through zsh login shell to get full PATH
try:
    result = subprocess.run(
        ["zsh", "-l", "-c", "which lark-cli 2>/dev/null; echo '---'; echo $PATH"],
        capture_output=True, text=True, timeout=10
    )
    print(f"zsh login result (exit={result.returncode}):")
    print(result.stdout[:500])
    if result.stderr:
        print(f"stderr: {result.stderr[:200]}")
except Exception as e:
    print(f"zsh login failed: {e}")

# Also try bash login
try:
    result = subprocess.run(
        ["bash", "-l", "-c", "which lark-cli 2>/dev/null; echo '---'; echo $PATH"],
        capture_output=True, text=True, timeout=10
    )
    print(f"bash login result (exit={result.returncode}):")
    print(result.stdout[:500])
except Exception as e:
    print(f"bash login failed: {e}")
