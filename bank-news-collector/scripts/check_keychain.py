import subprocess

# Search for any lark-related keychain entries
result = subprocess.run(
    ['security', 'dump-keychain'],
    capture_output=True, text=True
)
lines = result.stdout.split('\n')
for i, line in enumerate(lines):
    if 'lark' in line.lower() or 'feishu' in line.lower() or 'appsecret' in line.lower() or 'cli_a94d06' in line.lower():
        # Print surrounding context
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            print(f'{j}: {lines[j]}')
        print('---')
