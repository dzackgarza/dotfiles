/**
 * Control Center Service
 *
 * Architecture:
 * - Polls system state independently for each tile at appropriate intervals
 * - Each tile has a reader function that throws on errors (fail fast)
 * - Errors are caught by createPolledState and converted to error states
 * - UI (app.tsx) subscribes to state via Accessor functions
 * - Actions (toggle, set) refresh their specific tile after completion
 *
 * To add a new tile:
 * 1. Add state type (e.g., ToggleTileState, UsageTileState, InfoTileState)
 * 2. Add reader function (e.g., readBluetoothState()) that throws on errors
 * 3. Add poll setup in createControlCenterService() using createPolledState
 * 4. Add action function if needed (e.g., toggleBluetooth())
 * 5. Wire up in app.tsx UI components
 */

import { type Accessor, createState } from "ags"
import { readFile } from "ags/file"
import { execAsync } from "ags/process"
import { interval } from "ags/time"
import GLib from "gi://GLib?version=2.0"
import { createLogger } from "../index"
import { fetchClaudeUsage, type UsageCollection } from "../../services/claude-usage-fetcher"
import {
  clamp,
  cleanTooltip,
  firstLine,
  formatGiB,
  formatHours,
  formatRelative,
  formatTimestamp,
  parseKeyValueOutput,
  parseLeadingCount,
  parsePercentText,
  signalToBars,
  splitWords,
} from "../../lib/utils"

const HOME = GLib.get_home_dir()
const HYPR_SCRIPTS = `${HOME}/.config/hypr/scripts`
const VOLUME_SCRIPT = `${HYPR_SCRIPTS}/volumecontrol.sh`
const UPDATE_SCRIPT = `${HYPR_SCRIPTS}/systemupdate.sh`
const POWER_SCRIPT = `${HYPR_SCRIPTS}/power.sh`
const CLAUDE_USAGE_PATH = `${HOME}/.config/hypr/claude_usage_data.json`

export type PowerProfile = "power-saver" | "balanced" | "performance"

// Re-export from fetcher to avoid duplication
export type ClaudeUsageData = Awaited<ReturnType<typeof fetchClaudeUsage>>

// Base tile state with common fields
type BaseTileState = {
  detail: string
  error: string | null
}

type TwoLineState = BaseTileState & {
  line1: string
  line2: string
}

export type ToggleTileState = TwoLineState & {
  active: boolean
}

export type UsageTileState = TwoLineState & {
  percent: number
  percent2?: number
}

export type InfoTileState = TwoLineState

export type SliderState = {
  value: number
  valueLabel: string
  error: string | null
}

export type PowerProfileState = {
  profile: PowerProfile
  detail: string
  error: string | null
}

export type BatteryState = {
  iconName: string
  percentText: string
  etaText: string
  wattageText: string
  detail: string
  error: string | null
}

type PolledState<T> = {
  state: Accessor<T>
  refresh: () => Promise<void>
  setError: (error: unknown) => void
  suppressUpdates: Accessor<boolean>
  setSuppressUpdates: (suppress: boolean) => void
}

type PollOptions<T> = {
  initial: T
  intervalMs: number
  load: () => Promise<T> | T
  onError: (error: unknown) => T
  onSuccess?: () => void
  onFirstComplete?: () => void
}

type PolledStateWithInit<T> = PolledState<T> & {
  initialize: () => Promise<void>
  startPolling: () => void
}

const commandChecks = new Map<string, Promise<void>>()

async function requireCommand(command: string): Promise<void> {
  const existing = commandChecks.get(command)
  if (existing) return existing

  const check = execAsync(["sh", "-lc", `command -v ${command}`])
    .then(() => undefined)
    .catch(() => {
      throw new Error(`${command} is not installed`)
    })

  commandChecks.set(command, check)
  return check
}

function createPolledState<T>(options: PollOptions<T>): PolledStateWithInit<T> {
  const [state, setState] = createState(options.initial)
  const [suppressUpdates, setSuppressUpdates] = createState(false)
  let running = false
  let firstComplete = false
  let pollingStarted = false

  const refresh = async () => {
    if (running || suppressUpdates.peek()) return

    running = true
    try {
      const next = await options.load()
      setState(next)
      options.onSuccess?.()
    } catch (error) {
      setState(options.onError(error))
    } finally {
      running = false
      if (!firstComplete) {
        firstComplete = true
        options.onFirstComplete?.()
      }
    }
  }

  const setError = (error: unknown) => {
    setState(options.onError(error))
  }

  const initialize = async () => {
    await refresh()
  }

  const startPolling = () => {
    if (pollingStarted) return
    pollingStarted = true
    interval(options.intervalMs, () => {
      void refresh()
    })
  }

  return { state, refresh, setError, suppressUpdates, setSuppressUpdates, initialize, startPolling }
}

