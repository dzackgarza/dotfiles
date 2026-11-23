import { describe, expect, it } from "vitest"
import { formatUpdatedAgo, usageFetchFailure } from "../usage-status"

const NOW = new Date("2026-11-23T05:30:00Z")

describe("usageFetchFailure", () => {
  it("reports the fetch error as an error provider, not an empty list", () => {
    const collection = usageFetchFailure(new Error("spawn uv ENOENT"), NOW)
    expect(collection.providers).toHaveLength(1)
    expect(collection.providers[0].status).toBe("error")
    expect(collection.providers[0].errors[0].message).toBe("spawn uv ENOENT")
    expect(collection.captured_at).toBe(NOW.toISOString())
  })
})

describe("formatUpdatedAgo", () => {
  it("reports the age of the snapshot, not a constant", () => {
    expect(formatUpdatedAgo("2026-11-23T05:29:50Z", NOW)).toBe("Updated 10 sec ago")
    expect(formatUpdatedAgo("2026-11-23T05:25:00Z", NOW)).toBe("Updated 5 min ago")
    expect(formatUpdatedAgo("2026-11-23T02:30:00Z", NOW)).toBe("Updated 3 h ago")
  })

  it("says so when no snapshot has been captured", () => {
    expect(formatUpdatedAgo("", NOW)).toBe("Not yet updated")
  })
})
