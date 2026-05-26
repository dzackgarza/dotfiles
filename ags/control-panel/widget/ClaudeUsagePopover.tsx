import type { Accessor } from "ags";
import { For } from "ags";
import { Astal, Gdk, Gtk } from "ags/gtk4";
import type { ProviderSnapshot, UsageCollection } from "../services/claude-usage-fetcher";

const ICON_SIZE = 16;

interface ClaudeUsagePopoverProps {
  visible: Accessor<boolean>;
  onVisibleChange: (visible: boolean) => void;
  claudeUsageData?: Accessor<UsageCollection>;
}

function QuotaSection({
  title,
  icon,
  percentage,
  resetsIn,
  color = "rgb(34, 197, 94)",
}: {
  title: string;
  icon: string;
  percentage: number;
  resetsIn: string;
  color?: string;
}) {
  return (
    <box class="popover-section" orientation={Gtk.Orientation.VERTICAL} spacing={8}>
      <box
        class="popover-quota-row"
        orientation={Gtk.Orientation.HORIZONTAL}
        spacing={12}
        halign={Gtk.Align.FILL}
      >
        <image
          class="popover-quota-icon"
          iconName={icon}
          pixelSize={ICON_SIZE}
          valign={Gtk.Align.CENTER}
        />
        <label class="popover-quota-label" xalign={0} label={title} hexpand />
        <label class="popover-quota-value" xalign={1} label={`${percentage}%`} />
      </box>
      <Gtk.ProgressBar
        class={`popover-progress ${
          color === "rgb(239, 68, 68)"
            ? "popover-progress-red"
            : color === "rgb(250, 204, 21)"
              ? "popover-progress-yellow"
              : "popover-progress-green"
        }`}
        fraction={Math.min(Math.max(percentage / 100, 0), 1)}
        hexpand
        halign={Gtk.Align.FILL}
      />
      <label class="popover-resets-text" xalign={0} label={resetsIn} />
    </box>
  );
}

export function ClaudeUsagePopover({
  visible,
  onVisibleChange,
  claudeUsageData,
}: ClaudeUsagePopoverProps) {
  const { TOP, RIGHT, LEFT, BOTTOM } = Astal.WindowAnchor;

  const backdrop = (
    <box
      class="popover-backdrop"
      hexpand
      vexpand
      canTarget
      halign={Gtk.Align.FILL}
      valign={Gtk.Align.FILL}
    />
  ) as Gtk.Box;

  const click = Gtk.GestureClick.new();
  click.set_button(0);
  click.set_propagation_phase(Gtk.PropagationPhase.CAPTURE);
  click.connect("pressed", () => {
    if (visible.peek()) {
      onVisibleChange(false);
    }
  });
  backdrop.add_controller(click);

  const popoverContent = (
    <box class="popover-root" orientation={Gtk.Orientation.VERTICAL} spacing={0}>
      <Gtk.ScrolledWindow
        class="popover-scroller"
        hscrollbarPolicy={Gtk.PolicyType.NEVER}
        vscrollbarPolicy={Gtk.PolicyType.AUTOMATIC}
        vexpand
        hexpand
      >
        <box orientation={Gtk.Orientation.VERTICAL} spacing={0}>
          {claudeUsageData ? (
            <For each={claudeUsageData((data) => data.providers)}>
              {(provider: ProviderSnapshot) => (
                <box orientation={Gtk.Orientation.VERTICAL} spacing={0}>
                  <label class="popover-title" xalign={0} label={provider.display_name} />
                  <box class="popover-divider" />
                  {provider.errors?.length ? (
                    <box class="popover-section" orientation={Gtk.Orientation.VERTICAL} spacing={8}>
                      <label
                        class="popover-resets-text"
                        xalign={0}
                        label={provider.errors[0].message || "Failed to fetch usage"}
                      />
                    </box>
                  ) : (
                    <box orientation={Gtk.Orientation.VERTICAL} spacing={0}>
                      {provider.rows.map((row) => {
                        const isShortTerm =
                          row.identifier.toLowerCase().includes("5h") ||
                          row.identifier.toLowerCase().includes("hour");
                        const icon = isShortTerm
                          ? "xsi-alarm-symbolic"
                          : "xsi-x-office-calendar-symbolic";

                        let color = "rgb(34, 197, 94)"; // green
                        if (row.pct_used >= 80) {
                          color = "rgb(239, 68, 68)"; // red
                        } else if (row.pct_used >= 50) {
                          color = "rgb(250, 204, 21)"; // yellow
                        }

                        return (
                          <QuotaSection
                            title={row.identifier}
                            icon={icon}
                            percentage={row.pct_used}
                            resetsIn={
                              row.time_until_reset
                                ? `Resets ${row.time_until_reset}`
                                : "Resets at unknown time"
                            }
                            color={color}
                          />
                        );
                      })}
                    </box>
                  )}
                  <box class="popover-divider" />
                </box>
              )}
            </For>
          ) : (
            <label class="popover-title" xalign={0} label="Loading..." />
          )}
        </box>
      </Gtk.ScrolledWindow>

      {/* Footer */}
      <box
        class="popover-footer-row"
        orientation={Gtk.Orientation.HORIZONTAL}
        spacing={12}
        halign={Gtk.Align.FILL}
      >
        <label class="popover-updated-text" xalign={0} label="Updated 0 sec ago" hexpand />
        <button class="popover-refresh-btn" onClicked={() => console.log("Refresh clicked")}>
          <image iconName="view-refresh-symbolic" pixelSize={14} />
        </button>
      </box>
    </box>
  );

  return (
    <window
      name="claude-usage-popover"
      title="Usage Limits Popover"
      class="ClaudeUsagePopover"
      visible={visible}
      $={(self: Gtk.Window) => {
        const monitor = Gdk.Display.get_default()?.get_monitors().get_item(0) as Gdk.Monitor | null;
        const screenHeight = monitor?.get_geometry().height ?? 1080;
        const popoverHeight = Math.floor((screenHeight * 2) / 3);
        self.set_default_size(500, popoverHeight);

        const bindEscapeToggle = (widget: Gtk.Widget) => {
          const key = Gtk.EventControllerKey.new();
          key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE);
          key.connect("key-pressed", (_: Gtk.EventControllerKey, keyval: number) => {
            if (keyval !== 65307) return false; // Escape key code
            if (self.visible) onVisibleChange(false);
            return true;
          });
          widget.add_controller(key);
        };

        bindEscapeToggle(self);

        const catcher = new Astal.Window({
          name: "claude-usage-popover-catcher",
          visible: false,
          anchor: TOP | RIGHT | LEFT | BOTTOM,
          layer: Astal.Layer.TOP,
          keymode: Astal.Keymode.ON_DEMAND,
          exclusivity: Astal.Exclusivity.IGNORE,
          child: backdrop,
        });

        bindEscapeToggle(catcher);
        catcher.add_css_class("ClaudeUsagePopover");

        self.connect("notify::visible", () => {
          catcher.visible = visible.peek();
        });
        self.connect("destroy", () => catcher.destroy());
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
  );
}
