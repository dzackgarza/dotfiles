#!/bin/bash
set -euo pipefail

MODEL="$1"
IMAGE_B64=$(cat test-diagram.b64)

PROMPT="Describe this mathematical diagram in precise detail, including all labels, arrows, positions, and mathematical notation. The description should be detailed enough to reconstruct this diagram in TikZ. Include:
1. The exact mathematical symbols and LaTeX notation used
2. The position and arrangement of all nodes
3. The direction and labels of all arrows
4. Any special formatting or styling"

cat > request.json << EOJSON
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "$PROMPT"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,$IMAGE_B64"
          }
        }
      ]
    }
  ],
  "max_tokens": 2000
}
EOJSON

echo "Testing model: $MODEL"
curl -s "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d @request.json | jq -r '.choices[0].message.content' > "response_${MODEL//\//_}.txt"

echo "Response saved to response_${MODEL//\//_}.txt"
echo ""
head -50 "response_${MODEL//\//_}.txt"
