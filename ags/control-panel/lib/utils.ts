/**
 * Pure utility functions used across the AGS configuration
 */

export function splitWords(value: string): string[] {
  return value
    .trim()
    .split(" ")
    .map((part) => part.trim())
    .filter((part) => part.length > 0);
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function parsePercentText(value: string): number {
  const trimmed = value.trim();
  const normalized = trimmed.endsWith("%") ? trimmed.slice(0, -1) : trimmed;
  const parsed = Number.parseFloat(normalized);

  if (Number.isNaN(parsed)) {
    throw new Error(`Unable to parse percent: ${value}`);
  }

  return parsed;
}

export function parseLeadingCount(value: string): number | null {
  const token = value.trim().split(" ")[0];
  const parsed = Number.parseInt(token, 10);
  return Number.isNaN(parsed) ? -1 : parsed;
}

export function firstLine(text: string): string {
  return text.split("\n")[0] ?? "";
}

export function formatTimestamp(date: Date): string {
  const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  const weekday = weekdays[date.getDay()];
  const month = months[date.getMonth()];
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

  return `${weekday}. ${month} ${day}, ${hours}:${minutes}`;
}

export function formatHours(value: number): string {
  const rounded = Math.round(value * 10) / 10;
  if (Number.isInteger(rounded)) return rounded.toFixed(0);
  return rounded.toFixed(1);
}

export function formatGiB(bytes: number): string {
  const gib = bytes / (1024 * 1024 * 1024);
  const rounded = Math.round(gib * 10) / 10;
  if (Number.isInteger(rounded)) return rounded.toFixed(0);
  return rounded.toFixed(1);
}

export function signalToBars(signalPercent: number): number {
  if (signalPercent >= 80) return 4;
  if (signalPercent >= 60) return 3;
  if (signalPercent >= 40) return 2;
  if (signalPercent >= 20) return 1;
  return 0;
}

export function truncate(value: string, maxLength: number): string {
  if (value.length <= maxLength) return value;
  return `${value.slice(0, Math.max(0, maxLength - 1))}…`;
}

export function cleanTooltip(value: string): string {
  return value
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .join(" • ");
}

export function formatRelative(target: Date): string {
  const diffMs = target.getTime() - Date.now();

  if (diffMs <= 0) return "now";

  const totalMinutes = Math.floor(diffMs / 60000);
  const days = Math.floor(totalMinutes / (60 * 24));
  const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
  const minutes = totalMinutes % 60;

  if (days > 0) return `${days}d ${hours}h`;
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}

export function parseKeyValueOutput(output: string): Map<string, string> {
  const values = new Map<string, string>();

  output.split("\n").forEach((rawLine) => {
    const line = rawLine.trim();
    if (!line) return true;

    const separator = line.indexOf(":");
    if (separator === -1) return true;

    const key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim();

    if (key) values.set(key, value);
    return true;
  });

  return values;
}
