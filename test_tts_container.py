#!/usr/bin/env python3
import json, urllib.request

url = "http://127.0.0.1:8080/v1/tts"
data = json.dumps({
    "text": "你好，欢迎使用Fish Audio语音合成系统。这是一次测试。",
    "format": "wav",
    "streaming": False,
    "max_new_tokens": 1024,
    "chunk_length": 200,
    "top_p": 0.7,
    "repetition_penalty": 1.2,
    "temperature": 0.7,
}).encode("utf-8")

print("Sending TTS request...")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        audio = resp.read()
        out_path = "/mnt/e/fishtts/test_output.wav"
        with open(out_path, "wb") as f:
            f.write(audio)
        print(f"Success! Audio size: {len(audio)} bytes, saved to {out_path}")
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print("Response:", e.read().decode('utf-8', errors='replace'))
