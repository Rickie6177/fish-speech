#!/bin/bash
curl -s -X POST http://localhost:8080/v1/tts \
  -H "Content-Type: application/json" \
  --data '{"text": "你好，欢迎使用Fish Audio语音合成。", "format": "wav", "streaming": false}' \
  --output /mnt/e/fishtts/test_output.wav \
  --max-time 120
echo "Exit code: $?"
ls -lh /mnt/e/fishtts/test_output.wav
