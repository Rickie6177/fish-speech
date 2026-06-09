import json, urllib.request, sys

url = "http://localhost:8080/v1/tts"
data = json.dumps({
    "text": "你好，这是Fish Speech语音测试。",
    "format": "wav",
    "streaming": False
}).encode()

req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        audio = resp.read()
        with open("/mnt/e/fishtts/test_output.wav", "wb") as f:
            f.write(audio)
        print(f"Success! Audio size: {len(audio)} bytes")
except Exception as e:
    print(f"Error: {e}")
    # Also try to read error body
    if hasattr(e, 'read'):
        print("Response:", e.read().decode())
