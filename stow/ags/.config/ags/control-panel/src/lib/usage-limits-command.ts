export const USAGE_LIMITS_PROJECT = "/home/dzack/gitclones/usage-limits"

export const USAGE_LIMITS_JSON_COMMAND = [
  "uv",
  "run",
  "--project",
  USAGE_LIMITS_PROJECT,
  "usage-limits",
  "--json",
] as const
