import app from "ags/gtk4/app";
import { createLogger, initializeLogger } from "./src/lib/logger";
import { ControlCenterWindow } from "./src/windows/control-center";
import {
  BatteryHistoryWindow,
  toggleBatteryHistory,
} from "./src/windows/battery-history";
import style from "./style.scss";

initializeLogger();
const logger = createLogger(["ags", "app"]);

app.start({
  css: style,
  icons: `${SRC}/icons`,
  requestHandler(argv, response) {
    const [command] = argv;
    if (command === undefined || command === "ping") {
      response("control-panel running");
      return;
    }
    if (command === "battery-history") {
      toggleBatteryHistory();
      response("battery-history toggled");
      return;
    }
    response(`unknown command: ${command}`);
  },
  main() {
    logger.info`main() entry point [STARTUP]`;
    BatteryHistoryWindow();
    return <ControlCenterWindow />;
  },
});
