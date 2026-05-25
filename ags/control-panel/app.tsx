import app from "ags/gtk4/app"
import style from "./style.scss"
import { initializeLogger, createLogger } from "./src/lib/logger"
import { ControlCenterWindow } from "./src/windows/control-center"

initializeLogger()
const logger = createLogger(["ags", "app"])

app.start({
  css: style,
  icons: `${SRC}/icons`,
  main() {
    logger.info`main() entry point [STARTUP]`
    return <ControlCenterWindow />
  },
})
