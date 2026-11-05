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

// Saved one-time resets; null means the provider reports no reset inventory.
export interface SavedResets {
  available_count: number
  applicable_now_count: number
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
  saved_resets: SavedResets | null
}

export function savedResetsText(resets: SavedResets): string {
  return `Saved resets: ${resets.available_count} (usable now: ${resets.applicable_now_count})`
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
