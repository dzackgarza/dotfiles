import { execFileSync, spawn } from "node:child_process"
import { closeSync, openSync } from "node:fs"
import { afterAll, beforeAll, describe, expect, it } from "vitest"

const INSTANCE = "control-spinner-visual"
const LOG = "/tmp/opencode/ags-refresh-spinner-regression.log"

beforeAll(() => {
  const output = openSync(LOG, "w")
  spawn("ags", ["run", `${import.meta.dirname}/usage-refresh-spinner-harness.tsx`], {
    stdio: ["ignore", output, output],
    detached: true,
  }).unref()
  closeSync(output)
  execFileSync(
    "timeout",
    [
      "60",
      "bash",
      "-c",
      `until grep -q "All 14 system polls initialized successfully" ${LOG}; do sleep 0.2; done`,
    ],
    { stdio: "inherit" },
  )
}, 70_000)

afterAll(() => {
  execFileSync("ags", ["quit", "-i", INSTANCE])
})

describe("usage refresh spinner", () => {
  it("has a nonzero rendered size while usage is loading", () => {
    execFileSync("ags", ["request", "-i", INSTANCE, "show"], {
      encoding: "utf-8",
      timeout: 10_000,
    })
    const result = JSON.parse(
      execFileSync("ags", ["request", "-i", INSTANCE, "refresh"], {
        encoding: "utf-8",
        timeout: 10_000,
      }),
    ) as {
      loading: boolean
      spinners: Array<{
        visible: boolean
        spinning: boolean
        width: number
        height: number
      }>
    }

    expect(result.loading).toBe(true)
    expect(result.spinners).toHaveLength(1)
    expect(result.spinners[0].visible).toBe(true)
    expect(result.spinners[0].spinning).toBe(true)
    expect(result.spinners[0].width).toBeGreaterThan(0)
    expect(result.spinners[0].height).toBeGreaterThan(0)
  })
}, 20_000)
