import { execFileSync } from "node:child_process"
import { describe, expect, it } from "vitest"
import type { UsageCollection } from "../../../services/claude-usage-fetcher"
import { USAGE_LIMITS_JSON_COMMAND } from "../usage-limits-command"

function upstreamRows(data: UsageCollection) {
  return data.providers
    .filter((provider) => provider.provider === "antigravity")
    .flatMap((provider) =>
      provider.rows.map((row) => ({
        account: provider.account,
        identifier: row.identifier,
      })),
    )
}

describe("Antigravity usage windows", () => {
  it("preserves the upstream 5-hour and weekly rows in the panel service", () => {
    const [command, ...args] = USAGE_LIMITS_JSON_COMMAND
    const upstream = JSON.parse(
      execFileSync(command, [...args, "--provider", "antigravity"], {
        encoding: "utf-8",
        timeout: 30_000,
      }),
    ) as UsageCollection
    const expected = upstreamRows(upstream)
    expect(expected.map((row) => row.identifier)).toEqual(
      expect.arrayContaining([
        expect.stringContaining("(5h)"),
        expect.stringContaining("(Weekly)"),
      ]),
    )

    const harness = execFileSync(
      "ags",
      ["run", `${import.meta.dirname}/antigravity-usage-harness.tsx`],
      { encoding: "utf-8", timeout: 100_000 },
    )
    const match = /^USAGE_ROWS=(.*)$/m.exec(harness)
    expect(match).not.toBeNull()
    const actual = JSON.parse(match![1]) as ReturnType<typeof upstreamRows>

    expect(actual).toEqual(expected)
  })
})
