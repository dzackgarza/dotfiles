import { execAsync } from "ags/process"
import GLib from "gi://GLib?version=2.0"

const HOME = GLib.get_home_dir()

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
  status: "ok" | "error"
  rows: UsageRow[]
  availability: ModelAvailability[]
  metadata: Record<string, any>
  errors: Array<{ type: string; message: string }>
}

export interface UsageCollection {
  version: string
  captured_at: string
  providers: ProviderSnapshot[]
}

export async function fetchClaudeUsage(): Promise<UsageCollection> {
  try {
    const cmd = ["uv", "run", "--project", `${HOME}/dotfiles/usage-limits`, "usage-limits", "--json"]
    const output = await execAsync(cmd)
    return JSON.parse(output) as UsageCollection
  } catch (error) {
    throw new Error(`Failed to fetch LLM usage: ${error}`)
  }
}
