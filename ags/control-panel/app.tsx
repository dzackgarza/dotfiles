import app from "ags/gtk4/app";
import { createLogger, initializeLogger } from "./src/lib/logger";
import { ControlCenterWindow } from "./src/windows/control-center";
import style from "./style.scss";

initializeLogger();
const logger = createLogger(["ags", "app"]);

app.start({
  css: style,
  icons: `${SRC}/icons`,
  main() {
    logger.info`main() entry point [STARTUP]`;
    return <ControlCenterWindow />;
  },
});
