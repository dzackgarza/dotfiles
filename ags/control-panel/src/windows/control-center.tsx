import type { Accessor } from "ags"
import { createState, For } from "ags"
import app from "ags/gtk4/app"
import { Astal, Gdk, Gtk } from "ags/gtk4"
import { createLogger } from "../lib/logger"
import { ClaudeUsagePopover } from "../../widget/ClaudeUsagePopover"
import {
  getControlCenterService,
  type InfoTileState,
  type PowerProfile,
  type PowerProfileState,
  type SliderState,
  type ToggleTileState,
  type UsageTileState,
} from "../services/control-center"
import type {
  ProviderSnapshot,
  UsageCollection,
} from "../../services/claude-usage-fetcher"
import { ToggleTile } from "../components/ToggleTile"
import { UsageTile } from "../components/UsageTile"
import { InfoTile } from "../components/InfoTile"
import { PowerProfileTile } from "../components/PowerProfileTile"
import { SliderRow } from "../components/SliderRow"
import { StatusLine } from "../components/StatusLine"
import { formatRelative } from "../../lib/utils"

// Icon size constants (matches _tokens.scss)
const ICON_SIZE = {
  status: 12,
  tile: 22,
  tileAction: 18,
  slider: 18,
  statusMain: 20,
  statusAction: 16,
} as const

function joinClasses(
  ...classes: Array<string | false | null | undefined>
): string {
  return classes.filter((value) => Boolean(value)).join(" ")
}

const PROVIDER_ICONS: Record<string, string> = {
  antigravity: "antigravity-symbolic",
  claude: "claude-ai-symbolic",
  codex: "codex-symbolic",
  copilot: "copilot-symbolic",
  cursor: "cursor-symbolic",
  kiro: "kiro-symbolic",
  ollama: "ollama-symbolic",
  opencode: "opencode-symbolic",
  "opencode-go": "opencode-symbolic",
  "opencode-zen": "opencode-symbolic",
  qoder: "qoder-symbolic",
  trae: "trae-symbolic",
  windsurf: "windsurf-symbolic",
}

type ProviderAvail = "ok" | "rate_limited" | "unavailable"

function getProviderAvail(provider: ProviderSnapshot): ProviderAvail {
  if (provider.status === "rate_limited") return "rate_limited"
  if (provider.status === "error") return "unavailable"
  if (provider.availability.length > 0) {
    return provider.availability.some((m) => m.available_now)
      ? "ok"
      : "unavailable"
  }
  const anyOpen =
    provider.rows.length === 0 || provider.rows.some((r) => !r.is_exhausted)
  return anyOpen ? "ok" : "unavailable"
}

function providerEta(provider: ProviderSnapshot): string | null {
  const avail = provider.availability[0]
  if (!avail || avail.available_now || !avail.available_when) return null
  return formatRelative(new Date(avail.available_when))
}

function ProviderIcon({
  provider,
  onClicked,
}: {
  provider: ProviderSnapshot
  onClicked: () => void
}) {
  const iconName =
    PROVIDER_ICONS[provider.provider] ?? "xsi-help-browser-symbolic"
  const avail = getProviderAvail(provider)
  const eta = providerEta(provider)
  return (
    <button
      class="provider-icon-btn"
      onClicked={onClicked}
      tooltipText={
        provider.errors?.length
          ? `${provider.display_name}: ${provider.errors[0].message}`
          : provider.display_name
      }
    >
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={2}
        halign={Gtk.Align.CENTER}
      >
        <image iconName={iconName} pixelSize={24} halign={Gtk.Align.CENTER} />
        {avail === "ok" ? (
          <box
            class="provider-dot-ok"
            halign={Gtk.Align.CENTER}
            widthRequest={6}
            heightRequest={6}
          />
        ) : avail === "rate_limited" ? (
          <box
            class="provider-dot-unknown"
            halign={Gtk.Align.CENTER}
            widthRequest={6}
            heightRequest={6}
          />
        ) : (
          <label
            class="provider-eta"
            label={eta ?? "?"}
            halign={Gtk.Align.CENTER}
          />
        )}
      </box>
    </button>
  )
}

