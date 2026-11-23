import type { UsageCollection } from "../../services/claude-usage-fetcher"

/**
 * A whole-fetch failure (CLI missing, invalid JSON, non-zero exit) is shown as
 * one error provider, so the tile row and popover report it like any other
 * provider failure instead of rendering an empty list.
 */
export function usageFetchFailure(error: unknown, now: Date): UsageCollection {
  const message = error instanceof Error ? error.message : String(error)
  return {
    version: "1",
    captured_at: now.toISOString(),
    providers: [
      {
        provider: "usage-limits",
        display_name: "usage-limits",
        status: "error",
        rows: [],
        availability: [],
        metadata: {},
        errors: [{ type: "fetch", message }],
        account: null,
        saved_resets: null,
      },
    ],
  }
}

/** Footer text computed from the snapshot's own capture time. */
export function formatUpdatedAgo(capturedAt: string, now: Date): string {
  const captured = new Date(capturedAt)
  if (capturedAt === "" || Number.isNaN(captured.getTime())) {
    return "Not yet updated"
  }
  const seconds = Math.max(0, Math.floor((now.getTime() - captured.getTime()) / 1000))
  if (seconds < 60) return `Updated ${seconds} sec ago`
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `Updated ${minutes} min ago`
  return `Updated ${Math.floor(minutes / 60)} h ago`
}
