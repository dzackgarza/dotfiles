// Click-through label at the top-right corner of the focused Hyprland window,
// showing the resident memory (RSS) of the window's process tree.
import { Astal, Gtk } from "ags/gtk4"
import app from "ags/gtk4/app"
import { execAsync } from "ags/process"
import { interval } from "ags/time"
import AstalHyprland from "gi://AstalHyprland"
import Cairo from "cairo"

const POLL_MS = 1000
const LABEL_WIDTH = 70
const INSET = 6

// Sum RSS (kB) over `root` and all its descendants, from `ps -eo pid=,ppid=,rss=`.
function treeRssKb(ps: string, root: number): number {
  const children = new Map<number, number[]>()
  const rss = new Map<number, number>()
  for (const line of ps.trim().split("\n")) {
    const [pid, ppid, kb] = line.trim().split(/\s+/).map(Number)
    rss.set(pid, kb)
    children.set(ppid, [...(children.get(ppid) ?? []), pid])
  }
  let total = 0
  const stack = [root]
  while (stack.length > 0) {
    const pid = stack.pop()!
    total += rss.get(pid) ?? 0
    stack.push(...(children.get(pid) ?? []))
  }
  return total
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

    // Position follows Hyprland events at once; memory refreshes on a timer.
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
    const measure = async () => {
      const client = hypr.get_focused_client()
      if (client === null) return
      const ps = await execAsync(["ps", "-eo", "pid=,ppid=,rss="])
      text!.label = `${(treeRssKb(ps, client.get_pid()) / 1024 / 1024).toFixed(1)}GB`
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
