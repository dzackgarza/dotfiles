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

const REPO_MAP_PATH = `${GLib.get_home_dir()}/dotfiles/ags/control-panel/repo-map.json`

async function loadRepoMap(): Promise<Record<string, string>> {
  try {
    const out = await execAsync(["cat", REPO_MAP_PATH])
    const parsed = JSON.parse(out) as Record<string, string>
    return parsed
  } catch {
    return {}
  }
}

async function fetchLiveRepoPlans(): Promise<RepoPlan[]> {
  const map = await loadRepoMap()
  try {
    const out = await execAsync([
      "gh",
      "repo",
      "list",
      "dzackgarza",
      "--limit",
      "200",
      "--json",
      "nameWithOwner,pushedAt",
    ])
    const arr = JSON.parse(out) as { nameWithOwner: string; pushedAt: string }[]
    // Sort by latest pushes (pushedAt descending) — gh list has no --sort flag, so sort here
    arr.sort((a, b) => {
      const ta = a.pushedAt ? new Date(a.pushedAt).getTime() : 0
      const tb = b.pushedAt ? new Date(b.pushedAt).getTime() : 0
      return tb - ta
    })
    // Filter to past 14 days only
    const cutoff = Date.now() - 14 * 24 * 60 * 60 * 1000
    const recent = arr.filter((r) => {
      if (!r.pushedAt) return false
      const t = new Date(r.pushedAt).getTime()
      return t >= cutoff
    })
    return recent.map((r) => {
      const local = map[r.nameWithOwner]
      const hasLocal = !!local && local !== "None"
      return {
        repo: r.nameWithOwner,
        plan: hasLocal ? (local as string) : "No local checkout",
        progress: hasLocal ? 78 : 12,
      }
    })
  } catch (e) {
    console.error(`fetchLiveRepoPlans failed: ${String(e)}`)
    // fallback to map-driven mock with checkout lookup
    const fallback: RepoPlan[] = MOCK_REPO_PLANS.map((r) => {
      const local = map[r.repo]
      const hasLocal = !!local && local !== "None"
      return {
        repo: r.repo,
        plan: hasLocal ? (local as string) : "No local checkout",
        progress: hasLocal ? r.progress : 12,
      }
    })
    return fallback
  }
}

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

