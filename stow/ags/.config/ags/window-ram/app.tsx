// Click-through label at the top-right corner of the focused Hyprland window,
// showing the resident memory (RSS) of the window's process tree and that
// tree's share of total CPU time (all cores = 100%) since the previous poll.
import { Astal, Gtk } from "ags/gtk4";
import app from "ags/gtk4/app";
import { execAsync } from "ags/process";
import { interval } from "ags/time";
import AstalHyprland from "gi://AstalHyprland";
import GLib from "gi://GLib";
import Gdk from "gi://Gdk";
import Cairo from "cairo";

const POLL_MS = 1000;
const LABEL_WIDTH = 120;
const INSET = 6;

function readText(path: string): string | null {
  try {
    return new TextDecoder().decode(GLib.file_get_contents(path)[1]);
  } catch {
    return null; // process exited between `ps` and the read
  }
}

// `root` and all its descendants, from `ps -eo pid=,ppid=,rss=`, with summed RSS (kB).
function processTree(
  ps: string,
  root: number,
): { pids: number[]; rssKb: number } {
  const children = new Map<number, number[]>();
  const rss = new Map<number, number>();
  for (const line of ps.trim().split("\n")) {
    const [pid, ppid, kb] = line.trim().split(/\s+/).map(Number);
    rss.set(pid, kb);
    children.set(ppid, [...(children.get(ppid) ?? []), pid]);
  }
  const pids: number[] = [];
  let rssKb = 0;
  const stack = [root];
  while (stack.length > 0) {
    const pid = stack.pop()!;
    pids.push(pid);
    rssKb += rss.get(pid) ?? 0;
    stack.push(...(children.get(pid) ?? []));
  }
  return { pids, rssKb };
}

// utime + stime in clock ticks; fields 14 and 15 of proc_pid_stat(5).
function processTicks(pid: number): number {
  const stat = readText(`/proc/${pid}/stat`);
  if (stat === null) return 0;
  const fields = stat.slice(stat.lastIndexOf(")") + 2).split(" ");
  return Number(fields[11]) + Number(fields[12]);
}

// Sum of the first eight columns of the aggregate "cpu" line of
// proc_stat(5), in clock ticks. guest and guest_nice are already counted in
// user and nice.
function totalTicks(): number {
  const line = readText("/proc/stat")!.split("\n")[0];
  return line
    .trim()
    .split(/\s+/)
    .slice(1, 9)
    .map(Number)
    .reduce((a, b) => a + b, 0);
}

app.start({
  instanceName: "window-ram",
  css: `
    window { background: transparent; }
    label { font-family: monospace; font-size: 11px; color: #d3c6aa;
            background: rgba(0,0,0,0.6); border-radius: 5px; padding: 1px 6px; }
  `,
  main() {
    const hypr = AstalHyprland.get_default();
    const { TOP, RIGHT } = Astal.WindowAnchor;
    let text: Gtk.Label | null = null;

    const win = (
      <window
        name="window-ram"
        layer={Astal.Layer.OVERLAY}
        exclusivity={Astal.Exclusivity.IGNORE}
        anchor={TOP | RIGHT}
        application={app}
      >
        <label widthRequest={LABEL_WIDTH} $={(self) => (text = self)} />
      </window>
    ) as Astal.Window;

    win.connect("realize", () =>
      win.get_surface()?.set_input_region(new Cairo.Region()),
    );

    // Hyprland moves windows on a layout change without emitting an event,
    // and AstalHyprland keeps the stale geometry it cached on focus change.
    // Read the focused window from the compositor on every tick instead.
    type WindowState = {
      address: string;
      at: [number, number];
      size: [number, number];
      monitor: number;
      fullscreen: number;
      pid: number;
    };

    const focused = (): WindowState | null => {
      try {
        const state = JSON.parse(hypr.message("j/activewindow")) as WindowState;
        return typeof state.address === "string" &&
          Array.isArray(state.at) &&
          Array.isArray(state.size) &&
          typeof state.monitor === "number" &&
          typeof state.pid === "number" &&
          typeof state.fullscreen === "number"
          ? state
          : null;
      } catch {
        return null;
      }
    };

    // The connector name changes only when the window moves to another
    // monitor, so scan Gdk once per name instead of on every tick.
    let gdkMonitor: Gdk.Monitor | null = null;
    let gdkMonitorName: string | null = null;
    const monitorFor = (name: string): Gdk.Monitor | null => {
      if (name === gdkMonitorName) return gdkMonitor;
      gdkMonitorName = name;
      gdkMonitor = null;
      const monitors = Gdk.Display.get_default()?.get_monitors();
      if (!monitors) return null;
      for (let i = 0; i < monitors.get_n_items(); i++) {
        const candidate = monitors.get_item(i) as Gdk.Monitor;
        if (candidate.get_connector() === name) {
          gdkMonitor = candidate;
          break;
        }
      }
      return gdkMonitor;
    };

    const place = () => {
      const state = focused();
      if (
        state === null ||
        state.fullscreen !== AstalHyprland.Fullscreen.NONE
      ) {
        win.visible = false;
        return;
      }
      const monitor =
        state.monitor >= 0
          ? hypr.get_monitor(state.monitor)
          : hypr.get_focused_monitor();
      const gdkMonitors = Gdk.Display.get_default()?.get_monitors();
      if (gdkMonitors) {
        for (let i = 0; i < gdkMonitors.get_n_items(); i++) {
          const candidate = gdkMonitors.get_item(i) as Gdk.Monitor;
          if (candidate.get_connector() === monitor.get_name()) {
            if (win.gdkmonitor !== candidate) win.gdkmonitor = candidate;
            break;
          }
        }
      }
      const geometry = win.gdkmonitor?.get_geometry();
      const monitorX = geometry?.x ?? monitor.get_x();
      const monitorY = geometry?.y ?? monitor.get_y();
      const monitorWidth = geometry?.width ?? monitor.get_width();
      win.marginTop = state.at[1] - monitorY + INSET;
      win.marginRight =
        monitorX + monitorWidth - (state.at[0] + state.size[0]) + INSET;
      win.visible = true;
    };

    // CPU share needs two samples of the same process tree.
    let previous: { root: number; tree: number; total: number } | null = null;
    const measure = async () => {
      const state = focused();
      if (state === null) return;
      const root = state.pid;
      const ps = await execAsync(["ps", "-eo", "pid=,ppid=,rss="]);
      const { pids, rssKb } = processTree(ps, root);
      const sample = {
        root,
        tree: pids.map(processTicks).reduce((a, b) => a + b, 0),
        total: totalTicks(),
      };
      const cpu =
        previous !== null &&
        previous.root === root &&
        sample.total > previous.total
          ? `${((100 * Math.max(0, sample.tree - previous.tree)) / (sample.total - previous.total)).toFixed(0)}%`
          : "…";
      previous = sample;
      text!.label = `${(rssKb / 1024 / 1024).toFixed(1)}GB ${cpu}`;
    };
    hypr.connect("notify::focused-client", () => {
      place();
      void measure();
    });
    interval(100, place);
    interval(POLL_MS, () => void measure());
    place();
  },
});
