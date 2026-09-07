import type { Accessor } from "ags"
import { For } from "ags"
import { Astal, Gdk, Gtk } from "ags/gtk4"
import app from "ags/gtk4/app"

export interface RepoPlan {
  repo: string
  plan: string
  progress: number
}

export const MOCK_REPO_PLANS: RepoPlan[] = [
  { repo: "dzackgarza/dotfiles", plan: "control-center-v2", progress: 73 },
  { repo: "dzackgarza/notes", plan: "vault-audit", progress: 41 },
  { repo: "dzackgarza/ai-review-ci", plan: "gate-harness", progress: 92 },
  { repo: "dzackgarza/opencode", plan: "plan-42-refactor", progress: 18 },
  { repo: "dzackgarza/repo-plans", plan: "repo-panel-mock", progress: 56 },
]

function progressClass(pct: number): string {
  if (pct >= 80) return "repo-plan-progress-red"
  if (pct >= 50) return "repo-plan-progress-yellow"
  return "repo-plan-progress-green"
}

function RepoPlanRow({ entry }: { entry: RepoPlan }) {
  const pct = Math.round(Math.min(Math.max(entry.progress, 0), 100))
  const fraction = pct / 100

  return (
    <box
      class="repo-plan-row"
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={12}
      hexpand
      halign={Gtk.Align.FILL}
    >
      <image
        iconName="xsi-folder-symbolic"
        pixelSize={20}
        valign={Gtk.Align.CENTER}
        halign={Gtk.Align.CENTER}
        class="repo-plan-icon"
      />
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={2}
        hexpand
        halign={Gtk.Align.FILL}
        valign={Gtk.Align.CENTER}
      >
        <label
          class="repo-plan-repo"
          xalign={0}
          ellipsize={3}
          maxWidthChars={28}
          label={entry.repo}
        />
        <label
          class="repo-plan-plan"
          xalign={0}
          ellipsize={3}
          maxWidthChars={28}
          label={entry.plan}
        />
      </box>
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={4}
        widthRequest={140}
        halign={Gtk.Align.FILL}
        valign={Gtk.Align.CENTER}
      >
        <box
          orientation={Gtk.Orientation.HORIZONTAL}
          halign={Gtk.Align.FILL}
          hexpand
        >
          <label
            class="repo-plan-progress-label"
            xalign={0}
            label="progress"
            hexpand
          />
          <label
            class="repo-plan-progress-value"
            xalign={1}
            label={`${pct}%`}
          />
        </box>
        <Gtk.ProgressBar
          class={`repo-plan-progress ${progressClass(pct)}`}
          fraction={fraction}
          hexpand
          halign={Gtk.Align.FILL}
        />
      </box>
    </box>
  )
}

type RepoPlanPanelProps = {
  items?: RepoPlan[] | Accessor<RepoPlan[]>
  title?: string
}

export function RepoPlanPanel({
  items,
  title = "Repo Plans",
}: RepoPlanPanelProps) {
  const isAccessor = typeof items === "function"
  const staticItems = (items as RepoPlan[] | undefined) ?? MOCK_REPO_PLANS
  const accessorItems = items as Accessor<RepoPlan[]> | undefined

  return (
    <box
      class="repo-plan-panel"
      orientation={Gtk.Orientation.VERTICAL}
      spacing={0}
    >
      <box
        class="repo-plan-header"
        orientation={Gtk.Orientation.HORIZONTAL}
        spacing={8}
        halign={Gtk.Align.FILL}
      >
        <label class="repo-plan-title" xalign={0} label={title} hexpand />
        <label
          class="repo-plan-count"
          xalign={1}
          label={
            isAccessor && accessorItems
              ? accessorItems((v) => `${v.length} repos`)
              : `${staticItems.length} repos`
          }
        />
      </box>
      <box class="repo-plan-divider" />
      <box orientation={Gtk.Orientation.VERTICAL} spacing={8}>
        {isAccessor && accessorItems ? (
          <For each={accessorItems}>
            {(entry: RepoPlan) => <RepoPlanRow entry={entry} />}
          </For>
        ) : (
          staticItems.map((entry) => <RepoPlanRow entry={entry} />)
        )}
      </box>
    </box>
  )
}

export function RepoPlanPanelMockWindow() {
  const { TOP, RIGHT } = Astal.WindowAnchor
  return (
    <window
      name="repo-plan-panel-mock"
      title="Repo Plans Mock"
      class="RepoPlanPanelMock"
      application={app}
      visible
      anchor={TOP | RIGHT}
      marginTop={20}
      marginRight={20}
      layer={Astal.Layer.OVERLAY}
      keymode={Astal.Keymode.ON_DEMAND}
      exclusivity={Astal.Exclusivity.IGNORE}
      $={(self: Gtk.Window) => {
        const key = Gtk.EventControllerKey.new()
        key.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key.connect(
          "key-pressed",
          (_: Gtk.EventControllerKey, keyval: number) => {
            if (keyval !== Gdk.KEY_Escape) return false
            self.visible = false
            return true
          },
        )
        self.add_controller(key)
      }}
    >
      <box class="repo-plan-window-root">
        <RepoPlanPanel items={MOCK_REPO_PLANS} />
      </box>
    </window>
  )
}