// Generic error state creator - replaces 6 nearly-identical functions
function createErrorState<T>(
  baseState: T,
  error: unknown
): T & BaseTileState {
  const message = error instanceof Error ? error.message : String(error)
  return {
    ...baseState,
    detail: message,
    error: message,
  } as T & BaseTileState
}

// Specific error handlers using the generic creator
function toggleError(name: string, error: unknown): ToggleTileState {
  const errorMsg = error instanceof Error ? error.message : String(error)
  return createErrorState(
    {
      active: false,
      line1: name,
      line2: `Error: ${errorMsg}`,
    },
    error
  )
}

function usageError(name: string, error: unknown): UsageTileState {
  const errorMsg = error instanceof Error ? error.message : String(error)
  return createErrorState(
    {
      percent: 0,
      line1: name,
      line2: `Error: ${errorMsg}`,
    },
    error
  )
}

function infoError(name: string, error: unknown): InfoTileState {
  const errorMsg = error instanceof Error ? error.message : String(error)
  return createErrorState(
    {
      line1: name,
      line2: `Error: ${errorMsg}`,
    },
    error
  )
}

function sliderError(error: unknown): SliderState {
  const message = error instanceof Error ? error.message : String(error)
  return {
    value: 0,
    valueLabel: `ERR`,
    error: message,
  }
}

function powerProfileError(error: unknown): PowerProfileState {
  const message = error instanceof Error ? error.message : String(error)
  return {
    profile: "balanced",
    detail: message,
    error: message,
  }
}

function batteryError(error: unknown): BatteryState {
  const message = error instanceof Error ? error.message : String(error)
  return {
    iconName: "battery-missing-symbolic",
    percentText: "Error",
    etaText: message,
    wattageText: "--",
    detail: message,
    error: message,
  }
}

async function readBluetoothState(): Promise<ToggleTileState> {
  await requireCommand("rfkill")
  await requireCommand("bluetoothctl")

  const rfkillOutput = await execAsync(["rfkill", "list", "bluetooth"])
  const lines = rfkillOutput.split("\n")

  let hasAdapter = false
  let blocked = false

  for (const rawLine of lines) {
    const line = rawLine.trim()
    if (!line) continue

    if (line.endsWith(": Bluetooth")) {
      hasAdapter = true
      continue
    }

    if (line.startsWith("Soft blocked:")) {
      const value = line.slice("Soft blocked:".length).trim()
      if (value === "yes") blocked = true
    }
  }

  if (!hasAdapter) {
    throw new Error("No Bluetooth adapter found")
  }

  const devicesOutput = await execAsync(["bluetoothctl", "devices", "Connected"])
  const connectedCount = devicesOutput
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("Device "))
    .length

  const active = !blocked
  const deviceLabel = connectedCount === 1 ? "device" : "devices"

  return {
    active,
    line1: active ? "Powered On" : "Power Off",
    line2: `${connectedCount} ${deviceLabel}`,
    detail: active ? `${connectedCount} connected ${deviceLabel}` : "Bluetooth radio is disabled",
    error: null,
  }
}

async function readWifiState(): Promise<ToggleTileState> {
  await requireCommand("nmcli")

  const radioState = (await execAsync(["nmcli", "radio", "wifi"])).trim()
  if (radioState !== "enabled" && radioState !== "disabled") {
    throw new Error(`Unexpected Wi-Fi state: ${radioState}`)
  }

  const active = radioState === "enabled"
  let ssid = "No network"
  let signal = 0

  if (active) {
    const listOutput = await execAsync([
      "nmcli",
      "-t",
      "-f",
      "IN-USE,SIGNAL,SSID",
      "dev",
      "wifi",
      "list",
      "--rescan",
      "no",
    ])

    for (const rawLine of listOutput.split("\n")) {
      const line = rawLine.trimEnd()
      if (!line) continue

      const parts = line.split(":")
      if (parts[0]?.trim() !== "*") continue

      const parsedSignal = Number.parseInt((parts[1] ?? "").trim(), 10)
      if (Number.isNaN(parsedSignal)) {
        throw new Error(`Unexpected Wi-Fi signal line: ${line}`)
      }

      signal = parsedSignal
      ssid = parts.slice(2).join(":").trim() || "Hidden network"
      break
    }
  }

  const connected = active && ssid !== "No network"
  const bars = connected ? signalToBars(signal) : 0

  return {
    active,
    line1: connected ? `Connected • ${bars} bars` : active ? "Disconnected • 0 bars" : "Wi-Fi Off",
    line2: connected ? ssid : active ? "No network" : "Radio disabled",
    detail: connected ? `Signal strength ${signal}%` : active ? "Wi-Fi enabled but not connected" : "Wi-Fi radio disabled",
    error: null,
  }
}

