import { describe, expect, it } from "vitest";
import { formatDelta, formatRelativeDate } from "../time";

describe("formatDelta", () => {
  it('returns "in Nm" for deltas under an hour', () => {
    const now = Date.now();
    expect(formatDelta((now + 30_000) / 1000, now)).toBe("in 0m");
    expect(formatDelta((now + 5 * 60_000) / 1000, now)).toBe("in 5m");
    expect(formatDelta((now + 59 * 60_000) / 1000, now)).toBe("in 59m");
  });

  it('returns "in Nh Nm" for deltas in the hour range', () => {
    const now = Date.now();
    expect(formatDelta((now + 60 * 60_000) / 1000, now)).toBe("in 1h 0m");
    expect(formatDelta((now + 90 * 60_000) / 1000, now)).toBe("in 1h 30m");
    expect(formatDelta((now + 23 * 60 * 60_000) / 1000, now)).toBe("in 23h 0m");
  });

  it('returns "in Nd Nh" for deltas over a day', () => {
    const now = Date.now();
    expect(formatDelta((now + 24 * 60 * 60_000) / 1000, now)).toBe("in 1d 0h");
    expect(formatDelta((now + 50 * 60 * 60_000) / 1000, now)).toBe("in 2d 2h");
  });

  it('returns "overdue Nm" for negative deltas', () => {
    const now = Date.now();
    expect(formatDelta((now - 30_000) / 1000, now)).toBe("overdue 0m");
    expect(formatDelta((now - 10 * 60_000) / 1000, now)).toBe("overdue 10m");
  });
});

describe("formatRelativeDate", () => {
  it('returns "now" for past dates', () => {
    expect(formatRelativeDate(new Date(0), 1_000_000)).toBe("now");
    expect(formatRelativeDate(new Date(Date.now() - 10_000))).toBe("now");
  });

  it("returns the delta for future dates", () => {
    const now = Date.now();
    expect(formatRelativeDate(new Date(now + 30_000), now)).toBe("0m");
    expect(formatRelativeDate(new Date(now + 5 * 60_000), now)).toBe("5m");
    expect(formatRelativeDate(new Date(now + 60 * 60_000), now)).toBe("1h 0m");
    expect(formatRelativeDate(new Date(now + 24 * 60 * 60_000), now)).toBe("1d 0h");
  });
});
