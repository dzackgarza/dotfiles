import { describe, expect, it } from "vitest";
import { createLogger } from "../logger";

describe("createLogger", () => {
  it("returns a logger with expected methods", () => {
    // initializeLogger adds addEventListener shim and sets up LogTape sinks.
    // In the node test environment, LogTape won't have actual sink output,
    // but createLogger should still return a logger object with the expected API.
    const log = createLogger(["test"]);
    expect(log).toBeDefined();
    expect(typeof log.debug).toBe("function");
    expect(typeof log.info).toBe("function");
    expect(typeof log.warn).toBe("function");
    expect(typeof log.error).toBe("function");
    expect(typeof log.fatal).toBe("function");
  });

  it("returns the same logger instance for the same category", () => {
    const a = createLogger(["test"]);
    const b = createLogger(["test"]);
    expect(a).toBe(b);
  });
});
