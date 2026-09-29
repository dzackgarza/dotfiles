// Click-through label at the top-right corner of the focused Hyprland window,
// showing the resident memory (RSS) of the window's process tree and that
// tree's share of total CPU time (all cores = 100%) since the previous poll.
import { Astal, Gtk } from "ags/gtk4"
import app from "ags/gtk4/app"
import { execAsync } from "ags/process"
import { interval } from "ags/time"
import AstalHyprland from "gi://AstalHyprland"
import GLib from "gi://GLib"
import Cairo from "cairo"

const POLL_MS = 1000
const LABEL_WIDTH = 120
const INSET = 6

function readText(path: string): string | null {
  try {
    return new TextDecoder().decode(GLib.file_get_contents(path)[1])
  } catch {
    return null // process exited between `ps` and the read
  }
}

// `root` and all its descendants, from `ps -eo pid=,ppid=,rss=`, with summed RSS (kB).
function processTree(ps: string, root: number): { pids: number[]; rssKb: number } {
  const children = new Map<number, number[]>()
  const rss = new Map<number, number>()
  for (const line of ps.trim().split("\n")) {
    const [pid, ppid, kb] = line.trim().split(/\s+/).map(Number)
    rss.set(pid, kb)
    children.set(ppid, [...(children.get(ppid) ?? []), pid])
  }
  const pids: number[] = []
  let rssKb = 0
  const stack = [root]
  while (stack.length > 0) {
    const pid = stack.pop()!
    pids.push(pid)
    rssKb += rss.get(pid) ?? 0
    stack.push(...(children.get(pid) ?? []))
  }
  return { pids, rssKb }
}

// utime + stime in clock ticks; fields 14 and 15 of proc_pid_stat(5).
function processTicks(pid: number): number {
  const stat = readText(`/proc/${pid}/stat`)
  if (stat === null) return 0
  const fields = stat.slice(stat.lastIndexOf(")") + 2).split(" ")
  return Number(fields[11]) + Number(fields[12])
}

// Sum of all columns of the aggregate "cpu" line of proc_stat(5), in clock ticks.
function totalTicks(): number {
  const line = readText("/proc/stat")!.split("\n")[0]
  return line.trim().split(/\s+/).slice(1).map(Number).reduce((a, b) => a + b, 0)
}

app.start({
  instanceName: "window-ram",
  css: `
    window { background: transparent; }
    label { font-family: monospace; font-size: 11px; color: #d3c6aa;
            background: rgba(0,0,0,0.6); border-radius: 5px; padding: 1px 6px; }
  `,
  main() {
    const hypr = AstalHyprland.get_default()
    const { TOP, LEFT } = Astal.WindowAnchor
    let text: Gtk.Label | null = null

    const win = (
      <window
        name="window-ram"
        layer={Astal.Layer.OVERLAY}
        exclusivity={Astal.Exclusivity.IGNORE}
        anchor={TOP | LEFT}
        application={app}
      >
        <label widthRequest={LABEL_WIDTH} $={(self) => (text = self)} />
      </window>
    ) as Astal.Window

    win.connect("realize", () => win.get_surface()?.set_input_region(new Cairo.Region()))

    // Position follows Hyprland events at once; usage refreshes on a timer.
    const place = () => {
      const client = hypr.get_focused_client()
      if (client === null || client.get_fullscreen() !== AstalHyprland.Fullscreen.NONE) {
        win.visible = false
        return
      }
      const monitor = client.get_monitor()
      win.marginTop = client.get_y() - monitor.get_y() + INSET
      win.marginLeft = client.get_x() - monitor.get_x() + client.get_width() - LABEL_WIDTH - INSET
      win.visible = true
    }

    // CPU share needs two samples of the same process tree.
    let previous: { root: number; tree: number; total: number } | null = null
    const measure = async () => {
      const client = hypr.get_focused_client()
      if (client === null) return
      const root = client.get_pid()
      const ps = await execAsync(["ps", "-eo", "pid=,ppid=,rss="])
      const { pids, rssKb } = processTree(ps, root)
      const sample = { root, tree: pids.map(processTicks).reduce((a, b) => a + b, 0), total: totalTicks() }
      const cpu =
        previous !== null && previous.root === root && sample.total > previous.total
          ? `${((100 * Math.max(0, sample.tree - previous.tree)) / (sample.total - previous.total)).toFixed(0)}%`
          : "…"
      previous = sample
      text!.label = `${(rssKb / 1024 / 1024).toFixed(1)}GB ${cpu}`
    }
    hypr.connect("event", place)
    hypr.connect("notify::focused-client", () => {
      place()
      void measure()
    })
    interval(POLL_MS, () => void measure())
    place()
  },
})
