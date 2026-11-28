import app from "ags/gtk4/app"
import { interval } from "ags/time"
import { getControlCenterService } from "../../services/control-center"

app.start({
  instanceName: "antigravity-usage-window-regression",
  main() {
    const control = getControlCenterService()
    control.refreshUsage()
    setTimeout(() => {
      console.error("Timed out waiting for usage data")
      app.quit()
    }, 25_000)
    interval(100, () => {
      const providers = control.claudeUsageData.peek().providers
      if (providers.length === 0) return true
      const rows = providers
        .filter((provider) => provider.provider === "antigravity")
        .flatMap((provider) =>
          provider.rows.map((row) => ({
            account: provider.account,
            identifier: row.identifier,
          })),
        )
      print(`USAGE_ROWS=${JSON.stringify(rows)}`)
      app.quit()
      return false
    })
  },
})