function AiProviderIcons({
  claudeUsageData,
  onClicked,
}: {
  claudeUsageData: Accessor<UsageCollection>
  onClicked: () => void
}) {
  return (
    <box
      class="provider-icons-row"
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={4}
      halign={Gtk.Align.CENTER}
    >
      <For each={claudeUsageData((d) => d.providers)}>
        {(provider: ProviderSnapshot) => (
          <ProviderIcon provider={provider} onClicked={onClicked} />
        )}
      </For>
    </box>
  )
}

export function ControlCenterWindow() {
  const logger = createLogger(["ags", "control-center"])
  const control = getControlCenterService()
  const [claudeUsagePopoverVisible, setClaudeUsagePopoverVisible] =
    createState(false)

  // Initialize all state synchronously before building UI
  logger.info`Initializing service [SERVICE]`
  void control.initializeService().then(() => {
    logger.info`Service initialized [SERVICE]`
  })

  // Start polling loops after window is created
  setTimeout(() => {
    logger.info`Starting polling service [POLLING]`
    control.startPollingService()
  }, 0)

  const { TOP, RIGHT, LEFT, BOTTOM } = Astal.WindowAnchor

  const tileRows: JSX.Element[][] = [
    [
      <ToggleTile
        iconOn="xsi-bluetooth-active-symbolic"
        iconOff="xsi-bluetooth-disabled-symbolic"
        state={control.bluetooth}
        onToggle={control.toggleBluetooth}
      />,
      <ToggleTile
        iconOn="xsi-network-wireless-signal-excellent-symbolic"
        iconOff="xsi-network-wireless-offline-symbolic"
        state={control.wifi}
        onToggle={control.toggleWifi}
      />,
    ],
    [
      <PowerProfileTile
        state={control.powerProfile}
        onSetProfile={control.setPowerProfile}
      />,
      <ToggleTile
        iconOn="xsi-weather-clear-night-symbolic"
        iconOff="xsi-weather-clear-symbolic"
        state={control.appearance}
        onToggle={control.toggleAppearance}
      />,
    ],
    [
      <ToggleTile
        iconOn="xsi-notifications-disabled-symbolic"
        iconOff="xsi-notifications-symbolic"
        state={control.silent}
        onToggle={control.toggleSilent}
      />,
      <ToggleTile
        iconOn="xsi-microphone-sensitivity-muted-symbolic"
        iconOff="xsi-audio-input-microphone-symbolic"
        state={control.mic}
        onToggle={control.toggleMic}
      />,
    ],
    [
      <InfoTile
        icon="xsi-software-update-available-symbolic"
        state={control.updates}
      />,
      <InfoTile
        icon="xsi-notifications-symbolic"
        state={control.notifications}
        onActivate={control.openNotificationCenter}
      />,
    ],
    [
      <UsageTile icon="xsi-cpu-symbolic" state={control.cpu} />,
      <UsageTile icon="ram-symbolic" state={control.memory} />,
    ],
    [
      <UsageTile icon="xsi-drive-harddisk-symbolic" state={control.disk} />,
      <box />,
    ],
  ]

  const panel = (
    <box class="nc-root" orientation={Gtk.Orientation.VERTICAL} spacing={12}>
      <box
        class="tile-grid"
        orientation={Gtk.Orientation.VERTICAL}
        spacing={12}
      >
        {tileRows.map((row) => (
          <box
            class="tile-row"
            orientation={Gtk.Orientation.HORIZONTAL}
            spacing={12}
            homogeneous
            hexpand
            halign={Gtk.Align.FILL}
          >
            <box
              class="tile-cell"
              hexpand
              widthRequest={200}
              halign={Gtk.Align.FILL}
            >
              {row[0]}
            </box>
            <box
              class="tile-cell"
              hexpand
              widthRequest={200}
              halign={Gtk.Align.FILL}
            >
              {row[1]}
            </box>
          </box>
        ))}
      </box>
      <AiProviderIcons
        claudeUsageData={control.claudeUsageData}
        onClicked={() => setClaudeUsagePopoverVisible(true)}
      />
      <SliderRow
        icon="xsi-audio-volume-high-symbolic"
        state={control.volume}
        onSetValue={control.setVolume}
      />
      <SliderRow
        icon="xsi-display-brightness-symbolic"
        state={control.brightness}
        onSetValue={control.setBrightness}
      />
      <box
        class={control.battery((value) =>
          joinClasses("status-row", value.error && "error"),
        )}
        orientation={Gtk.Orientation.HORIZONTAL}
        spacing={12}
        tooltipText={control.battery((value) => value.detail)}
      >
        <image
          class="status-icon"
          iconName={control.battery((value) => value.iconName)}
          pixelSize={ICON_SIZE.statusMain}
        />
        <box orientation={Gtk.Orientation.VERTICAL} hexpand>
          <StatusLine
            icon="battery-bolt-symbolic"
            text={control.battery((value) => value.percentText)}
          />
          <StatusLine
            icon="hourglass-symbolic"
            text={control.battery((value) => value.etaText)}
          />
          <StatusLine
            icon="wattage-symbolic"
            text={control.battery((value) => value.wattageText)}
          />
        </box>
        <box
          class="status-actions"
          orientation={Gtk.Orientation.HORIZONTAL}
          spacing={6}
          halign={Gtk.Align.END}
        >
          <button
            class="status-action"
            onClicked={() => void control.suspend()}
          >
            <image
              iconName="media-playback-pause-symbolic"
              pixelSize={ICON_SIZE.statusAction}
            />
          </button>
          <button
            class="status-action"
            onClicked={() => void control.hibernate()}
          >
            <image
              iconName="media-playback-stop-symbolic"
              pixelSize={ICON_SIZE.statusAction}
            />
          </button>
          <button
            class="status-action"
            onClicked={() => void control.poweroff()}
          >
            <image
              iconName="xsi-shutdown-symbolic"
              pixelSize={ICON_SIZE.statusAction}
            />
          </button>
        </box>
      </box>
      <label
        class="last-updated"
        xalign={0}
        label={control.lastUpdated((val) => val)}
      />
      <label
        class="action-error"
        xalign={0}
        visible={control.actionError((value) => value.length > 0)}
        label={control.actionError((val) => val)}
      />
    </box>
  )

  return (
    <>
      <ClaudeUsagePopover
        visible={claudeUsagePopoverVisible}
        onVisibleChange={setClaudeUsagePopoverVisible}
        claudeUsageData={control.claudeUsageData}
      />
      <window
        name="claude-usage"
        title="Usage Limits"
        class="NotificationCenter"
        application={app}
        visible={false}
        $={(self) => {
          const bindEscapeToggle = (widget: Gtk.Widget) => {
            const key = Gtk.EventControllerKey.new()
            key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            key.connect("key-pressed", (_, keyval) => {
              if (keyval !== Gdk.KEY_Escape) return false
              if (self.visible) self.visible = false
              return true
            })
            widget.add_controller(key)
          }

          bindEscapeToggle(self)

          const backdrop = (
            <box
              class="nc-backdrop"
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
            name: "claude-usage-catcher",
            application: app,
            visible: false,
            anchor: TOP | RIGHT | LEFT | BOTTOM,
            layer: Astal.Layer.TOP,
            keymode: Astal.Keymode.ON_DEMAND,
            exclusivity: Astal.Exclusivity.IGNORE,
            child: backdrop,
          })

          bindEscapeToggle(catcher)
          catcher.add_css_class("NotificationCenter")

          self.connect("notify::visible", () => {
            if (self.visible && !control.ready.peek()) {
              self.visible = false
              return
            }
            if (self.visible) control.refreshUsage()
            catcher.visible = self.visible
          })
          self.connect("destroy", () => catcher.destroy())
        }}
        anchor={TOP | RIGHT}
        marginTop={20}
        marginRight={20}
        layer={Astal.Layer.OVERLAY}
        keymode={Astal.Keymode.ON_DEMAND}
        exclusivity={Astal.Exclusivity.IGNORE}
      >
        {panel}
      </window>
    </>
  )
}
