import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { PROVIDER_ICONS } from "../provider-icons";

const ICONS_DIR = resolve(import.meta.dirname, "../../../icons/hicolor/scalable/status");

describe("PROVIDER_ICONS", () => {
  it("every mapped icon exists as an SVG file on disk", () => {
    const missing: string[] = [];
    for (const [provider, iconName] of Object.entries(PROVIDER_ICONS)) {
      const svgPath = resolve(ICONS_DIR, `${iconName}.svg`);
      if (!existsSync(svgPath)) {
        missing.push(`${provider} -> ${iconName}.svg`);
      }
    }
    expect(missing).toEqual([]);
  });

  it("every mapped icon SVG is valid XML with a viewBox", () => {
    const invalid: string[] = [];
    for (const [provider, iconName] of Object.entries(PROVIDER_ICONS)) {
      const svgPath = resolve(ICONS_DIR, `${iconName}.svg`);
      if (!existsSync(svgPath)) continue;

      const content = readFileSync(svgPath, "utf-8");
      if (!content.includes("<svg") || !content.includes("viewBox")) {
        invalid.push(`${provider} -> ${iconName}.svg: missing <svg> or viewBox`);
      }
    }
    expect(invalid).toEqual([]);
  });
});
