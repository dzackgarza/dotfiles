import { configureSync, getConsoleSink, getLogger } from "@logtape/logtape";

export function initializeLogger(): boolean {
  // LogTape checks for addEventListener; shim it for GJS
  const g = globalThis as unknown as { addEventListener: () => boolean };
  if (typeof g.addEventListener === "undefined") {
    g.addEventListener = () => true;
  }

  configureSync({
    sinks: { console: getConsoleSink() },
    loggers: [{ category: [], lowestLevel: "debug", sinks: ["console"] }],
  });
  return true;
}

export function createLogger(category: string[]): ReturnType<typeof getLogger> {
  return getLogger(category);
}
