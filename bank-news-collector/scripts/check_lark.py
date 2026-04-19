import subprocess
import os

node_bin = '/Users/babyowen/.nvm/versions/node/v24.11.0/bin'
lark_cli = os.path.join(node_bin, 'lark-cli')

env = os.environ.copy()
env['PATH'] = node_bin + ':' + env.get('PATH', '')

# Check if lark-cli supports env variable for appSecret
result = subprocess.run(
    [lark_cli, '--help'],
    capture_output=True, text=True, env=env
)
print(result.stdout[:2000])
print('---STDERR---')
print(result.stderr[:1000])