function getLocalPathFromPlan(plan: string): string | null {
  if (plan === "No local checkout") return null
  // plan is either original mock plan name or absolute path
  // Heuristic: if starts with / then it's a path
  if (plan.startsWith("/")) return plan
  return null
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
  hideProgress,
}: {
  entry: RepoPlan
  issueCount?: Accessor<number>
  hideProgress?: boolean
}) {
  const pct = Math.round(Math.min(Math.max(entry.progress, 0), 100))
  const fraction = pct / 100
  const isMissing = entry.plan === "No local checkout"
  const localPath = getLocalPathFromPlan(entry.plan)
  const repoPath = isMissing ? "" : (localPath ?? getRepoPath(entry.repo))
  const hasLocal = !isMissing

  return (
    <box
      class="repo-plan-row"
      orientation={Gtk.Orientation.HORIZONTAL}
      spacing={10}
      hexpand
      halign={Gtk.Align.FILL}
    >
      <button
        class={
          isMissing
            ? "repo-folder-btn repo-folder-btn-missing"
            : "repo-folder-btn"
        }
        tooltipText={
          hasLocal ? `Open ${repoPath} in file manager` : "No local checkout"
        }
        sensitive={hasLocal}
        onClicked={() => {
          if (!hasLocal) return
          closeControlCenter()
          void execAsync(["xdg-open", repoPath]).catch((e) =>
            console.error(`xdg-open folder failed: ${String(e)}`),
          )
        }}
      >
        <image
          iconName="xsi-folder-symbolic"
          pixelSize={18}
          valign={Gtk.Align.CENTER}
          halign={Gtk.Align.CENTER}
          class="repo-plan-icon"
        />
      </button>
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={4}
        hexpand
        halign={Gtk.Align.FILL}
        valign={Gtk.Align.CENTER}
      >
        <box
          orientation={Gtk.Orientation.HORIZONTAL}
          spacing={8}
          hexpand
          halign={Gtk.Align.FILL}
          valign={Gtk.Align.CENTER}
        >
          <box
            orientation={Gtk.Orientation.HORIZONTAL}
            spacing={4}
            halign={Gtk.Align.START}
            valign={Gtk.Align.CENTER}
          >
            <button
              class="repo-launcher-btn"
              tooltipText={
                hasLocal
                  ? `Open claude --dangerously-skip-permissions in ${repoPath}`
                  : "No local checkout — cannot launch"
              }
              sensitive={hasLocal}
              onClicked={() => {
                if (!hasLocal) return
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
              <image iconName="claude-ai-symbolic" pixelSize={14} />
            </button>
            <button
              class="repo-launcher-btn"
              tooltipText={
                hasLocal
                  ? `Open codex --yolo --search in ${repoPath}`
                  : "No local checkout — cannot launch"
              }
              sensitive={hasLocal}
              onClicked={() => {
                if (!hasLocal) return
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
              <image iconName="openai-symbolic" pixelSize={14} />
            </button>
            <button
              class="repo-launcher-btn"
              tooltipText={
                hasLocal
                  ? `Open opencode in ${repoPath}`
                  : "No local checkout — cannot launch"
              }
              sensitive={hasLocal}
              onClicked={() => {
                if (!hasLocal) return
                closeControlCenter()
                void execAsync(["kitty", "-d", repoPath, "opencode"]).catch(
                  (e) => console.error(`kitty opencode failed: ${String(e)}`),
                )
              }}
            >
              <image iconName="opencode-symbolic" pixelSize={14} />
            </button>
          </box>
          <button
            class="repo-plan-repo-btn"
            tooltipText={
              hasLocal
                ? `Open ${repoPath} in kitty`
                : `Open ${repoPath} — No local checkout`
            }
            hexpand
            halign={Gtk.Align.FILL}
            sensitive={hasLocal}
            onClicked={() => {
              if (!hasLocal) return
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
        </box>
        <button
          class="gh-plan-btn"
          tooltipText={`Open https://github.com/${entry.repo}`}
          onClicked={() => {
            closeControlCenter()
            void execAsync([
              "xdg-open",
              `https://github.com/${entry.repo}`,
            ]).catch((e) => console.error(`xdg-open failed: ${String(e)}`))
          }}
        >
          <box
            orientation={Gtk.Orientation.HORIZONTAL}
            spacing={6}
            hexpand
            halign={Gtk.Align.FILL}
            valign={Gtk.Align.CENTER}
          >
            <image
              iconName="xsi-github-symbolic"
              pixelSize={12}
              class="gh-plan-icon"
            />
            <label
              class={
                issueCount
                  ? issueCount((n) =>
                      n > 0
                        ? "issue-badge issue-badge-has-issues"
                        : "issue-badge",
                    )
                  : "issue-badge"
              }
              halign={Gtk.Align.CENTER}
              valign={Gtk.Align.CENTER}
              label={
                issueCount
                  ? issueCount((n) => (n > 99 ? "99+" : String(n)))
                  : "0"
              }
            />
            <label
              class={
                isMissing
                  ? "repo-plan-plan repo-plan-plan-missing"
                  : hasLocal && localPath
                    ? "repo-plan-plan repo-plan-checkout"
                    : "repo-plan-plan"
              }
              xalign={0}
              ellipsize={3}
              maxWidthChars={isMissing ? 20 : 28}
              label={entry.plan}
              hexpand
            />
          </box>
        </button>
      </box>
      <box
        orientation={Gtk.Orientation.VERTICAL}
        spacing={6}
        widthRequest={hideProgress ? 1 : 112}
        halign={Gtk.Align.FILL}
        valign={Gtk.Align.CENTER}
        visible={!hideProgress}
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
  live?: boolean
}

export function RepoPlanPanel({
  items,
  title = "Repo Plans",
  live = true,
}: RepoPlanPanelProps) {
  const isAccessor = typeof items === "function"
  const staticItems = (items as RepoPlan[] | undefined) ?? MOCK_REPO_PLANS
  const accessorItems = items as Accessor<RepoPlan[]> | undefined

  const [liveItems, setLiveItems] = createState<RepoPlan[] | null>(null)
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

  // Live fetch: last 15 active repos mapped via static repo-map.json
  const initLive = async () => {
    console.log("[RepoPlan] initLive start")
    if (isAccessor || !live) {
      // static mode: use provided items
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
      return
    }
    const liveData = await fetchLiveRepoPlans()
    console.log("[RepoPlan] fetchLiveRepoPlans done", liveData.length)
    setLiveItems(liveData)
    void fetchAll(liveData.map((r) => r.repo))
  }

  setTimeout(() => {
    void initLive()
  }, 300)

  const effectiveTitle = live && !isAccessor ? "Active Repos" : title

  // Decide which items to render
  const hasLive = liveItems((v) => v !== null && v.length > 0)

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
        <label
          class="repo-plan-title"
          xalign={0}
          label={effectiveTitle}
          hexpand
        />
        <label
          class="repo-plan-count"
          xalign={1}
          label={
            isAccessor && accessorItems
              ? accessorItems((v) => `${v.length} repos`)
              : liveItems((v) =>
                  v ? `${v.length} repos` : `${staticItems.length} repos`,
                )
          }
        />
      </box>
      <box class="repo-plan-divider" />
      <box
        class="repo-plan-list"
        orientation={Gtk.Orientation.VERTICAL}
        spacing={6}
      >
        {isAccessor && accessorItems ? (
          <For each={accessorItems}>
            {(entry: RepoPlan) => (
              <RepoPlanRow
                entry={entry}
                issueCount={issueCounts((m) => m[entry.repo] ?? 0)}
              />
            )}
          </For>
        ) : live ? (
          // Live mode: render liveItems if available, else fallback skeleton from static
          <For each={liveItems((v) => v ?? staticItems)}>
            {(entry: RepoPlan) => (
              <RepoPlanRow
                entry={entry}
                issueCount={issueCounts((m) => m[entry.repo] ?? 0)}
                hideProgress={false}
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
        <RepoPlanPanel items={MOCK_REPO_PLANS} live={false} />
      </box>
    </window>
  )
}
