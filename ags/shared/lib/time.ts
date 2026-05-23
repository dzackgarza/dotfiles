/**
 * Format a time delta for display.
 *
 * @param dueEpochSec - Due time as Unix epoch seconds
 * @param nowMs - Current time as epoch milliseconds (pass Date.now())
 *
 * Returns strings like "in 1h 30m", "in 2d 3h", "overdue 10m", "in 0m".
 */
export function formatDelta(dueEpochSec: number, nowMs: number): string {
  const delta = dueEpochSec * 1000 - nowMs
  const abs = Math.abs(delta)
  const mins = Math.floor(abs / 60_000)
  const hours = Math.floor(mins / 60)
  const days = Math.floor(hours / 24)

  let magnitude: string
  if (days > 0) {
    magnitude = `${days}d ${hours % 24}h`
  } else if (hours > 0) {
    magnitude = `${hours}h ${mins % 60}m`
  } else {
    magnitude = `${mins}m`
  }

  return delta >= 0 ? `in ${magnitude}` : `overdue ${magnitude}`
}

/**
 * Format time until a Date relative to now.
 * Returns "now" when target is in the past.
 */
export function formatRelativeDate(target: Date, nowMs = Date.now()): string {
  const diffMs = target.getTime() - nowMs
  if (diffMs <= 0) return "now"
  const totalMinutes = Math.floor(diffMs / 60_000)
  const days = Math.floor(totalMinutes / (60 * 24))
  const hours = Math.floor((totalMinutes % (60 * 24)) / 60)
  const minutes = totalMinutes % 60
  if (days > 0) return `${days}d ${hours}h`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}
