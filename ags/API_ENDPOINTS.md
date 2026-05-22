# Usage API Endpoints

## Claude Usage

**Endpoint:**
```
GET https://api.anthropic.com/api/oauth/usage
```

**Authentication:**
- Header: `Authorization: Bearer {oauth_access_token}`
- OAuth token from Claude Code CLI credentials stored in macOS Keychain
- Service name: `"Claude Code-credentials"`
- Extract the OAuth access token from Keychain for authenticated requests

**Response Structure:**
```json
{
  "five_hour": {
    "utilization_pct": 20,
    "reset_at": "2025-02-05T19:00:00Z"
  },
  "seven_day": {
    "utilization_pct": 51,
    "reset_at": "2025-02-10T00:00:00Z"
  },
  "seven_day_opus": {
    "utilization_pct": 30
  }
}
```

**Note:** This uses the OAuth token from Claude Code CLI, not the browser session key. The Claude Code CLI stores credentials in macOS Keychain automatically when logged in.

## Codex Usage (ChatGPT)

**Endpoint:**
```
GET https://chatgpt.com/backend-api/wham/usage
```

**Authentication:**
- Cookies from ChatGPT session (session-token)

**Response Structure:**
```json
{
  "user_id": "user-XXX",
  "account_id": "user-XXX",
  "email": "user@example.com",
  "plan_type": "plus",
  "rate_limit": {
    "allowed": false,
    "limit_reached": true,
    "primary_window": {
      "used_percent": 31,
      "limit_window_seconds": 18000,
      "reset_after_seconds": 9615,
      "reset_at": 1770304728
    },
    "secondary_window": {
      "used_percent": 100,
      "limit_window_seconds": 604800,
      "reset_after_seconds": 364776,
      "reset_at": 1770659889
    }
  },
  "credits": {
    "has_credits": false,
    "unlimited": false,
    "balance": "0"
  }
}
```

**Key fields:**
- `rate_limit.primary_window.used_percent`: 5-hour window usage (0-100)
- `rate_limit.secondary_window.used_percent`: Weekly window usage (0-100)
- `rate_limit.primary_window.reset_after_seconds`: Seconds until 5-hour reset
- `rate_limit.secondary_window.reset_after_seconds`: Seconds until weekly reset

## Amp Usage (Balance)

**Endpoint:** UNKNOWN - No public endpoint found yet

**Expected Data:**
- Balance: $9.03 (out of $10 budget)
- Replenishment rate: +$0.42/hour

**Authentication:** UNKNOWN

**Note:** May require integration with Anthropic's billing system or separate Amp service
