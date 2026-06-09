import json

d = {
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "registry-mirrors": [
        "https://hub-mirror.c.163.com",
        "https://dockerproxy.com",
        "https://docker.nju.edu.cn"
    ]
}

with open('/etc/docker/daemon.json', 'w') as f:
    json.dump(d, f, indent=4)

print("Done!")
