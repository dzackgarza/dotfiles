import type { Accessor } from "ags"
import { createState, For } from "ags"
import { Astal, Gdk, Gtk } from "ags/gtk4"
import app from "ags/gtk4/app"
import { execAsync } from "ags/process"
import GLib from "gi://GLib?version=2.0"

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

function getRepoPath(repo: string): string {
  const short = repo.split("/").pop() ?? repo
  const home = GLib.get_home_dir()
  if (short === "dotfiles") return `${home}/dotfiles`
  if (short === "notes") return `${home}/notes`
  if (short === "ai-review-ci") return `${home}/ai-review-ci`
  const candidates = [
    `${home}/${short}`,
    `${home}/gitclones/${short}`,
    `${home}/dotfiles`,
    home,
  ]
  for (const p of candidates) {
    try {
      if (GLib.file_test(p, GLib.FileTest.IS_DIR)) return p
    } catch {}
  }
  return `${home}/${short}`
}

async function fetchIssueCount(repo: string): Promise<number> {
  // Try repos open_issues_count first (single call, includes PRs but fast)
  try {
    const out = await execAsync([
      "gh",
      "api",
      `repos/${repo}`,
      "--jq",
      ".open_issues_count",
    ])
    const n = parseInt(out.trim(), 10)
    if (!Number.isNaN(n)) return n
  } catch {}
  // Fallback to search total_count (issues only)
  try {
    const out = await execAsync([
      "gh",
      "api",
      `search/issues?q=repo:${repo}+type:issue+state:open`,
      "--jq",
      ".total_count",
    ])
    const n = parseInt(out.trim(), 10)
    if (!Number.isNaN(n)) return n
  } catch {}
  return 0
}

function progressClass(pct: number): string {
  if (pct >= 80) return "repo-plan-progress-red"
  if (pct >= 50) return "repo-plan-progress-yellow"
  return "repo-plan-progress-green"
}

function closeControlCenter() {
  try {
    const w = (
      app as unknown as { get_window?: (n: string) => Gtk.Window | null }
    ).get_window?.("claude-usage")
    if (w) {
      w.visible = false
      return
    }
  } catch {}
  try {
    const wins = (
      app as unknown as { get_windows?: () => Gtk.Window[] }
    ).get_windows?.()
    const target = wins?.find(
      (win) => (win as unknown as { name?: string }).name === "claude-usage",
    )
    if (target) {
      target.visible = false
      return
    }
  } catch {}
  void execAsync(["ags", "toggle", "claude-usage"]).catch(() => {})
}

function RepoPlanRow({
  entry,
  issueCount,
}: {
  entry: RepoPlan
  issueCount?: Accessor<number>
}) {
  const pct = Math.round(Math.min(Math.max(entry.progress, 0), 100))
  const fraction = pct / 100
  const repoPath = getRepoPath(entry.repo)

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
        <box
          orientation={Gtk.Orientation.HORIZONTAL}
          spacing={6}
          hexpand
          halign={Gtk.Align.FILL}
          valign={Gtk.Align.CENTER}
        >
          <button
            class="repo-plan-repo-btn"
            tooltipText={`Open ${repoPath} in kitty`}
            hexpand
            halign={Gtk.Align.FILL}
            onClicked={() => {
              closeControlCenter()
              void execAsync(["kitty", "-d", repoPath]).catch((e) =>
                console.error(`kitty -d ${repoPath} failed: ${String(e)}`),
              )
            }}
          >
            <label
              class="repo-plan-repo"
              xalign={0}
              ellipsize={3}
              maxWidthChars={24}
              label={entry.repo}
            />
          </button>
          <box
            orientation={Gtk.Orientation.HORIZONTAL}
            spacing={2}
            halign={Gtk.Align.END}
            valign={Gtk.Align.CENTER}
          >
            <button
              class="repo-launcher-btn"
              tooltipText={`Open https://github.com/${entry.repo}`}
              onClicked={() => {
                closeControlCenter()
                void execAsync([
                  "xdg-open",
                  `https://github.com/${entry.repo}`,
                ]).catch((e) => console.error(`xdg-open failed: ${String(e)}`))
              }}
            >
              <image iconName="xsi-github-symbolic" pixelSize={16} />
            </button>
            <button
              class="repo-launcher-btn"
              tooltipText={`Open claude --dangerously-skip-permissions in ${repoPath}`}
              onClicked={() => {
                closeControlCenter()
                void execAsync([
                  "kitty",
                  "-d",
                  repoPath,
                  "claude",
                  "--dangerously-skip-permissions",
                ]).catch((e) =>
                  console.error(`kitty claude failed: ${String(e)}`),
                )
              }}
            >
              <image iconName="claude-ai-symbolic" pixelSize={16} />
            </button>
            <button
              class="repo-launcher-btn"
              tooltipText={`Open codex --yolo --search in ${repoPath}`}
              onClicked={() => {
                closeControlCenter()
                void execAsync([
                  "kitty",
                  "-d",
                  repoPath,
                  "codex",
                  "--yolo",
                  "--search",
                ]).catch((e) =>
                  console.error(`kitty codex failed: ${String(e)}`),
                )
              }}
            >
              <image iconName="openai-symbolic" pixelSize={16} />
            </button>
            <button
              class="repo-launcher-btn"
              tooltipText={`Open opencode in ${repoPath}`}
              onClicked={() => {
                closeControlCenter()
                void execAsync(["kitty", "-d", repoPath, "opencode"]).catch(
                  (e) => console.error(`kitty opencode failed: ${String(e)}`),
                )
              }}
            >
              <image iconName="opencode-symbolic" pixelSize={16} />
            </button>
          </box>
        </box>
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

  const [issueCounts, setIssueCounts] = createState<Record<string, number>>({})

  const fetchAll = async (repos: string[]) => {
    try {
      const results = await Promise.all(
        repos.map(async (repo) => {
          const n = await fetchIssueCount(repo)
          return [repo, n] as const
        }),
      )
      const next: Record<string, number> = {}
      for (const [repo, n] of results) next[repo] = n
      setIssueCounts(next)
    } catch (e) {
      console.error(`fetch issue counts failed: ${String(e)}`)
    }
  }

  // Initial batch fetch
  setTimeout(() => {
    const repos = isAccessor
      ? (() => {
          try {
            const peeked = (
              accessorItems as unknown as { peek?: () => RepoPlan[] }
            )?.peek?.()
            if (peeked && Array.isArray(peeked))
              return peeked.map((r) => r.repo)
          } catch {}
          return staticItems.map((r) => r.repo)
        })()
      : staticItems.map((r) => r.repo)
    void fetchAll(repos)
  }, 300)

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
            {(entry: RepoPlan) => (
              <RepoPlanRow
                entry={entry}
                issueCount={issueCounts((m) => m[entry.repo] ?? 0)}
              />
            )}
          </For>
        ) : (
          staticItems.map((entry) => (
            <RepoPlanRow
              entry={entry}
              issueCount={issueCounts((m) => m[entry.repo] ?? 0)}
            />
          ))
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