async function readPowerProfileState(): Promise<PowerProfileState> {
  await requireCommand("powerprofilesctl")
  const profile = (await execAsync(["powerprofilesctl", "get"])).trim()

  if (profile !== "power-saver" && profile !== "balanced" && profile !== "performance") {
    throw new Error(`Unknown power profile: ${profile}`)
  }

  return {
    profile,
    detail: `Active profile: ${profile}`,
    error: null,
  }
}

async function readAppearanceState(): Promise<ToggleTileState> {
  await requireCommand("gsettings")

  const raw = (await execAsync([
    "gsettings",
    "get",
    "org.gnome.desktop.interface",
    "color-scheme",
  ])).trim()

  const dark = raw.includes("dark")

  return {
    active: dark,
    line1: dark ? "Dark" : "Light",
    line2: "Mode",
    detail: `gsettings color-scheme: ${raw}`,
    error: null,
  }
}

async function readSilentState(): Promise<ToggleTileState> {
  await requireCommand("swaync-client")
  const raw = (await execAsync(["swaync-client", "-D", "-sw"])).trim()

  if (raw !== "true" && raw !== "false") {
    throw new Error(`Unexpected DND state: ${raw}`)
  }

  const active = raw === "true"

  return {
    active,
    line1: active ? "Silent" : "Alerts On",
    line2: "Notifications",
    detail: active ? "Do not disturb is enabled" : "Notifications are enabled",
    error: null,
  }
}

async function readMicState(): Promise<ToggleTileState> {
  await requireCommand("pactl")
  const raw = await execAsync(["pactl", "get-source-mute", "@DEFAULT_SOURCE@"])
  const values = parseKeyValueOutput(raw)
  const muteValue = values.get("Mute")

  if (!muteValue || (muteValue !== "yes" && muteValue !== "no")) {
    throw new Error(`Unexpected microphone state: ${raw}`)
  }

  const muted = muteValue === "yes"

  return {
    active: muted,
    line1: muted ? "Muted" : "Live",
    line2: "Mic",
    detail: muted ? "Default input source is muted" : "Default input source is live",
    error: null,
  }
}

let previousCpuSample: { total: number; idle: number } | null = null

// Explicit return types for type safety - TypeScript will catch breaking changes at all call sites
function readCpuState(): UsageTileState {
  const statLine = firstLine(readFile("/proc/stat")).trim()
  const fields = splitWords(statLine)

  if (fields[0] !== "cpu") {
    throw new Error("Invalid /proc/stat format")
  }

  const counters = fields.slice(1).map((value) => Number.parseInt(value, 10))
  if (counters.some((value) => Number.isNaN(value))) {
    throw new Error("Unable to parse CPU counters")
  }

  const idle = counters[3] + counters[4]
  const total = counters.reduce((sum, value) => sum + value, 0)

  let usagePercent = 0
  if (previousCpuSample) {
    const totalDelta = total - previousCpuSample.total
    const idleDelta = idle - previousCpuSample.idle
    usagePercent = totalDelta <= 0 ? 0 : ((totalDelta - idleDelta) / totalDelta) * 100
  } else {
    usagePercent = total <= 0 ? 0 : ((total - idle) / total) * 100
  }

  previousCpuSample = { total, idle }

  const cpuInfo = readFile("/proc/cpuinfo")
  let mhz = 0
  let cores = 0

  for (const rawLine of cpuInfo.split("\n")) {
    const line = rawLine.trim()
    if (!line) continue

    if (line.startsWith("processor")) {
      cores += 1
      continue
    }

    if (!mhz && line.startsWith("cpu MHz")) {
      const parts = line.split(":")
      const parsed = Number.parseFloat((parts[1] ?? "").trim())
      if (!Number.isNaN(parsed)) mhz = parsed
    }
  }

  if (cores <= 0) throw new Error("Unable to determine CPU core count")
  if (mhz <= 0) throw new Error("Unable to determine CPU frequency")

  const roundedPercent = clamp(Math.round(usagePercent), 0, 100)
  const ghz = mhz / 1000

  return {
    percent: roundedPercent / 100,
    line1: `${roundedPercent}% • ${ghz.toFixed(1)} GHz`,
    line2: `${cores} cores`,
    detail: "Live sample from /proc/stat and /proc/cpuinfo",
    error: null,
  }
}

