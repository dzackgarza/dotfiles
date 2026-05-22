import type { Accessor } from "ags"
import { Astal, Gtk } from "ags/gtk4"

const ICON_SIZE = 16

interface ClaudeUsageData {
  fiveHourUtilization: number
  fiveHourResetAt: string
  sevenDayUtilization: number
  sevenDayResetAt: string
  sevenDayOpusUtilization?: number
}

interface ClaudeUsagePopoverProps {
  visible: Accessor<boolean>
  onVisibleChange: (visible: boolean) => void
  claudeUsageData?: Accessor<ClaudeUsageData>
}

function QuotaSection({
  title,
  icon,
  percentage,
  resetsIn,
  color = "rgb(34, 197, 94)",
}: {
  title: string
  icon: string
  percentage: Accessor<number> | number
  resetsIn: Accessor<string> | string
  color?: string
}) {
  const isAccessor = (val: any): val is Accessor<number> => typeof val === "function"
  const isAccessorStr = (val: any): val is Accessor<string> => typeof val === "function"
  
  return (
    <box class="popover-section" orientation={Gtk.Orientation.VERTICAL} spacing={8}>
      <box class="popover-quota-row" orientation={Gtk.Orientation.HORIZONTAL} spacing={12} halign={Gtk.Align.FILL}>
        <image class="popover-quota-icon" iconName={icon} pixelSize={ICON_SIZE} valign={Gtk.Align.CENTER} />
        <label class="popover-quota-label" xalign={0} label={title} hexpand />
        <label class="popover-quota-value" xalign={1} label={isAccessor(percentage) ? percentage((p) => `${p}%`) : `${percentage}%`} />
      </box>
      <Gtk.ProgressBar
        class={`popover-progress ${color === "rgb(34, 197, 94)" ? "popover-progress-green" : "popover-progress-yellow"}`}
        fraction={isAccessor(percentage) ? percentage((p) => p / 100) : percentage / 100}
        hexpand
        halign={Gtk.Align.FILL}
      />
      <label class="popover-resets-text" xalign={0} label={isAccessorStr(resetsIn) ? resetsIn : resetsIn} />
    </box>
  )
}

function AmountSection({
  title,
  icon,
  amount,
  replenishRate,
  usagePercent,
}: {
  title: string
  icon: string
  amount: string
  replenishRate: string
  usagePercent: number
}) {
  return (
    <box class="popover-section" orientation={Gtk.Orientation.VERTICAL} spacing={8}>
      <box class="popover-quota-row" orientation={Gtk.Orientation.HORIZONTAL} spacing={12} halign={Gtk.Align.FILL}>
        <image class="popover-quota-icon" iconName={icon} pixelSize={ICON_SIZE} valign={Gtk.Align.CENTER} />
        <label class="popover-quota-label" xalign={0} label={title} hexpand />
        <label class="popover-quota-value" xalign={1} label={amount} />
      </box>
      <Gtk.ProgressBar
        class="popover-progress popover-progress-green"
        fraction={usagePercent / 100}
        hexpand
        halign={Gtk.Align.FILL}
      />
      <label class="popover-resets-text" xalign={0} label={replenishRate} />
    </box>
  )
}

function formatResetTime(dateString: string): string {
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = date.getTime() - now.getTime()
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
    return `Resets in ${diffHours}h ${diffMinutes}m`
  } catch {
    return "Resets at unknown time"
  }
}

