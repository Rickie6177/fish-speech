#!/bin/bash
docker inspect fish-speech-api | python3 -c "
import json,sys
d=json.load(sys.stdin)[0]
s=d['State']
print('Status:', s['Status'])
print('ExitCode:', s['ExitCode'])
print('OOMKilled:', s['OOMKilled'])
print('RestartCount:', d['RestartCount'])
print('FinishedAt:', s['FinishedAt'])
"
