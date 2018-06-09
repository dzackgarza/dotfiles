!function(modules) {
    var installedModules = {};
    function __webpack_require__(moduleId) {
        if (installedModules[moduleId]) return installedModules[moduleId].exports;
        var module = installedModules[moduleId] = {
            i: moduleId,
            l: !1,
            exports: {}
        };
        return modules[moduleId].call(module.exports, module, module.exports, __webpack_require__), 
        module.l = !0, module.exports;
    }
    __webpack_require__.m = modules, __webpack_require__.c = installedModules, __webpack_require__.d = function(exports, name, getter) {
        __webpack_require__.o(exports, name) || Object.defineProperty(exports, name, {
            configurable: !1,
            enumerable: !0,
            get: getter
        });
    }, __webpack_require__.n = function(module) {
        var getter = module && module.__esModule ? function() {
            return module.default;
        } : function() {
            return module;
        };
        return __webpack_require__.d(getter, "a", getter), getter;
    }, __webpack_require__.o = function(object, property) {
        return Object.prototype.hasOwnProperty.call(object, property);
    }, __webpack_require__.p = "", __webpack_require__(__webpack_require__.s = 1212);
}({
    1: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var logger_1 = __webpack_require__(162);
        exports.SimpleLogger = logger_1.SimpleLogger, exports.Logger = logger_1.Logger;
        var logWriter_1 = __webpack_require__(73);
        exports.FunctionLogWriter = logWriter_1.FunctionLogWriter, exports.ConsoleLogWriter = logWriter_1.ConsoleLogWriter;
        var felogLogWriter_1 = __webpack_require__(164);
        exports.FelogLogWriter = felogLogWriter_1.FelogLogWriter;
        var logFilter_1 = __webpack_require__(74);
        exports.logLevelFilter = logFilter_1.logLevelFilter;
        var logConfig_1 = __webpack_require__(72);
        exports.LogConfig = logConfig_1.LogConfig;
    },
    10: function(module, exports, __webpack_require__) {
        "use strict";
        function __export(m) {
            for (var p in m) exports.hasOwnProperty(p) || (exports[p] = m[p]);
        }
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), __export(__webpack_require__(68)), __export(__webpack_require__(71)), __export(__webpack_require__(31)), 
        __export(__webpack_require__(70)), __export(__webpack_require__(75)), __export(__webpack_require__(69)), 
        __export(__webpack_require__(76));
        var mainConfig_1 = __webpack_require__(76), bundle_1 = __webpack_require__(31), stdlib_1 = __webpack_require__(3), log = __webpack_require__(1).Logger.create("config"), globalConfig = new stdlib_1.Global(function() {
            log.warn("Global config not initialized -- using fall back value.");
            var browser = stdlib_1.assertNonNull(bundle_1.TargetBrowser.detect(window), "runtime-detected browser type"), cfg = mainConfig_1.MainConfig.create(browser, bundle_1.TargetContext.detect(window, browser), mainConfig_1.ProcessEnv.fromBrowserify());
            return window.GR_CFG = cfg, cfg;
        });
        exports.getGlobal = function() {
            return globalConfig.get();
        }, exports.initGlobal = function(browser, context, env) {
            globalConfig.init(mainConfig_1.MainConfig.create(browser, context, env || mainConfig_1.ProcessEnv.fromBrowserify())), 
            window.GR_CFG = globalConfig.get();
        };
    },
    1212: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var Config = __webpack_require__(10);
        Config.initGlobal("chrome", "cs"), __webpack_require__(1).LogConfig.configure({
            edge: !1,
            prodCs: "prod" === Config.getGlobal().bundleInfo.env
        });
        var felogPixel = __webpack_require__(140), telemetry_1 = __webpack_require__(141), interface_1 = __webpack_require__(61), log = __webpack_require__(1).Logger.create("chrome.proxy"), browserObject = window.chrome || window.firefox, telemetry = new telemetry_1.Telemetry(felogPixel.sendEventPixel);
        function initProxy() {
            var com = [ interface_1.ports.bridge, interface_1.ports.background, interface_1.ports.broadcast ].reduce(function(obj, port) {
                return Object.assign({}, obj, ((_a = {})[port] = function(name) {
                    var port = browserObject.runtime.connect({
                        name: name
                    });
                    return port.onMessage.addListener(function(msg) {
                        return eventName = "message", void 0 === (data = {
                            msg: msg,
                            name: name
                        }) && (data = {}), document.dispatchEvent(new CustomEvent("grammarly:message", {
                            detail: Object.assign({
                                event: eventName
                            }, data)
                        }));
                        var eventName, data;
                    }), port.onDisconnect.addListener(function() {
                        log.warn("port malfunction " + name);
                        var error = browserObject.runtime.lastError;
                        telemetry.proxyPortDisconnected(name, error && error.message || "port malfunction: " + name), 
                        cleanListeners(), document.dispatchEvent(new CustomEvent("grammarly:error", {
                            detail: {
                                event: "disconnect",
                                name: name
                            }
                        }));
                    }), port;
                }(port), _a));
                var _a;
            }, {});
            function processAction(_a) {
                var _b = _a.detail, name = _b.name, data = _b.data;
                com && com[name].postMessage(data);
            }
            function processPing() {
                document.dispatchEvent(new CustomEvent("grammarly:pong")), document.dispatchEvent(new CustomEvent("grammarly:reset"));
            }
            function cleanListeners() {
                document.removeEventListener("grammarly:action", processAction), document.removeEventListener("grammarly:ping", processPing), 
                document.removeEventListener("grammarly:reset", cleanListeners), com = null;
            }
            document.addEventListener("grammarly:action", processAction), document.addEventListener("grammarly:ping", processPing), 
            document.dispatchEvent(new CustomEvent("grammarly:proxyports")), document.addEventListener("grammarly:proxyports", cleanListeners), 
            telemetry.proxyInit();
        }
        "loading" === document.readyState ? document.addEventListener("DOMContentLoaded", initProxy, !1) : initProxy();
    },
    140: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var config = __webpack_require__(25), log_1 = __webpack_require__(28);
        exports.sendEventPixel = function(logger, message, level, extra, context) {
            var img = document.createElement("img"), payload = log_1.createEventPayload({
                logger: logger,
                level: level,
                message: message,
                extra: extra
            }, {
                appName: config.appName,
                appVersion: config.getVersion(),
                env: config.ENV,
                context: context
            });
            return img.src = log_1.felogRequestUrl(payload, config.URLS.newFelog), Promise.resolve();
        };
    },
    141: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var Config = __webpack_require__(10), log_1 = __webpack_require__(28), telemetry_1 = __webpack_require__(97), stdlib_1 = __webpack_require__(3), log = __webpack_require__(1).Logger.create("lib.tracking.telemetry"), CARD_EVENTS_PROBABILITY = .1, PROXY_EVENTS_PROBABILITY = .05, usageMetricsProbability = {
            chrome: .1,
            firefox: .1,
            safari: .1,
            edge: 1
        }, getUsageMetricsProbability = function(target) {
            return usageMetricsProbability[target];
        }, Telemetry = function() {
            function Telemetry(_sendFelog, _sendFelogUsage, _setUserId, _setContainerId, _sendFelogTimings, _sendUsageMetrics, _perfMetrics, _sendPerfMetrics, _sendFelogManyEvents, _sendFelogCrashLogs, _getUsageMetricsProbability) {
                void 0 === _sendFelog && (_sendFelog = stdlib_1.noOp), void 0 === _sendFelogUsage && (_sendFelogUsage = stdlib_1.noOp), 
                void 0 === _setUserId && (_setUserId = stdlib_1.noOp), void 0 === _setContainerId && (_setContainerId = stdlib_1.noOp), 
                void 0 === _sendFelogTimings && (_sendFelogTimings = stdlib_1.noOp), void 0 === _sendUsageMetrics && (_sendUsageMetrics = !1), 
                void 0 === _perfMetrics && (_perfMetrics = telemetry_1.PerformanceMetrics.dummy), 
                void 0 === _sendPerfMetrics && (_sendPerfMetrics = !1), void 0 === _sendFelogManyEvents && (_sendFelogManyEvents = stdlib_1.noOp), 
                void 0 === _sendFelogCrashLogs && (_sendFelogCrashLogs = stdlib_1.noOp), void 0 === _getUsageMetricsProbability && (_getUsageMetricsProbability = getUsageMetricsProbability);
                var _this = this;
                this._sendFelog = _sendFelog, this._sendFelogUsage = _sendFelogUsage, this._setUserId = _setUserId, 
                this._setContainerId = _setContainerId, this._sendFelogTimings = _sendFelogTimings, 
                this._sendUsageMetrics = _sendUsageMetrics, this._perfMetrics = _perfMetrics, this._sendPerfMetrics = _sendPerfMetrics, 
                this._sendFelogManyEvents = _sendFelogManyEvents, this._sendFelogCrashLogs = _sendFelogCrashLogs, 
                this._getUsageMetricsProbability = _getUsageMetricsProbability, this._perfMetricsThrottleTimeMs = 6e4, 
                this._prepareDataString = function(logger, message, extra) {
                    var dataString;
                    try {
                        dataString = JSON.stringify(extra);
                    } catch (err) {
                        dataString = "Failed to stringify event properties: '" + err + "', '" + (err && err.message) + "'", 
                        log.warn(dataString, "for " + message + "@" + logger);
                    }
                    return dataString;
                }, this.pageLoadTimeout = function() {
                    _this._send("cs.connection.failover.pageLoad.timeout", "content script init failed", log_1.LogLevel.ERROR);
                }, this.appLoadTimeout = function() {
                    _this._send("cs.connection.failover.appLoad.timeout", "extension init timed out", log_1.LogLevel.ERROR);
                }, this.differentStateDomain = function(stateDomain) {
                    _this._send("cs.state.differentDomain", "received state for different domain", log_1.LogLevel.INFO, {
                        stateDomain: stateDomain
                    });
                }, this.restoredBgConnection = function(timeWithoutConnection) {
                    _this._send("cs.connection.bg.restored", "bg page connection restored", log_1.LogLevel.INFO, {
                        timeWithoutConnection: timeWithoutConnection
                    });
                }, this.initWithoutBgConnection = function() {
                    _this._send("cs.connection.bg.disconnected", "no connection to bg page", log_1.LogLevel.INFO);
                }, this.fetchDefinitionsFail = function() {
                    _this._send("cs.connection.api.definition.failed", "definitions fetch failed", log_1.LogLevel.WARN);
                }, this.infinityCheckResetFail = function(delay) {
                    _this._send("cs.connection.infiniteCheck.failed", "infinite check reset failed", log_1.LogLevel.ERROR, {
                        delay: delay
                    });
                }, this.tooLongPageConfigInit = function(initTime) {
                    _this._send("cs.pageConfig.init.exceeded", "page config init timeout", log_1.LogLevel.WARN, {
                        initTime: initTime
                    });
                }, this.tooLongUserUpdateTime = function(updateTime) {
                    _this._send("bg.state.user.update.exceeded", "user state update took too long", log_1.LogLevel.WARN, {
                        updateTime: updateTime
                    });
                }, this.lostBgPageConnection = function() {
                    _this._send("cs.gbutton.bgСonnection.lost", "gbutton connection to bg page lost", log_1.LogLevel.INFO);
                }, this.restoreBgPageConnection = function(time) {
                    _this._send("cs.gbutton.bgСonnection.restored", "gbutton connection to bg page restored", log_1.LogLevel.INFO, {
                        time: time
                    });
                }, this.badCursorPosition = function() {
                    _this._send("cs.editor.badCursorPosition", "incorrect cursor position in grammarly-editor", log_1.LogLevel.INFO);
                }, this.cursorJump = function() {
                    _this._send("cs.editor.cursorJump", "cursor jump detected", log_1.LogLevel.WARN);
                }, this.signinOpen = function() {
                    _this._send("cs.signin.open", "sign in dialog opened", log_1.LogLevel.INFO);
                }, this.signinClose = function(openTime) {
                    _this._send("cs.signin.close", "sign in dialog closed", log_1.LogLevel.INFO, {
                        openTime: openTime
                    });
                }, this.tabReloadClick = function() {
                    _this._send("cs.gbutton.reload.click", "gbutton reload clicked", log_1.LogLevel.WARN);
                }, this.popupLoadError = function(message, name) {
                    _this._send("cs.popup.load.error", "could not open pop-up editor", log_1.LogLevel.ERROR, {
                        message: message,
                        name: name
                    });
                }, this.loginNoBgPageConnection = function(message) {
                    _this._send("debug.cs.connection.signin.bg.timeout", "can not connect to bg page on login", log_1.LogLevel.INFO, {
                        message: message
                    });
                }, this.pageConfigCDNError = function(message) {
                    _this._send("cs.pageConfig.cdn.error", "could not read page config", log_1.LogLevel.ERROR, {
                        message: message
                    });
                }, this.pageConfigLocalStorageError = function(message, name) {
                    _this._send("cs.pageConfig.localStorage.error", "could not read page config from localStorage", log_1.LogLevel.INFO, {
                        message: message,
                        name: name
                    });
                }, this.pageConfigUpdated = function(oldVersion, newVersion) {
                    _this._send("cs.pageConfig.updated", "page config updated", log_1.LogLevel.INFO, {
                        oldVersion: oldVersion,
                        newVersion: newVersion
                    });
                }, this.settingsPopupTimeout = function() {
                    _this._send("settings.popup.init.timeout", "settings popup open timeout", log_1.LogLevel.WARN);
                }, this.settingsUsupportedShow = function(popupType) {
                    _this._send("settings.popup.state.unsupported.show", "page unsupported message shown", log_1.LogLevel.INFO, {
                        popupType: popupType
                    });
                }, this.socketBgError = function() {
                    _this._send("bg.socket.error", "bg page socket error", log_1.LogLevel.WARN);
                }, this.capiNotAuthorizedLoop = function(authDegradation, cookiesDisabled) {
                    _this._send("debug.socket.notAuthorizedLoop", "could not authenticate on capi and auth", log_1.LogLevel.INFO, {
                        authDegradation: authDegradation,
                        cookiesDisabled: cookiesDisabled
                    });
                }, this.socketDisabledCookie = function() {
                    _this._send("debug.socket.disabledCookies", "disabled cookies after failed authentication", log_1.LogLevel.INFO);
                }, this.socketBgRestored = function(tryCount) {
                    _this._send("debug.bg.socket.restored", "capi session restored", log_1.LogLevel.INFO, {
                        tryCount: tryCount
                    });
                }, this.socketBgReconnectFail = function(token, tryCount) {
                    _this._send("bg.socket.reconnect.fail", "could not restore ws connection", log_1.LogLevel.WARN, {
                        token: token,
                        tryCount: tryCount
                    });
                }, this.socketCsError = function() {
                    _this._send("cs.socket.error", "content script socket error", log_1.LogLevel.WARN);
                }, this.soketCsErrorMsg = function(message) {
                    _this._send("cs.socket.errorMsg", "capi error", log_1.LogLevel.WARN, {
                        message: message
                    });
                }, this.gnarClientInitFail = function(message) {
                    _this._send("gnar.bg.tracking.gnar.init.fail", "gnar init failed", log_1.LogLevel.WARN, {
                        message: message
                    });
                }, this.bgTrackingInitFail = function() {
                    _this._send("debug.tracking.init.fail", "bg page tracking library init failed", log_1.LogLevel.INFO);
                }, this.gnarSpecUndefinedInit = function() {
                    _this._send("debug.tracking.gnar.spec.init.fail", "gnar spec was failed to init", log_1.LogLevel.INFO);
                }, this.dailyPing = function() {
                    _this._send("debug.dailyPing", "daily ping", log_1.LogLevel.INFO);
                }, this.userUpgradeClick = function(placement) {
                    _this._send("cs.ui.action.upgradeClick", "upgrade hook clicked", log_1.LogLevel.INFO, {
                        placement: placement
                    });
                }, this.gButtonClick = function() {
                    _this._send("cs.ui.gbutton.click", "gbutton clicked", log_1.LogLevel.INFO);
                }, this.checkingToggledInField = function(enabled) {
                    _this._send("cs.ui.gbutton.toggleInField", "checking toggled in field", log_1.LogLevel.INFO, {
                        enabled: enabled
                    });
                }, this.sessionInvalidated = function(reason, userChanged) {
                    _this._send("bg.session.invalidated", "user session invalidated", log_1.LogLevel.INFO, {
                        reason: reason,
                        userChanged: userChanged
                    });
                }, this.unexpectedAnonymous = function(data) {
                    _this._send("debug.bg.session.unexpectedAnonymous", "user changed to anonymous", log_1.LogLevel.INFO, data);
                }, this.dapiPropInitialized = function(name, value) {
                    _this._send("bg.settings.dapi.prop.init", "save property to the DAPI", log_1.LogLevel.INFO, {
                        name: name,
                        value: value
                    });
                }, this.getDapiPropError = function(property, body) {
                    _this._send("bg.connection.dapi.getProp.error", "could not get dapi property", log_1.LogLevel.WARN, {
                        property: property,
                        body: body
                    });
                }, this.setDapiPropError = function(property, body) {
                    _this._send("bg.connection.dapi.setProp.error", "could not set dapi property", log_1.LogLevel.WARN, {
                        property: property,
                        body: body
                    });
                }, this.toggleExtensionDefs = function(enabled) {
                    _this._send("bg.settings.definitions.toggle", "definitions toggled for domain", log_1.LogLevel.INFO, {
                        enabled: enabled
                    });
                }, this.toggleExtension = function(enabled, placement) {
                    _this._send("bg.settings.extension.toggle", "extension toggled for domain", log_1.LogLevel.INFO, {
                        enabled: enabled,
                        placement: placement
                    });
                }, this.disableUntilNextVisit = function() {
                    _this._send("cs.gbutton.disableUntilNextVisit", "extension temporary disabled on the current tab", log_1.LogLevel.INFO);
                }, this.disableButtonClick = function() {
                    _this._send("cs.gbutton.disableButtonClick", "clicked on disable button in gButton", log_1.LogLevel.INFO);
                }, this.cookieOverflow = function(size, biggestCookie) {
                    _this._send("debug.bg.state.cookie.overflow", "cookie is too big", log_1.LogLevel.INFO, {
                        size: size,
                        biggestCookie: biggestCookie
                    });
                }, this.externalChangePlan = function() {
                    _this._send("bg.api.external.changePlan", "plan changed from editor", log_1.LogLevel.INFO);
                }, this.externalChangeDialect = function() {
                    _this._send("bg.api.external.changeDialect", "dialect changed from editor", log_1.LogLevel.INFO);
                }, this.externalChangeUser = function() {
                    _this._send("bg.api.external.changeUsed", "user changed from editor", log_1.LogLevel.INFO);
                }, this.externalLogout = function() {
                    _this._send("bg.api.external.logout", "user logged out form editor", log_1.LogLevel.INFO);
                }, this.bgPageStartFail = function(message, stack) {
                    _this._send("bg.start.fail", "bg page start failed", log_1.LogLevel.ERROR, {
                        message: message,
                        stack: stack
                    });
                }, this.bgPageInitTimeout = function(initTime) {
                    _this._send("bg.state.start.timeout", "bg page init timeout", log_1.LogLevel.WARN, {
                        initTime: initTime
                    });
                }, this.bgPageInitFail = function(initAttempts) {
                    _this._send("bg.state.init.fail", "bg page init failed", log_1.LogLevel.ERROR, {
                        initAttempts: initAttempts
                    });
                }, this.extensionUpdated = function(currentVersion, previousVersion) {
                    _this._send("bg.state.updated", "extension updated", log_1.LogLevel.INFO, {
                        currentVersion: currentVersion,
                        previousVersion: previousVersion
                    });
                }, this.extensionUpdateFail = function(previousVersion) {
                    _this._send("bg.state.update.fail", "extension update failed", log_1.LogLevel.INFO, {
                        previousVersion: previousVersion
                    });
                }, this.cannotGetInstallSource = function() {
                    _this._send("bg.getSource.fail", "failed to get extension install source", log_1.LogLevel.WARN);
                }, this.extensionInstall = function(source) {
                    _this._send("bg.state.install", "extension installed", log_1.LogLevel.INFO, {
                        source: source
                    });
                }, this.chromeForcedToUpdate = function(newVersion) {
                    _this._send("bg.chrome.forcedToUpdate", "chrome forced update", log_1.LogLevel.INFO, {
                        newVersion: newVersion
                    });
                }, this.chromeContentScriptLoadError = function(message, type) {
                    _this._send("bg.chrome.cs.load.error", "content script execution error", log_1.LogLevel.WARN, {
                        message: message,
                        type: type
                    });
                }, this.reloadNotificationShow = function() {
                    _this._send("bg.ui.notification.tabsReload.show", "extension reload notification shown", log_1.LogLevel.WARN);
                }, this.reloadNotificationClick = function() {
                    _this._send("bg.ui.notification.tabsReload.click", "reload notification clicked", log_1.LogLevel.INFO);
                }, this.fetchUserFail = function(reason, body, statusCode) {
                    _this._send("bg.user.fetch.fail", "failed to update user", log_1.LogLevel.WARN, {
                        body: body,
                        statusCode: statusCode,
                        reason: reason
                    });
                }, this.fetchMimicFail = function(body, statusCode) {
                    _this._send("bg.user.mimic.fail", "mimic request failed", log_1.LogLevel.WARN, {
                        body: body,
                        statusCode: statusCode
                    });
                }, this.fetchStatsFail = function(body, statusCode) {
                    _this._send("bg.user.dapi.prop.stats.fail", "dapi props request failed", log_1.LogLevel.WARN, {
                        body: body,
                        statusCode: statusCode
                    });
                }, this.fetchCookieFail = function() {
                    _this._send("bg.cookie.fail", "could not get grauth from cookie", log_1.LogLevel.WARN);
                }, this.fetchSettingsFail = function(body, statusCode) {
                    _this._send("bg.user.settings.fail", "could not get settings from auth", log_1.LogLevel.WARN, {
                        body: body,
                        statusCode: statusCode
                    });
                }, this.frequentCookieChanges = function(canceled) {
                    _this._send("debug.cookie.onChange.error", "cookie change too frequent", log_1.LogLevel.INFO, {
                        canceled: canceled
                    });
                }, this.initializePropFromDapi = function(name) {
                    _this._send("bg.state.dapi.prop.initialize", "set property from dapi", log_1.LogLevel.INFO, {
                        name: name
                    });
                }, this.onboardingPopupShow = function() {
                    _this._send("cs.onboarding.popup.show", "show onboarding popup to user after first time extension install", log_1.LogLevel.INFO);
                }, this.onboardingPopupCancel = function() {
                    _this._send("cs.onboarding.popup.cancel", "user canceled onboarding popup", log_1.LogLevel.INFO);
                }, this.onboardingTutorialShow = function() {
                    _this._send("cs.onboarding.tutorial.show", "opened onboarding dialog after popup", log_1.LogLevel.INFO);
                }, this.onboardingVideoLoaded = function() {
                    _this._send("cs.onboarding.tutorial.video.loaded", "load video data for onboarding tutorial", log_1.LogLevel.INFO);
                }, this.incognitoInit = function() {
                    _this._send("bg.incognito.init", "extension initialized in incognito mode", log_1.LogLevel.INFO);
                }, this.disabledCookiesInit = function() {
                    _this._send("bg.cookie.disabled", "extension initialized with disabled cookies", log_1.LogLevel.INFO);
                }, this.loginReminderPopupShow = function() {
                    _this._send("cs.gbutton.popup.loginReminder.show", "show login reminder popup to user", log_1.LogLevel.INFO);
                }, this.loginReminderBadgeShow = function() {
                    _this._send("bg.state.user.loginReminder.enable", "enable login reminder for sign out user", log_1.LogLevel.INFO);
                }, this.proxyInit = function() {
                    _this._sendWithProbability(PROXY_EVENTS_PROBABILITY, "proxy.init", "proxy script initialized", log_1.LogLevel.INFO);
                }, this.proxyPortDisconnected = function(portName, errorMessage) {
                    _this._sendWithProbability(PROXY_EVENTS_PROBABILITY, "proxy.disconnect", "proxy port disconnected", log_1.LogLevel.INFO, {
                        port: portName,
                        error: errorMessage
                    });
                }, this.unhandledBgPageException = function(e) {
                    _this._send("bg.unhandledException", "unhandled exception on background page", log_1.LogLevel.ERROR, {
                        message: e.error ? e.error.message : e.message
                    });
                }, this.unhandledBgPageRejection = function(e) {
                    _this._send("bg.unhandledRejection", "unhandled promise rejection on background page", log_1.LogLevel.ERROR, {
                        message: null != e.reason ? "string" == typeof e.reason ? e.reason : e.reason.message : void 0
                    });
                }, this.storageMigrationSucceeded = function() {
                    _this._send("bg.storageMigration.success", "storage migration succeeded", log_1.LogLevel.INFO, {});
                }, this.storageMigrationFailed = function(e) {
                    _this._send("bg.storageMigration.failure", "storage migration failed", log_1.LogLevel.ERROR, {
                        message: e && e.message
                    });
                }, this.cardShowAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.card.show", "show card action", log_1.LogLevel.INFO);
                }, this.cardHideAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.card.hide", "hide card action", log_1.LogLevel.INFO);
                }, this.cardReplacementAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.card.replacement", "click on the replacement in the card", log_1.LogLevel.INFO);
                }, this.cardAddToDictAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.card.addToDict", "click add to dictionary button in the card", log_1.LogLevel.INFO);
                }, this.cardIgnoreAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.card.ignore", "click ignore button in the card", log_1.LogLevel.INFO);
                }, this.synonymCardShowAction = function(notFoundCard) {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.synonym.show", "show synonymous card action", log_1.LogLevel.INFO, {
                        notFoundCard: notFoundCard
                    });
                }, this.synonymCardHideAction = function(notFoundCard) {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.synonym.hide", "hide synonymous card action", log_1.LogLevel.INFO, {
                        notFoundCard: notFoundCard
                    });
                }, this.synonymReplacementAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.synonym.replacement", "click on the replacement in the synonym", log_1.LogLevel.INFO);
                }, this.dictCardShowAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.dict.show", "show dictionary card action", log_1.LogLevel.INFO);
                }, this.dictCardHideAction = function() {
                    _this._sendWithProbability(CARD_EVENTS_PROBABILITY, "cs.editor.dict.hide", "hide dictionary card action", log_1.LogLevel.INFO);
                }, this.errorBySendEmailData = function() {
                    _this._send("cs.editor.emailData.send.error", "error by parsing email data in gmail", log_1.LogLevel.WARN);
                }, this.couldNotParseTransform = function(transformHTML, fallbackParseSuccessful) {
                    _this._send("cs.cards.transforms.parse.error", "Could not parse transform in inline cards", log_1.LogLevel.WARN, {
                        transformHTML: transformHTML,
                        fallbackParseSuccessful: fallbackParseSuccessful
                    });
                }, this.disabledTabLoad = function(domain, accountType) {
                    _this._sendUsage("usage.loadOnDisabledTab", "tab load event with disabled extension", log_1.LogLevel.INFO, {
                        domain: domain,
                        accountType: accountType
                    });
                }, this.disabledTabByUserLoad = function(domain, accountType) {
                    _this._sendUsage("usage.loadOnDisabledByUserTab", "tab load event with disabled by user extension", log_1.LogLevel.INFO, {
                        domain: domain,
                        accountType: accountType
                    });
                }, this.initSession = function(domain, accountType, fieldType, fieldSupported) {
                    _this._sendUsage("usage.session.init", "init in the field", log_1.LogLevel.INFO, {
                        domain: domain,
                        accountType: accountType,
                        fieldType: fieldType,
                        fieldSupported: fieldSupported
                    });
                }, this.cardFirstInteraction = function(domain, accountType, fieldType) {
                    _this._sendUsage("usage.card.interaction", "interaction with card in the field", log_1.LogLevel.INFO, {
                        domain: domain,
                        accountType: accountType,
                        fieldType: fieldType
                    });
                }, this.gdocs = {
                    initialGdocsDisable: function() {
                        return _this._send("cs.gdocs.initialDisableSet", "Gdocs initially disabled for opt-in to be shown.", log_1.LogLevel.INFO);
                    },
                    getInitialDocumentStateFailed: function(message) {
                        return _this._send("cs.gdocs.state.getInitialFailed", "Can not get initial gdocs state", log_1.LogLevel.INFO, {
                            message: message
                        });
                    },
                    localStateSwappedWithRemote: function() {
                        return _this._send("cs.gdocs.state.localStateSwapped", "Local state were swapped with remote state", log_1.LogLevel.INFO);
                    },
                    revisionSwitched: function() {
                        return _this._send("cs.gdocs.revisionsSwitched", "User swtiched document revision", log_1.LogLevel.INFO);
                    },
                    noMatchForUnderline: function() {
                        return _this._send("cs.gdocs.orphantUnderline.noMatchFoundByUnderine", "No match found for underline", log_1.LogLevel.INFO);
                    },
                    noMatchFoundForId: function() {
                        return _this._send("cs.gdocs.orphantUnderline.noMatchFoundById", "No match found for ID", log_1.LogLevel.INFO);
                    },
                    replacementFailed: function() {
                        return _this._send("cs.gdocs.replacementFailed", "Empty text were put instead of replacement value", log_1.LogLevel.INFO);
                    },
                    editingDisabledNotification: function(data) {
                        return _this._send("cs.gdocs.notifications.editingDisabledBloodyBar", "GDocs saving too long editing disabled notification shown", log_1.LogLevel.INFO, data);
                    },
                    somethingWentWrongNotification: function(data) {
                        return _this._send("cs.gdocs.notifications.somethingWentWrongButterBar", "GDocs something went wrong notification shown", log_1.LogLevel.INFO, data);
                    },
                    documentOpen: function() {
                        return _this._send("cs.gdocs.notifications.documentOpen", "GDocs document open", log_1.LogLevel.INFO);
                    },
                    injectedSciptRollback: function(reason) {
                        return _this._send("cs.gdocs.injectedScriptsRollback", "GDocs injected scripts were rolled back", log_1.LogLevel.INFO, {
                            reason: reason
                        });
                    },
                    emptyResponseCrash: function() {
                        return _this._send("cs.gdocs.emptyResponseCrash", "We crashed when response is empty", log_1.LogLevel.INFO);
                    }
                }, this.performance = {
                    pageFieldsWatch: this._createMetric("cs.pageFields.watch"),
                    grammarlyEditorInput: this._createMetric("cs.grammarlyEditor.input")
                };
            }
            return Telemetry.prototype._send = function(logger, message, level, extra) {
                var dataString = this._prepareDataString(logger, message, extra);
                try {
                    this._sendFelog(logger, message, level, null != extra ? {
                        json: dataString
                    } : void 0);
                } catch (err) {
                    log.warn("Failed to send felog for " + message + "@" + logger + ": '" + (err && err.message) + "'", err);
                }
            }, Telemetry.prototype._sendMany = function(logger, events) {
                try {
                    this._sendFelogManyEvents(events);
                } catch (err) {
                    log.warn("Failed to send performance data for " + logger + ": '" + (err && err.message) + "'", err);
                }
            }, Telemetry.prototype._sendUsage = function(logger, message, level, usage) {
                if (this._sendUsageMetrics && this._getUsageMetricsProbability(Config.getGlobal().bundleInfo.browser) > Math.random()) try {
                    this._sendFelogUsage(logger, message, level, usage);
                } catch (err) {
                    log.warn("Failed to send usage felog for " + message + "@" + logger + ": '" + (err && err.message) + "'", err);
                }
            }, Telemetry.prototype._sendTimings = function(logger, timings) {
                try {
                    this._sendFelogTimings(logger, timings);
                } catch (err) {
                    log.warn("Failed to send felog timings for " + logger + ": '" + (err && err.message) + "'", err);
                }
            }, Telemetry.prototype._sendWithProbability = function(probability, logger, message, level, extra) {
                probability > Math.random() && this._send(logger, message, level, extra);
            }, Telemetry.prototype._createMetric = function(name) {
                var _this = this;
                if (this._sendPerfMetrics) {
                    var flush_1 = stdlib_1.throttle(this._perfMetricsThrottleTimeMs, function() {
                        _this._sendMany(name, _this._perfMetrics.flushMeasures(name).map(function(x) {
                            return {
                                logger: name,
                                level: log_1.LogLevel.INFO,
                                message: "",
                                extra_performance: parseFloat(x.toFixed(4))
                            };
                        }));
                    });
                    return {
                        startMeasure: function() {
                            log.debug("startMeasure: " + name);
                            var r = _this._perfMetrics.startMeasure(name);
                            return {
                                endMeasure: function() {
                                    r.endMeasure(), flush_1();
                                }
                            };
                        },
                        measure: function(fn) {
                            log.debug("measure: " + name);
                            var r = _this._perfMetrics.measure(name, fn);
                            return flush_1(), r;
                        }
                    };
                }
                return {
                    startMeasure: function() {
                        return {
                            endMeasure: stdlib_1.noOp
                        };
                    },
                    measure: function(fn) {
                        return fn();
                    }
                };
            }, Telemetry.prototype.sendCrashLogs = function(logger, events) {
                try {
                    this._sendFelogCrashLogs(events);
                } catch (err) {
                    log.warn("Failed to send crash data data for " + logger + ": '" + (err && err.message) + "'", err);
                }
            }, Telemetry.prototype.setUserId = function(id) {
                this._setUserId(id);
            }, Telemetry.prototype.setContainerId = function(id) {
                this._setContainerId(id);
            }, Telemetry.prototype.notificationShown = function(type) {
                this._send("cs.notification.show", "show notification on the page", log_1.LogLevel.INFO, {
                    type: type
                });
            }, Telemetry.prototype.notificationHide = function(type) {
                this._send("cs.notification.hide", "hide notification on the page", log_1.LogLevel.INFO, {
                    type: type
                });
            }, Telemetry;
        }();
        exports.Telemetry = Telemetry;
    },
    156: function(module, exports, __webpack_require__) {
        "use strict";
        var extendStatics, __extends = this && this.__extends || (extendStatics = Object.setPrototypeOf || {
            __proto__: []
        } instanceof Array && function(d, b) {
            d.__proto__ = b;
        } || function(d, b) {
            for (var p in b) b.hasOwnProperty(p) && (d[p] = b[p]);
        }, function(d, b) {
            function __() {
                this.constructor = d;
            }
            extendStatics(d, b), d.prototype = null === b ? Object.create(b) : (__.prototype = b.prototype, 
            new __());
        });
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var AssertionError = function(_super) {
            function AssertionError(msg) {
                return _super.call(this, "Assertion failed: " + (msg ? "string" == typeof msg ? msg : msg() : "(unnamed)")) || this;
            }
            return __extends(AssertionError, _super), AssertionError;
        }(Error);
        exports.AssertionError = AssertionError, exports.assert = function(cond, msg) {
            if (!cond) throw new AssertionError(msg);
        }, exports.assertNonNull = function(value, name) {
            if (null == value) throw new AssertionError(function() {
                return name ? "Expected " + name + " to be non-null" : "Expected non-null";
            });
            return value;
        };
    },
    157: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var CircularBuffer = function() {
            function CircularBuffer(capacity) {
                if (this.capacity = capacity, this._start = 0, this._end = 0, this._isFull = !1, 
                capacity <= 0) throw new Error("Invalid capacity " + capacity);
                this._buffer = new Array(capacity);
            }
            return Object.defineProperty(CircularBuffer.prototype, "size", {
                get: function() {
                    return this._isFull ? this._buffer.length : (this._end - this._start + this._buffer.length) % this._buffer.length;
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(CircularBuffer.prototype, "isEmpty", {
                get: function() {
                    return 0 === this.size;
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(CircularBuffer.prototype, "isFull", {
                get: function() {
                    return this._isFull;
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(CircularBuffer.prototype, "head", {
                get: function() {
                    return this.isEmpty ? null : this._buffer[this._start];
                },
                enumerable: !0,
                configurable: !0
            }), Object.defineProperty(CircularBuffer.prototype, "tail", {
                get: function() {
                    return this.isEmpty ? null : this._buffer[0 === this._end ? this.capacity - 1 : this._end - 1];
                },
                enumerable: !0,
                configurable: !0
            }), CircularBuffer.prototype.enqueue = function(element) {
                var pushedAway = null;
                return this.isFull && (pushedAway = this._buffer[this._start], this._startInc()), 
                this._buffer[this._end] = element, this._endInc(), this._start === this._end && (this._isFull = !0), 
                pushedAway;
            }, CircularBuffer.prototype.dequeue = function() {
                if (this.isEmpty) return null;
                var element = this._buffer[this._start];
                return this._buffer[this._start] = null, this._startInc(), this._isFull = !1, element;
            }, CircularBuffer.prototype.delete = function(element) {
                var ind = this._buffer.indexOf(element);
                if (ind >= 0) {
                    if (ind < this._end) {
                        for (var i = ind; i < this._end - 1; i++) this._buffer[i] = this._buffer[i + 1];
                        this._buffer[--this._end] = null;
                    } else {
                        for (i = this._start; i < ind; i++) this._buffer[i + 1] = this._buffer[i];
                        this._buffer[this._start] = null, this._startInc();
                    }
                    return this._isFull = !1, !0;
                }
                return !1;
            }, CircularBuffer.prototype._startInc = function() {
                this._start++, this._start === this.capacity && (this._start = 0);
            }, CircularBuffer.prototype._endInc = function() {
                this._end++, this._end === this.capacity && (this._end = 0);
            }, CircularBuffer.prototype.clear = function() {
                this._buffer = new Array(this.capacity), this._start = this._end = 0, this._isFull = !1;
            }, CircularBuffer.prototype.toArray = function() {
                var res;
                if (this.isEmpty) res = []; else if (this._start < this._end) res = this._buffer.slice(this._start, this._end); else {
                    res = new Array(this.size);
                    for (var j = 0, i = this._start; i < this.capacity; ++i, ++j) res[j] = this._buffer[i];
                    for (i = 0; i < this._end; ++i, ++j) res[j] = this._buffer[i];
                }
                return res;
            }, CircularBuffer;
        }();
        exports.CircularBuffer = CircularBuffer;
    },
    158: function(module, exports, __webpack_require__) {
        "use strict";
        var __read = this && this.__read || function(o, n) {
            var m = "function" == typeof Symbol && o[Symbol.iterator];
            if (!m) return o;
            var r, e, i = m.call(o), ar = [];
            try {
                for (;(void 0 === n || n-- > 0) && !(r = i.next()).done; ) ar.push(r.value);
            } catch (error) {
                e = {
                    error: error
                };
            } finally {
                try {
                    r && !r.done && (m = i.return) && m.call(i);
                } finally {
                    if (e) throw e.error;
                }
            }
            return ar;
        }, __spread = this && this.__spread || function() {
            for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
            return ar;
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.flatMap = function(f, xs) {
            return (_a = []).concat.apply(_a, __spread(xs.map(f)));
            var _a;
        }, exports.flatten = function(xss) {
            return (_a = []).concat.apply(_a, __spread(xss));
            var _a;
        }, exports.distinct = function(xs) {
            return __spread(new Set(xs));
        }, exports.distinctBy = function(f, xs) {
            var s = new Set();
            return xs.filter(function(x) {
                var k = f(x), r = !s.has(k);
                return s.add(k), r;
            });
        }, exports.scan = function(f, seed, xs) {
            for (var r = [ seed ], acc = seed, i = 0; i < xs.length; i++) acc = f(acc, xs[i]), 
            r.push(acc);
            return r;
        }, exports.maximum = function(xs) {
            return xs.reduce(function(max, x) {
                return x > max ? x : max;
            }, xs[0]);
        }, exports.maximumBy = function(xs, f) {
            return 0 === xs.length ? void 0 : xs.reduce(function(acc, x) {
                var y = f(x);
                return y > acc[1] ? [ x, y ] : acc;
            }, [ xs[0], f(xs[0]) ])[0];
        }, exports.reverse = function(xs) {
            return xs.slice().reverse();
        }, exports.partition = function(f, xs) {
            for (var ys = [], zs = [], j = 0, k = 0, i = 0; i < xs.length; i++) f(xs[i]) ? ys[j++] = xs[i] : zs[k++] = xs[i];
            return [ ys, zs ];
        }, exports.chunkBySize = function(size, xs) {
            if (size < 1) throw new Error("Invalid chunk size, expected > 0");
            if (0 === xs.length) return [ [] ];
            for (var result = [], x = 0; x < Math.ceil(xs.length / size); x++) result.push(xs.slice(x * size, (x + 1) * size));
            return result;
        }, exports.unfold = function(f, seed) {
            for (var r = [], res = f(seed); void 0 !== res; ) r.push(res[0]), res = f(res[1]);
            return r;
        }, exports.range = function(arg1, arg2) {
            return void 0 !== arg2 ? Array.from(Array(arg2 - arg1), function(_, i) {
                return i + arg1;
            }) : Array.from(Array(arg1), function(_, i) {
                return i;
            });
        }, exports.groupBy = function(xs, eq) {
            if (void 0 === eq && (eq = function(a, b) {
                return a === b;
            }), 0 === xs.length) return [];
            for (var acc = [ [ xs[0] ] ], i = 1; i < xs.length; i += 1) {
                var a = acc[acc.length - 1][0], b = xs[i];
                eq(a, b) ? acc[acc.length - 1].push(b) : acc.push([ b ]);
            }
            return acc;
        };
    },
    159: function(module, exports, __webpack_require__) {
        "use strict";
        var __values = this && this.__values || function(o) {
            var m = "function" == typeof Symbol && o[Symbol.iterator], i = 0;
            return m ? m.call(o) : {
                next: function() {
                    return o && i >= o.length && (o = void 0), {
                        value: o && o[i++],
                        done: !o
                    };
                }
            };
        }, __read = this && this.__read || function(o, n) {
            var m = "function" == typeof Symbol && o[Symbol.iterator];
            if (!m) return o;
            var r, e, i = m.call(o), ar = [];
            try {
                for (;(void 0 === n || n-- > 0) && !(r = i.next()).done; ) ar.push(r.value);
            } catch (error) {
                e = {
                    error: error
                };
            } finally {
                try {
                    r && !r.done && (m = i.return) && m.call(i);
                } finally {
                    if (e) throw e.error;
                }
            }
            return ar;
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.map = function(f, o) {
            var r = {};
            return Object.keys(o).forEach(function(k) {
                return r[k] = f(k, o[k]);
            }), r;
        }, exports.filter = function(f, o) {
            var r = {};
            return Object.keys(o).forEach(function(k) {
                f(k, o[k]) && (r[k] = o[k]);
            }), r;
        }, exports.values = function(o) {
            return Object.keys(o).map(function(k) {
                return o[k];
            });
        }, exports.pairs = function(o) {
            return Object.keys(o).map(function(k) {
                return [ k, o[k] ];
            });
        }, exports.create = function(kvs) {
            var e_1, _b, r = {};
            try {
                for (var kvs_1 = __values(kvs), kvs_1_1 = kvs_1.next(); !kvs_1_1.done; kvs_1_1 = kvs_1.next()) {
                    var _a = __read(kvs_1_1.value, 2), k = _a[0], v = _a[1];
                    r[k] = v;
                }
            } catch (e_1_1) {
                e_1 = {
                    error: e_1_1
                };
            } finally {
                try {
                    kvs_1_1 && !kvs_1_1.done && (_b = kvs_1.return) && _b.call(kvs_1);
                } finally {
                    if (e_1) throw e_1.error;
                }
            }
            return r;
        };
    },
    160: function(module, exports, __webpack_require__) {
        "use strict";
        var __values = this && this.__values || function(o) {
            var m = "function" == typeof Symbol && o[Symbol.iterator], i = 0;
            return m ? m.call(o) : {
                next: function() {
                    return o && i >= o.length && (o = void 0), {
                        value: o && o[i++],
                        done: !o
                    };
                }
            };
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.find = function(m, p) {
            try {
                for (var _a = __values(m.values()), _b = _a.next(); !_b.done; _b = _a.next()) {
                    var x = _b.value;
                    if (p(x)) return x;
                }
            } catch (e_1_1) {
                e_1 = {
                    error: e_1_1
                };
            } finally {
                try {
                    _b && !_b.done && (_c = _a.return) && _c.call(_a);
                } finally {
                    if (e_1) throw e_1.error;
                }
            }
            return null;
            var e_1, _c;
        };
    },
    161: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.second = 1e3, exports.minute = 60 * exports.second, exports.hour = 60 * exports.minute, 
        exports.day = 24 * exports.hour, exports.week = 7 * exports.day, exports.seconds = function(s) {
            return s * exports.second;
        }, exports.hertz = function(hz) {
            return exports.second / hz;
        };
    },
    162: function(module, exports, __webpack_require__) {
        "use strict";
        var extendStatics, __extends = this && this.__extends || (extendStatics = Object.setPrototypeOf || {
            __proto__: []
        } instanceof Array && function(d, b) {
            d.__proto__ = b;
        } || function(d, b) {
            for (var p in b) b.hasOwnProperty(p) && (d[p] = b[p]);
        }, function(d, b) {
            function __() {
                this.constructor = d;
            }
            extendStatics(d, b), d.prototype = null === b ? Object.create(b) : (__.prototype = b.prototype, 
            new __());
        }), __assign = this && this.__assign || Object.assign || function(t) {
            for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
            return t;
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var logConfig_1 = __webpack_require__(72), SimpleLogger = function(_super) {
            function SimpleLogger(name, _config) {
                var _this = _super.call(this, name) || this;
                return _this._config = _config, _this;
            }
            return __extends(SimpleLogger, _super), SimpleLogger.prototype.handleEvent = function(event) {
                this._config.filterFn(event) && this._config.writer.write(event);
            }, SimpleLogger;
        }(function() {
            function AbstractLogger(name) {
                this.name = name, this._isError = function(error) {
                    var errorLike = error;
                    return errorLike && (void 0 !== errorLike.message && void 0 !== errorLike.name || void 0 !== errorLike.stack);
                };
            }
            return AbstractLogger.prototype.trace = function(message, exceptionOrData, data) {
                this._logMessage("TRACE", message, exceptionOrData, data);
            }, AbstractLogger.prototype.debug = function(message, exceptionOrData, data) {
                this._logMessage("DEBUG", message, exceptionOrData, data);
            }, AbstractLogger.prototype.info = function(message, exceptionOrData, data) {
                this._logMessage("INFO", message, exceptionOrData, data);
            }, AbstractLogger.prototype.warn = function(message, exceptionOrData, data) {
                this._logMessage("WARN", message, exceptionOrData, data);
            }, AbstractLogger.prototype.error = function(message, exceptionOrData, data) {
                this._logMessage("ERROR", message, exceptionOrData, data);
            }, AbstractLogger.prototype.fatal = function(message, exceptionOrData, data) {
                this._logMessage("FATAL", message, exceptionOrData, data);
            }, AbstractLogger.prototype._logMessage = function(logLevel, message, exceptionOrData, data) {
                var event = {
                    level: logLevel,
                    loggerName: this.name,
                    message: message,
                    timestamp: new Date()
                };
                exceptionOrData && (this._isError(exceptionOrData) ? event.exception = exceptionOrData : event.data = exceptionOrData), 
                event.data = event.data || data, this.handleEvent(event);
            }, AbstractLogger;
        }());
        exports.SimpleLogger = SimpleLogger, function(Logger) {
            Logger.create = function(name, config) {
                return new SimpleLogger(name, __assign({}, logConfig_1.LogConfig.getGlobal(), config || {}));
            };
        }(exports.Logger || (exports.Logger = {}));
    },
    163: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var _a, logRank = ((_a = {}).TRACE = 1, _a.DEBUG = 2, _a.INFO = 3, _a.WARN = 4, 
        _a.ERROR = 5, _a.FATAL = 6, _a);
        exports.getLogRank = function(level) {
            return logRank[level] || 0;
        };
    },
    164: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var log_1 = __webpack_require__(28);
        function logLevelToFelogLogLevel(level) {
            return "INFO" === level || "TRACE" === level ? log_1.LogLevel.INFO : "WARN" === level ? log_1.LogLevel.WARN : "FATAL" === level || "ERROR" === level ? log_1.LogLevel.ERROR : log_1.LogLevel.INFO;
        }
        function logEventToFelogLogEvent(event) {
            var stringifiedData = "";
            try {
                stringifiedData = JSON.stringify(event.data);
            } catch (e) {}
            return {
                logger: event.loggerName,
                level: logLevelToFelogLogLevel(event.level),
                timestamp: +event.timestamp,
                message: event.message,
                extra: {
                    json: stringifiedData
                }
            };
        }
        exports.logLevelToFelogLogLevel = logLevelToFelogLogLevel, exports.logEventToFelogLogEvent = logEventToFelogLogEvent;
        var maxEventsToReport = 5e3, FelogLogWriter = function() {
            return function(_config) {
                var _this = this;
                this._config = _config, this._events = [], this.write = function(event) {
                    "DEBUG" !== event.level && (_this._events.push(event), _this._events.length > maxEventsToReport && _this._events.splice(0, _this._events.length - maxEventsToReport));
                }, this.send = function() {
                    0 !== _this._events.length && (_this._config.felog.sendCrashLogs("crash logs", _this._events.map(logEventToFelogLogEvent)), 
                    _this._events = []);
                };
            };
        }();
        exports.FelogLogWriter = FelogLogWriter;
    },
    182: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var logger_1 = __webpack_require__(1), stdlib_1 = __webpack_require__(3), PerformanceMetricsImpl = function() {
            function PerformanceMetricsImpl(_perf) {
                this._perf = _perf, this._log = logger_1.Logger.create("cs.telemetry.PerformanceMetricsImpl");
            }
            return PerformanceMetricsImpl.prototype.flushMeasures = function(name) {
                try {
                    var measures = this._perf.getEntriesByName(name, "measure");
                    return this._perf.clearMeasures(name), measures.map(function(x) {
                        return x.duration;
                    });
                } catch (err) {
                    return this._log.warn("failed to retrieve perf measurements", err), [];
                }
            }, PerformanceMetricsImpl.prototype.startMeasure = function(name) {
                var _this = this, salt = Math.random(), startName = "__" + name + "_" + salt + "-start", endName = "__" + name + "_" + salt + "-end";
                try {
                    this._perf.mark(startName);
                } catch (err) {
                    return this._log.warn("could not start measure – ignoring measurement", err), {
                        endMeasure: stdlib_1.noOp
                    };
                }
                var endMeasureCalled = !1;
                return {
                    endMeasure: function() {
                        if (!endMeasureCalled) {
                            endMeasureCalled = !0;
                            try {
                                _this._perf.mark(endName), _this._perf.measure(name, startName, endName);
                            } catch (err) {
                                _this._log.warn("could not complete measure", err);
                            }
                        }
                    }
                };
            }, PerformanceMetricsImpl.prototype.measure = function(name, fn) {
                var startName = "__" + name + "-start", endName = "__" + name + "-end";
                try {
                    this._perf.mark(startName);
                } catch (err) {
                    return this._log.warn("could not start measure – ignoring measurement", err), fn();
                }
                try {
                    return fn();
                } finally {
                    try {
                        this._perf.mark(endName), this._perf.measure(name, startName, endName);
                    } catch (err) {
                        this._log.warn("could not complete measure", err);
                    }
                }
            }, PerformanceMetricsImpl;
        }();
        exports.PerformanceMetricsImpl = PerformanceMetricsImpl, function(PerformanceMetrics) {
            PerformanceMetrics.dummy = {
                flushMeasures: function(_) {
                    return [];
                },
                measure: function(_, fn) {
                    return fn();
                },
                startMeasure: function(_) {
                    return {
                        endMeasure: function() {}
                    };
                }
            }, PerformanceMetrics.create = function(p) {
                return void 0 !== p ? new PerformanceMetricsImpl(p) : PerformanceMetrics.dummy;
            };
        }(exports.PerformanceMetrics || (exports.PerformanceMetrics = {}));
    },
    25: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var globalConfig = __webpack_require__(10).getGlobal();
        function isBg() {
            return "bg" === globalConfig.bundleInfo.context;
        }
        function isPopup() {
            return "popup" === globalConfig.bundleInfo.context;
        }
        exports.isTestsMode = function() {
            return !!window.__extensionTestsMode;
        }, exports.getUuid = function() {
            return globalConfig.appConfig.extensionId;
        }, exports.isFF = function() {
            return "firefox" === globalConfig.bundleInfo.browser;
        }, exports.isChrome = function() {
            return "chrome" === globalConfig.bundleInfo.browser;
        }, exports.isSafari = function() {
            return "safari" === globalConfig.bundleInfo.browser;
        }, exports.isEdge = function() {
            return "edge" === globalConfig.bundleInfo.browser;
        }, exports.isWindows = function() {
            return globalConfig.systemInfo.os.isWindows;
        }, exports.isBg = isBg, exports.isPopup = isPopup, exports.isBgOrPopup = function() {
            return isBg() || isPopup();
        }, exports.getBrowser = function() {
            return globalConfig.bundleInfo.browser;
        }, exports.getVersion = function() {
            return globalConfig.buildInfo.version;
        }, exports.ENV = globalConfig.bundleInfo.env, exports.URLS = globalConfig.appConfig.url, 
        exports.appName = globalConfig.appConfig.felog.appName, exports.gnarAppName = globalConfig.appConfig.gnar.appName, 
        exports.GRAMMARLY_DOMAIN = globalConfig.appConfig.url.grammarlyDomain;
    },
    28: function(module, exports, __webpack_require__) {
        "use strict";
        var LogLevel;
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), function(LogLevel) {
            LogLevel[LogLevel.INFO = 0] = "INFO", LogLevel[LogLevel.WARN = 1] = "WARN", LogLevel[LogLevel.ERROR = 2] = "ERROR";
        }(LogLevel = exports.LogLevel || (exports.LogLevel = {})), function(LogLevel) {
            LogLevel.toFelogString = function(l) {
                switch (l) {
                  case LogLevel.INFO:
                    return "INFO";

                  case LogLevel.WARN:
                    return "WARN";

                  case LogLevel.ERROR:
                    return "ERROR";

                  default:
                    throw new TypeError("Unrecognized log level " + l);
                }
            };
        }(LogLevel = exports.LogLevel || (exports.LogLevel = {})), exports.createEventPayload = function(event, appLevelData) {
            return {
                application: appLevelData.appName,
                version: appLevelData.appVersion,
                env: appLevelData.env,
                logger: event.logger,
                message: event.message,
                extra: event.extra,
                extra_usage: event.extra_usage,
                extra_performance: event.extra_performance,
                level: LogLevel.toFelogString(event.level),
                sessionId: appLevelData.context && appLevelData.sessionId,
                userId: appLevelData.context && appLevelData.context.userId,
                containerId: appLevelData.context && appLevelData.context.containerId,
                timestamp: event.timestamp
            };
        }, exports.felogRequestUrl = function(payload, baseUrl) {
            return baseUrl + "/log?json=" + encodeURIComponent(JSON.stringify(payload));
        }, exports.felogUsageRequestUrl = function(payload, baseUrl) {
            return baseUrl + "/log?json=" + encodeURIComponent(JSON.stringify(payload));
        };
    },
    3: function(module, exports, __webpack_require__) {
        "use strict";
        var extendStatics, __extends = this && this.__extends || (extendStatics = Object.setPrototypeOf || {
            __proto__: []
        } instanceof Array && function(d, b) {
            d.__proto__ = b;
        } || function(d, b) {
            for (var p in b) b.hasOwnProperty(p) && (d[p] = b[p]);
        }, function(d, b) {
            function __() {
                this.constructor = d;
            }
            extendStatics(d, b), d.prototype = null === b ? Object.create(b) : (__.prototype = b.prototype, 
            new __());
        });
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var assert_1 = __webpack_require__(156);
        exports.assert = assert_1.assert, exports.assertNonNull = assert_1.assertNonNull, 
        exports.AssertionError = assert_1.AssertionError;
        var promise_1 = __webpack_require__(63);
        exports.SafePromise = promise_1.SafePromise;
        var circularbuffer_1 = __webpack_require__(157);
        exports.CircularBuffer = circularbuffer_1.CircularBuffer;
        var promise_2 = __webpack_require__(63), Arr = __webpack_require__(158);
        exports.Arr = Arr;
        var Obj = __webpack_require__(159);
        exports.Obj = Obj;
        var MapEx = __webpack_require__(160);
        exports.MapEx = MapEx;
        var Ms = __webpack_require__(161);
        exports.Ms = Ms;
        var Global = function() {
            function Global(_getFallbackValue) {
                this._getFallbackValue = _getFallbackValue;
            }
            return Global.prototype.init = function(v) {
                if (void 0 !== this._value) throw new Error("Global value already initialized.");
                this._value = v;
            }, Global.prototype.get = function() {
                if (void 0 === this._value) {
                    if (void 0 === this._getFallbackValue) throw new Error("Global value not initialized and no fallback value provided.");
                    this._value = this._getFallbackValue();
                }
                return this._value;
            }, Global;
        }();
        function optionalStringUnion(allowedValues, value) {
            return allowedValues.some(function(x) {
                return x === value;
            }) ? value : void 0;
        }
        exports.Global = Global, exports.optionalStringUnion = optionalStringUnion, exports.assertStringUnion = function(allowedValues, value, name) {
            var validated = optionalStringUnion(allowedValues, value);
            if (void 0 !== validated) return validated;
            throw new TypeError('Unrecognized string union value "' + value + '"' + (name ? " for " + name : ""));
        };
        var MatchingNotExhaustiveError = function(_super) {
            function MatchingNotExhaustiveError(actualValue) {
                return _super.call(this, "Matching not exhaustive" + (actualValue ? ": unexpected value " + actualValue : "")) || this;
            }
            return __extends(MatchingNotExhaustiveError, _super), MatchingNotExhaustiveError;
        }(Error);
        function optionalIntString(val) {
            var parsed = parseInt(val, 10);
            return isNaN(parsed) ? void 0 : parsed;
        }
        exports.MatchingNotExhaustiveError = MatchingNotExhaustiveError, exports.assertNever = function(x) {
            throw new MatchingNotExhaustiveError(x);
        }, exports.optionalIntString = optionalIntString, exports.assertIntString = function(val, name) {
            var opt = optionalIntString(val);
            if (void 0 !== opt) return opt;
            throw new Error("Expected a number string, got '" + val + "'" + (void 0 !== name ? " for " + name : ""));
        }, exports.try_ = function(run, handle) {
            try {
                return run();
            } catch (err) {
                return handle(err);
            }
        }, exports.noOp = function() {}, exports.throttle = function(timeMs, fn) {
            var lastCallTs, result, gate = !0;
            function runIndeterminate(afterMs) {
                return gate && (gate = !1, result = promise_2.SafePromise.createCompletionSource(), 
                setTimeout(function() {
                    try {
                        result.resolve(fn());
                    } catch (err) {
                        result.reject(err);
                    } finally {
                        gate = !0;
                    }
                }, afterMs)), result.promise;
            }
            return function() {
                var oldLastCallTs = lastCallTs;
                return lastCallTs = Date.now(), runIndeterminate(void 0 === oldLastCallTs || lastCallTs - oldLastCallTs >= timeMs ? 0 : timeMs - (lastCallTs - oldLastCallTs));
            };
        };
        var LazyImpl = function() {
            function LazyImpl(_factory) {
                this._factory = _factory, this._hasValue = !1;
            }
            return LazyImpl.prototype.get = function() {
                return this._hasValue || (this._value = this._factory(), this._hasValue = !0), this._value;
            }, LazyImpl;
        }();
        exports.lazy = function(factory) {
            return new LazyImpl(factory);
        }, function(Guid) {
            function s4() {
                return (65536 * (1 + Math.random()) | 0).toString(16).substring(1);
            }
            Guid.create = function() {
                return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
            };
        }(exports.Guid || (exports.Guid = {}));
    },
    31: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var stdlib_1 = __webpack_require__(3);
        !function(TargetBrowser) {
            TargetBrowser.create = function(x) {
                return stdlib_1.optionalStringUnion([ "chrome", "safari", "firefox", "edge" ], x);
            }, TargetBrowser.detect = function(win) {
                return win.chrome && /google/i.test(win.navigator.vendor) ? "chrome" : -1 !== win.navigator.userAgent.indexOf("Firefox") ? "firefox" : /^((?!chrome).)*safari/i.test(win.navigator.userAgent) ? "safari" : "Netscape" === win.navigator.appName && win.navigator.appVersion.indexOf("Edge") > -1 ? "edge" : void 0;
            };
        }(exports.TargetBrowser || (exports.TargetBrowser = {})), function(TargetEnv) {
            TargetEnv.create = function(x) {
                return stdlib_1.optionalStringUnion([ "dev", "prod", "qa" ], x);
            };
        }(exports.TargetEnv || (exports.TargetEnv = {})), function(TargetContext) {
            TargetContext.create = function(x) {
                return stdlib_1.optionalStringUnion([ "bg", "cs", "popup" ], x);
            }, TargetContext.detect = function(win, browser) {
                var isBg = !!win.IS_BG, isPopup = "safari" === browser ? function() {
                    try {
                        return win.safari.extension.globalPage.contentWindow !== win;
                    } catch (_) {
                        return !1;
                    }
                }() : !!win.IS_POPUP;
                return isBg ? "bg" : isPopup ? "popup" : "cs";
            };
        }(exports.TargetContext || (exports.TargetContext = {})), function(BundleInfo) {
            BundleInfo.create = function(browser, env, context) {
                return {
                    browser: browser,
                    env: env,
                    context: context
                };
            };
        }(exports.BundleInfo || (exports.BundleInfo = {}));
    },
    61: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.ports = {
            bridge: "bridge",
            background: "message:to-priv",
            broadcast: "message:to-non-priv"
        };
    },
    63: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), function(SafePromise) {
            function create(run) {
                return new Promise(run);
            }
            SafePromise.create = create, SafePromise.createCompletionSource = function() {
                var res, rej;
                return {
                    promise: new Promise(function(res_, rej_) {
                        res = res_, rej = rej_;
                    }),
                    resolve: function(v) {
                        res(v);
                    },
                    reject: function(err) {
                        rej(err);
                    }
                };
            }, SafePromise.sync = function(run) {
                return create(function(r, _) {
                    return r(run());
                });
            };
        }(exports.SafePromise || (exports.SafePromise = {}));
    },
    68: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var stdlib_1 = __webpack_require__(3), url_1 = __webpack_require__(69), services_1 = __webpack_require__(70);
        !function(AppConfig) {
            var forgeExtensionId = "87677a2c52b84ad3a151a4a72f5bd3c4", grammarlyProdDomain = "grammarly.com", newsVersion = 0;
            AppConfig.create = function(browser, env, edgePopupUrl, emptyScriptUrl) {
                var felogUrl = "prod" === env ? "https://f-log-extension.grammarly.io" : "qa" === env || "dev" === env ? "https://127.0.0.1:8000" : stdlib_1.assertNever(env), sumoLogicUrl = "prod" === env ? "https://endpoint2.collection.us2.sumologic.com/receiver/v1/http/ZaVnC4dhaV1OF-4ic11yqpre0casnyvs_ZoaCHciEYdRyBkrfwP6DMlsWt8tSVU76RPqgGvAGjXGQk_UNuxPx-pYbToJapM_Fr0CUcgKaA8_IVl-lhSr5Q==" : "qa" === env || "dev" === env ? "https://127.0.0.1:8000" : stdlib_1.assertNever(env), gnarDomain = "prod" === env ? grammarlyProdDomain : "qa" === env || "dev" === env ? "qagr.io" : stdlib_1.assertNever(env);
                return {
                    url: url_1.UrlConfig.create(grammarlyProdDomain, felogUrl, sumoLogicUrl, edgePopupUrl, emptyScriptUrl),
                    gnar: services_1.GnarConfig.create(browser, gnarDomain),
                    felog: services_1.FelogConfig.create(browser),
                    sumologic: services_1.SumoLogicConfig.create(browser),
                    capi: services_1.CapiConfig.create(),
                    extensionId: forgeExtensionId,
                    newsVersion: newsVersion
                };
            };
        }(exports.AppConfig || (exports.AppConfig = {}));
    },
    69: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        }), function(UrlConfig) {
            UrlConfig.create = function(grammarlyDomain, felogUrl, sumologicUrl, edgePopupUrl, emptyScriptUrl) {
                var funnel = "https://www." + grammarlyDomain, dapi = "https://data." + grammarlyDomain, editor = "https://app." + grammarlyDomain, auth = "https://auth." + grammarlyDomain + "/v3";
                return {
                    app: editor,
                    appPersonalDictionary: editor + "/profile/dictionary",
                    capi: "wss://capi." + grammarlyDomain + "/freews",
                    capiGDocs: "wss://capi." + grammarlyDomain + "/gdocs",
                    dapiMimic: dapi + "/api/mimic",
                    dapiProps: dapi + "/api/props/v2",
                    editorDictionary: editor + "/profile/dictionary",
                    dictionary: "https://capi." + grammarlyDomain + "/api/defs",
                    docs: editor + "/docs",
                    docsApi: "https://dox." + grammarlyDomain + "/documents",
                    newDoc: editor + "/docs/new",
                    userOrAnonymous: auth + "/user/oranonymous",
                    authSignin: auth + "/api/login",
                    authSignup: auth + "/api/signup",
                    signin: funnel + "/signin",
                    signup: funnel + "/signup",
                    fbSignin: funnel + "/signin?fromExtensionFb=true",
                    fbSignup: funnel + "/signup?fromExtensionFb=true",
                    googleSignin: funnel + "/signin?fromExtensionGoogle=true",
                    googleSignup: funnel + "/signup?fromExtensionGoogle=true",
                    resetPassword: funnel + "/resetpassword",
                    newFelog: felogUrl,
                    sumoLogic: sumologicUrl,
                    welcomeC: funnel + "/extension-success",
                    afterInstall: funnel + "/after_install_page",
                    upgrade: funnel + "/upgrade",
                    uninstall: funnel + "/extension-uninstall",
                    terms: funnel + "/terms",
                    policy: funnel + "/privacy-policy",
                    pageConfigUrl: "https://d3cv4a9a9wh0bt.cloudfront.net/browserplugin/config.json",
                    edgePopupUrl: edgePopupUrl,
                    emptyScriptUrl: emptyScriptUrl,
                    grammarlyDomain: grammarlyDomain
                };
            };
        }(exports.UrlConfig || (exports.UrlConfig = {}));
    },
    70: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var stdlib_1 = __webpack_require__(3);
        !function(GnarConfig) {
            var gnarAppName = {
                chrome: "chromeExt",
                firefox: "firefoxExt",
                safari: "safariExt",
                edge: "edgeExt"
            };
            GnarConfig.create = function(browserType, domain) {
                return {
                    appName: stdlib_1.assertNonNull(gnarAppName[browserType], "gnar app name"),
                    url: "https://gnar." + domain,
                    domain: "." + domain,
                    sendEmailInfoTracking: !0,
                    googleAnalyticsId: "UA-6331378-16"
                };
            };
        }(exports.GnarConfig || (exports.GnarConfig = {})), function(FelogConfig) {
            var felogAppName = {
                chrome: "extensionChrome",
                firefox: "extensionFirefox",
                safari: "extensionSafari",
                edge: "extensionEdge"
            };
            FelogConfig.create = function(browser) {
                return {
                    appName: stdlib_1.assertNonNull(felogAppName[browser], "felog app name"),
                    sendUsageMetrics: "chrome" === browser,
                    sendPerfMetrics: !1
                };
            };
        }(exports.FelogConfig || (exports.FelogConfig = {})), function(SumoLogicConfig) {
            var sumoLogicAppName = {
                chrome: "extensionChrome",
                firefox: "extensionFirefox",
                safari: "extensionSafari",
                edge: "extensionEdge"
            };
            SumoLogicConfig.create = function(browser) {
                return {
                    appName: stdlib_1.assertNonNull(sumoLogicAppName[browser], "sumologic app name")
                };
            };
        }(exports.SumoLogicConfig || (exports.SumoLogicConfig = {})), function(CapiConfig) {
            CapiConfig.create = function() {
                return {
                    sendEmailData: !0
                };
            };
        }(exports.CapiConfig || (exports.CapiConfig = {}));
    },
    71: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var stdlib_1 = __webpack_require__(3), log = __webpack_require__(1).Logger.create("config.build");
        !function(BuildInfo) {
            BuildInfo.create = function(major, minor, patch, browser, env, branch, commit) {
                var branch_ = void 0 !== branch && void 0 !== commit ? branch : "UNVERSIONED", manifestVersion = major + "." + minor + "." + patch;
                return {
                    version: manifestVersion,
                    fullVersion: manifestVersion + "-" + [ browser, [ "prod" !== env ? env : null, branch_ !== browser ? branch_ : null ].filter(function(x) {
                        return !!x;
                    }).join(".") ].filter(function(x) {
                        return "" !== x;
                    }).join("/"),
                    commitHash: commit,
                    gitBranch: branch
                };
            }, BuildInfo.getManifestVersion = function(browser, context, win) {
                try {
                    switch (browser) {
                      case "safari":
                        switch (context) {
                          case "bg":
                          case "popup":
                            return win.safari.extension.displayVersion;

                          default:
                            return;
                        }

                      case "chrome":
                        return win.chrome.runtime.getManifest().version;

                      case "firefox":
                        return win.firefox.runtime.getManifest().version;

                      case "edge":
                        return win.edge.runtime.getManifest().version;

                      default:
                        return stdlib_1.assertNever(browser);
                    }
                } catch (e) {
                    return void log.error("Could not get extension version from manifest", e);
                }
            };
        }(exports.BuildInfo || (exports.BuildInfo = {}));
    },
    72: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var logWriter_1 = __webpack_require__(73), logFilter_1 = __webpack_require__(74);
        !function(LogConfig) {
            LogConfig.defaultConfig = {
                writer: new logWriter_1.ConsoleLogWriter({
                    useColors: !1
                }),
                filterFn: function(_) {
                    return !0;
                }
            };
            var globalConfig = LogConfig.defaultConfig;
            function updateGlobal(updates) {
                globalConfig = Object.assign({}, globalConfig, updates);
            }
            LogConfig.getGlobal = function() {
                return globalConfig;
            }, LogConfig.updateGlobal = updateGlobal, LogConfig.configure = function(options) {
                updateGlobal({
                    writer: new logWriter_1.ConsoleLogWriter({
                        useColors: !options.edge
                    }),
                    filterFn: options.prodCs ? logFilter_1.logLevelFilter("ERROR") : function(_) {
                        return !0;
                    }
                });
            };
        }(exports.LogConfig || (exports.LogConfig = {}));
    },
    73: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var FunctionLogWriter = function() {
            return function(write) {
                this.write = write;
            };
        }();
        exports.FunctionLogWriter = FunctionLogWriter;
        var _a, ConsoleLogWriter = function() {
            function ConsoleLogWriter(_config) {
                void 0 === _config && (_config = {
                    useColors: !0
                }), this._config = _config, this._writeColor = function(event) {
                    var cfg = ConsoleLogWriter._outputConfigMap[event.level];
                    if (cfg) {
                        var exceptionOrData = event.data || event.exception, data = event.data && event.exception;
                        cfg.writeFunc("%c" + event.loggerName + "%c %c" + event.level + "%c %c" + event.message, "font-weight: bold; color: #00b", "", "color: " + cfg.foreground + "; background: " + cfg.background, "", "", "", exceptionOrData || "", data || "");
                    }
                }, this._writeMonochrome = function(event) {
                    var cfg = ConsoleLogWriter._outputConfigMap[event.level];
                    if (cfg) {
                        var exceptionOrData = event.data || event.exception, data = event.data && event.exception;
                        cfg.writeFunc(event.loggerName + " [" + event.level + "] " + event.message, exceptionOrData || "", data || "", "", "", "", "", "", "");
                    }
                }, this.write = this._config.useColors ? this._writeColor : this._writeMonochrome;
            }
            return ConsoleLogWriter._outputConfigMap = ((_a = {}).TRACE = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.log(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "#fff",
                background: "#bbb"
            }, _a.DEBUG = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.log(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "#fff",
                background: "#666"
            }, _a.INFO = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.info(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "#000",
                background: ""
            }, _a.WARN = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.warn(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "",
                background: ""
            }, _a.ERROR = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.error(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "",
                background: ""
            }, _a.FATAL = {
                writeFunc: function(a0, a1, a2, a3, a4, a5, a6, a7, a8) {
                    return console.error(a0, a1, a2, a3, a4, a5, a6, a7, a8);
                },
                foreground: "#fff",
                background: "#f00"
            }, _a), ConsoleLogWriter;
        }();
        exports.ConsoleLogWriter = ConsoleLogWriter;
    },
    74: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var common_1 = __webpack_require__(163);
        exports.logLevelFilter = function(level) {
            return function(event) {
                return common_1.getLogRank(event.level) >= common_1.getLogRank(level);
            };
        };
    },
    75: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var BrowserInfo, OsInfo, bundle_1 = __webpack_require__(31), stdlib_1 = __webpack_require__(3);
        !function(BrowserInfo) {
            BrowserInfo.create = function(targetBrowser, win) {
                return {
                    type: bundle_1.TargetBrowser.detect(win) || "other",
                    isWE: "firefox" === targetBrowser ? stdlib_1.try_(function() {
                        return !!firefox.runtime;
                    }, function(_) {
                        return !1;
                    }) : "chrome" === targetBrowser || "edge" === targetBrowser
                };
            };
        }(BrowserInfo = exports.BrowserInfo || (exports.BrowserInfo = {})), function(OsInfo) {
            OsInfo.create = function(win) {
                return {
                    isWindows: -1 !== win.navigator.appVersion.indexOf("Win")
                };
            };
        }(OsInfo = exports.OsInfo || (exports.OsInfo = {})), function(SystemInfo) {
            SystemInfo.create = function(targetBrowser, win) {
                return {
                    browser: BrowserInfo.create(targetBrowser, win),
                    os: OsInfo.create(win)
                };
            };
        }(exports.SystemInfo || (exports.SystemInfo = {}));
    },
    76: function(module, exports, __webpack_require__) {
        "use strict";
        var __read = this && this.__read || function(o, n) {
            var m = "function" == typeof Symbol && o[Symbol.iterator];
            if (!m) return o;
            var r, e, i = m.call(o), ar = [];
            try {
                for (;(void 0 === n || n-- > 0) && !(r = i.next()).done; ) ar.push(r.value);
            } catch (error) {
                e = {
                    error: error
                };
            } finally {
                try {
                    r && !r.done && (m = i.return) && m.call(i);
                } finally {
                    if (e) throw e.error;
                }
            }
            return ar;
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var app_1 = __webpack_require__(68), build_1 = __webpack_require__(71), system_1 = __webpack_require__(75), bundle_1 = __webpack_require__(31), stdlib_1 = __webpack_require__(3), log = __webpack_require__(1).Logger.create("config.mainConfig");
        !function(ProcessEnv) {
            function create(env, major_number, build_number, release_number, git_branch, git_commit, edge_popup_url, empty_script_url) {
                return {
                    env: env,
                    major_number: major_number,
                    build_number: build_number,
                    release_number: release_number,
                    git_branch: git_branch,
                    git_commit: git_commit,
                    edge_popup_url: edge_popup_url,
                    empty_script_url: empty_script_url
                };
            }
            ProcessEnv.create = create, ProcessEnv.fromBrowserify = function() {
                return create("prod", "14", "848", "1663", "UNVERSIONED", "4c6ce505d14dd9ba5fe5cccdd8c53a9097f7acca", "", "");
            };
        }(exports.ProcessEnv || (exports.ProcessEnv = {})), function(MainConfig) {
            MainConfig.create = function(browser, context, processEnv) {
                var env_;
                if (processEnv.env) {
                    var e = bundle_1.TargetEnv.create(processEnv.env);
                    void 0 !== e ? env_ = e : (log.warn("*** process.env.ENV is invalid ('" + processEnv.env + "'), assuming 'prod' env"), 
                    env_ = "prod");
                } else log.warn("*** process.env.ENV is not defined, assuming 'prod' env"), env_ = "prod";
                var finalVersion, env = stdlib_1.assertNonNull(env_, "ENV env var OR a fallback value"), processEnvVersion = [ processEnv.major_number, processEnv.build_number, processEnv.release_number ].map(stdlib_1.optionalIntString);
                if (3 === processEnvVersion.length && processEnvVersion.every(function(x) {
                    return void 0 !== x;
                })) finalVersion = processEnvVersion; else {
                    var manifestVersion = (build_1.BuildInfo.getManifestVersion(browser, context, window) || "").split(".").map(stdlib_1.optionalIntString);
                    finalVersion = 3 === manifestVersion.length && manifestVersion.every(function(x) {
                        return void 0 !== x;
                    }) ? manifestVersion : [ 0, 0, 0 ];
                }
                var _a = __read(finalVersion, 3), versionMajor = _a[0], versionMinor = _a[1], versionPatch = _a[2];
                return {
                    buildInfo: build_1.BuildInfo.create(versionMajor, versionMinor, versionPatch, browser, env, processEnv.git_branch, processEnv.git_commit),
                    bundleInfo: bundle_1.BundleInfo.create(browser, env, context),
                    appConfig: app_1.AppConfig.create(browser, env, processEnv.edge_popup_url, processEnv.empty_script_url),
                    systemInfo: system_1.SystemInfo.create(browser, window)
                };
            };
        }(exports.MainConfig || (exports.MainConfig = {}));
    },
    97: function(module, exports, __webpack_require__) {
        "use strict";
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var performanceMetrics_1 = __webpack_require__(182);
        exports.PerformanceMetrics = performanceMetrics_1.PerformanceMetrics;
    }
});