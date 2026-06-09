#!/bin/bash
echo "Waiting for fish-speech-api to be ready..."
for i in $(seq 1 60); do
    sleep 3
    if docker logs fish-speech-api 2>&1 | grep -q "Application startup complete"; then
        echo "✅ API is ready!"
        docker logs fish-speech-api 2>&1 | grep -E "startup complete|running on|GET /v1/health|Shutting|Error" | tail -5
        exit 0
    fi
    echo "  ... still loading ($((i*3))s)"
done
echo "❌ Timeout waiting for startup"
exit 1
