import { execFileSync } from "node:child_process"
import { beforeAll, describe, expect, it } from "vitest"
import { PROVIDER_ICONS } from "../provider-icons"
import { USAGE_LIMITS_JSON_COMMAND } from "../usage-limits-command"

interface UsageRow {
  identifier: string
  pct_used: number
  is_exhausted: boolean
  reset_at: string | null
  time_until_reset: string
}

interface ModelAvailability {
  name: string
  available_now: boolean
  available_when?: string
}

interface ProviderSnapshot {
  provider: string
  display_name: string
  status: "ok" | "error" | "rate_limited"
  rows: UsageRow[]
  availability: ModelAvailability[]
  errors: { type: string; message: string }[]
  metadata: Record<string, unknown>
  account: string | null
}

interface UsageCollection {
  version: string
  captured_at: string
  providers: ProviderSnapshot[]
}

let data: UsageCollection

beforeAll(() => {
  const [command, ...args] = USAGE_LIMITS_JSON_COMMAND
  const output = execFileSync(command, args, {
    encoding: "utf-8",
    timeout: 30_000,
  })
  data = JSON.parse(output) as UsageCollection
})

describe("usage-limits --json", () => {
  it("produces valid JSON with the expected top-level schema", () => {
    expect(data).toHaveProperty("version")
    expect(data.version).toBe("1")
    expect(data).toHaveProperty("captured_at")
    expect(typeof data.captured_at).toBe("string")
    expect(data.captured_at.length).toBeGreaterThan(0)
    expect(() => new Date(data.captured_at)).not.toThrow()
    expect(Array.isArray(data.providers)).toBe(true)
    expect(data.providers.length).toBeGreaterThan(0)
  })

  it("returns at least the core set of expected providers", () => {
    const found = new Set(data.providers.map((p) => p.provider))
    for (const key of [
      "antigravity",
      "claude",
      "codex",
      "copilot",
      "cursor",
      "kiro",
      "ollama",
      "opencode-go",
      "opencode-zen",
      "trae",
    ]) {
      expect(found.has(key)).toBe(true)
    }
  })

  it("returns account-specific Antigravity snapshots without cache corruption errors", () => {
    const antigravity = data.providers.filter((p) => p.provider === "antigravity")

    expect(antigravity).toHaveLength(4)
    expect(antigravity.every((p) => p.status === "ok")).toBe(true)
    expect(antigravity.map((p) => p.account).sort()).toEqual([
      "dzackgarza.tw@gmail.com",
      "dzackgarza@gmail.com",
      "skippydzg@gmail.com",
      "zack@ncts.ntu.edu.tw",
    ])
    expect(antigravity.flatMap((p) => p.errors)).toEqual([])
  })

  it("every provider has the required ProviderSnapshot fields", () => {
    for (const provider of data.providers) {
      expect(typeof provider.provider).toBe("string")
      expect(typeof provider.display_name).toBe("string")
      expect(["ok", "error", "rate_limited"]).toContain(provider.status)

      expect(Array.isArray(provider.rows)).toBe(true)
      for (const row of provider.rows) {
        expect(typeof row.identifier).toBe("string")
        expect(typeof row.pct_used).toBe("number")
        expect(typeof row.is_exhausted).toBe("boolean")
        if (row.reset_at !== null) expect(typeof row.reset_at).toBe("string")
        expect(typeof row.time_until_reset).toBe("string")
      }

      expect(Array.isArray(provider.availability)).toBe(true)
      for (const a of provider.availability) {
        expect(typeof a.name).toBe("string")
        expect(typeof a.available_now).toBe("boolean")
      }

      expect(Array.isArray(provider.errors)).toBe(true)
      for (const e of provider.errors) {
        expect(typeof e.type).toBe("string")
        expect(typeof e.message).toBe("string")
      }

      expect(typeof provider.metadata).toBe("object")
      if (provider.account !== null) {
        expect(typeof provider.account).toBe("string")
      }
    }
  })

  it("every provider has pct_used values that produce valid Gtk fractions", () => {
    for (const provider of data.providers) {
      for (const row of provider.rows) {
        const fraction = row.pct_used / 100
        expect(fraction).toBeGreaterThanOrEqual(0)
        expect(fraction).toBeLessThanOrEqual(1)
      }
    }
  })

  it("every provider from CLI output has an icon in PROVIDER_ICONS", () => {
    const iconKeys = new Set(Object.keys(PROVIDER_ICONS))
    const missing = data.providers
      .filter((p) => !iconKeys.has(p.provider))
      .map((p) => p.provider)
    expect(missing).toEqual([])
  })
})
