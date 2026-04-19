import os, subprocess

# Check /opt/pmk/env/global/bin
pmk_bin = "/opt/pmk/env/global/bin"
if os.path.isdir(pmk_bin):
    entries = sorted(os.listdir(pmk_bin))
    print(f"pmk bin entries ({len(entries)}):")
    for e in entries:
        print(f"  {e}")
    # Check for lark
    lark_entries = [e for e in entries if 'lark' in e.lower()]
    print(f"\nLark-related: {lark_entries}")
else:
    print(f"{pmk_bin} does not exist")

# Check for lark config
config_paths = [
    os.path.expanduser("~/.lark-cli"),
    os.path.expanduser("~/.config/lark-cli"),
    os.path.expanduser("~/.lark"),
]
for p in config_paths:
    if os.path.exists(p):
        print(f"\nFound config: {p}")
        if os.path.isdir(p):
            print(f"  Contents: {os.listdir(p)}")
