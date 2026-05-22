#!/bin/bash

CREDS_FILE="$HOME/.claude/.credentials.json"
TOKEN_URL="https://api.anthropic.com/api/oauth/token"

# Read credentials
CREDS=$(cat "$CREDS_FILE")
ACCESS_TOKEN=$(echo "$CREDS" | jq -r '.claudeAiOauth.accessToken')
REFRESH_TOKEN=$(echo "$CREDS" | jq -r '.claudeAiOauth.refreshToken')
EXPIRES_AT=$(echo "$CREDS" | jq -r '.claudeAiOauth.expiresAt')
NOW=$(date +%s%N | cut -b1-13)

echo "Token expires at: $EXPIRES_AT, now: $NOW" >&2

# Check if expired (with 5 min buffer)
BUFFER=$((5 * 60 * 1000))
if [ "$EXPIRES_AT" -lt $((NOW + BUFFER)) ]; then
  echo "Token expired or expiring soon, refreshing..." >&2
  
  # Refresh token
  RESPONSE=$(curl -s -X POST "$TOKEN_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"grant_type\": \"refresh_token\",
      \"refresh_token\": \"$REFRESH_TOKEN\",
      \"client_id\": \"feO2zC5PiER4r4uXKwh9qDrJL3gV6nLb\"
    }")
  
  NEW_ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
  NEW_REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token // empty')
  EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in')
  
  if [ -z "$NEW_ACCESS_TOKEN" ] || [ "$NEW_ACCESS_TOKEN" = "null" ]; then
    echo "Failed to refresh token: $RESPONSE" >&2
    exit 1
  fi
  
  # Update credentials file
  UPDATED_CREDS=$(echo "$CREDS" | jq \
    --arg token "$NEW_ACCESS_TOKEN" \
    --arg refresh "${NEW_REFRESH_TOKEN:-$REFRESH_TOKEN}" \
    --arg expires "$(($NOW + $EXPIRES_IN * 1000))" \
    '.claudeAiOauth.accessToken = $token | .claudeAiOauth.refreshToken = $refresh | .claudeAiOauth.expiresAt = ($expires | tonumber)')
  
  echo "$UPDATED_CREDS" > "$CREDS_FILE"
  echo "Token refreshed" >&2
  ACCESS_TOKEN="$NEW_ACCESS_TOKEN"
fi

echo "$ACCESS_TOKEN"
