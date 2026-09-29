import { execAsync } from "ags/process"
import { USAGE_LIMITS_JSON_COMMAND } from "../src/lib/usage-limits-command"

export interface UsageRow {
  identifier: string
  pct_used: number
  reset_at: string | null
  is_exhausted: boolean
  time_until_reset: string
}

export interface ModelAvailability {
  name: string
  available_now: boolean
  available_when: string | null
}

export interface ProviderSnapshot {
  provider: string
  display_name: string
  status: "ok" | "error" | "rate_limited"
  rows: UsageRow[]
  availability: ModelAvailability[]
  metadata: Record<string, unknown>
  errors: Array<{ type: string; message: string }>
  account: string | null
}

export interface UsageCollection {
  version: string
  captured_at: string
  providers: ProviderSnapshot[]
}

export async function fetchClaudeUsage(): Promise<UsageCollection> {
  const output = await execAsync([...USAGE_LIMITS_JSON_COMMAND])
  return JSON.parse(output) as UsageCollection
}
