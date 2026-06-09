#!/bin/bash
curl -s -X POST http://localhost:8080/v1/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"你好，我是Fish Speech，一个强大的语音合成模型。","format":"wav","streaming":false}' \
  -o /tmp/test_output.wav \
  -w "HTTP:%{http_code} SIZE:%{size_download}\n"

echo "Exit: $?"
ls -lh /tmp/test_output.wav 2>/dev/null || echo "File not found"
