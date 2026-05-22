import { execAsync } from "ags/process"
import GLib from "gi://GLib?version=2.0"

const HOME = GLib.get_home_dir()
const CREDENTIALS_PATH = `${HOME}/.claude/.credentials.json`
const TOKEN_URL = "https://api.anthropic.com/api/oauth/token"
const CLIENT_ID = "feO2zC5PiER4r4uXKwh9qDrJL3gV6nLb"

export interface ClaudeUsageData {
  fiveHourUtilization: number
  fiveHourResetAt: string
  sevenDayUtilization: number
  sevenDayResetAt: string
  sevenDayOpusUtilization?: number
}

interface Credentials {
  claudeAiOauth: {
    accessToken: string
    refreshToken: string
    expiresAt: number
  }
  organizationUuid: string
}

async function readCredentialsFile(): Promise<Credentials> {
  try {
    const content = await execAsync(`cat "${CREDENTIALS_PATH}"`)
    return JSON.parse(content)
  } catch (error) {
    throw new Error(`Failed to read credentials file: ${error}`)
  }
}

async function writeCredentialsFile(creds: Credentials): Promise<void> {
  try {
    const json = JSON.stringify(creds, null, 2)
    await execAsync(`cat > "${CREDENTIALS_PATH}" << 'EOF'\n${json}\nEOF`)
  } catch (error) {
    throw new Error(`Failed to write credentials file: ${error}`)
  }
}

async function refreshAccessToken(refreshToken: string): Promise<{ accessToken: string; refreshToken: string; expiresIn: number }> {
  try {
    const response = await fetch(TOKEN_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        client_id: CLIENT_ID,
      }),
    })

    if (!response.ok) {
      throw new Error(`Token refresh failed: ${response.statusText}`)
    }

    const data = (await response.json()) as any

    if (!data.access_token) {
      throw new Error(`No access token in refresh response`)
    }

    return {
      accessToken: data.access_token,
      refreshToken: data.refresh_token || refreshToken,
      expiresIn: data.expires_in || 3600,
    }
  } catch (error) {
    throw new Error(`Failed to refresh token: ${error}`)
  }
}

async function getAccessToken(): Promise<string> {
  let creds = await readCredentialsFile()
  const now = Date.now()
  const buffer = 5 * 60 * 1000 // 5 minute buffer

  // Check if token is expired or expiring soon
  if (creds.claudeAiOauth.expiresAt < now + buffer) {
    const refreshed = await refreshAccessToken(creds.claudeAiOauth.refreshToken)
    creds.claudeAiOauth.accessToken = refreshed.accessToken
    creds.claudeAiOauth.refreshToken = refreshed.refreshToken
    creds.claudeAiOauth.expiresAt = now + refreshed.expiresIn * 1000

    await writeCredentialsFile(creds)
  }

  return creds.claudeAiOauth.accessToken
}

export async function fetchClaudeUsage(): Promise<ClaudeUsageData> {
  const accessToken = await getAccessToken()

  try {
    const response = await fetch("https://api.anthropic.com/api/oauth/usage", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
        "User-Agent": "claude-code/2.1.5",
        "anthropic-beta": "oauth-2025-04-20",
      },
    })

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }

    const data = (await response.json()) as any

    return {
      fiveHourUtilization: Math.round(data.five_hour?.utilization ?? 0),
      fiveHourResetAt: data.five_hour?.resets_at ?? "",
      sevenDayUtilization: Math.round(data.seven_day?.utilization ?? 0),
      sevenDayResetAt: data.seven_day?.resets_at ?? "",
      sevenDayOpusUtilization: data.seven_day_opus ? Math.round(data.seven_day_opus.utilization) : undefined,
    }
  } catch (error) {
    throw new Error(`Failed to fetch Claude usage: ${error}`)
  }
}
