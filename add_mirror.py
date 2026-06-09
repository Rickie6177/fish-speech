import json
import os

filepath = '/etc/docker/daemon.json'
# fallback if daemon.json doesn't exist
d = {}
if os.path.exists(filepath):
    try:
        with open(filepath, 'r') as f:
            d = json.load(f)
    except Exception:
        pass

d['registry-mirrors'] = [
    'https://docker.m.daocloud.io',
    'https://docker.nju.edu.cn',
    'https://mirror.baidubce.com'
]

with open(filepath, 'w') as f:
    json.dump(d, f, indent=4)
