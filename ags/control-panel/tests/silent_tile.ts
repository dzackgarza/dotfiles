import { exit } from "system"
import app from "ags/gtk4/app"
import { readSilentState } from "../src/services/control-center"

app.start({
  main() {
    readSilentState()
      .then(() => exit(0))
      .catch((e: unknown) => {
        const msg = e instanceof Error ? e.message : String(e)
        console.error("FAIL:", msg)
        exit(1)
      })
    return null
  },
})
