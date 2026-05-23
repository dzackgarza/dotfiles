import { configureSync, getConsoleSink, getLogger } from "@logtape/logtape"

export function initializeLogger(): void {
  // LogTape checks for addEventListener; shim it for GJS
  if (typeof (globalThis as any).addEventListener === "undefined") {
    ;(globalThis as any).addEventListener = () => {}
  }

  configureSync({
    sinks: { console: getConsoleSink() },
    loggers: [{ category: [], lowestLevel: "debug", sinks: ["console"] }],
  })
}

export function createLogger(category: string[]): ReturnType<typeof getLogger> {
  return getLogger(category)
}