export function ClaudeUsagePopover({ visible, onVisibleChange, claudeUsageData }: ClaudeUsagePopoverProps) {
  const { TOP, RIGHT, LEFT, BOTTOM } = Astal.WindowAnchor

  const backdrop = (
    <box
      class="popover-backdrop"
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
    if (visible.peek()) {
      onVisibleChange(false)
    }
  })
  backdrop.add_controller(click)

  const popoverContent = (
    <box class="popover-root" orientation={Gtk.Orientation.VERTICAL} spacing={0}>
      {/* Claude Usage Header */}
      <label class="popover-title" xalign={0} label="Claude Usage" />

      <box class="popover-divider" />

      {/* 5-Hour Window Section */}
      <QuotaSection
        title="5-Hour Window"
        icon="xsi-alarm-symbolic"
        percentage={claudeUsageData ? claudeUsageData((data) => data.fiveHourUtilization) : (() => 0)()}
        resetsIn={claudeUsageData ? claudeUsageData((data) => formatResetTime(data.fiveHourResetAt)) : (() => "Loading...")()}
        color="rgb(34, 197, 94)"
      />

      {/* Weekly Section */}
      <QuotaSection
        title="7-Day"
        icon="xsi-x-office-calendar-symbolic"
        percentage={claudeUsageData ? claudeUsageData((data) => data.sevenDayUtilization) : (() => 0)()}
        resetsIn={claudeUsageData ? claudeUsageData((data) => formatResetTime(data.sevenDayResetAt)) : (() => "Loading...")()}
        color="rgb(250, 204, 21)"
      />

      <box class="popover-divider" />

      {/* Codex Usage Header */}
      <label class="popover-title" xalign={0} label="Codex Usage" />

      <box class="popover-divider" />

      {/* 5-Hour Window Section */}
      <QuotaSection
        title="5-Hour Window"
        icon="xsi-alarm-symbolic"
        percentage={35}
        resetsIn="Resets in 4h 54m"
        color="rgb(34, 197, 94)"
      />

      {/* Weekly Section */}
      <QuotaSection
        title="7-Day"
        icon="xsi-x-office-calendar-symbolic"
        percentage={62}
        resetsIn="Resets Mon 2:59 PM"
        color="rgb(250, 204, 21)"
      />

      <box class="popover-divider" />

      {/* Amp Usage Header */}
      <label class="popover-title" xalign={0} label="Amp Usage" />

      <box class="popover-divider" />

      {/* Amp Balance Section */}
      <AmountSection
        title="Balance"
        icon="xsi-x-office-calendar-symbolic"
        amount="$9.03"
        replenishRate="Replenishes +$0.42/hour"
        usagePercent={9.7}
      />

      <box class="popover-divider" />

      {/* Footer */}
      <box class="popover-footer-row" orientation={Gtk.Orientation.HORIZONTAL} spacing={12} halign={Gtk.Align.FILL}>
        <label class="popover-updated-text" xalign={0} label="Updated 0 sec ago" hexpand />
         <button class="popover-refresh-btn" onClicked={() => console.log("Refresh clicked")}>
          <image iconName="view-refresh-symbolic" pixelSize={14} />
        </button>
      </box>
    </box>
  )

  return (
    <window
      name="claude-usage-popover"
      class="ClaudeUsagePopover"
      visible={visible}
      $={(self) => {
        const bindEscapeToggle = (widget: Gtk.Widget) => {
          const key = Gtk.EventControllerKey.new()
          key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
          key.connect("key-pressed", (_, keyval) => {
            if (keyval !== 65307) return false // Escape key code
            if (self.visible) onVisibleChange(false)
            return true
          })
          widget.add_controller(key)
        }

        bindEscapeToggle(self)

        const catcher = new Astal.Window({
          name: "claude-usage-popover-catcher",
          visible: false,
          anchor: TOP | RIGHT | LEFT | BOTTOM,
          layer: Astal.Layer.TOP,
          keymode: Astal.Keymode.ON_DEMAND,
          exclusivity: Astal.Exclusivity.IGNORE,
          child: backdrop,
        })

        bindEscapeToggle(catcher)
        catcher.add_css_class("ClaudeUsagePopover")

        self.connect("notify::visible", () => {
          catcher.visible = visible.peek()
        })
        self.connect("destroy", () => catcher.destroy())
      }}
      anchor={TOP | LEFT}
      marginTop={70}
      marginLeft={150}
      layer={Astal.Layer.OVERLAY}
      keymode={Astal.Keymode.ON_DEMAND}
      exclusivity={Astal.Exclusivity.IGNORE}
    >
      {popoverContent}
    </window>
  )
}
