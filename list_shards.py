import json, sys
with open('/mnt/e/fishtts/checkpoints/s2-pro/model.safetensors.index.json') as f:
    d = json.load(f)
files = set(d['weight_map'].values())
print('Shard files needed:')
for f in sorted(files):
    print(f)
