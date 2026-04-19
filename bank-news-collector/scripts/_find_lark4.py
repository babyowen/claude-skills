import subprocess, os, sys

# Try to find lark-cli via pip
try:
    result = subprocess.run(
        ["pip3", "list"], capture_output=True, text=True, timeout=10
    )
    for line in result.stdout.split("\n"):
        if "lark" in line.lower():
            print(f"pip: {line}")
except Exception as e:
    print(f"pip3 failed: {e}")

# Try via python module
try:
    result = subprocess.run(
        ["python3", "-m", "pip", "list"], capture_output=True, text=True, timeout=10
    )
    for line in result.stdout.split("\n"):
        if "lark" in line.lower():
            print(f"python3 -m pip: {line}")
except Exception as e:
    print(f"python3 -m pip failed: {e}")

# Try running as python module
try:
    result = subprocess.run(
        ["python3", "-m", "lark_cli", "--version"],
        capture_output=True, text=True, timeout=10
    )
    print(f"python3 -m lark_cli: exit={result.returncode}")
    print(f"stdout: {result.stdout[:200]}")
    print(f"stderr: {result.stderr[:200]}")
except Exception as e:
    print(f"python3 -m lark_cli failed: {e}")

# Try python3 -m lark
try:
    result = subprocess.run(
        ["python3", "-m", "lark", "--version"],
        capture_output=True, text=True, timeout=10
    )
    print(f"python3 -m lark: exit={result.returncode}")
    print(f"stdout: {result.stdout[:200]}")
except Exception as e:
    print(f"python3 -m lark failed: {e}")