function readMemoryState(): UsageTileState {
  const memInfo = parseKeyValueOutput(readFile("/proc/meminfo"))

  const parseMemKb = (key: string) => {
    const raw = memInfo.get(key)
    if (!raw) throw new Error(`Missing ${key} in /proc/meminfo`)

    const value = Number.parseInt(raw.split(" ")[0] ?? "", 10)
    if (Number.isNaN(value)) throw new Error(`Invalid ${key} value: ${raw}`)
    return value
  }

  const totalKb = parseMemKb("MemTotal")
  const availableKb = parseMemKb("MemAvailable")
  const swapTotalKb = parseMemKb("SwapTotal")
  const swapFreeKb = parseMemKb("SwapFree")

  const usedKb = totalKb - availableKb
  const swapUsedKb = swapTotalKb - swapFreeKb
  const usedPercent = totalKb <= 0 ? 0 : (usedKb / totalKb) * 100
  const roundedPercent = clamp(Math.round(usedPercent), 0, 100)

  return {
    percent: roundedPercent / 100,
    line1: `${roundedPercent}% • ${formatGiB(usedKb * 1024)}/${formatGiB(totalKb * 1024)} GB`,
    line2: `Swap ${formatGiB(swapUsedKb * 1024)}/${formatGiB(swapTotalKb * 1024)} GB`,
    detail: `Available RAM: ${formatGiB(availableKb * 1024)} GB`,
    error: null,
  }
}

async function readDiskState(): Promise<UsageTileState> {
  await requireCommand("df")
  const output = await execAsync(["df", "-B1", "/", "/home"])

  const lines = output
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)

  if (lines.length < 2) {
    throw new Error("df output did not include filesystem rows")
  }

  const entries = lines.slice(1).map((line) => {
    const fields = splitWords(line)
    if (fields.length < 6) throw new Error(`Unable to parse df row: ${line}`)

    const total = Number.parseInt(fields[1] ?? "", 10)
    const used = Number.parseInt(fields[2] ?? "", 10)
    const percent = parsePercentText(fields[4] ?? "")
    const mount = fields[5] ?? ""

    if (Number.isNaN(total) || Number.isNaN(used)) {
      throw new Error(`Unable to parse disk sizes: ${line}`)
    }

    return { mount, total, used, percent }
  })

  const rootEntry = entries.find((entry) => entry.mount === "/") ?? entries[0]
  if (!rootEntry) throw new Error("Root filesystem entry not found")

  const homeEntry = entries.find((entry) => entry.mount === "/home") ?? rootEntry
  const rootPercent = clamp(Math.round(rootEntry.percent), 0, 100)
  const homePercent = clamp(Math.round(homeEntry.percent), 0, 100)

  return {
    percent: rootPercent / 100,
    line1: `${rootPercent}% • ${formatGiB(rootEntry.used)}/${formatGiB(rootEntry.total)} GB`,
    line2: `/home ${formatGiB(homeEntry.used)} GB`,
    detail: `/ ${rootPercent}% • /home ${homePercent}%`,
    error: null,
  }
}

async function fetchClaudeUsageData(): Promise<ClaudeUsageData> {
  const logger = createLogger(["ags", "claude"])
  const data = await fetchClaudeUsage()
  const claude = data.providers.find(p => p.provider === "claude")
  if (claude && claude.status === "ok") {
    const row5h = claude.rows.find(r => r.identifier.includes("5h"))
    const row7d = claude.rows.find(r => r.identifier.includes("7d"))
    const pct5h = row5h ? row5h.pct_used : 0
    const pct7d = row7d ? row7d.pct_used : 0
    logger.debug`Fetched Claude usage: 5h=${pct5h}% 7d=${pct7d}%`
  } else {
    logger.debug`Fetched Claude usage: (claude provider not found or failed)`
  }
  return data
}

async function readAiUsageState(): Promise<UsageTileState> {
  const data = await fetchClaudeUsageData()

  // Find the claude provider snapshot
  const claude = data.providers.find(p => p.provider === "claude")
  if (!claude) {
    throw new Error("Claude provider not found in usage collection")
  }
  if (claude.status === "error") {
    const errMsg = claude.errors?.[0]?.message || "Claude provider returned error status"
    throw new Error(errMsg)
  }

  // Find 5h and 7d rows
  const row5h = claude.rows.find(r => r.identifier.includes("5h"))
  const row7d = claude.rows.find(r => r.identifier.includes("7d"))

  if (!row5h || !row7d) {
    throw new Error("Required 5h or 7d usage rows not found for Claude")
  }

  const fiveUtilization = row5h.pct_used
  const sevenUtilization = row7d.pct_used

  // Parse reset dates or use fallback if null
  const fiveReset = row5h.reset_at ? new Date(row5h.reset_at) : new Date()
  const sevenReset = row7d.reset_at ? new Date(row7d.reset_at) : new Date()

  if (Number.isNaN(fiveReset.getTime())) {
    throw new Error(`Invalid fiveHourResetAt: ${row5h.reset_at}`)
  }
  if (Number.isNaN(sevenReset.getTime())) {
    throw new Error(`Invalid sevenDayResetAt: ${row7d.reset_at}`)
  }

  const fiveFraction = clamp(fiveUtilization / 100, 0, 1)
  const sevenFraction = clamp(sevenUtilization / 100, 0, 1)
  const fiveHours = 5 * fiveFraction
  const sevenHours = 35 * sevenFraction

  return {
    percent: fiveFraction,
    percent2: sevenFraction,
    line1: `${Math.round(fiveUtilization)}% • ${formatHours(fiveHours)}/5h`,
    line2: `7d ${formatHours(sevenHours)}/35h`,
    detail: `5h reset in ${formatRelative(fiveReset)} • 7d reset in ${formatRelative(sevenReset)}`,
    error: null,
  }
}

