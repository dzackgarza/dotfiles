import { createState } from "ags"
import { Astal, Gdk, Gtk } from "ags/gtk4"
import app from "ags/gtk4/app"
import { createBatteryHistoryService } from "../services/battery-history"

let setBatteryHistoryVisible: ((visible: boolean) => void) | null = null

export function toggleBatteryHistory() {
  setBatteryHistoryVisible?.(
    !(app.get_window("battery-history")?.visible ?? false),
  )
}

export function BatteryHistoryWindow() {
  const { TOP, RIGHT, LEFT, BOTTOM } = Astal.WindowAnchor
  const service = createBatteryHistoryService()
  const [visible, setVisible] = createState(false)
  const [range, setRange] = createState(3600)
  setBatteryHistoryVisible = (nextVisible) => {
    setVisible(nextVisible)
    if (nextVisible) void service.refresh(range.peek())
  }
  void service.refresh(3600)

  const monitor = Gdk.Display.get_default()
    ?.get_monitors()
    .get_item(0) as Gdk.Monitor | null
  const geometry = monitor?.get_geometry()
  const width = Math.min(900, Math.max(680, Math.floor((geometry?.width ?? 1920) * 0.42)))
  const height = Math.min(650, Math.max(440, Math.floor((geometry?.height ?? 1200) * 0.5)))

  const buttons = ([
    ["1h", 3600],
    ["3h", 10800],
    ["8h", 28800],
    ["1d", 86400],
  ] as const).map(([label, seconds]) => (
    <button
      class={range((value) => (value === seconds ? "battery-range active" : "battery-range"))}
      sensitive={range((value) => value !== seconds)}
      onClicked={() => {
        setRange(seconds)
        void service.refresh(seconds)
      }}
      label={label}
    />
  ))

  const content = (
    <box
      class="battery-panel"
      orientation={Gtk.Orientation.VERTICAL}
      spacing={0}
      widthRequest={width}
      heightRequest={height}
      halign={Gtk.Align.CENTER}
      valign={Gtk.Align.CENTER}
    >
      <box class="battery-controls" spacing={4} halign={Gtk.Align.CENTER}>
        {buttons}
      </box>
      <label
        class="battery-loading"
        label="Rendering battery history…"
        visible={service.state((state) => state.loading)}
        hexpand
        vexpand
      />
      <label
        class="battery-error"
        label={service.state((state) => state.error)}
        visible={service.state((state) => !state.loading && Boolean(state.error))}
        wrap
        hexpand
        vexpand
      />
      <image
        file={service.state((state) => state.imagePath)}
        visible={service.state((state) => !state.loading && !state.error)}
        class="battery-graph"
        hexpand
        vexpand
        halign={Gtk.Align.FILL}
        valign={Gtk.Align.FILL}
        widthRequest={width - 40}
        heightRequest={height - 90}
      />
    </box>
  )

  return (
    <window
      name="battery-history"
      title="Battery history"
      class="BatteryHistory"
      application={app}
      visible={visible}
      widthRequest={width}
      heightRequest={height}
      anchor={TOP | LEFT}
      marginTop={Math.max(0, Math.floor(((geometry?.height ?? 1200) - height) / 2))}
      marginLeft={Math.max(0, Math.floor(((geometry?.width ?? 1920) - width) / 2))}
      layer={Astal.Layer.OVERLAY}
      keymode={Astal.Keymode.ON_DEMAND}
      exclusivity={Astal.Exclusivity.IGNORE}
      $={(self: Gtk.Window) => {
        self.set_default_size(width, height)

        const key = Gtk.EventControllerKey.new()
        key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key.connect("key-pressed", (_controller, keyval) => {
          if (keyval !== Gdk.KEY_Escape) return false
          self.visible = false
          return true
        })
        self.add_controller(key)

        const backdrop = (
          <box
            class="BatteryHistoryCatcher"
            hexpand
            vexpand
            canTarget
            halign={Gtk.Align.FILL}
            valign={Gtk.Align.FILL}
          />
        ) as Gtk.Box
        const click = Gtk.GestureClick.new()
        click.set_button(0)
        click.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        click.connect("pressed", () => {
          if (self.visible) self.visible = false
        })
        backdrop.add_controller(click)

        const catcher = new Astal.Window({
          name: "battery-history-catcher",
          application: app,
          visible: false,
          anchor: TOP | RIGHT | LEFT | BOTTOM,
          layer: Astal.Layer.TOP,
          keymode: Astal.Keymode.ON_DEMAND,
          exclusivity: Astal.Exclusivity.IGNORE,
          child: backdrop,
        })
        catcher.add_css_class("BatteryHistoryCatcher")
        catcher.add_controller(
          (() => {
            const controller = Gtk.EventControllerKey.new()
            controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            controller.connect("key-pressed", (_c, keyval) => {
              if (keyval !== Gdk.KEY_Escape) return false
              self.visible = false
              return true
            })
            return controller
          })(),
        )

        self.connect("notify::visible", () => {
          catcher.visible = self.visible
        })
        self.connect("destroy", () => catcher.destroy())
      }}
    >
      {content}
    </window>
  )
}
