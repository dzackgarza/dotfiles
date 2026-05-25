/**
 * Application logging setup using LogTape
 * Zero dependencies, works across all JavaScript runtimes
 * 
 * Uses text formatter which works cleanly in terminals
 */

import { configureSync, getLogger, getTextFormatter, type LogRecord } from "@logtape/logtape"

/**
 * Console sink with clean text formatting
 */
const consoleLogSink = (record: LogRecord) => {
  const formatter = getTextFormatter()
  const formatted = formatter(record)
  console.log(formatted)
}

/**
 * Initialize the logging system
 * Must be called before any log statements
 */
export function initializeLogger(): void {
  // Shim addEventListener for GJS environment (LogTape checks for it)
  if (typeof globalThis.addEventListener === "undefined") {
    (globalThis as any).addEventListener = () => {}
  }

  configureSync({
    sinks: {
      console: consoleLogSink,
    },
    loggers: [
      {
        category: [],
        lowestLevel: "debug",
        sinks: ["console"],
      },
    ],
  })
}

/**
 * Get a logger for a specific module/component
 * @param category - Hierarchical category path (e.g., ["ags", "service"])
 */
export function createLogger(category: string[]): ReturnType<typeof getLogger> {
  return getLogger(category)
}