async function readUpdatesState(): Promise<InfoTileState> {
  const output = (await execAsync([UPDATE_SCRIPT, "--check"])).trim()

  // Strict JSON parsing with clear error messages
  let parsed: unknown
  try {
    parsed = JSON.parse(output)
  } catch (error) {
    throw new Error(`Update script returned invalid JSON: ${firstLine(output)}`)
  }

  if (!parsed || typeof parsed !== "object") {
    throw new Error("Update script JSON is not an object")
  }

  const data = parsed as Record<string, unknown>
  const text = typeof data.text === "string" ? data.text : ""
  const tooltip = cleanTooltip(typeof data.tooltip === "string" ? data.tooltip : "")
  const checkTime = formatTimestamp(new Date())

  const count = parseLeadingCount(text)

  if (count !== null) {
    const label = count === 1 ? "package" : "packages"
    return {
      line1: `${count} ${label} available`,
      line2: checkTime,
      detail: tooltip || "Updates available",
      error: null,
    }
  }

  if (text === "✓") {
    return {
      line1: "Packages up to date",
      line2: checkTime,
      detail: tooltip || "No updates available",
      error: null,
    }
  }

  if (text === "?") {
    return {
      line1: "Update check unavailable",
      line2: checkTime,
      detail: tooltip || "Network not available",
      error: null,
    }
  }

  throw new Error(`Unexpected update response: ${text}`)
}

async function readNotificationState(): Promise<InfoTileState> {
  await requireCommand("swaync-client")

  const countRaw = (await execAsync(["swaync-client", "-c", "-sw"])).trim()
  const count = Number.parseInt(countRaw, 10)

  if (Number.isNaN(count)) {
    throw new Error(`Unexpected notification count: ${countRaw}`)
  }

  return {
    line1: `${count} unread`,
    line2: count > 0 ? "Open Notification Center" : "No unread notifications",
    detail: `${count} unread notifications`,
    error: null,
  }
}

async function readVolumeState(): Promise<SliderState> {
  await requireCommand("pactl")

  const volumeOutput = await execAsync(["pactl", "get-sink-volume", "@DEFAULT_SINK@"])
  const volumeLine = firstLine(volumeOutput)
  const sections = volumeLine.split("/")
  if (sections.length < 2) throw new Error(`Unexpected sink volume output: ${volumeLine}`)

  const percentToken = splitWords(sections[1] ?? "")[0] ?? ""
  const percent = clamp(parsePercentText(percentToken), 0, 100)

  const muteOutput = await execAsync(["pactl", "get-sink-mute", "@DEFAULT_SINK@"])
  const muteValues = parseKeyValueOutput(muteOutput)
  const muteValue = muteValues.get("Mute")
  if (!muteValue || (muteValue !== "yes" && muteValue !== "no")) {
    throw new Error(`Unexpected sink mute output: ${muteOutput}`)
  }

  const muted = muteValue === "yes"

  return {
    value: percent / 100,
    valueLabel: muted ? "Muted" : `${Math.round(percent)}%`,
    error: null,
  }
}

async function readBrightnessState(): Promise<SliderState> {
  await requireCommand("brightnessctl")
  const output = (await execAsync(["brightnessctl", "-m"])).trim()
  // Format: device,class,current,percent,max
  // Example: intel_backlight,backlight,48000,50%,96000
  const percentStr = output.split(",")[3] ?? "0%"
  const percent = clamp(parsePercentText(percentStr), 0, 100)

  return {
    value: percent / 100,
    valueLabel: `${Math.round(percent)}%`,
    error: null,
  }
}

