import subprocess
import os
import json

node_bin = '/Users/babyowen/.nvm/versions/node/v24.11.0/bin'
lark_cli = os.path.join(node_bin, 'lark-cli')

# Try to get appsecret from keychain
result = subprocess.run(
    ['security', 'find-generic-password', '-s', 'lark-cli/appsecret:cli_a94d06a768b8dbde', '-w'],
    capture_output=True, text=True
)
app_secret = result.stdout.strip()
print(f'Keychain access result: returncode={result.returncode}')
if result.returncode != 0:
    print(f'stderr: {result.stderr.strip()}')
    # Try alternative: check if lark-cli has config files
    config_paths = [
        os.path.expanduser('~/.config/lark-cli/config.json'),
        os.path.expanduser('~/.lark-cli/config.json'),
        os.path.expanduser('~/.lark/config.json'),
    ]
    for p in config_paths:
        if os.path.exists(p):
            print(f'Found config at: {p}')
            with open(p) as f:
                print(f.read()[:500])
else:
    print(f'Got app_secret (length={len(app_secret)})')

    # Now get tenant_access_token via API
    import urllib.request
    token_url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = json.dumps({
        'app_id': 'cli_a94d06a768b8dbde',
        'app_secret': app_secret
    }).encode()
    req = urllib.request.Request(token_url, data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    token_data = json.loads(resp.read())
    print(f'Token response: {token_data.get("code")}, msg: {token_data.get("msg")}')

    if token_data.get('code') == 0:
        tenant_token = token_data['tenant_access_token']
        # Send message
        with open('/tmp/feishu_report.txt', 'r') as f:
            text = f.read().strip()

        msg_url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id'
        msg_data = json.dumps({
            'receive_id': 'ou_e9bf22aaaeae8652f04b87ec28fb6bd9',
            'msg_type': 'text',
            'content': json.dumps({'text': text})
        }).encode()
        msg_req = urllib.request.Request(msg_url, data=msg_data, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {tenant_token}'
        })
        msg_resp = urllib.request.urlopen(msg_req)
        msg_result = json.loads(msg_resp.read())
        print(f'Send result: code={msg_result.get("code")}, msg={msg_result.get("msg")}')
        if msg_result.get('code') == 0:
            print('Message sent successfully!')
