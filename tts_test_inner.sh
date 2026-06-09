#!/bin/bash
curl -s -X POST http://127.0.0.1:8080/v1/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"你好，这是Fish Speech的语音测试","format":"wav","streaming":false}' \
  --output /tmp/test.wav \
  --max-time 120

echo "curl exit: $?"
ls -lh /tmp/test.wav 2>&1