async function readBatteryState(): Promise<BatteryState> {
  await requireCommand("upower")

  const devices = await execAsync(["upower", "-e"])
  const batteryPath = devices
    .split("\n")
    .map((line) => line.trim())
    .find((line) => line.includes("/battery_"))

  if (!batteryPath) throw new Error("No UPower battery device found")

  const details = await execAsync(["upower", "-i", batteryPath])
  const values = parseKeyValueOutput(details)

  const percentage = values.get("percentage")
  const state = values.get("state")
  const energyRate = values.get("energy-rate")
  const iconNameRaw = values.get("icon-name")
  const timeToFull = values.get("time to full")
  const timeToEmpty = values.get("time to empty")

  if (!percentage || !state || !energyRate || !iconNameRaw) {
    throw new Error("Missing required battery fields from UPower")
  }

  const iconName = iconNameRaw.replaceAll("'", "")
  const etaText =
    state === "charging"
      ? timeToFull
        ? `to full ${timeToFull}`
        : "charging"
      : state === "discharging"
        ? timeToEmpty
          ? `remaining ${timeToEmpty}`
          : "discharging"
        : state

  return {
    iconName,
    percentText: percentage,
    etaText,
    wattageText: energyRate,
    detail: `${percentage} • ${etaText} • ${energyRate}`,
    error: null,
  }
}

export type ControlCenterService = {
  ready: Accessor<boolean>
  bluetooth: Accessor<ToggleTileState>
  wifi: Accessor<ToggleTileState>
  powerProfile: Accessor<PowerProfileState>
  appearance: Accessor<ToggleTileState>
  silent: Accessor<ToggleTileState>
  mic: Accessor<ToggleTileState>
  updates: Accessor<InfoTileState>
  notifications: Accessor<InfoTileState>
  cpu: Accessor<UsageTileState>
  memory: Accessor<UsageTileState>
  disk: Accessor<UsageTileState>
  volume: Accessor<SliderState>
  brightness: Accessor<SliderState>
  battery: Accessor<BatteryState>
  claudeUsageData: Accessor<UsageCollection>
  lastUpdated: Accessor<string>
  actionError: Accessor<string>
  initializeService: () => Promise<void>
  startPollingService: () => void
  refreshUsage: () => void
  suppressVolumeDrag: (suppress: boolean) => void
  suppressBrightnessDrag: (suppress: boolean) => void
  toggleBluetooth: () => Promise<void>
  toggleWifi: () => Promise<void>
  setPowerProfile: (profile: PowerProfile) => Promise<void>
  toggleAppearance: () => Promise<void>
  toggleSilent: () => Promise<void>
  toggleMic: () => Promise<void>
  openNotificationCenter: () => Promise<void>
  setVolume: (value: number) => Promise<void>
  setBrightness: (value: number) => Promise<void>
  suspend: () => Promise<void>
  hibernate: () => Promise<void>
  poweroff: () => Promise<void>
}

