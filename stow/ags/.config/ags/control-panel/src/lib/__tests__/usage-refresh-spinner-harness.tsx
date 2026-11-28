import app from "ags/gtk4/app"
import { Gtk } from "ags/gtk4"
import { ControlCenterWindow } from "../../windows/control-center"
import { getControlCenterService } from "../../services/control-center"
import { initializeLogger } from "../logger"
import style from "../../../style.scss"

initializeLogger()

function spinners(root: Gtk.Widget): Array<Record<string, boolean | number>> {
  const found: Array<Record<string, boolean | number>> = []
  let child = root.get_first_child()
  while (child !== null) {
    if (child instanceof Gtk.Spinner) {
      found.push({
        visible: child.visible,
        spinning: child.spinning,
        width: child.get_width(),
        height: child.get_height(),
      })
    }
    found.push(...spinners(child))
    child = child.get_next_sibling()
  }
  return found
}

app.start({
  instanceName: "control-spinner-visual",
  css: style,
  icons: "/home/dzack/dotfiles/stow/ags/.config/ags/control-panel/icons",
  requestHandler(argv, response) {
    const control = getControlCenterService()
    const window = app.get_window("claude-usage")
    const [command] = argv
    const snapshot = () =>
      JSON.stringify({
        command,
        ready: control.ready.peek(),
        loading: control.usageLoading.peek(),
        windowVisible: window?.visible,
        spinners: window ? spinners(window) : [],
      })
    if (command === "show" && window) window.visible = true
    if (command === "refresh") control.refreshUsage()
    if (window) {
      window.add_tick_callback(() => {
        response(snapshot())
        return false
      })
      return
    }
    response(snapshot())
  },
  main() {
    return <ControlCenterWindow />
  },
})
