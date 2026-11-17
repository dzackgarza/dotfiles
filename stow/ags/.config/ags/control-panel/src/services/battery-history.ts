import { createState } from "ags"
import { execAsync } from "ags/process"

const RENDERER = "/home/dzack/.config/waybar/scripts/battery-history.py"

export type BatteryHistoryState = {
  loading: boolean
  imagePath: string
  error: string
}

export function createBatteryHistoryService() {
  const [state, setState] = createState<BatteryHistoryState>({
    loading: true,
    imagePath: "",
    error: "",
  })
  let generation = 0
  let onRendered: ((path: string) => void) | null = null

  const refresh = async (rangeSeconds: number) => {
    const currentGeneration = ++generation
    const outputPath = `/tmp/ags-battery-history-${Date.now()}-${currentGeneration}.png`
    setState({ loading: true, imagePath: "", error: "" })
    try {
      await execAsync([
        "python3",
        RENDERER,
        "--render",
        String(rangeSeconds),
        outputPath,
      ])
      if (currentGeneration === generation) {
        onRendered?.(outputPath)
        setState({ loading: false, imagePath: outputPath, error: "" })
      }
    } catch (error) {
      if (currentGeneration === generation) {
        setState({
          loading: false,
          imagePath: "",
          error: error instanceof Error ? error.message : String(error),
        })
      }
    }
  }

  return {
    state,
    refresh,
    setOnRendered(callback: (path: string) => void) {
      onRendered = callback
    },
  }
}