function createControlCenterService(): ControlCenterService {
  const logger = createLogger(["ags", "control-center"])
  const totalPolls = 14
  const [pendingPolls, setPendingPolls] = createState(totalPolls)
  const ready = pendingPolls((count) => count === 0)
  const [lastUpdated, setLastUpdated] = createState("Last updated: waiting for first poll")
  const [actionError, setActionError] = createState("")

  const markUpdated = () => {
    setLastUpdated(`Last updated: ${formatTimestamp(new Date())}`)
  }

  const setActionFailure = (label: string, error: unknown) => {
    const msg = error instanceof Error ? error.message : String(error)
    setActionError(`${label} failed: ${msg}`)
  }

  const clearActionError = () => {
    if (actionError().length > 0) setActionError("")
  }

  const markFirstPollComplete = () => {
    setPendingPolls((count) => Math.max(0, count - 1))
  }

  const bluetoothPoll = createPolledState({
    initial: {
      active: false,
      line1: "Loading...",
      line2: "Bluetooth",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 4000,
    load: readBluetoothState,
    onError: (error) => toggleError("Bluetooth", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const wifiPoll = createPolledState({
    initial: {
      active: false,
      line1: "Loading...",
      line2: "Wi-Fi",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 4000,
    load: readWifiState,
    onError: (error) => toggleError("Wi-Fi", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const powerProfilePoll = createPolledState({
    initial: {
      profile: "balanced",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 5000,
    load: readPowerProfileState,
    onError: powerProfileError,
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const appearancePoll = createPolledState({
    initial: {
      active: false,
      line1: "Loading...",
      line2: "Appearance",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 5000,
    load: readAppearanceState,
    onError: (error) => toggleError("Appearance", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const silentPoll = createPolledState({
    initial: {
      active: false,
      line1: "Loading...",
      line2: "Notifications",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 3000,
    load: readSilentState,
    onError: (error) => toggleError("Silent", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const micPoll = createPolledState({
    initial: {
      active: false,
      line1: "Loading...",
      line2: "Mic",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 2000,
    load: readMicState,
    onError: (error) => toggleError("Mic", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const updatesPoll = createPolledState({
    initial: {
      line1: "Loading...",
      line2: "Updates",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 120000,
    load: readUpdatesState,
    onError: (error) => infoError("Updates", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const notificationsPoll = createPolledState({
    initial: {
      line1: "Loading...",
      line2: "Notification Center",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 3000,
    load: readNotificationState,
    onError: (error) => infoError("Notification Center", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const cpuPoll = createPolledState({
    initial: {
      percent: 0,
      line1: "Loading...",
      line2: "CPU",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 2000,
    load: readCpuState,
    onError: (error) => usageError("CPU", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const memoryPoll = createPolledState({
    initial: {
      percent: 0,
      line1: "Loading...",
      line2: "Memory",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 3000,
    load: readMemoryState,
    onError: (error) => usageError("Memory", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const diskPoll = createPolledState({
    initial: {
      percent: 0,
      line1: "Loading...",
      line2: "Disk",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 15000,
    load: readDiskState,
    onError: (error) => usageError("Disk", error),
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const USAGE_TTL_MS = 120_000 // 2 minutes
  let usageLastFetchedAt = 0

  const claudeUsageDataPoll = createPolledState({
    initial: {
      version: "1",
      captured_at: "",
      providers: [],
    } as ClaudeUsageData,
    intervalMs: 0, // no background polling — refreshed on window open via refreshUsage()
    load: fetchClaudeUsageData,
    onError: (error) => {
      logger.error`Failed to fetch Claude usage: ${error}`
      throw error
    },
    onSuccess: () => { usageLastFetchedAt = Date.now(); markUpdated() },
    onFirstComplete: markFirstPollComplete,
  })

  const refreshUsage = () => {
    if (Date.now() - usageLastFetchedAt < USAGE_TTL_MS) return
    void claudeUsageDataPoll.refresh()
  }

  const volumePoll = createPolledState({
    initial: {
      value: 0,
      valueLabel: "--",
      error: null,
    },
    intervalMs: 1500,
    load: readVolumeState,
    onError: sliderError,
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const brightnessPoll = createPolledState({
    initial: {
      value: 0,
      valueLabel: "--",
      error: null,
    },
    intervalMs: 2000,
    load: readBrightnessState,
    onError: sliderError,
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  const batteryPoll = createPolledState({
    initial: {
      iconName: "battery-missing-symbolic",
      percentText: "--",
      etaText: "Loading...",
      wattageText: "--",
      detail: "Waiting for first poll",
      error: null,
    },
    intervalMs: 10000,
    load: readBatteryState,
    onError: batteryError,
    onSuccess: markUpdated,
    onFirstComplete: markFirstPollComplete,
  })

  let actionInFlight = false

  const runPolledAction = async <T>(
    label: string,
    poll: PolledState<T>,
    action: () => Promise<void>,
  ) => {
    try {
      actionInFlight = true
      await action()
      await poll.refresh()
      clearActionError()
    } catch (error) {
      poll.setError(error)
      setActionFailure(label, error)
    } finally {
      actionInFlight = false
    }
  }

  const runSystemAction = async (label: string, action: () => Promise<void>) => {
    try {
      await action()
      clearActionError()
    } catch (error) {
      setActionFailure(label, error)
    }
  }

  // Initialize all state
  const initializeService = async () => {
    // Await all initializations before resolving
    const logger = createLogger(["ags", "control-center"])
    logger.info`Initializing 14 system polls [SERVICE] (initializeService)`
    try {
      await Promise.all([
        bluetoothPoll.initialize(),
        wifiPoll.initialize(),
        powerProfilePoll.initialize(),
        appearancePoll.initialize(),
        silentPoll.initialize(),
        micPoll.initialize(),
        updatesPoll.initialize(),
        notificationsPoll.initialize(),
        cpuPoll.initialize(),
        memoryPoll.initialize(),
        diskPoll.initialize(),
        claudeUsageDataPoll.initialize(),
        volumePoll.initialize(),
        brightnessPoll.initialize(),
        batteryPoll.initialize(),
      ])
      logger.info`All 14 system polls initialized successfully [SERVICE] (initializeService)`
    } catch (error) {
      logger.error`Initialization error: ${error} [SERVICE] (initializeService)`
      throw error
    }
  }

  // Start polling for all state
  const startPollingService = () => {
    const logger = createLogger(["ags", "control-center"])
    logger.info`Starting continuous polling of all 14 system states [SERVICE] (startPollingService)`
    bluetoothPoll.startPolling()
    wifiPoll.startPolling()
    powerProfilePoll.startPolling()
    appearancePoll.startPolling()
    silentPoll.startPolling()
    micPoll.startPolling()
    updatesPoll.startPolling()
    notificationsPoll.startPolling()
    cpuPoll.startPolling()
    memoryPoll.startPolling()
    diskPoll.startPolling()
    // claudeUsageData: no background polling — refreshed on window open via refreshUsage()
    volumePoll.startPolling()
    brightnessPoll.startPolling()
    batteryPoll.startPolling()
    logger.info`Polling started for all 14 system states [SERVICE] (startPollingService)`
  }

  return {
    ready,
    bluetooth: bluetoothPoll.state,
    wifi: wifiPoll.state,
    powerProfile: powerProfilePoll.state,
    appearance: appearancePoll.state,
    silent: silentPoll.state,
    mic: micPoll.state,
    updates: updatesPoll.state,
    notifications: notificationsPoll.state,
    cpu: cpuPoll.state,
    memory: memoryPoll.state,
    disk: diskPoll.state,
    claudeUsageData: claudeUsageDataPoll.state,
    volume: volumePoll.state,
    brightness: brightnessPoll.state,
    battery: batteryPoll.state,
    lastUpdated,
    actionError,
    initializeService,
    startPollingService,
    refreshUsage,
    suppressVolumeDrag: (suppress: boolean) => {
      if (suppress) {
        volumePoll.setSuppressUpdates(true)
      } else {
        // Don't re-enable polling if action is still in flight
        if (!actionInFlight) {
          volumePoll.setSuppressUpdates(false)
        }
      }
    },
    suppressBrightnessDrag: (suppress: boolean) => {
      if (suppress) {
        brightnessPoll.setSuppressUpdates(true)
      } else {
        // Don't re-enable polling if action is still in flight
        if (!actionInFlight) {
          brightnessPoll.setSuppressUpdates(false)
        }
      }
    },
    async toggleBluetooth() {
      const enable = !bluetoothPoll.state.peek().active
      await runPolledAction("Bluetooth", bluetoothPoll, async () => {
        await requireCommand("rfkill")
        await execAsync(["rfkill", enable ? "unblock" : "block", "bluetooth"])
      })
    },
    async toggleWifi() {
      const enable = !wifiPoll.state.peek().active
      await runPolledAction("Wi-Fi", wifiPoll, async () => {
        await requireCommand("nmcli")
        await execAsync(["nmcli", "radio", "wifi", enable ? "on" : "off"])
      })
    },
    async setPowerProfile(profile: PowerProfile) {
      await runPolledAction("Power Profile", powerProfilePoll, async () => {
        await requireCommand("powerprofilesctl")
        await execAsync(["powerprofilesctl", "set", profile])
      })
    },
    async toggleAppearance() {
      const makeDark = !appearancePoll.state.peek().active
      await runPolledAction("Appearance", appearancePoll, async () => {
        await requireCommand("gsettings")
        await execAsync([
          "gsettings",
          "set",
          "org.gnome.desktop.interface",
          "color-scheme",
          makeDark ? "prefer-dark" : "prefer-light",
        ])
      })
    },
    async toggleSilent() {
      await runPolledAction("Silent", silentPoll, async () => {
        await requireCommand("swaync-client")
        await execAsync(["swaync-client", "-d", "-sw"])
      })
    },
    async toggleMic() {
      await runPolledAction("Microphone", micPoll, async () => {
        await execAsync([VOLUME_SCRIPT, "--toggle-mic"])
      })
    },
    async openNotificationCenter() {
      await runSystemAction("Notification Center", async () => {
        await requireCommand("swaync-client")
        await execAsync(["swaync-client", "-t", "-sw"])
      })
    },
    async setVolume(value: number) {
      await runPolledAction("Volume", volumePoll, async () => {
        await requireCommand("pactl")
        const percent = clamp(Math.round(value * 100), 0, 100)
        await execAsync(["pactl", "set-sink-volume", "@DEFAULT_SINK@", `${percent}%`])
        if (percent > 0) {
          await execAsync(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "false"])
        }
      })
    },
    async setBrightness(value: number) {
      await runPolledAction("Brightness", brightnessPoll, async () => {
        await requireCommand("brightnessctl")
        const percent = clamp(Math.round(value * 100), 0, 100)
        console.log(`setBrightness: setting to ${percent}%`)
        const result = await execAsync(["brightnessctl", "set", `${percent}%`, "-n"])
        console.log(`setBrightness: result = ${result}`)
      })
    },
    async suspend() {
      await runSystemAction("Suspend", async () => {
        await execAsync(["systemctl", "suspend"])
      })
    },
    async hibernate() {
      await runSystemAction("Hibernate", async () => {
        await execAsync(["systemctl", "hibernate"])
      })
    },
    async poweroff() {
      await runSystemAction("Poweroff", async () => {
        await execAsync([POWER_SCRIPT, "--poweroff"])
      })
    },
  }
}

let cachedService: ControlCenterService | null = null

export function getControlCenterService(): ControlCenterService {
  if (!cachedService) cachedService = createControlCenterService()
  return cachedService
}
