import { execAsync } from "ags/process"

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
}

export interface UsageCollection {
  version: string
  captured_at: string
  providers: ProviderSnapshot[]
}

export async function fetchClaudeUsage(): Promise<UsageCollection> {
  const cmd = [
    "uvx",
    "git+https://github.com/dzackgarza/usage-limits",
    "--json",
  ]
  const output = await execAsync(cmd)
  return JSON.parse(output) as UsageCollection
}
