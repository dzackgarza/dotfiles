#!/bin/bash

# Fetch Claude usage from OAuth endpoint using credentials from Claude Code CLI
# Returns JSON with usage data

TOKEN=$(cat ~/.claude/.credentials.json 2>/dev/null | jq -r '.claudeAiOauth.accessToken' 2>/dev/null)

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo '{"error": "No OAuth token found in ~/.claude/.credentials.json"}'
  exit 1
fi

curl -s \
  -H "Authorization: Bearer $TOKEN" \
  -H "anthropic-beta: oauth-2025-04-20" \
  -H "User-Agent: claude-code/2.1.5" \
  "https://api.anthropic.com/api/oauth/usage"
