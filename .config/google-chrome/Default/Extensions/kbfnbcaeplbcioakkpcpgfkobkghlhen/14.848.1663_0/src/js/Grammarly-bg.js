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
    }, __webpack_require__.p = "", __webpack_require__(__webpack_require__.s = 1134);
}([ , function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    }, __spread = this && this.__spread || function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var transform = __webpack_require__(118), nch = __webpack_require__(194), newConfig_1 = __webpack_require__(25), newConfig_2 = __webpack_require__(25);
    function interval(cb, time) {
        var items = interval.items = interval.items || {}, item = items[cb];
        if (item || time) {
            if (item && !time) return clearTimeout(item), void delete items[cb];
            !function() {
                function _cb() {
                    timeout(), cb();
                }
                function timeout() {
                    var tid = setTimeout(_cb, time);
                    items[cb] = tid;
                }
                timeout();
            }();
        }
    }
    function s4() {
        return (65536 * (1 + Math.random()) | 0).toString(16).substring(1);
    }
    function _f() {}
    function delay(ms) {
        return new Promise(function(resolve) {
            return setTimeout(resolve, ms);
        });
    }
    exports.isTestsMode = newConfig_2.isTestsMode, exports.getBrowser = newConfig_2.getBrowser, 
    exports.isBg = newConfig_2.isBg, exports.isBgOrPopup = newConfig_2.isBgOrPopup, 
    exports.isChrome = newConfig_2.isChrome, exports.isFF = newConfig_2.isFF, exports.isPopup = newConfig_2.isPopup, 
    exports.isSafari = newConfig_2.isSafari, exports.isEdge = newConfig_2.isEdge, exports.isWindows = newConfig_2.isWindows, 
    exports.chromeBgError = function() {
        return window.chrome && window.chrome.runtime && window.chrome.runtime.lastError;
    }, exports.isFunction = function(obj) {
        return !!(obj && obj.constructor && obj.call && obj.apply);
    }, exports.interval = interval, function(interval) {
        interval.items = {};
    }(interval = exports.interval || (exports.interval = {})), exports.cancelInterval = function(cb) {
        interval(cb);
    }, exports.guid = function() {
        return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
    }, exports.bytes = function(str) {
        for (var codePoint, next, result = 0, len = str.length, i = 0; i < len; i++) (codePoint = str.charCodeAt(i)) >= 55296 && codePoint < 57344 && codePoint < 56320 && i + 1 < len && (next = str.charCodeAt(i + 1)) >= 56320 && next < 57344 ? (result += 4, 
        i++) : result += codePoint < 128 ? 1 : codePoint < 2048 ? 2 : 3;
        return result;
    }, exports.chunks = function(s, len) {
        for (var curr = len, prev = 0, result = []; s[curr]; ) if (" " === s[curr++]) result.push(s.substring(prev, curr)), 
        prev = curr, curr += len; else {
            var currReverse = curr;
            do {
                if (" " === s.substring(currReverse - 1, currReverse)) {
                    result.push(s.substring(prev, currReverse)), prev = currReverse, curr = currReverse + len;
                    break;
                }
                currReverse--;
            } while (currReverse > prev);
        }
        return result.push(s.substr(prev)), result;
    }, exports._f = _f, exports._F = function() {
        return !0;
    }, exports.bgPageReload = function() {
        window.chrome && window.chrome.runtime && window.chrome.runtime.reload ? window.chrome.runtime.reload() : window.location.reload();
    }, exports.isGmail = function(doc) {
        if (doc.location) {
            var host = "mail.google.com" == doc.location.host, frames = doc.querySelector("iframe#js_frame") && doc.querySelector("iframe#sound_frame");
            return host || frames;
        }
    }, exports.isValidEmail = function(value) {
        return /^[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+@[-!#$%&\'*+\\/0-9=?A-Z^_`a-z{|}~]+\.[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+$/.test(value);
    }, exports.formatNumber = function(i) {
        return i.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }, exports.declension = function(value, arr) {
        return arr[1 == value ? 0 : 1];
    }, exports.stub = function(methods) {
        return transform(methods, function(result, m) {
            return result[m] = _f;
        });
    }, exports.memoize = function(func, resolver, ttl) {
        var cache = {};
        return function() {
            var key = "_memoize_" + (resolver ? resolver.apply(this, arguments) : arguments[0]);
            return window.hasOwnProperty.call(cache, key) ? cache[key] : (ttl && setTimeout(function() {
                delete cache[key];
            }, ttl), cache[key] = func.apply(this, arguments));
        };
    }, exports.syncWait = function(promise, methods) {
        return Object.keys(methods).reduce(function(obj, method) {
            return Object.assign({}, obj, ((_a = {})[method] = function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return promise.then(function() {
                    return methods[method].apply(methods, __spread(args));
                });
            }, _a));
            var _a;
        }, {});
    }, exports.promisify = function(method) {
        return new Promise(function(resolve) {
            return method(resolve);
        });
    }, exports.getRandomIntInclusive = function(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }, exports.delay = delay;
    var months = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
    exports.formatDate = function(dateStr) {
        if (dateStr) {
            var date = new Date(dateStr);
            if ("Invalid Date" !== date.toString()) return months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();
        }
    }, exports.createClass = function(getPrototype) {
        var _class = function() {};
        return _class.prototype = getPrototype(), _class;
    }, exports.versionComparator = function(v1, v2) {
        function splitToArray(str) {
            return str.split(".").map(function(el) {
                return Number(el) || 0;
            });
        }
        void 0 === v1 && (v1 = ""), void 0 === v2 && (v2 = "");
        var v1arr = splitToArray(v1), v2arr = splitToArray(v2), postfix = Array(Math.abs(v1arr.length - v2arr.length)).fill(0);
        if (v1arr.length > v2arr.length ? v2arr.push.apply(v2arr, __spread(postfix)) : v1arr.push.apply(v1arr, __spread(postfix)), 
        v1arr.every(function(v, i) {
            return v === v2arr[i];
        })) return 0;
        for (var i = 0, len = v1arr.length; i < len; i++) {
            if (v1arr[i] > v2arr[i]) return 1;
            if (v1arr[i] < v2arr[i]) return -1;
        }
        return -1;
    }, exports.isBgAlive = function() {
        return __awaiter(this, void 0, void 0, function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    if (!newConfig_1.isChrome() && !newConfig_1.isFF()) return [ 2, null ];
                    _a.label = 1;

                  case 1:
                    return _a.trys.push([ 1, 3, , 4 ]), [ 4, Promise.race([ new Promise(function(resolve) {
                        return window.chrome.runtime.sendMessage("ping", resolve);
                    }), delay(1e4).then(function(_) {
                        return "timeouted";
                    }) ]) ];

                  case 2:
                    return [ 2, _a.sent() ];

                  case 3:
                    return _a.sent(), [ 2, "orphaned" ];

                  case 4:
                    return [ 2 ];
                }
            });
        });
    }, exports.asyncCall = function(cb, time) {
        void 0 === time && (time = 10), setTimeout(cb, time);
    }, exports.createChannel = function(_a) {
        var _b = (void 0 === _a ? {} : _a).buffered, buffered = void 0 === _b || _b, messageQueue = [], resolveQueue = [];
        return {
            take: function() {
                return messageQueue.length ? Promise.resolve(messageQueue.shift()) : new Promise(function(resolve) {
                    return resolveQueue.push(resolve);
                });
            },
            put: function(msg) {
                resolveQueue.length > 0 ? resolveQueue.shift()(msg) : buffered ? messageQueue.push(msg) : messageQueue[0] = msg;
            }
        };
    }, exports.normalizedHashCode = function(str, base) {
        if (void 0 === base && (base = 100), !str) return NaN;
        var algo = nch.createHash("superfasthash");
        return parseInt(algo.hash(str), 16) % base;
    }, exports.keyCode = function(event) {
        return event.which || event.charCode || event.keyCode || 0;
    }, exports.NBSP_RE = new RegExp(String.fromCharCode(160), "g");
    var nbsp = String.fromCharCode(160), reBr = /\n/g, reLastSpace = /\s$/g, reBrSpace = new RegExp("\n" + String.fromCharCode(32), "g");
    exports.br = function(val, last) {
        return val = val.replace(reBrSpace, "<br>" + nbsp).replace(reBr, "<br>"), last && (val = val.replace(reLastSpace, nbsp)), 
        val;
    }, exports.trimLeft = function(s) {
        return s.replace(/^\s+/, "");
    }, exports.trimRight = function(s) {
        return s.replace(/\s+$/, "");
    }, exports.SECOND = 1e3, exports.MINUTE = 60 * exports.SECOND, exports.HOUR = 60 * exports.MINUTE, 
    exports.DAY = 24 * exports.HOUR, exports.ESC_KEY = 27, exports.ENTER_KEY = 13, exports.pastDays = function(date) {
        return Math.round(Math.abs(+new Date() - +new Date(date)) / exports.DAY);
    }, exports.getNextPingDate = function() {
        var now = new Date();
        return now.getHours() > 2 && now.setDate(now.getDate() + 1), now.setHours(3), now.setMinutes(Math.floor(60 * Math.random())), 
        now.getTime();
    }, exports.escapeRegExp = function(str) {
        return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
    };
}, function(module, exports, __webpack_require__) {
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
}, , , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var call_1 = __webpack_require__(115);
    exports.call = call_1.call, exports.getLog = call_1.getLog, exports.logCall = call_1.logCall;
    var logger_1 = __webpack_require__(188);
    exports.felog = logger_1.felog;
}, function(module, exports) {
    var isArray = Array.isArray;
    module.exports = isArray;
}, function(module, exports) {
    module.exports = function(value) {
        var type = typeof value;
        return null != value && ("object" == type || "function" == type);
    };
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
    });
    var Config = __webpack_require__(10), newConfig_1 = __webpack_require__(25);
    exports.isTestsMode = newConfig_1.isTestsMode, exports.getVersion = newConfig_1.getVersion, 
    exports.getUuid = newConfig_1.getUuid, exports.ENV = newConfig_1.ENV, exports.URLS = newConfig_1.URLS, 
    exports.GRAMMARLY_DOMAIN = newConfig_1.GRAMMARLY_DOMAIN, exports.appName = newConfig_1.appName, 
    exports.gnarAppName = newConfig_1.gnarAppName;
    exports.GNAR = Config.getGlobal().appConfig.gnar, exports.news = [ "The G logo gets out of the way when you're typing", "Switch between American, British, Australian, and Canadian English", "Quickly disable checking in certain types of text fields", "A fully redesigned and improved interface" ], 
    exports.userFields = [ "id", "email", "firstName", "anonymous", "type", "subscriptionFree", "experiments", "isTest", "premium", "settings", "registrationDate", "mimic", "groups", "extensionInstallDate", "fixed_errors" ], 
    exports.userFields.push("token"), exports.nextVerClass = "gr_ver_2", exports.grammarlyAttrs = [ "data-gramm_editor", "data-gramm", "data-gramm_id", "gramm_editor" ], 
    exports.restrictedAttrs = __spread(exports.grammarlyAttrs, [ "readonly", "disabled" ]), 
    exports.customFieldsRestrictedAttrs = [ "pm-container", [ "class", "ProseMirror" ], "data-synchrony", [ "data-gramm", "false" ], [ "data-enable-grammarly", "false" ], [ "class", "redactor-layer" ], [ "class", "redactor-editor" ], [ "class", "ck-editor__editable" ], [ "class", "redactor_box" ], [ "aria-label", "Search Facebook" ] ], 
    exports.allRestrictedAttrs = __spread(exports.restrictedAttrs, exports.customFieldsRestrictedAttrs), 
    exports.forceEnableAttr = {
        name: "data-enable-grammarly",
        value: "true"
    }, exports.restrictedParentAttrs = "[data-reactid]", exports.externalEvents = [ "changed-user", "changed-plan", "changed-dialect", "cleanup", "editor-fix" ], 
    exports.development = "127.0.0.1:3117" === document.location.host;
}, function(module, exports, __webpack_require__) {
    var freeGlobal = __webpack_require__(122), freeSelf = "object" == typeof self && self && self.Object === Object && self, root = freeGlobal || freeSelf || Function("return this")();
    module.exports = root;
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    (function(process) {
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
        }, __spread = this && this.__spread || function() {
            for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
            return ar;
        };
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var throttle = __webpack_require__(180), emitter = __webpack_require__(18), util_1 = __webpack_require__(2), events_1 = __webpack_require__(139), extension_api_1 = __webpack_require__(66), message = (process && process.env, 
        extension_api_1.getGlobalExtensionApi()).message, errorEmitter = emitter({}), Listeners = {};
        function on(type, callback) {
            if ("__bgerror" !== type) {
                var listeners = Listeners[type] = Listeners[type] || [];
                if (listeners.push(callback), 1 === listeners.length) try {
                    message.listen(type, function() {
                        for (var e_1, _a, args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                        try {
                            for (var listeners_1 = __values(listeners), listeners_1_1 = listeners_1.next(); !listeners_1_1.done; listeners_1_1 = listeners_1.next()) {
                                listeners_1_1.value.apply(void 0, __spread(args));
                            }
                        } catch (e_1_1) {
                            e_1 = {
                                error: e_1_1
                            };
                        } finally {
                            try {
                                listeners_1_1 && !listeners_1_1.done && (_a = listeners_1.return) && _a.call(listeners_1);
                            } finally {
                                if (e_1) throw e_1.error;
                            }
                        }
                    });
                } catch (e) {
                    exports.emitError(e);
                }
            } else errorEmitter.on("__bgerror", callback);
        }
        function off(type, callback) {
            if ("__bgerror" !== type) {
                var listeners = Listeners[type];
                if (listeners) {
                    var i = listeners.indexOf(callback);
                    -1 !== i && listeners.splice(i, 1), 0 === listeners.length && delete Listeners[type];
                }
            } else errorEmitter.off("__bgerror", callback);
        }
        exports.emitError = throttle(function(e) {
            return errorEmitter.emit("__bgerror", e);
        }, 1e3), util_1.isBg() && events_1.listen(document, "grammarly:offline", function() {
            return exports.emitError("proxy dead");
        }, void 0), exports.one = function(type, cb) {
            on(type, function _cb() {
                for (var data = [], _i = 0; _i < arguments.length; _i++) data[_i] = arguments[_i];
                off(type, _cb), cb.apply(this, data);
            });
        }, exports.on = on, exports.off = off, exports.emitTabs = function(type) {
            try {
                switch (message.kind) {
                  case "background-message-api":
                    message.broadcast(type, {});
                    break;

                  default:
                    throw new Error("emitTabs can be used only on background");
                }
            } catch (e) {
                exports.emitError(e);
            }
        }, exports.emitTo = function(tabId, type, content, _callback) {
            void 0 === content && (content = {});
            var callback = _callback || function() {};
            try {
                if (!tabId) throw TypeError("emitTo can't be used without destination point");
                switch (message.kind) {
                  case "background-message-api":
                    message.sendTo(tabId, type, content, callback);
                    break;

                  default:
                    throw new Error("emitTo can be used only on background");
                }
            } catch (e) {
                exports.emitError(e);
            }
        }, exports.emitFocusedTab = function(type, content) {
            try {
                message.toFocused(type, content);
            } catch (e) {
                exports.emitError(e);
            }
        }, exports.emitBackground = function(type, content, callback) {
            try {
                switch (message.kind) {
                  case "content-script-message-api":
                    message.broadcastBackground(type, content, callback);
                    break;

                  default:
                    throw new Error("emitBackground can be used only in content script");
                }
            } catch (e) {
                exports.emitError(e);
            }
        }, exports.promiseBackground = function(type, data, timeout) {
            void 0 === data && (data = {}), void 0 === timeout && (timeout = 1e4);
            var request = new Promise(function(resolve, reject) {
                try {
                    switch (message.kind) {
                      case "content-script-message-api":
                        message.broadcastBackground(type, data, resolve, reject);
                        break;

                      default:
                        throw new Error("promiseBackground can be used only on client scripts");
                    }
                } catch (e) {
                    reject(e), exports.emitError(e);
                }
            });
            return Promise.race([ request, util_1.delay(timeout).then(function() {
                throw new Error("Request to bg page (" + message + ") rejected by timeout");
            }) ]);
        };
    }).call(exports, __webpack_require__(60));
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var util_1 = __webpack_require__(2), defaults_1 = __webpack_require__(109), stdlib_1 = __webpack_require__(3), stripDomain = function(domain) {
        return domain.replace("www.", "");
    };
    function currentUrl(_a) {
        var _this = this, tabs = _a.tabs;
        return stdlib_1.SafePromise.create(function(resolve) {
            return __awaiter(_this, void 0, void 0, function() {
                var retry, url;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return retry = setTimeout(function() {
                            return tabs.getActiveTabUrl().then(resolve);
                        }, 2e3), [ 4, tabs.getActiveTabUrl() ];

                      case 1:
                        return url = _a.sent(), clearTimeout(retry), resolve(url), [ 2 ];
                    }
                });
            });
        });
    }
    function getDomain(el) {
        var doc = el && el.ownerDocument || document, location = doc.location || doc.defaultView.location;
        return location ? stripDomain(location.hostname) : "";
    }
    function domainFromUrl(url) {
        if (util_1.isFF() && /^about:/.test(url)) return url;
        var location = document.createElement("a");
        return location.href = url, stripDomain(location.hostname);
    }
    function getUrl(el) {
        var doc = el && el.ownerDocument || document, location = doc.location || doc.defaultView.location;
        return location ? location.pathname + location.search : "";
    }
    exports.currentUrl = currentUrl, exports.getDomain = getDomain, exports.promiseGetDomain = function(api) {
        return Promise.race([ currentUrl(api).then(domainFromUrl), util_1.delay(1e4).then(function() {
            throw new Error("Request to tabs.getCurrentTabUrl rejected by timeout");
        }) ]);
    }, exports.domainFromUrl = domainFromUrl, exports.isFacebookSite = function() {
        return defaults_1.FACEBOOK_SITES.includes(getDomain());
    }, exports.isGdocsSite = function() {
        return /\/document\//.test(getUrl()) && "docs.google.com" === getDomain();
    }, exports.isGdocsDocument = function() {
        return /\/document\/d\/.*$/.test(getUrl()) && "docs.google.com" === getDomain();
    }, exports.isJiraSite = function() {
        return /\.atlassian\.net/.test(getDomain());
    }, exports.isBlackboardSite = function() {
        return /\.blackboard\.com/.test(getDomain());
    }, exports.isGmailSite = function() {
        return "mail.google.com" === getDomain();
    }, exports.getUrl = getUrl, exports.getFavicon = function() {
        for (var isAbsolute = new RegExp("^(?:[a-z]+:)?//", "i"), favicon = "", links = document.getElementsByTagName("link"), i = 0; i < links.length; i++) {
            var link = links[i];
            -1 !== ('"' + link.getAttribute("rel") + '"').search(/(\"icon )|( icon\")|(\"icon\")|( icon )/i) && (favicon = link.getAttribute("href"));
        }
        return favicon || (favicon = "favicon.ico"), isAbsolute.test(favicon) ? favicon : "/" !== favicon[0] ? "//" + document.location.host + document.location.pathname + favicon : "//" + document.location.host + favicon;
    };
}, function(module, exports) {
    module.exports = function(value) {
        return null != value && "object" == typeof value;
    };
}, function(module, exports, __webpack_require__) {
    try {
        module.exports = __webpack_require__(300);
    } catch (e) {}
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    (function(process) {
        Object.defineProperty(exports, "__esModule", {
            value: !0
        });
        var _extends = Object.assign || function(target) {
            for (var i = 1; i < arguments.length; i++) {
                var source = arguments[i];
                for (var key in source) Object.prototype.hasOwnProperty.call(source, key) && (target[key] = source[key]);
            }
            return target;
        };
        exports.ident = function(v) {
            return v;
        }, exports.check = function(value, predicate, error) {
            if (!predicate(value)) throw new Error(error);
        }, exports.remove = function(array, item) {
            var index = array.indexOf(item);
            index >= 0 && array.splice(index, 1);
        }, exports.deferred = deferred, exports.arrayOfDeffered = function(length) {
            for (var arr = [], i = 0; i < length; i++) arr.push(deferred());
            return arr;
        }, exports.autoInc = function() {
            var seed = arguments.length <= 0 || void 0 === arguments[0] ? 0 : arguments[0];
            return function() {
                return ++seed;
            };
        }, exports.asap = function(action) {
            return Promise.resolve(1).then(function() {
                return action();
            });
        }, exports.warnDeprecated = function(msg) {
            isDev && console.warn("DEPRECATION WARNING", msg);
        };
        var sym = exports.sym = function(id) {
            return "@@redux-saga/" + id;
        }, TASK = exports.TASK = sym("TASK");
        exports.kTrue = function() {
            return !0;
        }, exports.noop = function() {};
        var isDev = exports.isDev = void 0 !== process && process.env && !1;
        var is = exports.is = {
            undef: function(v) {
                return null == v;
            },
            notUndef: function(v) {
                return null != v;
            },
            func: function(f) {
                return "function" == typeof f;
            },
            array: Array.isArray,
            promise: function(p) {
                return p && is.func(p.then);
            },
            iterator: function(it) {
                return it && is.func(it.next) && is.func(it.throw);
            },
            task: function(it) {
                return it && it[TASK];
            }
        };
        function deferred() {
            var props = arguments.length <= 0 || void 0 === arguments[0] ? {} : arguments[0], def = _extends({}, props), promise = new Promise(function(resolve, reject) {
                def.resolve = resolve, def.reject = reject;
            });
            return def.promise = promise, def;
        }
    }).call(exports, __webpack_require__(60));
}, , function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), getRawTag = __webpack_require__(222), objectToString = __webpack_require__(223), nullTag = "[object Null]", undefinedTag = "[object Undefined]", symToStringTag = Symbol ? Symbol.toStringTag : void 0;
    module.exports = function(value) {
        return null == value ? void 0 === value ? undefinedTag : nullTag : symToStringTag && symToStringTag in Object(value) ? getRawTag(value) : objectToString(value);
    };
}, , function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    var baseIsNative = __webpack_require__(239), getValue = __webpack_require__(242);
    module.exports = function(object, key) {
        var value = getValue(object, key);
        return baseIsNative(value) ? value : void 0;
    };
}, , function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    var isFunction = __webpack_require__(41), isLength = __webpack_require__(78);
    module.exports = function(value) {
        return null != value && isLength(value.length) && !isFunction(value);
    };
}, , function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    var arrayLikeKeys = __webpack_require__(121), baseKeys = __webpack_require__(165), isArrayLike = __webpack_require__(29);
    module.exports = function(object) {
        return isArrayLike(object) ? arrayLikeKeys(object) : baseKeys(object);
    };
}, function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(12).Symbol;
    module.exports = Symbol;
}, function(module, exports) {
    var g;
    g = function() {
        return this;
    }();
    try {
        g = g || Function("return this")() || (0, eval)("this");
    } catch (e) {
        "object" == typeof window && (g = window);
    }
    module.exports = g;
}, function(module, exports, __webpack_require__) {
    (function(module) {
        var root = __webpack_require__(12), stubFalse = __webpack_require__(224), freeExports = "object" == typeof exports && exports && !exports.nodeType && exports, freeModule = freeExports && "object" == typeof module && module && !module.nodeType && module, Buffer = freeModule && freeModule.exports === freeExports ? root.Buffer : void 0, isBuffer = (Buffer ? Buffer.isBuffer : void 0) || stubFalse;
        module.exports = isBuffer;
    }).call(exports, __webpack_require__(77)(module));
}, function(module, exports) {
    module.exports = function(value, other) {
        return value === other || value != value && other != other;
    };
}, function(module, exports, __webpack_require__) {
    var assignValue = __webpack_require__(178), baseAssignValue = __webpack_require__(67);
    module.exports = function(source, props, object, customizer) {
        var isNew = !object;
        object || (object = {});
        for (var index = -1, length = props.length; ++index < length; ) {
            var key = props[index], newValue = customizer ? customizer(object[key], source[key], key, object, source) : void 0;
            void 0 === newValue && (newValue = source[key]), isNew ? baseAssignValue(object, key, newValue) : assignValue(object, key, newValue);
        }
        return object;
    };
}, , function(module, exports, __webpack_require__) {
    module.exports = __webpack_require__(304);
}, function(module, exports, __webpack_require__) {
    var baseIsTypedArray = __webpack_require__(225), baseUnary = __webpack_require__(79), nodeUtil = __webpack_require__(105), nodeIsTypedArray = nodeUtil && nodeUtil.isTypedArray, isTypedArray = nodeIsTypedArray ? baseUnary(nodeIsTypedArray) : baseIsTypedArray;
    module.exports = isTypedArray;
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), isObject = __webpack_require__(9), asyncTag = "[object AsyncFunction]", funcTag = "[object Function]", genTag = "[object GeneratorFunction]", proxyTag = "[object Proxy]";
    module.exports = function(value) {
        if (!isObject(value)) return !1;
        var tag = baseGetTag(value);
        return tag == funcTag || tag == genTag || tag == asyncTag || tag == proxyTag;
    };
}, function(module, exports, __webpack_require__) {
    var isSymbol = __webpack_require__(51), INFINITY = 1 / 0;
    module.exports = function(value) {
        if ("string" == typeof value || isSymbol(value)) return value;
        var result = value + "";
        return "0" == result && 1 / value == -INFINITY ? "-0" : result;
    };
}, function(module, exports, __webpack_require__) {
    var arrayLikeKeys = __webpack_require__(121), baseKeysIn = __webpack_require__(285), isArrayLike = __webpack_require__(29);
    module.exports = function(object) {
        return isArrayLike(object) ? arrayLikeKeys(object, !0) : baseKeysIn(object);
    };
}, , function(module, exports, __webpack_require__) {
    var baseIsArguments = __webpack_require__(221), isObjectLike = __webpack_require__(17), objectProto = Object.prototype, hasOwnProperty = objectProto.hasOwnProperty, propertyIsEnumerable = objectProto.propertyIsEnumerable, isArguments = baseIsArguments(function() {
        return arguments;
    }()) ? baseIsArguments : function(value) {
        return isObjectLike(value) && hasOwnProperty.call(value, "callee") && !propertyIsEnumerable.call(value, "callee");
    };
    module.exports = isArguments;
}, , function(module, exports, __webpack_require__) {
    var listCacheClear = __webpack_require__(229), listCacheDelete = __webpack_require__(230), listCacheGet = __webpack_require__(231), listCacheHas = __webpack_require__(232), listCacheSet = __webpack_require__(233);
    function ListCache(entries) {
        var index = -1, length = null == entries ? 0 : entries.length;
        for (this.clear(); ++index < length; ) {
            var entry = entries[index];
            this.set(entry[0], entry[1]);
        }
    }
    ListCache.prototype.clear = listCacheClear, ListCache.prototype.delete = listCacheDelete, 
    ListCache.prototype.get = listCacheGet, ListCache.prototype.has = listCacheHas, 
    ListCache.prototype.set = listCacheSet, module.exports = ListCache;
}, function(module, exports, __webpack_require__) {
    var eq = __webpack_require__(36);
    module.exports = function(array, key) {
        for (var length = array.length; length--; ) if (eq(array[length][0], key)) return length;
        return -1;
    };
}, function(module, exports, __webpack_require__) {
    var nativeCreate = __webpack_require__(26)(Object, "create");
    module.exports = nativeCreate;
}, function(module, exports, __webpack_require__) {
    var isKeyable = __webpack_require__(251);
    module.exports = function(map, key) {
        var data = map.__data__;
        return isKeyable(key) ? data["string" == typeof key ? "string" : "hash"] : data.map;
    };
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), isObjectLike = __webpack_require__(17), symbolTag = "[object Symbol]";
    module.exports = function(value) {
        return "symbol" == typeof value || isObjectLike(value) && baseGetTag(value) == symbolTag;
    };
}, function(module, exports) {
    module.exports = function(value) {
        return value;
    };
}, function(module, exports, __webpack_require__) {
    var isObject = __webpack_require__(9), now = __webpack_require__(299), toNumber = __webpack_require__(200), FUNC_ERROR_TEXT = "Expected a function", nativeMax = Math.max, nativeMin = Math.min;
    module.exports = function(func, wait, options) {
        var lastArgs, lastThis, maxWait, result, timerId, lastCallTime, lastInvokeTime = 0, leading = !1, maxing = !1, trailing = !0;
        if ("function" != typeof func) throw new TypeError(FUNC_ERROR_TEXT);
        function invokeFunc(time) {
            var args = lastArgs, thisArg = lastThis;
            return lastArgs = lastThis = void 0, lastInvokeTime = time, result = func.apply(thisArg, args);
        }
        function shouldInvoke(time) {
            var timeSinceLastCall = time - lastCallTime;
            return void 0 === lastCallTime || timeSinceLastCall >= wait || timeSinceLastCall < 0 || maxing && time - lastInvokeTime >= maxWait;
        }
        function timerExpired() {
            var time = now();
            if (shouldInvoke(time)) return trailingEdge(time);
            timerId = setTimeout(timerExpired, function(time) {
                var timeWaiting = wait - (time - lastCallTime);
                return maxing ? nativeMin(timeWaiting, maxWait - (time - lastInvokeTime)) : timeWaiting;
            }(time));
        }
        function trailingEdge(time) {
            return timerId = void 0, trailing && lastArgs ? invokeFunc(time) : (lastArgs = lastThis = void 0, 
            result);
        }
        function debounced() {
            var time = now(), isInvoking = shouldInvoke(time);
            if (lastArgs = arguments, lastThis = this, lastCallTime = time, isInvoking) {
                if (void 0 === timerId) return function(time) {
                    return lastInvokeTime = time, timerId = setTimeout(timerExpired, wait), leading ? invokeFunc(time) : result;
                }(lastCallTime);
                if (maxing) return timerId = setTimeout(timerExpired, wait), invokeFunc(lastCallTime);
            }
            return void 0 === timerId && (timerId = setTimeout(timerExpired, wait)), result;
        }
        return wait = toNumber(wait) || 0, isObject(options) && (leading = !!options.leading, 
        maxWait = (maxing = "maxWait" in options) ? nativeMax(toNumber(options.maxWait) || 0, wait) : maxWait, 
        trailing = "trailing" in options ? !!options.trailing : trailing), debounced.cancel = function() {
            void 0 !== timerId && clearTimeout(timerId), lastInvokeTime = 0, lastArgs = lastCallTime = lastThis = timerId = void 0;
        }, debounced.flush = function() {
            return void 0 === timerId ? result : trailingEdge(now());
        }, debounced;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.asEffect = exports.SELECT_ARG_ERROR = exports.INVALID_PATTERN = exports.CANCEL_ARG_ERROR = exports.JOIN_ARG_ERROR = exports.FORK_ARG_ERROR = exports.CALL_FUNCTION_ARG_ERROR = void 0;
    var _slicedToArray = function() {
        return function(arr, i) {
            if (Array.isArray(arr)) return arr;
            if (Symbol.iterator in Object(arr)) return function(arr, i) {
                var _arr = [], _n = !0, _d = !1, _e = void 0;
                try {
                    for (var _s, _i = arr[Symbol.iterator](); !(_n = (_s = _i.next()).done) && (_arr.push(_s.value), 
                    !i || _arr.length !== i); _n = !0) ;
                } catch (err) {
                    _d = !0, _e = err;
                } finally {
                    try {
                        !_n && _i.return && _i.return();
                    } finally {
                        if (_d) throw _e;
                    }
                }
                return _arr;
            }(arr, i);
            throw new TypeError("Invalid attempt to destructure non-iterable instance");
        };
    }();
    exports.matcher = function(pattern) {
        return ("*" === pattern ? matchers.wildcard : _utils.is.array(pattern) ? matchers.array : _utils.is.func(pattern) ? matchers.predicate : matchers.default)(pattern);
    }, exports.take = function(pattern) {
        if (arguments.length > 0 && _utils.is.undef(pattern)) throw new Error(INVALID_PATTERN);
        return effect(TAKE, _utils.is.undef(pattern) ? "*" : pattern);
    }, exports.put = function(action) {
        return effect(PUT, action);
    }, exports.race = function(effects) {
        return effect(RACE, effects);
    }, exports.call = function(fn) {
        for (var _len = arguments.length, args = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) args[_key - 1] = arguments[_key];
        return effect(CALL, getFnCallDesc(fn, args));
    }, exports.apply = function(context, fn) {
        var args = arguments.length <= 2 || void 0 === arguments[2] ? [] : arguments[2];
        return effect(CALL, getFnCallDesc({
            context: context,
            fn: fn
        }, args));
    }, exports.cps = function(fn) {
        for (var _len2 = arguments.length, args = Array(_len2 > 1 ? _len2 - 1 : 0), _key2 = 1; _key2 < _len2; _key2++) args[_key2 - 1] = arguments[_key2];
        return effect(CPS, getFnCallDesc(fn, args));
    }, exports.fork = function(fn) {
        for (var _len3 = arguments.length, args = Array(_len3 > 1 ? _len3 - 1 : 0), _key3 = 1; _key3 < _len3; _key3++) args[_key3 - 1] = arguments[_key3];
        return effect(FORK, getFnCallDesc(fn, args));
    }, exports.join = function(taskDesc) {
        if (!isForkedTask(taskDesc)) throw new Error(JOIN_ARG_ERROR);
        return effect(JOIN, taskDesc);
    }, exports.cancel = function(taskDesc) {
        if (!isForkedTask(taskDesc)) throw new Error(CANCEL_ARG_ERROR);
        return effect(CANCEL, taskDesc);
    }, exports.select = function(selector) {
        for (var _len4 = arguments.length, args = Array(_len4 > 1 ? _len4 - 1 : 0), _key4 = 1; _key4 < _len4; _key4++) args[_key4 - 1] = arguments[_key4];
        0 === arguments.length ? selector = _utils.ident : (0, _utils.check)(selector, _utils.is.func, SELECT_ARG_ERROR);
        return effect(SELECT, {
            selector: selector,
            args: args
        });
    };
    var _utils = __webpack_require__(21);
    function _defineProperty(obj, key, value) {
        return key in obj ? Object.defineProperty(obj, key, {
            value: value,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : obj[key] = value, obj;
    }
    var CALL_FUNCTION_ARG_ERROR = exports.CALL_FUNCTION_ARG_ERROR = "call/cps/fork first argument must be a function, an array [context, function] or an object {context, fn}", JOIN_ARG_ERROR = (exports.FORK_ARG_ERROR = "fork first argument must be a generator function or an iterator", 
    exports.JOIN_ARG_ERROR = "join argument must be a valid task (a result of a fork)"), CANCEL_ARG_ERROR = exports.CANCEL_ARG_ERROR = "cancel argument must be a valid task (a result of a fork)", INVALID_PATTERN = exports.INVALID_PATTERN = "Invalid pattern passed to `take` (HINT: check if you didn't mispell a constant)", SELECT_ARG_ERROR = exports.SELECT_ARG_ERROR = "select first argument must be a function", IO = (0, 
    _utils.sym)("IO"), TAKE = "TAKE", PUT = "PUT", RACE = "RACE", CALL = "CALL", CPS = "CPS", FORK = "FORK", JOIN = "JOIN", CANCEL = "CANCEL", SELECT = "SELECT", effect = function(type, payload) {
        var _ref;
        return _defineProperty(_ref = {}, IO, !0), _defineProperty(_ref, type, payload), 
        _ref;
    }, matchers = {
        wildcard: function() {
            return _utils.kTrue;
        },
        default: function(pattern) {
            return function(input) {
                return input.type === pattern;
            };
        },
        array: function(patterns) {
            return function(input) {
                return patterns.some(function(p) {
                    return p === input.type;
                });
            };
        },
        predicate: function(_predicate) {
            return function(input) {
                return _predicate(input);
            };
        }
    };
    function getFnCallDesc(fn, args) {
        (0, _utils.check)(fn, _utils.is.notUndef, CALL_FUNCTION_ARG_ERROR);
        var context = null;
        if (_utils.is.array(fn)) {
            var _fn2 = _slicedToArray(fn, 2);
            context = _fn2[0], fn = _fn2[1];
        } else if (fn.fn) {
            var _fn3 = fn;
            context = _fn3.context, fn = _fn3.fn;
        }
        return (0, _utils.check)(fn, _utils.is.func, CALL_FUNCTION_ARG_ERROR), {
            context: context,
            fn: fn,
            args: args
        };
    }
    var isForkedTask = function(task) {
        return task[_utils.TASK];
    };
    exports.asEffect = {
        take: function(effect) {
            return effect && effect[IO] && effect[TAKE];
        },
        put: function(effect) {
            return effect && effect[IO] && effect[PUT];
        },
        race: function(effect) {
            return effect && effect[IO] && effect[RACE];
        },
        call: function(effect) {
            return effect && effect[IO] && effect[CALL];
        },
        cps: function(effect) {
            return effect && effect[IO] && effect[CPS];
        },
        fork: function(effect) {
            return effect && effect[IO] && effect[FORK];
        },
        join: function(effect) {
            return effect && effect[IO] && effect[JOIN];
        },
        cancel: function(effect) {
            return effect && effect[IO] && effect[CANCEL];
        },
        select: function(effect) {
            return effect && effect[IO] && effect[SELECT];
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    function SagaCancellationException(type, saga, origin) {
        var message = "SagaCancellationException; type: " + type + ", saga: " + saga + ", origin: " + origin;
        this.name = "SagaCancellationException", this.message = message, this.type = type, 
        this.saga = saga, this.origin = origin, this.stack = new Error().stack;
    }
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.default = SagaCancellationException, SagaCancellationException.prototype = Object.create(Error.prototype), 
    SagaCancellationException.prototype.constructor = SagaCancellationException;
}, function(module, exports) {
    var objectProto = Object.prototype;
    module.exports = function(value) {
        var Ctor = value && value.constructor;
        return value === ("function" == typeof Ctor && Ctor.prototype || objectProto);
    };
}, function(module, exports, __webpack_require__) {
    var ListCache = __webpack_require__(47), stackClear = __webpack_require__(234), stackDelete = __webpack_require__(235), stackGet = __webpack_require__(236), stackHas = __webpack_require__(237), stackSet = __webpack_require__(238);
    function Stack(entries) {
        var data = this.__data__ = new ListCache(entries);
        this.size = data.size;
    }
    Stack.prototype.clear = stackClear, Stack.prototype.delete = stackDelete, Stack.prototype.get = stackGet, 
    Stack.prototype.has = stackHas, Stack.prototype.set = stackSet, module.exports = Stack;
}, function(module, exports, __webpack_require__) {
    var DataView = __webpack_require__(262), Map = __webpack_require__(80), Promise = __webpack_require__(263), Set = __webpack_require__(193), WeakMap = __webpack_require__(264), baseGetTag = __webpack_require__(23), toSource = __webpack_require__(124), dataViewCtorString = toSource(DataView), mapCtorString = toSource(Map), promiseCtorString = toSource(Promise), setCtorString = toSource(Set), weakMapCtorString = toSource(WeakMap), getTag = baseGetTag;
    (DataView && "[object DataView]" != getTag(new DataView(new ArrayBuffer(1))) || Map && "[object Map]" != getTag(new Map()) || Promise && "[object Promise]" != getTag(Promise.resolve()) || Set && "[object Set]" != getTag(new Set()) || WeakMap && "[object WeakMap]" != getTag(new WeakMap())) && (getTag = function(value) {
        var result = baseGetTag(value), Ctor = "[object Object]" == result ? value.constructor : void 0, ctorString = Ctor ? toSource(Ctor) : "";
        if (ctorString) switch (ctorString) {
          case dataViewCtorString:
            return "[object DataView]";

          case mapCtorString:
            return "[object Map]";

          case promiseCtorString:
            return "[object Promise]";

          case setCtorString:
            return "[object Set]";

          case weakMapCtorString:
            return "[object WeakMap]";
        }
        return result;
    }), module.exports = getTag;
}, function(module, exports, __webpack_require__) {
    var getPrototype = __webpack_require__(123)(Object.getPrototypeOf, Object);
    module.exports = getPrototype;
}, function(module, exports) {
    var cachedSetTimeout, cachedClearTimeout, process = module.exports = {};
    function defaultSetTimout() {
        throw new Error("setTimeout has not been defined");
    }
    function defaultClearTimeout() {
        throw new Error("clearTimeout has not been defined");
    }
    function runTimeout(fun) {
        if (cachedSetTimeout === setTimeout) return setTimeout(fun, 0);
        if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) return cachedSetTimeout = setTimeout, 
        setTimeout(fun, 0);
        try {
            return cachedSetTimeout(fun, 0);
        } catch (e) {
            try {
                return cachedSetTimeout.call(null, fun, 0);
            } catch (e) {
                return cachedSetTimeout.call(this, fun, 0);
            }
        }
    }
    !function() {
        try {
            cachedSetTimeout = "function" == typeof setTimeout ? setTimeout : defaultSetTimout;
        } catch (e) {
            cachedSetTimeout = defaultSetTimout;
        }
        try {
            cachedClearTimeout = "function" == typeof clearTimeout ? clearTimeout : defaultClearTimeout;
        } catch (e) {
            cachedClearTimeout = defaultClearTimeout;
        }
    }();
    var currentQueue, queue = [], draining = !1, queueIndex = -1;
    function cleanUpNextTick() {
        draining && currentQueue && (draining = !1, currentQueue.length ? queue = currentQueue.concat(queue) : queueIndex = -1, 
        queue.length && drainQueue());
    }
    function drainQueue() {
        if (!draining) {
            var timeout = runTimeout(cleanUpNextTick);
            draining = !0;
            for (var len = queue.length; len; ) {
                for (currentQueue = queue, queue = []; ++queueIndex < len; ) currentQueue && currentQueue[queueIndex].run();
                queueIndex = -1, len = queue.length;
            }
            currentQueue = null, draining = !1, function(marker) {
                if (cachedClearTimeout === clearTimeout) return clearTimeout(marker);
                if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) return cachedClearTimeout = clearTimeout, 
                clearTimeout(marker);
                try {
                    cachedClearTimeout(marker);
                } catch (e) {
                    try {
                        return cachedClearTimeout.call(null, marker);
                    } catch (e) {
                        return cachedClearTimeout.call(this, marker);
                    }
                }
            }(timeout);
        }
    }
    function Item(fun, array) {
        this.fun = fun, this.array = array;
    }
    function noop() {}
    process.nextTick = function(fun) {
        var args = new Array(arguments.length - 1);
        if (arguments.length > 1) for (var i = 1; i < arguments.length; i++) args[i - 1] = arguments[i];
        queue.push(new Item(fun, args)), 1 !== queue.length || draining || runTimeout(drainQueue);
    }, Item.prototype.run = function() {
        this.fun.apply(null, this.array);
    }, process.title = "browser", process.browser = !0, process.env = {}, process.argv = [], 
    process.version = "", process.versions = {}, process.on = noop, process.addListener = noop, 
    process.once = noop, process.off = noop, process.removeListener = noop, process.removeAllListeners = noop, 
    process.emit = noop, process.prependListener = noop, process.prependOnceListener = noop, 
    process.listeners = function(name) {
        return [];
    }, process.binding = function(name) {
        throw new Error("process.binding is not supported");
    }, process.cwd = function() {
        return "/";
    }, process.chdir = function(dir) {
        throw new Error("process.chdir is not supported");
    }, process.umask = function() {
        return 0;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.ports = {
        bridge: "bridge",
        background: "message:to-priv",
        broadcast: "message:to-non-priv"
    };
}, , function(module, exports, __webpack_require__) {
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
}, function(module, exports) {
    var MAX_SAFE_INTEGER = 9007199254740991, reIsUint = /^(?:0|[1-9]\d*)$/;
    module.exports = function(value, length) {
        var type = typeof value;
        return !!(length = null == length ? MAX_SAFE_INTEGER : length) && ("number" == type || "symbol" != type && reIsUint.test(value)) && value > -1 && value % 1 == 0 && value < length;
    };
}, function(module, exports, __webpack_require__) {
    var baseMatches = __webpack_require__(227), baseMatchesProperty = __webpack_require__(266), identity = __webpack_require__(52), isArray = __webpack_require__(8), property = __webpack_require__(275);
    module.exports = function(value) {
        return "function" == typeof value ? value : null == value ? identity : "object" == typeof value ? isArray(value) ? baseMatchesProperty(value[0], value[1]) : baseMatches(value) : property(value);
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var stdlib_1 = __webpack_require__(3), log = __webpack_require__(1).Logger.create("extension-api");
    !function(m) {
        for (var p in m) exports.hasOwnProperty(p) || (exports[p] = m[p]);
    }(__webpack_require__(61)), exports.initGlobalExtensionApi = function(api) {
        window.extensionApi && log.warn("Extension Api init called more than once"), window.extensionApi = window.extensionApi || api;
    }, exports.getGlobalExtensionApi = function() {
        return stdlib_1.assertNonNull(window.extensionApi, "extension api was not initialized");
    };
}, function(module, exports, __webpack_require__) {
    var defineProperty = __webpack_require__(135);
    module.exports = function(object, key, value) {
        "__proto__" == key && defineProperty ? defineProperty(object, key, {
            configurable: !0,
            enumerable: !0,
            value: value,
            writable: !0
        }) : object[key] = value;
    };
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports) {
    module.exports = function(module) {
        return module.webpackPolyfill || (module.deprecate = function() {}, module.paths = [], 
        module.children || (module.children = []), Object.defineProperty(module, "loaded", {
            enumerable: !0,
            get: function() {
                return module.l;
            }
        }), Object.defineProperty(module, "id", {
            enumerable: !0,
            get: function() {
                return module.i;
            }
        }), module.webpackPolyfill = 1), module;
    };
}, function(module, exports) {
    var MAX_SAFE_INTEGER = 9007199254740991;
    module.exports = function(value) {
        return "number" == typeof value && value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER;
    };
}, function(module, exports) {
    module.exports = function(func) {
        return function(value) {
            return func(value);
        };
    };
}, function(module, exports, __webpack_require__) {
    var Map = __webpack_require__(26)(__webpack_require__(12), "Map");
    module.exports = Map;
}, function(module, exports, __webpack_require__) {
    var mapCacheClear = __webpack_require__(243), mapCacheDelete = __webpack_require__(250), mapCacheGet = __webpack_require__(252), mapCacheHas = __webpack_require__(253), mapCacheSet = __webpack_require__(254);
    function MapCache(entries) {
        var index = -1, length = null == entries ? 0 : entries.length;
        for (this.clear(); ++index < length; ) {
            var entry = entries[index];
            this.set(entry[0], entry[1]);
        }
    }
    MapCache.prototype.clear = mapCacheClear, MapCache.prototype.delete = mapCacheDelete, 
    MapCache.prototype.get = mapCacheGet, MapCache.prototype.has = mapCacheHas, MapCache.prototype.set = mapCacheSet, 
    module.exports = MapCache;
}, function(module, exports, __webpack_require__) {
    var baseIsEqualDeep = __webpack_require__(255), isObjectLike = __webpack_require__(17);
    module.exports = function baseIsEqual(value, other, bitmask, customizer, stack) {
        return value === other || (null == value || null == other || !isObjectLike(value) && !isObjectLike(other) ? value != value && other != other : baseIsEqualDeep(value, other, bitmask, customizer, baseIsEqual, stack));
    };
}, function(module, exports, __webpack_require__) {
    var isArray = __webpack_require__(8), isKey = __webpack_require__(84), stringToPath = __webpack_require__(268), toString = __webpack_require__(170);
    module.exports = function(value, object) {
        return isArray(value) ? value : isKey(value, object) ? [ value ] : stringToPath(toString(value));
    };
}, function(module, exports, __webpack_require__) {
    var isArray = __webpack_require__(8), isSymbol = __webpack_require__(51), reIsDeepProp = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, reIsPlainProp = /^\w*$/;
    module.exports = function(value, object) {
        if (isArray(value)) return !1;
        var type = typeof value;
        return !("number" != type && "symbol" != type && "boolean" != type && null != value && !isSymbol(value)) || reIsPlainProp.test(value) || !reIsDeepProp.test(value) || null != object && value in Object(object);
    };
}, function(module, exports) {
    module.exports = function(array, iteratee) {
        for (var index = -1, length = null == array ? 0 : array.length, result = Array(length); ++index < length; ) result[index] = iteratee(array[index], index, array);
        return result;
    };
}, , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.MANUAL_CANCEL = exports.RACE_AUTO_CANCEL = exports.PARALLEL_AUTO_CANCEL = exports.CANCEL = exports.undefindInputError = exports.NOT_ITERATOR_ERROR = void 0, 
    exports.default = function proc(iterator) {
        var subscribe = arguments.length <= 1 || void 0 === arguments[1] ? function() {
            return _utils.noop;
        } : arguments[1];
        var dispatch = arguments.length <= 2 || void 0 === arguments[2] ? _utils.noop : arguments[2];
        var getState = arguments.length <= 3 || void 0 === arguments[3] ? _utils.noop : arguments[3];
        var monitor = arguments.length <= 4 || void 0 === arguments[4] ? _utils.noop : arguments[4];
        var parentEffectId = arguments.length <= 5 || void 0 === arguments[5] ? 0 : arguments[5];
        var name = arguments.length <= 6 || void 0 === arguments[6] ? "anonymous" : arguments[6];
        var forked = arguments[7];
        (0, _utils.check)(iterator, _utils.is.iterator, NOT_ITERATOR_ERROR);
        var UNDEFINED_INPUT_ERROR = undefindInputError(name);
        var deferredInputs = [];
        var deferredEnd = (0, _utils.deferred)();
        var unsubscribe = subscribe(function(input) {
            if (void 0 === input) throw UNDEFINED_INPUT_ERROR;
            for (var i = 0; i < deferredInputs.length; i++) {
                var def = deferredInputs[i];
                def.match(input) && (deferredInputs = [], def.resolve(input));
            }
        });
        next.cancel = _utils.noop;
        var task = function(id, name, iterator, done, forked) {
            var _ref6;
            return _defineProperty(_ref6 = {}, _utils.TASK, !0), _defineProperty(_ref6, "id", id), 
            _defineProperty(_ref6, "name", name), _defineProperty(_ref6, "done", done), _defineProperty(_ref6, "forked", forked), 
            _defineProperty(_ref6, "cancel", function(error) {
                error instanceof _SagaCancellationException2.default || (error = new _SagaCancellationException2.default(MANUAL_CANCEL, name, error)), 
                done[CANCEL](error);
            }), _defineProperty(_ref6, "isRunning", function() {
                return iterator._isRunning;
            }), _defineProperty(_ref6, "result", function() {
                return iterator._result;
            }), _defineProperty(_ref6, "error", function() {
                return iterator._error;
            }), _ref6;
        }(parentEffectId, name, iterator, deferredEnd.promise, forked);
        task.done[CANCEL] = function(_ref) {
            var type = _ref.type, origin = _ref.origin;
            next.cancel(new _SagaCancellationException2.default(type, name, origin));
        };
        iterator._isRunning = !0;
        next();
        return task;
        function logError(level, message, error) {
            "undefined" == typeof window ? console.log("redux-saga " + level + ": " + message + "\n" + error.stack) : console[level].call(console, message, error);
        }
        function next(error, arg) {
            if (!iterator._isRunning) throw new Error("Trying to resume an already finished generator");
            try {
                var result = error ? iterator.throw(error) : iterator.next(arg);
                result.done ? end(result.value) : runEffect(result.value, parentEffectId, "", next);
            } catch (error) {
                end(error, !0), error instanceof _SagaCancellationException2.default ? _utils.isDev && logError("warn", name + ": uncaught", error) : logError("error", name + ": uncaught", error);
            }
        }
        function end(result, isError) {
            iterator._isRunning = !1, isError ? (iterator._error = result, deferredEnd.reject(result)) : (iterator._result = result, 
            deferredEnd.resolve(result)), unsubscribe();
        }
        function runEffect(effect, parentEffectId) {
            var label = arguments.length <= 2 || void 0 === arguments[2] ? "" : arguments[2], cb = arguments[3], effectId = nextEffectId();
            monitor(monitorActions.effectTriggered(effectId, parentEffectId, label, effect));
            var effectSettled = void 0;
            function currCb(err, res) {
                effectSettled || (effectSettled = !0, cb.cancel = _utils.noop, monitor(err ? monitorActions.effectRejected(effectId, err) : monitorActions.effectResolved(effectId, res)), 
                cb(err, res));
            }
            currCb.cancel = _utils.noop, cb.cancel = function(cancelError) {
                if (!effectSettled) {
                    effectSettled = !0;
                    try {
                        currCb.cancel(cancelError);
                    } catch (err) {}
                    currCb.cancel = _utils.noop, cb(cancelError), monitor(monitorActions.effectRejected(effectId, cancelError));
                }
            };
            var data = void 0;
            return _utils.is.promise(effect) ? resolvePromise(effect, currCb) : _utils.is.iterator(effect) ? resolveIterator(effect, effectId, name, currCb) : _utils.is.array(effect) ? function(effects, effectId, cb) {
                if (!effects.length) return void cb(null, []);
                var completedCount = 0, completed = void 0, results = Array(effects.length);
                var childCbs = effects.map(function(eff, idx) {
                    var chCbAtIdx = function(err, res) {
                        if (!completed) if (err) {
                            try {
                                cb.cancel(new _SagaCancellationException2.default(PARALLEL_AUTO_CANCEL, name, name));
                            } catch (err) {}
                            cb(err);
                        } else results[idx] = res, ++completedCount === results.length && (completed = !0, 
                        cb(null, results));
                    };
                    return chCbAtIdx.cancel = _utils.noop, chCbAtIdx;
                });
                cb.cancel = function(cancelError) {
                    completed || (completed = !0, childCbs.forEach(function(chCb) {
                        return chCb.cancel(cancelError);
                    }));
                }, effects.forEach(function(eff, idx) {
                    return runEffect(eff, effectId, idx, childCbs[idx]);
                });
            }(effect, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.take(effect)) ? function(pattern, cb) {
                var def = {
                    match: (0, _io.matcher)(pattern),
                    pattern: pattern,
                    resolve: function(input) {
                        return cb(null, input);
                    }
                };
                deferredInputs.push(def), cb.cancel = function() {
                    return (0, _utils.remove)(deferredInputs, def);
                };
            }(data, currCb) : _utils.is.notUndef(data = _io.asEffect.put(effect)) ? function(action, cb) {
                (0, _utils.asap)(function() {
                    return cb(null, dispatch(action));
                });
            }(data, currCb) : _utils.is.notUndef(data = _io.asEffect.race(effect)) ? function(effects, effectId, cb) {
                var completed = void 0, keys = Object.keys(effects), childCbs = {};
                keys.forEach(function(key) {
                    var chCbAtKey = function(err, res) {
                        if (!completed) if (err) {
                            try {
                                cb.cancel(new _SagaCancellationException2.default(RACE_AUTO_CANCEL, name, name));
                            } catch (err) {}
                            cb(_defineProperty({}, key, err));
                        } else {
                            try {
                                cb.cancel(new _SagaCancellationException2.default(RACE_AUTO_CANCEL, name, name));
                            } catch (err) {}
                            completed = !0, cb(null, _defineProperty({}, key, res));
                        }
                    };
                    chCbAtKey.cancel = _utils.noop, childCbs[key] = chCbAtKey;
                }), cb.cancel = function(cancelError) {
                    completed || (completed = !0, keys.forEach(function(key) {
                        return childCbs[key].cancel(cancelError);
                    }));
                }, keys.forEach(function(key) {
                    return runEffect(effects[key], effectId, key, childCbs[key]);
                });
            }(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.call(effect)) ? function(_ref2, effectId, cb) {
                var context = _ref2.context, fn = _ref2.fn, args = _ref2.args, result = void 0;
                try {
                    result = fn.apply(context, args);
                } catch (error) {
                    return cb(error);
                }
                return _utils.is.promise(result) ? resolvePromise(result, cb) : _utils.is.iterator(result) ? resolveIterator(result, effectId, fn.name, cb) : cb(null, result);
            }(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.cps(effect)) ? function(_ref3, cb) {
                var context = _ref3.context, fn = _ref3.fn, args = _ref3.args;
                try {
                    fn.apply(context, args.concat(cb));
                } catch (error) {
                    return cb(error);
                }
            }(data, currCb) : _utils.is.notUndef(data = _io.asEffect.fork(effect)) ? function(_ref4, effectId, cb) {
                var context = _ref4.context, fn = _ref4.fn, args = _ref4.args, result = void 0, error = void 0, _iterator = void 0;
                try {
                    result = fn.apply(context, args);
                } catch (err) {
                    error = error;
                }
                _iterator = _utils.is.iterator(result) ? result : (error ? regeneratorRuntime.mark(function _callee() {
                    return regeneratorRuntime.wrap(function(_context) {
                        for (;;) switch (_context.prev = _context.next) {
                          case 0:
                            throw error;

                          case 1:
                          case "end":
                            return _context.stop();
                        }
                    }, _callee, this);
                }) : regeneratorRuntime.mark(function _callee2() {
                    return regeneratorRuntime.wrap(function(_context2) {
                        for (;;) switch (_context2.prev = _context2.next) {
                          case 0:
                            return _context2.next = 2, result;

                          case 2:
                            return _context2.abrupt("return", _context2.sent);

                          case 3:
                          case "end":
                            return _context2.stop();
                        }
                    }, _callee2, this);
                }))();
                cb(null, proc(_iterator, subscribe, dispatch, getState, monitor, effectId, fn.name, !0));
            }(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.join(effect)) ? function(task, cb) {
                resolvePromise(task.done, cb);
            }(data, currCb) : _utils.is.notUndef(data = _io.asEffect.cancel(effect)) ? function(task, cb) {
                task.done[CANCEL](new _SagaCancellationException2.default(MANUAL_CANCEL, name, name)), 
                cb();
            }(data, currCb) : _utils.is.notUndef(data = _io.asEffect.select(effect)) ? function(_ref5, cb) {
                var selector = _ref5.selector, args = _ref5.args;
                try {
                    var state = selector.apply(void 0, [ getState() ].concat(function(arr) {
                        {
                            if (Array.isArray(arr)) {
                                for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];
                                return arr2;
                            }
                            return Array.from(arr);
                        }
                    }(args)));
                    cb(null, state);
                } catch (error) {
                    cb(error);
                }
            }(data, currCb) : currCb(null, effect);
        }
        function resolvePromise(promise, cb) {
            var cancelPromise = promise[CANCEL];
            "function" == typeof cancelPromise && (cb.cancel = cancelPromise), promise.then(function(result) {
                return cb(null, result);
            }, function(error) {
                return cb(error);
            });
        }
        function resolveIterator(iterator, effectId, name, cb) {
            resolvePromise(proc(iterator, subscribe, dispatch, getState, monitor, effectId, name).done, cb);
        }
    };
    var obj, _utils = __webpack_require__(21), _io = __webpack_require__(54), monitorActions = function(obj) {
        {
            if (obj && obj.__esModule) return obj;
            var newObj = {};
            if (null != obj) for (var key in obj) Object.prototype.hasOwnProperty.call(obj, key) && (newObj[key] = obj[key]);
            return newObj.default = obj, newObj;
        }
    }(__webpack_require__(88)), _SagaCancellationException = __webpack_require__(55), _SagaCancellationException2 = (obj = _SagaCancellationException) && obj.__esModule ? obj : {
        default: obj
    };
    function _toConsumableArray(arr) {
        if (Array.isArray(arr)) {
            for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) {
                arr2[i] = arr[i];
            }
            return arr2;
        } else {
            return Array.from(arr);
        }
    }
    function _defineProperty(obj, key, value) {
        return key in obj ? Object.defineProperty(obj, key, {
            value: value,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : obj[key] = value, obj;
    }
    var NOT_ITERATOR_ERROR = exports.NOT_ITERATOR_ERROR = "proc first argument (Saga function result) must be an iterator", undefindInputError = exports.undefindInputError = function(name) {
        return "\n  " + name + " saga was provided with an undefined input action\n  Hints :\n  - check that your Action Creator returns a non undefined value\n  - if the Saga was started using runSaga, check that your subscribe source provides the action to its listeners\n";
    }, CANCEL = exports.CANCEL = (0, _utils.sym)("@@redux-saga/cancelPromise"), PARALLEL_AUTO_CANCEL = exports.PARALLEL_AUTO_CANCEL = "PARALLEL_AUTO_CANCEL", RACE_AUTO_CANCEL = exports.RACE_AUTO_CANCEL = "RACE_AUTO_CANCEL", MANUAL_CANCEL = exports.MANUAL_CANCEL = "MANUAL_CANCEL", nextEffectId = (0, 
    _utils.autoInc)();
    function proc(iterator) {
        var subscribe = arguments.length <= 1 || arguments[1] === undefined ? function() {
            return _utils.noop;
        } : arguments[1];
        var dispatch = arguments.length <= 2 || arguments[2] === undefined ? _utils.noop : arguments[2];
        var getState = arguments.length <= 3 || arguments[3] === undefined ? _utils.noop : arguments[3];
        var monitor = arguments.length <= 4 || arguments[4] === undefined ? _utils.noop : arguments[4];
        var parentEffectId = arguments.length <= 5 || arguments[5] === undefined ? 0 : arguments[5];
        var name = arguments.length <= 6 || arguments[6] === undefined ? "anonymous" : arguments[6];
        var forked = arguments[7];
        (0, _utils.check)(iterator, _utils.is.iterator, NOT_ITERATOR_ERROR);
        var UNDEFINED_INPUT_ERROR = undefindInputError(name);
        var deferredInputs = [];
        var deferredEnd = (0, _utils.deferred)();
        var unsubscribe = subscribe(function(input) {
            if (input === undefined) throw UNDEFINED_INPUT_ERROR;
            for (var i = 0; i < deferredInputs.length; i++) {
                var def = deferredInputs[i];
                if (def.match(input)) {
                    deferredInputs = [];
                    def.resolve(input);
                }
            }
        });
        next.cancel = _utils.noop;
        var task = newTask(parentEffectId, name, iterator, deferredEnd.promise, forked);
        task.done[CANCEL] = function(_ref) {
            var type = _ref.type;
            var origin = _ref.origin;
            next.cancel(new _SagaCancellationException2.default(type, name, origin));
        };
        iterator._isRunning = true;
        next();
        return task;
        function logError(level, message, error) {
            if (typeof window === "undefined") {
                console.log("redux-saga " + level + ": " + message + "\n" + error.stack);
            } else {
                console[level].call(console, message, error);
            }
        }
        function next(error, arg) {
            if (!iterator._isRunning) throw new Error("Trying to resume an already finished generator");
            try {
                var result = error ? iterator.throw(error) : iterator.next(arg);
                if (!result.done) {
                    runEffect(result.value, parentEffectId, "", next);
                } else {
                    end(result.value);
                }
            } catch (error) {
                end(error, true);
                if (error instanceof _SagaCancellationException2.default) {
                    if (_utils.isDev) {
                        logError("warn", name + ": uncaught", error);
                    }
                } else {
                    logError("error", name + ": uncaught", error);
                }
            }
        }
        function end(result, isError) {
            iterator._isRunning = false;
            if (!isError) {
                iterator._result = result;
                deferredEnd.resolve(result);
            } else {
                iterator._error = result;
                deferredEnd.reject(result);
            }
            unsubscribe();
        }
        function runEffect(effect, parentEffectId) {
            var label = arguments.length <= 2 || arguments[2] === undefined ? "" : arguments[2];
            var cb = arguments[3];
            var effectId = nextEffectId();
            monitor(monitorActions.effectTriggered(effectId, parentEffectId, label, effect));
            var effectSettled = undefined;
            function currCb(err, res) {
                if (effectSettled) return;
                effectSettled = true;
                cb.cancel = _utils.noop;
                err ? monitor(monitorActions.effectRejected(effectId, err)) : monitor(monitorActions.effectResolved(effectId, res));
                cb(err, res);
            }
            currCb.cancel = _utils.noop;
            cb.cancel = function(cancelError) {
                if (effectSettled) return;
                effectSettled = true;
                try {
                    currCb.cancel(cancelError);
                } catch (err) {
                    void 0;
                }
                currCb.cancel = _utils.noop;
                cb(cancelError);
                monitor(monitorActions.effectRejected(effectId, cancelError));
            };
            var data = undefined;
            return _utils.is.promise(effect) ? resolvePromise(effect, currCb) : _utils.is.iterator(effect) ? resolveIterator(effect, effectId, name, currCb) : _utils.is.array(effect) ? runParallelEffect(effect, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.take(effect)) ? runTakeEffect(data, currCb) : _utils.is.notUndef(data = _io.asEffect.put(effect)) ? runPutEffect(data, currCb) : _utils.is.notUndef(data = _io.asEffect.race(effect)) ? runRaceEffect(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.call(effect)) ? runCallEffect(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.cps(effect)) ? runCPSEffect(data, currCb) : _utils.is.notUndef(data = _io.asEffect.fork(effect)) ? runForkEffect(data, effectId, currCb) : _utils.is.notUndef(data = _io.asEffect.join(effect)) ? runJoinEffect(data, currCb) : _utils.is.notUndef(data = _io.asEffect.cancel(effect)) ? runCancelEffect(data, currCb) : _utils.is.notUndef(data = _io.asEffect.select(effect)) ? runSelectEffect(data, currCb) : currCb(null, effect);
        }
        function resolvePromise(promise, cb) {
            var cancelPromise = promise[CANCEL];
            if (typeof cancelPromise === "function") {
                cb.cancel = cancelPromise;
            }
            promise.then(function(result) {
                return cb(null, result);
            }, function(error) {
                return cb(error);
            });
        }
        function resolveIterator(iterator, effectId, name, cb) {
            resolvePromise(proc(iterator, subscribe, dispatch, getState, monitor, effectId, name).done, cb);
        }
        function runTakeEffect(pattern, cb) {
            var def = {
                match: (0, _io.matcher)(pattern),
                pattern: pattern,
                resolve: function resolve(input) {
                    return cb(null, input);
                }
            };
            deferredInputs.push(def), cb.cancel = function() {
                return (0, _utils.remove)(deferredInputs, def);
            };
        }
        function runPutEffect(action, cb) {
            (0, _utils.asap)(function() {
                return cb(null, dispatch(action));
            });
        }
        function runCallEffect(_ref2, effectId, cb) {
            var context = _ref2.context, fn = _ref2.fn, args = _ref2.args, result = undefined;
            try {
                result = fn.apply(context, args);
            } catch (error) {
                return cb(error);
            }
            return _utils.is.promise(result) ? resolvePromise(result, cb) : _utils.is.iterator(result) ? resolveIterator(result, effectId, fn.name, cb) : cb(null, result);
        }
        function runCPSEffect(_ref3, cb) {
            var context = _ref3.context, fn = _ref3.fn, args = _ref3.args;
            try {
                fn.apply(context, args.concat(cb));
            } catch (error) {
                return cb(error);
            }
        }
        function runForkEffect(_ref4, effectId, cb) {
            var context = _ref4.context, fn = _ref4.fn, args = _ref4.args, result = undefined, error = undefined, _iterator = undefined;
            try {
                result = fn.apply(context, args);
            } catch (err) {
                error = error;
            }
            if (_utils.is.iterator(result)) {
                _iterator = result;
            } else {
                _iterator = (error ? regeneratorRuntime.mark(function _callee() {
                    return regeneratorRuntime.wrap(function _callee$(_context) {
                        while (1) {
                            switch (_context.prev = _context.next) {
                              case 0:
                                throw error;

                              case 1:
                              case "end":
                                return _context.stop();
                            }
                        }
                    }, _callee, this);
                }) : regeneratorRuntime.mark(function _callee2() {
                    return regeneratorRuntime.wrap(function _callee2$(_context2) {
                        while (1) {
                            switch (_context2.prev = _context2.next) {
                              case 0:
                                _context2.next = 2;
                                return result;

                              case 2:
                                return _context2.abrupt("return", _context2.sent);

                              case 3:
                              case "end":
                                return _context2.stop();
                            }
                        }
                    }, _callee2, this);
                }))();
            }
            cb(null, proc(_iterator, subscribe, dispatch, getState, monitor, effectId, fn.name, true));
        }
        function runJoinEffect(task, cb) {
            resolvePromise(task.done, cb);
        }
        function runCancelEffect(task, cb) {
            task.done[CANCEL](new _SagaCancellationException2.default(MANUAL_CANCEL, name, name)), 
            cb();
        }
        function runParallelEffect(effects, effectId, cb) {
            if (!effects.length) {
                cb(null, []);
                return;
            }
            var completedCount = 0, completed = undefined, results = Array(effects.length);
            function checkEffectEnd() {
                if (completedCount === results.length) {
                    completed = true;
                    cb(null, results);
                }
            }
            var childCbs = effects.map(function(eff, idx) {
                var chCbAtIdx = function chCbAtIdx(err, res) {
                    if (completed) return;
                    if (err) {
                        try {
                            cb.cancel(new _SagaCancellationException2.default(PARALLEL_AUTO_CANCEL, name, name));
                        } catch (err) {
                            void 0;
                        }
                        cb(err);
                    } else {
                        results[idx] = res;
                        completedCount++;
                        checkEffectEnd();
                    }
                };
                chCbAtIdx.cancel = _utils.noop;
                return chCbAtIdx;
            });
            cb.cancel = function(cancelError) {
                if (!completed) {
                    completed = true;
                    childCbs.forEach(function(chCb) {
                        return chCb.cancel(cancelError);
                    });
                }
            }, effects.forEach(function(eff, idx) {
                return runEffect(eff, effectId, idx, childCbs[idx]);
            });
        }
        function runRaceEffect(effects, effectId, cb) {
            var completed = undefined, keys = Object.keys(effects), childCbs = {};
            keys.forEach(function(key) {
                var chCbAtKey = function chCbAtKey(err, res) {
                    if (completed) return;
                    if (err) {
                        try {
                            cb.cancel(new _SagaCancellationException2.default(RACE_AUTO_CANCEL, name, name));
                        } catch (err) {
                            void 0;
                        }
                        cb(_defineProperty({}, key, err));
                    } else {
                        try {
                            cb.cancel(new _SagaCancellationException2.default(RACE_AUTO_CANCEL, name, name));
                        } catch (err) {
                            void 0;
                        }
                        completed = true;
                        cb(null, _defineProperty({}, key, res));
                    }
                };
                chCbAtKey.cancel = _utils.noop;
                childCbs[key] = chCbAtKey;
            }), cb.cancel = function(cancelError) {
                if (!completed) {
                    completed = true;
                    keys.forEach(function(key) {
                        return childCbs[key].cancel(cancelError);
                    });
                }
            }, keys.forEach(function(key) {
                return runEffect(effects[key], effectId, key, childCbs[key]);
            });
        }
        function runSelectEffect(_ref5, cb) {
            var selector = _ref5.selector, args = _ref5.args;
            try {
                var state = selector.apply(undefined, [ getState() ].concat(_toConsumableArray(args)));
                cb(null, state);
            } catch (error) {
                cb(error);
            }
        }
        function newTask(id, name, iterator, done, forked) {
            var _ref6;
            return _defineProperty(_ref6 = {}, _utils.TASK, true), _defineProperty(_ref6, "id", id), 
            _defineProperty(_ref6, "name", name), _defineProperty(_ref6, "done", done), _defineProperty(_ref6, "forked", forked), 
            _defineProperty(_ref6, "cancel", function cancel(error) {
                if (!(error instanceof _SagaCancellationException2.default)) {
                    error = new _SagaCancellationException2.default(MANUAL_CANCEL, name, error);
                }
                done[CANCEL](error);
            }), _defineProperty(_ref6, "isRunning", function isRunning() {
                return iterator._isRunning;
            }), _defineProperty(_ref6, "result", function result() {
                return iterator._result;
            }), _defineProperty(_ref6, "error", function error() {
                return iterator._error;
            }), _ref6;
        }
    }
}, function(module, exports, __webpack_require__) {
    "use strict";
    function _defineProperty(obj, key, value) {
        return key in obj ? Object.defineProperty(obj, key, {
            value: value,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : obj[key] = value, obj;
    }
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.effectTriggered = function(effectId, parentEffectId, label, effect) {
        var _ref;
        return _defineProperty(_ref = {}, MONITOR_ACTION, !0), _defineProperty(_ref, "type", EFFECT_TRIGGERED), 
        _defineProperty(_ref, "effectId", effectId), _defineProperty(_ref, "parentEffectId", parentEffectId), 
        _defineProperty(_ref, "label", label), _defineProperty(_ref, "effect", effect), 
        _ref;
    }, exports.effectResolved = function(effectId, result) {
        var _ref2;
        return _defineProperty(_ref2 = {}, MONITOR_ACTION, !0), _defineProperty(_ref2, "type", EFFECT_RESOLVED), 
        _defineProperty(_ref2, "effectId", effectId), _defineProperty(_ref2, "result", result), 
        _ref2;
    }, exports.effectRejected = function(effectId, error) {
        var _ref3;
        return _defineProperty(_ref3 = {}, MONITOR_ACTION, !0), _defineProperty(_ref3, "type", EFFECT_REJECTED), 
        _defineProperty(_ref3, "effectId", effectId), _defineProperty(_ref3, "error", error), 
        _ref3;
    };
    var MONITOR_ACTION = exports.MONITOR_ACTION = "MONITOR_ACTION", EFFECT_TRIGGERED = exports.EFFECT_TRIGGERED = "EFFECT_TRIGGERED", EFFECT_RESOLVED = exports.EFFECT_RESOLVED = "EFFECT_RESOLVED", EFFECT_REJECTED = exports.EFFECT_REJECTED = "EFFECT_REJECTED";
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.t = {
        SETTINGS_INITIAL: "settings/SETTINGS_INITIAL",
        TOGGLE_DEFS: "settings/TOGGLE_DEFS",
        TOGGLE_SITE: "settings/TOGGLE_SITE",
        TOGGLE_FIELD: "settings/TOGGLE_FIELD",
        DISABLE_ON_TAB: "settings/DISABLE_ON_TAB",
        DISABLE_REMINDER_NOTIFICATION: "settings/DISABLE_REMINDER_NOTIFICATION",
        SHOW_DISABLE_REMINDER: "settings/SHOW_DISABLE_REMINDER",
        DISABLE_EMAIL_SUMMARIZATION: "settings/DISABLE_EMAIL_SUMMARIZATION",
        SHOW_NEWS: "settings/SHOW_NEWS",
        SEEN_NEWS: "settings/SEEN_NEWS",
        SEEN_GDOCS_OPT_IN: "settings/SEEN_GDOCS_OPT_IN",
        SEEN_GDOCS_LARGE_DOCUMENT_WARNING: "settings/SEEN_GDOCS_LARGE_DOCUMENT_WARNING",
        SET_GDOCS_INITIAL_DISABLE: "setting/SET_GDOCS_INITIAL_DISABLE",
        SHOW_ONBOARDING: "settings/SHOW_ONBOARDING",
        SEEN_ONBOARDING: "settings/SEEN_ONBOARDING",
        SHOW_LOGIN_REMINDER: "settings/SHOW_LOGIN_REMINDER",
        HIDE_LOGIN_REMINDER: "settings/HIDE_LOGIN_REMINDER",
        DISABLE_LOGIN_REMINDER: "settings/DISABLE_LOGIN_REMINDER",
        SET_DAPI_PROP: "settings/SET_DAPI_PROP",
        CHANGE_WEAK_DIALECT: "settings/CHANGE_WEAK_DIALECT",
        CHANGE_STRONG_DIALECT: "settings/CHANGE_STRONG_DIALECT",
        SAVE_ANONYMOUS_PROPERTIES: "settings/SAVE_ANONYMOUS_PROPERTIES",
        EDGE_POPUP_FROM_GBUTTON: "settings/EDGE_POPUP_FROM_GBUTTON",
        SAVE_EMAIL_CONNECTEDNESS_DATA: "settings/SAVE_EMAIL_CONNECTEDNESS_DATA"
    }, exports.DAPI_ACTIONS = [ exports.t.CHANGE_WEAK_DIALECT, exports.t.CHANGE_STRONG_DIALECT ], 
    exports.CACHED_ACTIONS = [ exports.t.TOGGLE_DEFS, exports.t.TOGGLE_SITE, exports.t.TOGGLE_FIELD, exports.t.SEEN_NEWS, exports.t.SEEN_GDOCS_OPT_IN, exports.t.SEEN_GDOCS_LARGE_DOCUMENT_WARNING, exports.t.SET_GDOCS_INITIAL_DISABLE, exports.t.SHOW_ONBOARDING, exports.t.SEEN_ONBOARDING, exports.t.SHOW_LOGIN_REMINDER, exports.t.HIDE_LOGIN_REMINDER, exports.t.DISABLE_LOGIN_REMINDER, exports.t.SHOW_DISABLE_REMINDER, exports.t.DISABLE_REMINDER_NOTIFICATION, exports.t.DISABLE_EMAIL_SUMMARIZATION, exports.t.EDGE_POPUP_FROM_GBUTTON ], 
    exports.setDapiProp = function(propKey, data) {
        return {
            type: exports.t.SET_DAPI_PROP,
            propKey: propKey,
            data: data
        };
    }, exports.changeWeakDialect = function(data) {
        return {
            type: exports.t.CHANGE_WEAK_DIALECT,
            data: data
        };
    }, exports.changeStrongDialect = function(data) {
        return {
            type: exports.t.CHANGE_STRONG_DIALECT,
            data: data
        };
    }, exports.initialSettings = function(data) {
        return {
            type: exports.t.SETTINGS_INITIAL,
            data: data
        };
    }, exports.toggleDefs = function(enabledDefs) {
        return {
            type: exports.t.TOGGLE_DEFS,
            enabledDefs: enabledDefs
        };
    }, exports.toggleSite = function(enabled, domain) {
        return {
            type: exports.t.TOGGLE_SITE,
            domain: domain,
            enabled: enabled
        };
    }, exports.toggleField = function(data, domain) {
        return {
            type: exports.t.TOGGLE_FIELD,
            domain: domain,
            data: data
        };
    }, exports.seenNews = function() {
        return {
            type: exports.t.SEEN_NEWS
        };
    }, exports.gdocsDisabledInitially = function() {
        return {
            type: exports.t.SET_GDOCS_INITIAL_DISABLE
        };
    }, exports.seenGdocsOptIn = function() {
        return {
            type: exports.t.SEEN_GDOCS_OPT_IN
        };
    }, exports.seenGdocsLargeDocumentWarning = function() {
        return {
            type: exports.t.SEEN_GDOCS_LARGE_DOCUMENT_WARNING
        };
    }, exports.showOnboarding = function() {
        return {
            type: exports.t.SHOW_ONBOARDING
        };
    }, exports.seenOnboarding = function() {
        return {
            type: exports.t.SEEN_ONBOARDING
        };
    }, exports.showNews = function(showNews) {
        return {
            type: exports.t.SHOW_NEWS,
            showNews: showNews
        };
    }, exports.saveAnonymousProps = function(props) {
        return {
            type: exports.t.SAVE_ANONYMOUS_PROPERTIES,
            props: props
        };
    }, exports.disableOnTab = function() {
        return {
            type: exports.t.DISABLE_ON_TAB
        };
    }, exports.showDisableReminder = function(domain) {
        return {
            type: exports.t.SHOW_DISABLE_REMINDER,
            domain: domain
        };
    }, exports.disableReminder = function(domain) {
        return {
            type: exports.t.DISABLE_REMINDER_NOTIFICATION,
            domain: domain
        };
    }, exports.showEdgePopupFromGButton = function() {
        return {
            type: exports.t.EDGE_POPUP_FROM_GBUTTON
        };
    }, exports.showLoginReminder = function(loginReminderType) {
        return {
            type: exports.t.SHOW_LOGIN_REMINDER,
            loginReminderType: loginReminderType
        };
    }, exports.hideLoginReminder = function() {
        return {
            type: exports.t.HIDE_LOGIN_REMINDER
        };
    }, exports.disableLoginReminder = function() {
        return {
            type: exports.t.DISABLE_LOGIN_REMINDER
        };
    }, exports.disableEmailSummarization = function() {
        return {
            type: exports.t.DISABLE_EMAIL_SUMMARIZATION
        };
    }, exports.saveEmailConnectednessData = function(emailConnectednessData) {
        return {
            type: exports.t.SAVE_EMAIL_CONNECTEDNESS_DATA,
            emailConnectednessData: emailConnectednessData
        };
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var newConfig_1 = __webpack_require__(25), util_1 = __webpack_require__(2);
    function getUTMQueryParam(name, value) {
        return name + "=" + encodeURIComponent(value);
    }
    function getUTMQuery(type, place) {
        return getUTMQueryParam("utm_medium", "internal") + "&" + getUTMQueryParam("utm_source", type) + "&" + getUTMQueryParam("utm_campaign", place);
    }
    function getSocialUTMQuery(type) {
        return getUTMQueryParam("utm_medium", "internal") + "&" + getUTMQueryParam("utm_source", type);
    }
    exports.getSignUpURL = function(type, place) {
        return newConfig_1.URLS.signup + "?" + getUTMQuery(type, place);
    }, exports.getSignInURL = function() {
        return newConfig_1.URLS.signin + "?" + getSocialUTMQuery("signinHook");
    }, exports.getFbSigninURL = function() {
        return newConfig_1.URLS.fbSignin + "&" + getSocialUTMQuery("signinHook");
    }, exports.getGoogleSigninURL = function() {
        return newConfig_1.URLS.googleSignin + "&" + getSocialUTMQuery("signinHook");
    }, exports.getFbSignupURL = function(type) {
        return newConfig_1.URLS.fbSignup + "&" + getSocialUTMQuery(type);
    }, exports.getGoogleSignupURL = function(type) {
        return newConfig_1.URLS.googleSignup + "&" + getSocialUTMQuery(type);
    }, exports.getResetPasswordURL = function() {
        return newConfig_1.URLS.resetPassword + "?" + getUTMQueryParam("utm_medium", "internal");
    }, exports.getTermsURL = function() {
        return newConfig_1.URLS.terms + "?" + getUTMQueryParam("utm_medium", "internal");
    }, exports.getPrivatePolicyURL = function() {
        return newConfig_1.URLS.policy + "?" + getUTMQueryParam("utm_medium", "internal");
    }, exports.getUpgradeURL = function(type, place) {
        return newConfig_1.URLS.upgrade + "?" + getUTMQuery(type, place);
    }, exports.getExtensionSuccessURL = function(hasFunnelRedirectCookie) {
        var browser = util_1.getBrowser(), utmMediumVal = hasFunnelRedirectCookie ? "navigation" : "store";
        return newConfig_1.URLS.welcomeC + "?" + getUTMQueryParam("utm_medium", utmMediumVal) + "&" + getUTMQueryParam("utm_source", browser);
    }, exports.getAfterInstallURL = function(isFunnel) {
        var browser = util_1.getBrowser(), url = newConfig_1.URLS.afterInstall + "/?extension_install=true", utmMediumVal = isFunnel ? "navigation" : "store", utmSourceParam = isFunnel ? "" : "&" + getUTMQueryParam("utm_source", browser);
        return url + "&" + getUTMQueryParam("utm_medium", utmMediumVal) + utmSourceParam;
    }, exports.getUninstallURL = function(domain) {
        var queryParams = getUTMQueryParam("utm_medium", "internal") + "&" + getUTMQueryParam("utm_campaign", "extensionUninstall");
        return domain ? newConfig_1.URLS.uninstall + "?domain=" + encodeURI(domain) + "&" + queryParams : newConfig_1.URLS.uninstall + "?" + queryParams;
    }, exports.addParamsToUpgradeURL = function(url, type, place) {
        return url + "&" + getUTMQuery(type, place);
    };
}, , function(module, exports) {
    module.exports = function(array, iteratee) {
        for (var index = -1, length = null == array ? 0 : array.length; ++index < length && !1 !== iteratee(array[index], index, array); ) ;
        return array;
    };
}, function(module, exports, __webpack_require__) {
    var castPath = __webpack_require__(83), toKey = __webpack_require__(42);
    module.exports = function(object, path) {
        for (var index = 0, length = (path = castPath(path, object)).length; null != object && index < length; ) object = object[toKey(path[index++])];
        return index && index == length ? object : void 0;
    };
}, function(module, exports, __webpack_require__) {
    var identity = __webpack_require__(52), overRest = __webpack_require__(196), setToString = __webpack_require__(198);
    module.exports = function(func, start) {
        return setToString(overRest(func, start, identity), func + "");
    };
}, , function(module, exports, __webpack_require__) {
    module.exports = __webpack_require__(301);
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var performanceMetrics_1 = __webpack_require__(182);
    exports.PerformanceMetrics = performanceMetrics_1.PerformanceMetrics;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.t = {
        UPDATE_CONNECTION: "connection/UPDATE_CONNECTION",
        ONLINE_STATE: "connection/ONLINE_STATE"
    }, exports.updateConnection = function(data) {
        return {
            type: exports.t.UPDATE_CONNECTION,
            data: data
        };
    }, exports.onlineConnection = function(online) {
        return {
            type: exports.t.ONLINE_STATE,
            online: online
        };
    };
}, function(module, exports, __webpack_require__) {
    module.exports = __webpack_require__(150);
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var _timers = {};
    exports.timers = {
        start: function(id) {
            _timers[id] = Date.now();
        },
        stop: function(id) {
            var passed = this.passed(id);
            return delete _timers[id], passed;
        },
        passed: function(id) {
            return id && _timers[id] ? Date.now() - _timers[id] : 0;
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var helpers_1 = __webpack_require__(117), util_1 = __webpack_require__(2), Config = __webpack_require__(10), stdlib_1 = __webpack_require__(3), interface_1 = __webpack_require__(61), log = __webpack_require__(1).Logger.create("extension-api.message.bg");
    function isPopup(url) {
        if (!url) return !1;
        var browser = Config.getGlobal().bundleInfo.browser, re = "firefox" === browser ? /^moz-extension:\/\/.*\/src\/popup.html$/ : "edge" === browser ? /^ms-browser-extension:\/\/.*\/src\/popup.html$/ : "chrome" === browser ? chrome && chrome.runtime && chrome.runtime.id ? new RegExp(chrome.runtime.id + "/src/popup.html") : void 0 : stdlib_1.assertNever(browser);
        return void 0 !== re && re.test(url);
    }
    exports.SETTINGS_TAB_ID = "popup", exports.bgPreload = function() {
        var chromeCheck = (util_1.isChrome() || util_1.isFF()) && (!chrome.extension || !chrome.tabs || !chrome.runtime || !chrome.runtime.onConnect), edgeCheck = util_1.isEdge() && (!edge.extension || !edge.tabs || !edge.runtime || !edge.runtime.onConnect);
        if (chromeCheck || edgeCheck) {
            var timesFailed = window.localStorage.getItem("bgInitFail") || "0", bgInitFail = parseInt(timesFailed, 10);
            bgInitFail > 4 ? log.error("too many bgInitFail " + bgInitFail) : (window.localStorage.setItem("bgInitFail", (bgInitFail + 1).toString()), 
            document.location.reload());
        }
    };
    var GenericBackgroundMessageApiImpl = function() {
        function GenericBackgroundMessageApiImpl(onPortConnection, _getActiveTab, _getAllTabs) {
            var _this = this;
            this._getActiveTab = _getActiveTab, this._getAllTabs = _getAllTabs, this.kind = "background-message-api", 
            this._callbacks = {}, this._tabPorts = {
                popup: []
            }, this._messageHelper = new helpers_1.MessageHelperImpl(), this._sendMessageToPorts = function(id, msg) {
                var ports = _this._tabPorts[id];
                ports && ports.forEach(function(port) {
                    return port.postMessage(msg);
                });
            }, this.toFocused = function(type, content) {
                return _this._getActiveTab().then(function(_a) {
                    var id = _a.id, url = _a.url;
                    if (id) return isPopup(url) ? log.warn("toFocussed not allowed for popup when it open like regular tab " + type, content) : void _this._sendMessageToPorts(id.toString(), {
                        type: type,
                        content: content,
                        callid: util_1.guid()
                    });
                });
            }, this.broadcast = function(type, content) {
                if (content) {
                    var emitTabs = function(_a) {
                        var id = _a.id, url = _a.url;
                        id && url && -1 === url.indexOf("chrome-extension:") && _this._sendMessageToPorts(id.toString(), {
                            type: type,
                            callid: util_1.guid(),
                            content: content
                        });
                    };
                    _this._getAllTabs().then(function(tabs) {
                        return tabs.forEach(emitTabs);
                    }), _this._tabPorts.popup && _this._tabPorts.popup.length && _this._getActiveTab().then(function(_a) {
                        var url = _a.url, active = _a.active;
                        emitTabs({
                            id: exports.SETTINGS_TAB_ID,
                            url: url,
                            active: active
                        });
                    });
                }
            }, this._initPortListener = function(port) {
                if (port.name === interface_1.ports.bridge) port.onMessage(function(msg) {
                    "message.toFocussed" === msg.method && _this.toFocused(msg.params && msg.params.type, msg.params && msg.params.content);
                }); else if (port.name === interface_1.ports.broadcast) port.onMessage(function(message) {
                    return _this.broadcast(message.type, message.content);
                }); else if (port.name === interface_1.ports.background) {
                    var sender_1 = port.sender;
                    if (sender_1) {
                        if (sender_1.tab) {
                            var _a = sender_1.tab, id_1 = _a.id, url_1 = _a.url;
                            if (id_1) {
                                var ports_1 = _this._tabPorts[id_1];
                                void 0 === ports_1 && (ports_1 = _this._tabPorts[id_1] = []), ports_1.push(port);
                            }
                            url_1 && 0 === url_1.indexOf("http") && _this._messageHelper.fire("tab-connected", {
                                tab: id_1,
                                url: url_1
                            }), port.onDisconnect(function() {
                                if (id_1) {
                                    var ports = _this._tabPorts[id_1];
                                    ports && ports.splice(ports.indexOf(port), 1);
                                }
                            });
                        }
                        var url = sender_1.url ? sender_1.url : sender_1.tab ? sender_1.tab.url : "";
                        if (url && isPopup(url)) {
                            var pid_1 = exports.SETTINGS_TAB_ID;
                            _this._tabPorts[pid_1] = _this._tabPorts[pid_1] || [], _this._tabPorts[pid_1].push(port), 
                            port.onDisconnect(function() {
                                var ports = _this._tabPorts[pid_1];
                                ports.splice(ports.indexOf(port), 1);
                            });
                        }
                    }
                    port.onMessage(function(message) {
                        var processMessage = function(_a) {
                            var callid = _a.callid, content = _a.content, type = _a.type;
                            _this._callbacks[callid] && (_this._callbacks[callid](content), delete _this._callbacks[callid]);
                            _this._messageHelper.fire(type, content, function(content) {
                                return port.postMessage({
                                    content: content,
                                    callid: callid
                                });
                            }, sender_1 && sender_1.tab ? sender_1.tab.id : -1);
                        };
                        "tab-connected" === message.type ? _this._getActiveTab().then(function(_a) {
                            var url = _a.url;
                            message.content = {
                                tab: exports.SETTINGS_TAB_ID,
                                url: url
                            }, processMessage(message);
                        }) : processMessage(message);
                    });
                }
            }, onPortConnection(this._initPortListener);
        }
        return GenericBackgroundMessageApiImpl.prototype.sendTo = function(tabId, type, content, callback, error) {
            var ports = this._tabPorts[tabId];
            if (ports && ports.length) {
                var msg = {
                    type: type,
                    content: content
                };
                callback && "function" == typeof callback && (msg.callid = util_1.guid(), this._callbacks[msg.callid] = callback), 
                ports.forEach(function(port) {
                    return port.postMessage(msg);
                });
            } else error && error({
                message: "no ports on specified tabId"
            });
        }, GenericBackgroundMessageApiImpl.prototype.listen = function(type, callback) {
            this._messageHelper.listen(type, callback);
        }, GenericBackgroundMessageApiImpl;
    }();
    exports.GenericBackgroundMessageApiImpl = GenericBackgroundMessageApiImpl;
}, function(module, exports, __webpack_require__) {
    var baseFor = __webpack_require__(120), keys = __webpack_require__(32);
    module.exports = function(object, iteratee) {
        return object && baseFor(object, iteratee, keys);
    };
}, function(module, exports, __webpack_require__) {
    (function(module) {
        var freeGlobal = __webpack_require__(122), freeExports = "object" == typeof exports && exports && !exports.nodeType && exports, freeModule = freeExports && "object" == typeof module && module && !module.nodeType && module, freeProcess = freeModule && freeModule.exports === freeExports && freeGlobal.process, nodeUtil = function() {
            try {
                return freeProcess && freeProcess.binding && freeProcess.binding("util");
            } catch (e) {}
        }();
        module.exports = nodeUtil;
    }).call(exports, __webpack_require__(77)(module));
}, function(module, exports) {
    module.exports = function(array, values) {
        for (var index = -1, length = values.length, offset = array.length; ++index < length; ) array[offset + index] = values[index];
        return array;
    };
}, function(module, exports, __webpack_require__) {
    var arrayFilter = __webpack_require__(192), stubArray = __webpack_require__(169), propertyIsEnumerable = Object.prototype.propertyIsEnumerable, nativeGetSymbols = Object.getOwnPropertySymbols, getSymbols = nativeGetSymbols ? function(object) {
        return null == object ? [] : (object = Object(object), arrayFilter(nativeGetSymbols(object), function(symbol) {
            return propertyIsEnumerable.call(object, symbol);
        }));
    } : stubArray;
    module.exports = getSymbols;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    }, __spread = this && this.__spread || function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var stdlib_1 = __webpack_require__(3), storage_migration_1 = __webpack_require__(195), content_1 = __webpack_require__(132);
    exports.runCompatibilityFixes = content_1.runCompatibilityFixes;
    var bg_1 = __webpack_require__(103);
    exports.bgPreload = bg_1.bgPreload, function(preferencesApi) {
        preferencesApi.windowLocalStorage = {
            get: function(key) {
                return stdlib_1.SafePromise.sync(function() {
                    return window.localStorage.getItem(key);
                });
            },
            set: function(key, value) {
                return stdlib_1.SafePromise.sync(function() {
                    return window.localStorage.setItem(key, value);
                });
            },
            getAll: function() {
                return stdlib_1.SafePromise.sync(function() {
                    var all = {};
                    return Object.keys(window.localStorage).forEach(function(key) {
                        all[key] = window.localStorage.getItem(key);
                    }), all;
                });
            },
            remove: function(key) {
                return stdlib_1.SafePromise.sync(function() {
                    return window.localStorage.removeItem(key);
                });
            },
            removeAll: function() {
                return stdlib_1.SafePromise.sync(function() {
                    return window.localStorage.clear();
                });
            }
        }, preferencesApi.browserStorageLocal = {
            get: function(key) {
                return __awaiter(this, void 0, void 0, function() {
                    var valueObject;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return [ 4, firefox.storage.local.get(key) ];

                          case 1:
                            return [ 2, (valueObject = _a.sent()).hasOwnProperty(key) ? valueObject[key] : null ];
                        }
                    });
                });
            },
            set: function(key, value) {
                return firefox.storage.local.set(((_a = {})[key] = value, _a));
                var _a;
            },
            getAll: function() {
                return firefox.storage.local.get(null);
            },
            remove: function(key) {
                return firefox.storage.local.remove(key);
            },
            removeAll: function() {
                return __awaiter(this, void 0, void 0, function() {
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return [ 4, firefox.storage.local.clear() ];

                          case 1:
                            return _a.sent(), [ 2 ];
                        }
                    });
                });
            }
        };
        var migration = new storage_migration_1.StorageMigration("firefoxLocalStorageToExtApi", preferencesApi.windowLocalStorage, preferencesApi.browserStorageLocal, [ "version" ]), migrationCompleted = Promise.resolve(!1), ensureMigrationCompletedCalled = !1;
        function getMigrationAwareMethod(apiName) {
            return function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return stdlib_1.assert(!0 === ensureMigrationCompletedCalled, "supposed to run data migration before accessing prefs with web-extensions API"), 
                migrationCompleted.then(function(completed) {
                    var instance = completed ? migration.migrationAwareDestination : preferencesApi.windowLocalStorage;
                    return instance[apiName].apply(instance, __spread(args));
                });
            };
        }
        preferencesApi.ensureMigrationCompleted = function() {
            ensureMigrationCompletedCalled = !0;
            var migrationCompletedPcs = stdlib_1.SafePromise.createCompletionSource();
            return migrationCompleted = migrationCompletedPcs.promise, migration.ensureMigrationCompleted().then(function(x) {
                return migrationCompletedPcs.resolve(!0), Promise.resolve(x);
            }, function(err) {
                return migrationCompletedPcs.resolve(!1), Promise.reject(err);
            });
        }, preferencesApi.migrationAware = {
            get: getMigrationAwareMethod("get"),
            set: getMigrationAwareMethod("set"),
            getAll: getMigrationAwareMethod("getAll"),
            remove: getMigrationAwareMethod("remove"),
            removeAll: getMigrationAwareMethod("removeAll")
        };
    }(exports.preferencesApi || (exports.preferencesApi = {}));
}, function(module, exports, __webpack_require__) {
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
    });
    var merge = __webpack_require__(172), config_1 = __webpack_require__(11);
    exports.PROTOCOL_VERSION = "1.0", exports.SITES_TO_RELOAD = [ "inbox.google.com", "mail.google.com", "yahoo.com", "mail.live.com", "facebook.com", "tumblr.com", "stackoverflow.com", "wordpress.com", "wordpress.org", "blogspot.com" ], 
    exports.FACEBOOK_SITES = [ "facebook.com", "messenger.com", "work.fb.com", "business.facebook.com" ], 
    exports.HTML_GHOST_SITES = __spread([ "twitter.com" ], exports.FACEBOOK_SITES), 
    exports.CUSTOM_UNSUPPORTED_MESSAGES = {
        "drive.google.com": {
            title: "Google Drive Not Supported",
            message: 'We hope to support Google Drive apps<br/> in the future, but for now please use your</br> <a class="openGrammarly" href="' + config_1.URLS.app + '">Grammarly Editor</a>.'
        },
        "docs.google.com": {
            title: "Google Drive Not Supported",
            message: 'We hope to support Google Drive apps<br/> in the future, but for now please use your</br> <a class="openGrammarly" href="' + config_1.URLS.app + '">Grammarly Editor</a>.'
        },
        "chrome.google.com": {
            title: "Web Store Not Supported"
        }
    };
    exports.PAGE_CONFIG_DEFAULT_INTERVAL = 18e5, exports.PAGE_CONFIG_UPDATE_INTERVALS = [ 6e5, exports.PAGE_CONFIG_DEFAULT_INTERVAL, 36e5, 108e5, 432e5, 864e5, 31536e6 ], 
    exports.OVERRIDE_PAGE_CONFIG = {}, exports.PAGE_CONFIG_INTERNAL = ((_a = {
        version: {
            enabled: !1,
            servicePage: !0
        },
        extensions: {
            enabled: !1,
            servicePage: !0
        },
        settings: {
            enabled: !1,
            servicePage: !0
        },
        "com.safari.grammarlyspellcheckergrammarchecker": {
            enabled: !1,
            matchInclusions: !0,
            servicePage: !0
        }
    })["app." + config_1.GRAMMARLY_DOMAIN] = {
        enabled: !1,
        grammarlyEditor: !0
    }, _a["linkedin.com"] = {
        pages: {
            "/messaging": {
                afterReplaceEvents: [ "input" ]
            }
        }
    }, _a["plus.google.com"] = {
        afterReplaceEvents: [ "keyup" ],
        minFieldHeight: 0,
        minFieldWidth: 0
    }, _a["facebook.com"] = {
        minFieldHeight: 0,
        pages: {
            "/marketplace": {
                afterReplaceEvents: [ "input" ]
            }
        }
    }, _a["mail.google.com"] = {
        fields: [ {
            name: "to"
        }, {
            name: "cc"
        }, {
            name: "bcc"
        }, {
            className: "vO"
        } ],
        subframes: !1
    }, _a["drive.google.com"] = {
        track: !0
    }, _a["docs.google.com"] = {
        track: !0
    }, _a["app.asana.com"] = {
        fields: [ {
            className: "task-row-text-input"
        } ]
    }, _a["tumblr.com"] = {
        fields: [ {
            attr: [ "aria-label", "Post title" ]
        }, {
            attr: [ "aria-label", "Type or paste a URL" ]
        } ]
    }, _a["chrome.google.com"] = {
        dontShowDisabledBadge: !0
    }, _a);
    var _a;
    exports.PAGE_CONFIG = {
        pageConfig: merge({}, {
            "hootsuite.com": {
                enabled: !1
            },
            "chrome.google.com": {
                enabled: !1
            },
            "facebook.com": {
                enabled: !0,
                pages: {
                    ".*/notes": {
                        enabled: !1
                    }
                }
            },
            "onedrive.live.com": {
                enabled: !1
            },
            "docs.com": {
                enabled: !1
            },
            "sp.docs.com": {
                enabled: !1
            },
            "docs.google.com": {
                enabled: !1
            },
            "drive.google.com": {
                enabled: !1
            },
            "texteditor.nsspot.net": {
                enabled: !1
            },
            "jsbin.com": {
                enabled: !1
            },
            "jsfiddle.net": {
                enabled: !1
            },
            "quora.com": {
                enabled: !1
            },
            "paper.dropbox.com": {
                enabled: !1
            },
            "mail.live.com": {
                enabled: !1,
                matchInclusions: !0
            },
            "imperavi.com": {
                enabled: !1
            },
            "usecanvas.com": {
                enabled: !1
            }
        }, exports.PAGE_CONFIG_INTERNAL)
    };
}, function(module, exports, __webpack_require__) {
    var Uint8Array = __webpack_require__(128);
    module.exports = function(arrayBuffer) {
        var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
        return new Uint8Array(result).set(new Uint8Array(arrayBuffer)), result;
    };
}, function(module, exports, __webpack_require__) {
    var isArrayLike = __webpack_require__(29), isObjectLike = __webpack_require__(17);
    module.exports = function(value) {
        return isObjectLike(value) && isArrayLike(value);
    };
}, function(module, exports, __webpack_require__) {
    var baseRest = __webpack_require__(94), isIterateeCall = __webpack_require__(199);
    module.exports = function(assigner) {
        return baseRest(function(object, sources) {
            var index = -1, length = sources.length, customizer = length > 1 ? sources[length - 1] : void 0, guard = length > 2 ? sources[2] : void 0;
            for (customizer = assigner.length > 3 && "function" == typeof customizer ? (length--, 
            customizer) : void 0, guard && isIterateeCall(sources[0], sources[1], guard) && (customizer = length < 3 ? void 0 : customizer, 
            length = 1), object = Object(object); ++index < length; ) {
                var source = sources[index];
                source && assigner(object, source, index, customizer);
            }
            return object;
        });
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var __WEBPACK_IMPORTED_MODULE_0__baseGetTag_js__ = __webpack_require__(310), __WEBPACK_IMPORTED_MODULE_1__getPrototype_js__ = __webpack_require__(315), __WEBPACK_IMPORTED_MODULE_2__isObjectLike_js__ = __webpack_require__(317), objectTag = "[object Object]", funcProto = Function.prototype, objectProto = Object.prototype, funcToString = funcProto.toString, hasOwnProperty = objectProto.hasOwnProperty, objectCtorString = funcToString.call(Object);
    __webpack_exports__.a = function(value) {
        if (!Object(__WEBPACK_IMPORTED_MODULE_2__isObjectLike_js__.a)(value) || Object(__WEBPACK_IMPORTED_MODULE_0__baseGetTag_js__.a)(value) != objectTag) return !1;
        var proto = Object(__WEBPACK_IMPORTED_MODULE_1__getPrototype_js__.a)(value);
        if (null === proto) return !0;
        var Ctor = hasOwnProperty.call(proto, "constructor") && proto.constructor;
        return "function" == typeof Ctor && Ctor instanceof Ctor && funcToString.call(Ctor) == objectCtorString;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.t = {
        SET_USER: "user/SET_USER",
        SET_GROUPS: "user/SET_GROUPS",
        SET_SETTINGS: "user/SET_SETTINGS",
        SESSION_INVALIDATE: "user/SESSION_INVALIDATE",
        INC_FIXED: "user/INC_FIXED",
        UPDATE_GROUPS: "user/UPDATE_GROUPS"
    }, exports.setUser = function(data) {
        return {
            type: exports.t.SET_USER,
            data: data
        };
    }, exports.setGroups = function(data) {
        return {
            type: exports.t.SET_GROUPS,
            data: data
        };
    }, exports.setSettings = function(data) {
        return {
            type: exports.t.SET_SETTINGS,
            data: data
        };
    }, exports.sessionInvalidate = function(reason) {
        return {
            type: exports.t.SESSION_INVALIDATE,
            reason: reason
        };
    }, exports.incFixed = function() {
        return {
            type: exports.t.INC_FIXED
        };
    }, exports.updateGroups = function() {
        return {
            type: exports.t.UPDATE_GROUPS
        };
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __assign = this && this.__assign || Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
        return t;
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
    }, __spread = this && this.__spread || function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var bgPageCallImpls, message = __webpack_require__(15), util_1 = __webpack_require__(2), tracker_1 = __webpack_require__(187), felogPixel_1 = __webpack_require__(140), config = __webpack_require__(11), felogClient_1 = __webpack_require__(334), sumoLogicClient_1 = __webpack_require__(335), log = __webpack_require__(1).Logger.create("lib.tracking.call");
    !function(bgPageCallImpls) {
        var felogClient = util_1.isBg() ? new felogClient_1.DefaultFelogClient(config.URLS.newFelog, config.appName, config.getVersion(), config.ENV, window.fetch.bind(window)) : void 0, sumoLogicClient = util_1.isBg() ? new sumoLogicClient_1.SumoLogicClient(config.URLS.sumoLogic, config.appName, config.getVersion(), config.ENV, window.fetch.bind(window)) : void 0;
        !function(methods) {
            methods.sendFelog = function(logger, message, level, extra) {
                if (!felogClient) throw Error("sendFelog unavailable");
                felogClient.sendEvent({
                    logger: logger,
                    message: message,
                    level: level,
                    extra: extra
                }).catch(function(_) {
                    return felogPixel_1.sendEventPixel(logger, message, level, extra, felogClient.getContext());
                });
            }, methods.sendSumoLogic = function(logger, message, level, extra) {
                if (!sumoLogicClient) throw Error("sumoLogicClient unavailable");
                sumoLogicClient.send({
                    logger: logger,
                    message: message,
                    level: level,
                    extra: extra
                }).catch(function(_) {
                    return felogPixel_1.sendEventPixel(logger, message, level, extra, sumoLogicClient.getContext());
                });
            }, methods.sendFelogManyEvents = function(events) {
                felogClient && felogClient.sendManyEvents(events);
            }, methods.sendFelogCrashLogs = function(events) {
                felogClient && felogClient.sendManyEvents(events, !0);
            }, methods.sendFelogUsageEvent = function(logger, message, level, usage) {
                if (!felogClient) throw Error("felogClient unavailable");
                felogClient.sendUsageEvent(logger, message, level, usage).catch(function(_) {
                    return felogPixel_1.sendEventPixel(logger, message, level);
                });
            }, methods.setUserId = function(id) {
                felogClient && felogClient.setUserId(id), sumoLogicClient && sumoLogicClient.setUserId(id);
            }, methods.setContainerId = function(containerId) {
                felogClient && felogClient.setContainerId(containerId), sumoLogicClient && sumoLogicClient.setContainerId(containerId);
            }, methods.sendTimes = function(name, times) {
                felogClient && times.forEach(function(t) {
                    return felogClient.sendTimer(name, t);
                });
            };
        }(bgPageCallImpls.methods || (bgPageCallImpls.methods = {})), bgPageCallImpls.CALL_HANDLER_ID = "tracking/RPC";
    }(bgPageCallImpls || (bgPageCallImpls = {})), exports.callBgPage = Object.keys(bgPageCallImpls.methods).reduce(function(o, k) {
        return o[k] = function() {
            for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
            return call.apply(void 0, __spread([ bgPageCallImpls.CALL_HANDLER_ID, k ], args));
        }, o;
    }, {});
    var trackingLog = [];
    function call(msg) {
        for (var data = [], _i = 1; _i < arguments.length; _i++) data[_i - 1] = arguments[_i];
        var fallback = function(e) {
            log.warn("tracking call " + msg + " failed, reason: ", e);
        };
        if (util_1.isBg()) util_1.asyncCall(function() {
            try {
                switch (logCall(msg, data), msg) {
                  case bgPageCallImpls.CALL_HANDLER_ID:
                    var method = data[0], args = data.slice(1);
                    (_a = bgPageCallImpls.methods)[method].apply(_a, __spread(args));
                    break;

                  default:
                    runMessage(msg, data);
                }
            } catch (e) {
                fallback(e);
            }
            var _a;
        }, 20); else {
            var timeout_1, preventTimeout_1 = function() {
                return clearInterval(timeout_1);
            };
            timeout_1 = window.setTimeout(function() {
                return e = "timeout call through bg page", preventTimeout_1(), void fallback(e);
                var e;
            }, 1e4), message.emitBackground("tracking-call", {
                msg: msg,
                data: data
            }, preventTimeout_1);
        }
    }
    function runMessage(msg, data) {
        var _c, _a = __read(msg.split("."), 2), p = _a[0], m = _a[1];
        if ("gnar" === p) if (tracker_1.tracker.gnar) if ("track" === m) {
            var _b = __read(data, 2), event_1 = _b[0], props = _b[1];
            tracker_1.tracker.gnar.track(__assign({
                eventName: config.gnarAppName + "/" + event_1
            }, props));
        } else tracker_1.tracker.gnar[m] ? (_c = tracker_1.tracker.gnar)[m].apply(_c, __spread(data)) : log.error("gnar client does not have method '" + m + "' for '" + msg + "' in runMessage"); else log.error("gnar client not available for '" + msg + "' in runMessage"); else log.error("unrecognized '" + msg + "' in runMessage");
    }
    function logCall(msg, data) {
        log.info(msg, data);
    }
    exports.call = call, exports.runMessage = runMessage, exports.logCall = logCall, 
    exports.getLog = function() {
        var result = trackingLog.slice(0);
        return trackingLog.length = 0, result;
    };
}, , function(module, exports, __webpack_require__) {
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
    });
    var config_1 = __webpack_require__(11), log = __webpack_require__(1).Logger.create("extension-api.message"), _f = function() {}, MessageHelperImpl = function() {
        return function() {
            var _this = this;
            this._listeners = {}, this._queue = {}, this.fire = function(type, content, callback, sender) {
                void 0 === callback && (callback = _f);
                var listeners = _this._listeners[type] || [];
                listeners.length ? listeners.forEach(function(fn) {
                    return fn(content, callback, sender);
                }) : (_this._queue[type] = _this._queue[type] || [], _this._queue[type].push({
                    content: content,
                    callback: callback,
                    sender: sender
                }));
            }, this.unlisten = function(type, cb) {
                var listeners = _this._listeners[type] || [], index = listeners.indexOf(cb);
                -1 !== index && (1 === listeners.length ? delete _this._listeners[type] : listeners.splice(index, 1));
            }, this.listenOnce = function(type, callback) {
                var listener = function(data, reply, sender) {
                    _this.unlisten(type, listener), callback && callback(data, reply, sender);
                };
                _this.listen(type, listener);
            }, this.listen = function(type, callback) {
                _this._listeners[type] = _this._listeners[type] || [], -1 === _this._listeners[type].indexOf(callback) && _this._listeners[type].push(callback);
                var queue = _this._queue[type] || [];
                if (queue.length) {
                    try {
                        for (var queue_1 = __values(queue), queue_1_1 = queue_1.next(); !queue_1_1.done; queue_1_1 = queue_1.next()) {
                            var item = queue_1_1.value;
                            try {
                                callback(item.content, item.callback, item.sender);
                            } catch (e) {
                                log.error("exception during proccesing buffered messages", e);
                            }
                        }
                    } catch (e_1_1) {
                        e_1 = {
                            error: e_1_1
                        };
                    } finally {
                        try {
                            queue_1_1 && !queue_1_1.done && (_a = queue_1.return) && _a.call(queue_1);
                        } finally {
                            if (e_1) throw e_1.error;
                        }
                    }
                    var e_1, _a;
                    delete _this._queue[type];
                }
            };
        };
    }();
    function getSafariActiveTab() {
        return safari.application.activeBrowserWindow && safari.application.activeBrowserWindow.activeTab;
    }
    exports.MessageHelperImpl = MessageHelperImpl, exports.safariBridgeId = "forge-bridge" + config_1.getUuid(), 
    exports.getSafariActiveTab = getSafariActiveTab, exports.getSafariActiveTabUrl = function() {
        var activeTab = getSafariActiveTab();
        return activeTab && activeTab.url || "http://newtab";
    }, exports.emitter = function() {
        var callbacks = {}, messageBuffer = {};
        return {
            emit: function(type, data, callback) {
                var listeners = callbacks[type];
                listeners ? listeners.forEach(function(cb) {
                    return cb(data, callback);
                }) : (messageBuffer[type] || (messageBuffer[type] = []), messageBuffer[type].push({
                    data: data,
                    callback: callback
                }));
            },
            on: function(type, cb) {
                callbacks[type] || (callbacks[type] = []), callbacks[type].push(cb), messageBuffer[type] && messageBuffer[type].forEach(function(msg) {
                    return cb(msg.data, msg.callback);
                });
            }
        };
    };
}, function(module, exports, __webpack_require__) {
    var arrayEach = __webpack_require__(92), baseCreate = __webpack_require__(119), baseForOwn = __webpack_require__(104), baseIteratee = __webpack_require__(65), getPrototype = __webpack_require__(59), isArray = __webpack_require__(8), isBuffer = __webpack_require__(35), isFunction = __webpack_require__(41), isObject = __webpack_require__(9), isTypedArray = __webpack_require__(40);
    module.exports = function(object, iteratee, accumulator) {
        var isArr = isArray(object), isArrLike = isArr || isBuffer(object) || isTypedArray(object);
        if (iteratee = baseIteratee(iteratee, 4), null == accumulator) {
            var Ctor = object && object.constructor;
            accumulator = isArrLike ? isArr ? new Ctor() : [] : isObject(object) && isFunction(Ctor) ? baseCreate(getPrototype(object)) : {};
        }
        return (isArrLike ? arrayEach : baseForOwn)(object, function(value, index, object) {
            return iteratee(accumulator, value, index, object);
        }), accumulator;
    };
}, function(module, exports, __webpack_require__) {
    var isObject = __webpack_require__(9), objectCreate = Object.create, baseCreate = function() {
        function object() {}
        return function(proto) {
            if (!isObject(proto)) return {};
            if (objectCreate) return objectCreate(proto);
            object.prototype = proto;
            var result = new object();
            return object.prototype = void 0, result;
        };
    }();
    module.exports = baseCreate;
}, function(module, exports, __webpack_require__) {
    var baseFor = __webpack_require__(219)();
    module.exports = baseFor;
}, function(module, exports, __webpack_require__) {
    var baseTimes = __webpack_require__(220), isArguments = __webpack_require__(45), isArray = __webpack_require__(8), isBuffer = __webpack_require__(35), isIndex = __webpack_require__(64), isTypedArray = __webpack_require__(40), hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(value, inherited) {
        var isArr = isArray(value), isArg = !isArr && isArguments(value), isBuff = !isArr && !isArg && isBuffer(value), isType = !isArr && !isArg && !isBuff && isTypedArray(value), skipIndexes = isArr || isArg || isBuff || isType, result = skipIndexes ? baseTimes(value.length, String) : [], length = result.length;
        for (var key in value) !inherited && !hasOwnProperty.call(value, key) || skipIndexes && ("length" == key || isBuff && ("offset" == key || "parent" == key) || isType && ("buffer" == key || "byteLength" == key || "byteOffset" == key) || isIndex(key, length)) || result.push(key);
        return result;
    };
}, function(module, exports, __webpack_require__) {
    (function(global) {
        var freeGlobal = "object" == typeof global && global && global.Object === Object && global;
        module.exports = freeGlobal;
    }).call(exports, __webpack_require__(34));
}, function(module, exports) {
    module.exports = function(func, transform) {
        return function(arg) {
            return func(transform(arg));
        };
    };
}, function(module, exports) {
    var funcToString = Function.prototype.toString;
    module.exports = function(func) {
        if (null != func) {
            try {
                return funcToString.call(func);
            } catch (e) {}
            try {
                return func + "";
            } catch (e) {}
        }
        return "";
    };
}, function(module, exports, __webpack_require__) {
    var SetCache = __webpack_require__(126), arraySome = __webpack_require__(258), cacheHas = __webpack_require__(127), COMPARE_PARTIAL_FLAG = 1, COMPARE_UNORDERED_FLAG = 2;
    module.exports = function(array, other, bitmask, customizer, equalFunc, stack) {
        var isPartial = bitmask & COMPARE_PARTIAL_FLAG, arrLength = array.length, othLength = other.length;
        if (arrLength != othLength && !(isPartial && othLength > arrLength)) return !1;
        var stacked = stack.get(array);
        if (stacked && stack.get(other)) return stacked == other;
        var index = -1, result = !0, seen = bitmask & COMPARE_UNORDERED_FLAG ? new SetCache() : void 0;
        for (stack.set(array, other), stack.set(other, array); ++index < arrLength; ) {
            var arrValue = array[index], othValue = other[index];
            if (customizer) var compared = isPartial ? customizer(othValue, arrValue, index, other, array, stack) : customizer(arrValue, othValue, index, array, other, stack);
            if (void 0 !== compared) {
                if (compared) continue;
                result = !1;
                break;
            }
            if (seen) {
                if (!arraySome(other, function(othValue, othIndex) {
                    if (!cacheHas(seen, othIndex) && (arrValue === othValue || equalFunc(arrValue, othValue, bitmask, customizer, stack))) return seen.push(othIndex);
                })) {
                    result = !1;
                    break;
                }
            } else if (arrValue !== othValue && !equalFunc(arrValue, othValue, bitmask, customizer, stack)) {
                result = !1;
                break;
            }
        }
        return stack.delete(array), stack.delete(other), result;
    };
}, function(module, exports, __webpack_require__) {
    var MapCache = __webpack_require__(81), setCacheAdd = __webpack_require__(256), setCacheHas = __webpack_require__(257);
    function SetCache(values) {
        var index = -1, length = null == values ? 0 : values.length;
        for (this.__data__ = new MapCache(); ++index < length; ) this.add(values[index]);
    }
    SetCache.prototype.add = SetCache.prototype.push = setCacheAdd, SetCache.prototype.has = setCacheHas, 
    module.exports = SetCache;
}, function(module, exports) {
    module.exports = function(cache, key) {
        return cache.has(key);
    };
}, function(module, exports, __webpack_require__) {
    var Uint8Array = __webpack_require__(12).Uint8Array;
    module.exports = Uint8Array;
}, function(module, exports, __webpack_require__) {
    var isObject = __webpack_require__(9);
    module.exports = function(value) {
        return value == value && !isObject(value);
    };
}, function(module, exports) {
    module.exports = function(key, srcValue) {
        return function(object) {
            return null != object && object[key] === srcValue && (void 0 !== srcValue || key in Object(object));
        };
    };
}, function(module, exports) {
    module.exports = {
        toU8IntArray: function(inputString) {
            for (var array = [], tempArrayOfChar = [], i = 0; i < inputString.length; i++) {
                var temp, charCode = inputString.charCodeAt(i);
                for (tempArrayOfChar.length = 0; (temp = 255 & charCode) || charCode; ) tempArrayOfChar.push(temp), 
                charCode >>>= 8;
                array = array.concat(tempArrayOfChar.reverse());
            }
            return array;
        },
        intToUnsignedHex: function(number) {
            for (var temp, hexArray = []; (temp = 65535 & number) || number; ) temp = temp.toString(16), 
            temp = "0000".slice(temp.length) + temp, hexArray.push(temp), number >>>= 16;
            return hexArray.reverse().join("");
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var stdlib_1 = __webpack_require__(3), helpers_1 = __webpack_require__(117), util_1 = __webpack_require__(2), interface_1 = __webpack_require__(61), log = __webpack_require__(1).Logger.create("Messaging.extension-api.content"), GenericContentScriptMessageApiImpl = function() {
        function GenericContentScriptMessageApiImpl(createPortConnection) {
            var _this = this;
            this.kind = "content-script-message-api", this._callbacks = {}, this._messageHelper = new helpers_1.MessageHelperImpl(), 
            this._proxyPortsStorage = {}, this.broadcastBackground = function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return _this._emit(_this.backgroundPort, "bg").apply(null, args);
            }, this.broadcast = function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return _this._emit(_this.broadcastPort, "tabs").apply(null, args);
            }, this._onPortMessage = function(msg) {
                log.trace("portMessage", msg);
            }, this._checkHealth = function() {
                var pingInterval = null, timeout = null, sendPing = function() {
                    return document.dispatchEvent(new CustomEvent("grammarly:ping"));
                }, alive = function() {
                    clearCheckers();
                }, abortByTimeout = function() {
                    [ _this.port, _this.backgroundPort, _this.broadcastPort ].forEach(function(x) {
                        x && x.removeMessageListeners && x.removeMessageListeners();
                    }), _this.port = _this.backgroundPort = _this.broadcastPort = null, clearCheckers(), 
                    document.addEventListener("grammarly:proxyports", _this._onGrammarlyResetAfterTimeout), 
                    document.dispatchEvent(new CustomEvent("grammarly:offline"));
                };
                function clearCheckers() {
                    document.removeEventListener("grammarly:pong", alive), timeout && (clearTimeout(timeout), 
                    timeout = null), pingInterval && (clearInterval(pingInterval), pingInterval = null);
                }
                return function() {
                    clearCheckers(), document.addEventListener("grammarly:pong", alive), pingInterval = window.setInterval(sendPing, 500), 
                    timeout = window.setTimeout(abortByTimeout, 5e3);
                };
            }(), this._onGrammarlyResetAfterTimeout = function() {
                document.removeEventListener("grammarly:proxyports", _this._onGrammarlyResetAfterTimeout), 
                _this.port = _this._initProxyPort(interface_1.ports.bridge, _this._onPortMessage, _this._checkHealth, !0), 
                _this.backgroundPort = _this._initProxyPort(interface_1.ports.background, _this._onBgPortMessage, _this._checkHealth), 
                _this.broadcastPort = _this._initProxyPort(interface_1.ports.broadcast, null, _this._checkHealth);
            }, this._onBgPortMessage = function(_a) {
                var callid = _a.callid, content = _a.content, type = _a.type;
                _this._callbacks[callid] ? (_this._callbacks[callid](content), delete _this._callbacks[callid]) : _this._messageHelper.fire(type, content, function(content) {
                    if (!_this.backgroundPort) throw new Error("fail reply to bg page - connection lost");
                    _this.backgroundPort.postMessage({
                        content: content,
                        callid: callid
                    });
                });
            }, this._initProxyPort = function(name, onMessage, onDisconnect, isCheckHealth) {
                void 0 === isCheckHealth && (isCheckHealth = !1);
                var port = _this._proxyPort(name);
                return isCheckHealth && _this._checkHealth(), onMessage && port.onMessage(onMessage), 
                onDisconnect && port.onDisconnect(onDisconnect), port;
            }, this._emit = function(port, name) {
                return function(type, content, callback, error) {
                    var callid = util_1.guid();
                    callback && "function" == typeof callback && (_this._callbacks[callid] = callback);
                    try {
                        if (!port) throw new Error("lost connection to " + name + " port");
                        port.postMessage({
                            type: type,
                            callid: callid,
                            content: content
                        });
                    } catch (e) {
                        if (!error) throw e;
                        error(e);
                    }
                };
            }, this._proxyPort = function(name) {
                _this._proxyPortsStorage[name] = {};
                var process = function(type, e) {
                    var data = e.detail;
                    if (data.name === name) {
                        var cb = _this._proxyPortsStorage[name][type];
                        cb && cb(data.msg);
                    }
                }, successProccess = function(e) {
                    return process("success", e);
                }, errorProccess = function(e) {
                    return process("error", e);
                };
                return document.addEventListener("grammarly:message", successProccess), document.addEventListener("grammarly:error", errorProccess), 
                {
                    postMessage: function(data) {
                        void 0 === data && (data = {});
                        var detail = {
                            data: data,
                            name: name
                        };
                        return document.dispatchEvent(new CustomEvent("grammarly:action", {
                            detail: detail
                        }));
                    },
                    onMessage: function(cb) {
                        _this._proxyPortsStorage[name].success = cb;
                    },
                    onDisconnect: function(cb) {
                        _this._proxyPortsStorage[name].error = cb;
                    },
                    removeMessageListeners: function() {
                        document.removeEventListener("grammarly:message", successProccess), document.removeEventListener("grammarly:error", errorProccess);
                    }
                };
            }, this.port = createPortConnection(interface_1.ports.bridge), this.port.onMessage(this._onPortMessage), 
            this.port.onDisconnect(function() {
                _this.port = null, _this.port = _this._initProxyPort(interface_1.ports.bridge, _this._onPortMessage, _this._checkHealth, !0);
            }), this.backgroundPort = createPortConnection(interface_1.ports.background), this.backgroundPort.onMessage(this._onBgPortMessage), 
            this.backgroundPort.onDisconnect(function() {
                _this.backgroundPort = null, _this.backgroundPort = _this._initProxyPort(interface_1.ports.background, _this._onBgPortMessage, _this._checkHealth);
            }), this.broadcastPort = createPortConnection(interface_1.ports.broadcast), this.broadcastPort.onDisconnect(function() {
                _this.broadcastPort = null, _this.broadcastPort = _this._initProxyPort(interface_1.ports.broadcast, null, _this._checkHealth);
            });
        }
        return GenericContentScriptMessageApiImpl.prototype.listen = function(type, callback) {
            this._messageHelper.listen(type, callback);
        }, GenericContentScriptMessageApiImpl.prototype.toFocused = function(type, content) {
            var _this = this;
            return stdlib_1.SafePromise.create(function(resolve) {
                if (!_this.port) throw new Error("lost connection to bg page");
                _this.port.postMessage({
                    method: "message.toFocussed",
                    params: {
                        type: type,
                        content: content
                    }
                }), resolve();
            });
        }, GenericContentScriptMessageApiImpl;
    }();
    exports.GenericContentScriptMessageApiImpl = GenericContentScriptMessageApiImpl, 
    exports.runCompatibilityFixes = function() {
        window.addEventListener("update-window-size-gr", function(e) {
            var node = document.createElement("div");
            if (node.style.height = "1px", e.detail && e.detail.force) {
                var interval_1 = setInterval(function() {
                    document.body.appendChild(node), setTimeout(function() {
                        node.parentNode && node.parentNode.removeChild(node);
                    }, 10);
                }, 100);
                setTimeout(function() {
                    return clearInterval(interval_1);
                }, 405);
            }
        }, !1), window.addEventListener("close-popup-gr", function() {
            -1 !== window.navigator.userAgent.indexOf("Firefox") && window.close();
        }, !1);
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.handleChromeError = function(onOk, handleErr) {
        chrome.runtime.lastError ? handleErr(chrome.runtime.lastError) : onOk();
    };
}, function(module, exports, __webpack_require__) {
    var baseAssignValue = __webpack_require__(67), eq = __webpack_require__(36);
    module.exports = function(object, key, value) {
        (void 0 === value || eq(object[key], value)) && (void 0 !== value || key in object) || baseAssignValue(object, key, value);
    };
}, function(module, exports, __webpack_require__) {
    var getNative = __webpack_require__(26), defineProperty = function() {
        try {
            var func = getNative(Object, "defineProperty");
            return func({}, "", {}), func;
        } catch (e) {}
    }();
    module.exports = defineProperty;
}, function(module, exports) {
    module.exports = function(object, key) {
        return "__proto__" == key ? void 0 : object[key];
    };
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var each = __webpack_require__(96), util_1 = (__webpack_require__(39), __webpack_require__(2)), lKey = util_1.guid();
    function listen(e, event, cb, unbind, bubble) {
        if (void 0 === bubble && (bubble = !1), null != e) {
            var el = e;
            if ("string" != typeof event) return each(event, function(value, key) {
                listen(el, key, value, unbind);
            });
            if (cb) {
                var listeners = el[lKey] || [];
                return el[lKey] = listeners, unbind ? (el[lKey] = listeners.filter(function(l) {
                    return !(l.event === event && l.cb === cb);
                }), el.removeEventListener(event, cb, bubble)) : (listeners.push({
                    event: event,
                    cb: cb
                }), el.addEventListener(event, cb, bubble)), {
                    el: el,
                    event: event,
                    cb: cb,
                    bubble: bubble
                };
            }
        }
    }
    exports.listen = listen, exports.unlisten = function unlisten(e, event, cb, bubble) {
        var el = e;
        event || null == el[lKey] ? listen(el, event, cb, !0, bubble) : el[lKey].forEach(function(l) {
            return unlisten(el, l.event, l.cb, l.bubble);
        });
    };
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var repeat = exports.repeat = function(str, times) {
        return new Array(times + 1).join(str);
    }, pad = exports.pad = function(num, maxLength) {
        return repeat("0", maxLength - num.toString().length) + num;
    };
    exports.formatTime = function(time) {
        return pad(time.getHours(), 2) + ":" + pad(time.getMinutes(), 2) + ":" + pad(time.getSeconds(), 2) + "." + pad(time.getMilliseconds(), 3);
    }, exports.timer = "undefined" != typeof performance && null !== performance && "function" == typeof performance.now ? performance : Date;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    Object.defineProperty(__webpack_exports__, "__esModule", {
        value: !0
    });
    var __WEBPACK_IMPORTED_MODULE_0__createStore__ = __webpack_require__(144), __WEBPACK_IMPORTED_MODULE_1__combineReducers__ = __webpack_require__(321), __WEBPACK_IMPORTED_MODULE_2__bindActionCreators__ = __webpack_require__(322), __WEBPACK_IMPORTED_MODULE_3__applyMiddleware__ = __webpack_require__(323), __WEBPACK_IMPORTED_MODULE_4__compose__ = __webpack_require__(147);
    __webpack_require__(146);
    __webpack_require__.d(__webpack_exports__, "createStore", function() {
        return __WEBPACK_IMPORTED_MODULE_0__createStore__.b;
    }), __webpack_require__.d(__webpack_exports__, "combineReducers", function() {
        return __WEBPACK_IMPORTED_MODULE_1__combineReducers__.a;
    }), __webpack_require__.d(__webpack_exports__, "bindActionCreators", function() {
        return __WEBPACK_IMPORTED_MODULE_2__bindActionCreators__.a;
    }), __webpack_require__.d(__webpack_exports__, "applyMiddleware", function() {
        return __WEBPACK_IMPORTED_MODULE_3__applyMiddleware__.a;
    }), __webpack_require__.d(__webpack_exports__, "compose", function() {
        return __WEBPACK_IMPORTED_MODULE_4__compose__.a;
    });
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_require__.d(__webpack_exports__, "a", function() {
        return ActionTypes;
    }), __webpack_exports__.b = function createStore(reducer, preloadedState, enhancer) {
        var _ref2;
        "function" == typeof preloadedState && void 0 === enhancer && (enhancer = preloadedState, 
        preloadedState = void 0);
        if (void 0 !== enhancer) {
            if ("function" != typeof enhancer) throw new Error("Expected the enhancer to be a function.");
            return enhancer(createStore)(reducer, preloadedState);
        }
        if ("function" != typeof reducer) throw new Error("Expected the reducer to be a function.");
        var currentReducer = reducer;
        var currentState = preloadedState;
        var currentListeners = [];
        var nextListeners = currentListeners;
        var isDispatching = !1;
        function ensureCanMutateNextListeners() {
            nextListeners === currentListeners && (nextListeners = currentListeners.slice());
        }
        function getState() {
            return currentState;
        }
        function subscribe(listener) {
            if ("function" != typeof listener) throw new Error("Expected listener to be a function.");
            var isSubscribed = !0;
            return ensureCanMutateNextListeners(), nextListeners.push(listener), function() {
                if (isSubscribed) {
                    isSubscribed = !1, ensureCanMutateNextListeners();
                    var index = nextListeners.indexOf(listener);
                    nextListeners.splice(index, 1);
                }
            };
        }
        function dispatch(action) {
            if (!Object(__WEBPACK_IMPORTED_MODULE_0_lodash_es_isPlainObject__.a)(action)) throw new Error("Actions must be plain objects. Use custom middleware for async actions.");
            if (void 0 === action.type) throw new Error('Actions may not have an undefined "type" property. Have you misspelled a constant?');
            if (isDispatching) throw new Error("Reducers may not dispatch actions.");
            try {
                isDispatching = !0, currentState = currentReducer(currentState, action);
            } finally {
                isDispatching = !1;
            }
            for (var listeners = currentListeners = nextListeners, i = 0; i < listeners.length; i++) {
                var listener = listeners[i];
                listener();
            }
            return action;
        }
        dispatch({
            type: ActionTypes.INIT
        });
        return _ref2 = {
            dispatch: dispatch,
            subscribe: subscribe,
            getState: getState,
            replaceReducer: function(nextReducer) {
                if ("function" != typeof nextReducer) throw new Error("Expected the nextReducer to be a function.");
                currentReducer = nextReducer, dispatch({
                    type: ActionTypes.INIT
                });
            }
        }, _ref2[__WEBPACK_IMPORTED_MODULE_1_symbol_observable__.a] = function() {
            var _ref, outerSubscribe = subscribe;
            return (_ref = {
                subscribe: function(observer) {
                    if ("object" != typeof observer) throw new TypeError("Expected the observer to be an object.");
                    function observeState() {
                        observer.next && observer.next(getState());
                    }
                    observeState();
                    var unsubscribe = outerSubscribe(observeState);
                    return {
                        unsubscribe: unsubscribe
                    };
                }
            })[__WEBPACK_IMPORTED_MODULE_1_symbol_observable__.a] = function() {
                return this;
            }, _ref;
        }, _ref2;
    };
    var __WEBPACK_IMPORTED_MODULE_0_lodash_es_isPlainObject__ = __webpack_require__(113), __WEBPACK_IMPORTED_MODULE_1_symbol_observable__ = __webpack_require__(318), ActionTypes = {
        INIT: "@@redux/INIT"
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var Symbol = __webpack_require__(311).a.Symbol;
    __webpack_exports__.a = Symbol;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function() {
        for (var _len = arguments.length, funcs = Array(_len), _key = 0; _key < _len; _key++) funcs[_key] = arguments[_key];
        if (0 === funcs.length) return function(arg) {
            return arg;
        };
        if (1 === funcs.length) return funcs[0];
        return funcs.reduce(function(a, b) {
            return function() {
                return a(b.apply(void 0, arguments));
            };
        });
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.utils = exports.effects = exports.takeLatest = exports.takeEvery = exports.storeIO = exports.runSaga = exports.isCancelError = exports.SagaCancellationException = void 0;
    var _runSaga = __webpack_require__(325);
    Object.defineProperty(exports, "runSaga", {
        enumerable: !0,
        get: function() {
            return _runSaga.runSaga;
        }
    }), Object.defineProperty(exports, "storeIO", {
        enumerable: !0,
        get: function() {
            return _runSaga.storeIO;
        }
    });
    var _sagaHelpers = __webpack_require__(326);
    Object.defineProperty(exports, "takeEvery", {
        enumerable: !0,
        get: function() {
            return _sagaHelpers.takeEvery;
        }
    }), Object.defineProperty(exports, "takeLatest", {
        enumerable: !0,
        get: function() {
            return _sagaHelpers.takeLatest;
        }
    });
    var _middleware2 = _interopRequireDefault(__webpack_require__(327)), _SagaCancellationException3 = _interopRequireDefault(__webpack_require__(55)), effects = _interopRequireWildcard(__webpack_require__(150)), utils = _interopRequireWildcard(__webpack_require__(328));
    function _interopRequireWildcard(obj) {
        if (obj && obj.__esModule) return obj;
        var newObj = {};
        if (null != obj) for (var key in obj) Object.prototype.hasOwnProperty.call(obj, key) && (newObj[key] = obj[key]);
        return newObj.default = obj, newObj;
    }
    function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
            default: obj
        };
    }
    exports.default = _middleware2.default;
    var SagaCancellationException = exports.SagaCancellationException = _SagaCancellationException3.default;
    exports.isCancelError = function(error) {
        return error instanceof SagaCancellationException;
    };
    exports.effects = effects, exports.utils = utils;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.default = function() {
        var cbs = [];
        return {
            subscribe: function(cb) {
                return cbs.push(cb), function() {
                    return (0, _utils.remove)(cbs, cb);
                };
            },
            emit: function(item) {
                cbs.slice().forEach(function(cb) {
                    return cb(item);
                });
            }
        };
    };
    var _utils = __webpack_require__(21);
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.select = exports.cancel = exports.join = exports.fork = exports.cps = exports.apply = exports.call = exports.race = exports.put = exports.take = void 0;
    var _io = __webpack_require__(54);
    exports.take = _io.take, exports.put = _io.put, exports.race = _io.race, exports.call = _io.call, 
    exports.apply = _io.apply, exports.cps = _io.cps, exports.fork = _io.fork, exports.join = _io.join, 
    exports.cancel = _io.cancel, exports.select = _io.select;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var userActions = __webpack_require__(114), settingsActions = __webpack_require__(89), user = userActions, connection = __webpack_require__(98), settings = settingsActions;
    exports.pureActions = Object.assign({}, user, connection, settings);
}, function(module, exports, __webpack_require__) {
    "use strict";
    var ErrorLike;
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), function(ErrorLike) {
        ErrorLike.isErrorLike = function(error) {
            var errorLike = error;
            return errorLike && (void 0 !== errorLike.message && void 0 !== errorLike.name || void 0 !== errorLike.stack);
        };
    }(ErrorLike = exports.ErrorLike || (exports.ErrorLike = {})), function(EventProps) {
        EventProps.fromAny = function(obj) {
            return function fromAnyInternal(obj, refs, searchNonEnumerable) {
                if (!obj) return {};
                var res = {}, getKeys = searchNonEnumerable ? Object.getOwnPropertyNames : Object.keys;
                return getKeys(obj).forEach(function(key) {
                    var v = obj[key];
                    if (null == v || "number" == typeof v || "string" == typeof v || "boolean" == typeof v) res[key] = v; else if ("object" == typeof v) if (v instanceof Boolean || v instanceof Number || v instanceof String || v instanceof Date || v instanceof RegExp) res[key] = v.toString(); else if (-1 === refs.indexOf(v)) {
                        refs.push(v);
                        var newObj = fromAnyInternal(v, refs, ErrorLike.isErrorLike(v));
                        Object.keys(newObj).length > 0 && (res[key] = newObj);
                    }
                }), res;
            }(obj, [ obj ], ErrorLike.isErrorLike(obj));
        };
    }(exports.EventProps || (exports.EventProps = {}));
    var nameRegexp = /^(?!\.[\w])[\w.]*\w$/;
    exports.validateName = function(name) {
        if ("" === name) throw new Error("Empty name");
        if (!nameRegexp.test(name)) throw new Error("Invalid name: " + name + ". Should be hierarchical dot separated string and may contain only word characters)");
    };
}, , , , function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.second = 1e3, exports.minute = 60 * exports.second, exports.hour = 60 * exports.minute, 
    exports.day = 24 * exports.hour, exports.week = 7 * exports.day, exports.seconds = function(s) {
        return s * exports.second;
    }, exports.hertz = function(hz) {
        return exports.second / hz;
    };
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var _a, logRank = ((_a = {}).TRACE = 1, _a.DEBUG = 2, _a.INFO = 3, _a.WARN = 4, 
    _a.ERROR = 5, _a.FATAL = 6, _a);
    exports.getLogRank = function(level) {
        return logRank[level] || 0;
    };
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    var isPrototype = __webpack_require__(56), nativeKeys = __webpack_require__(226), hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(object) {
        if (!isPrototype(object)) return nativeKeys(object);
        var result = [];
        for (var key in Object(object)) hasOwnProperty.call(object, key) && "constructor" != key && result.push(key);
        return result;
    };
}, function(module, exports) {
    module.exports = function(set) {
        var index = -1, result = Array(set.size);
        return set.forEach(function(value) {
            result[++index] = value;
        }), result;
    };
}, function(module, exports, __webpack_require__) {
    var baseGetAllKeys = __webpack_require__(168), getSymbols = __webpack_require__(107), keys = __webpack_require__(32);
    module.exports = function(object) {
        return baseGetAllKeys(object, keys, getSymbols);
    };
}, function(module, exports, __webpack_require__) {
    var arrayPush = __webpack_require__(106), isArray = __webpack_require__(8);
    module.exports = function(object, keysFunc, symbolsFunc) {
        var result = keysFunc(object);
        return isArray(object) ? result : arrayPush(result, symbolsFunc(object));
    };
}, function(module, exports) {
    module.exports = function() {
        return [];
    };
}, function(module, exports, __webpack_require__) {
    var baseToString = __webpack_require__(271);
    module.exports = function(value) {
        return null == value ? "" : baseToString(value);
    };
}, function(module, exports, __webpack_require__) {
    var baseIsEqual = __webpack_require__(82);
    module.exports = function(value, other) {
        return baseIsEqual(value, other);
    };
}, function(module, exports, __webpack_require__) {
    var baseMerge = __webpack_require__(282), merge = __webpack_require__(112)(function(object, source, srcIndex) {
        baseMerge(object, source, srcIndex);
    });
    module.exports = merge;
}, function(module, exports, __webpack_require__) {
    (function(module) {
        var root = __webpack_require__(12), freeExports = "object" == typeof exports && exports && !exports.nodeType && exports, freeModule = freeExports && "object" == typeof module && module && !module.nodeType && module, Buffer = freeModule && freeModule.exports === freeExports ? root.Buffer : void 0, allocUnsafe = Buffer ? Buffer.allocUnsafe : void 0;
        module.exports = function(buffer, isDeep) {
            if (isDeep) return buffer.slice();
            var length = buffer.length, result = allocUnsafe ? allocUnsafe(length) : new buffer.constructor(length);
            return buffer.copy(result), result;
        };
    }).call(exports, __webpack_require__(77)(module));
}, function(module, exports, __webpack_require__) {
    var cloneArrayBuffer = __webpack_require__(110);
    module.exports = function(typedArray, isDeep) {
        var buffer = isDeep ? cloneArrayBuffer(typedArray.buffer) : typedArray.buffer;
        return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
    };
}, function(module, exports) {
    module.exports = function(source, array) {
        var index = -1, length = source.length;
        for (array || (array = Array(length)); ++index < length; ) array[index] = source[index];
        return array;
    };
}, function(module, exports, __webpack_require__) {
    var baseCreate = __webpack_require__(119), getPrototype = __webpack_require__(59), isPrototype = __webpack_require__(56);
    module.exports = function(object) {
        return "function" != typeof object.constructor || isPrototype(object) ? {} : baseCreate(getPrototype(object));
    };
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), getPrototype = __webpack_require__(59), isObjectLike = __webpack_require__(17), objectTag = "[object Object]", funcProto = Function.prototype, objectProto = Object.prototype, funcToString = funcProto.toString, hasOwnProperty = objectProto.hasOwnProperty, objectCtorString = funcToString.call(Object);
    module.exports = function(value) {
        if (!isObjectLike(value) || baseGetTag(value) != objectTag) return !1;
        var proto = getPrototype(value);
        if (null === proto) return !0;
        var Ctor = hasOwnProperty.call(proto, "constructor") && proto.constructor;
        return "function" == typeof Ctor && Ctor instanceof Ctor && funcToString.call(Ctor) == objectCtorString;
    };
}, function(module, exports, __webpack_require__) {
    var baseAssignValue = __webpack_require__(67), eq = __webpack_require__(36), hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(object, key, value) {
        var objValue = object[key];
        hasOwnProperty.call(object, key) && eq(objValue, value) && (void 0 !== value || key in object) || baseAssignValue(object, key, value);
    };
}, , function(module, exports, __webpack_require__) {
    var debounce = __webpack_require__(53), isObject = __webpack_require__(9), FUNC_ERROR_TEXT = "Expected a function";
    module.exports = function(func, wait, options) {
        var leading = !0, trailing = !0;
        if ("function" != typeof func) throw new TypeError(FUNC_ERROR_TEXT);
        return isObject(options) && (leading = "leading" in options ? !!options.leading : leading, 
        trailing = "trailing" in options ? !!options.trailing : trailing), debounce(func, wait, {
            leading: leading,
            maxWait: wait,
            trailing: trailing
        });
    };
}, function(module, exports, __webpack_require__) {
    var baseForOwn = __webpack_require__(104), baseEach = __webpack_require__(302)(baseForOwn);
    module.exports = baseEach;
}, function(module, exports, __webpack_require__) {
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
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.logger = exports.defaults = void 0;
    var obj, _extends = Object.assign || function(target) {
        for (var i = 1; i < arguments.length; i++) {
            var source = arguments[i];
            for (var key in source) Object.prototype.hasOwnProperty.call(source, key) && (target[key] = source[key]);
        }
        return target;
    }, _core = __webpack_require__(306), _helpers = __webpack_require__(142), _defaults = __webpack_require__(309), _defaults2 = (obj = _defaults) && obj.__esModule ? obj : {
        default: obj
    };
    function createLogger() {
        var options = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}, loggerOptions = _extends({}, _defaults2.default, options), logger = loggerOptions.logger, transformer = loggerOptions.transformer, stateTransformer = loggerOptions.stateTransformer, errorTransformer = loggerOptions.errorTransformer, predicate = loggerOptions.predicate, logErrors = loggerOptions.logErrors, diffPredicate = loggerOptions.diffPredicate;
        if (void 0 === logger) return function() {
            return function(next) {
                return function(action) {
                    return next(action);
                };
            };
        };
        if (transformer && console.error("Option 'transformer' is deprecated, use 'stateTransformer' instead!"), 
        options.getState && options.dispatch) return console.error("[redux-logger] redux-logger not installed. Make sure to pass logger instance as middleware:\n\n// Logger with default options\nimport { logger } from 'redux-logger'\nconst store = createStore(\n  reducer,\n  applyMiddleware(logger)\n)\n\n\n// Or you can create your own logger with custom options http://bit.ly/redux-logger-options\nimport createLogger from 'redux-logger'\n\nconst logger = createLogger({\n  // ...options\n});\n\nconst store = createStore(\n  reducer,\n  applyMiddleware(logger)\n)\n"), 
        function() {
            return function(next) {
                return function(action) {
                    return next(action);
                };
            };
        };
        var logBuffer = [];
        return function(_ref) {
            var getState = _ref.getState;
            return function(next) {
                return function(action) {
                    if ("function" == typeof predicate && !predicate(getState, action)) return next(action);
                    var logEntry = {};
                    logBuffer.push(logEntry), logEntry.started = _helpers.timer.now(), logEntry.startedTime = new Date(), 
                    logEntry.prevState = stateTransformer(getState()), logEntry.action = action;
                    var returnedValue = void 0;
                    if (logErrors) try {
                        returnedValue = next(action);
                    } catch (e) {
                        logEntry.error = errorTransformer(e);
                    } else returnedValue = next(action);
                    logEntry.took = _helpers.timer.now() - logEntry.started, logEntry.nextState = stateTransformer(getState());
                    var diff = loggerOptions.diff && "function" == typeof diffPredicate ? diffPredicate(getState, action) : loggerOptions.diff;
                    if ((0, _core.printBuffer)(logBuffer, _extends({}, loggerOptions, {
                        diff: diff
                    })), logBuffer.length = 0, logEntry.error) throw logEntry.error;
                    return returnedValue;
                };
            };
        };
    }
    var defaultLogger = createLogger();
    exports.defaults = _defaults2.default, exports.logger = defaultLogger, exports.default = createLogger, 
    module.exports = exports.default;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var actions_1 = __webpack_require__(114);
    exports.defaultUser = {
        anonymous: !0,
        premium: !1
    }, exports.userReducer = function(state, _a) {
        void 0 === state && (state = exports.defaultUser);
        var type = _a.type, _b = _a.data, data = void 0 === _b ? {} : _b;
        switch (type) {
          case actions_1.t.SET_USER:
            return data;

          case actions_1.t.SET_SETTINGS:
            return Object.assign({}, state, {
                settings: data
            });

          case actions_1.t.SET_GROUPS:
            return Object.assign({}, state, {
                mimic: data.mimic,
                experiments: data.experiments
            });

          case actions_1.t.INC_FIXED:
            var fixed_errors = state.fixed_errors + 1;
            return Object.assign({}, state, {
                fixed_errors: fixed_errors
            });

          default:
            return state;
        }
    };
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.tracker = {};
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Config = __webpack_require__(10), call_1 = __webpack_require__(115), telemetry_1 = __webpack_require__(141), telemetry_2 = __webpack_require__(97), newConfig_1 = __webpack_require__(25), log = __webpack_require__(1).Logger.create("lib.tracking.logger");
    exports.felog = new telemetry_1.Telemetry(call_1.callBgPage.sendFelog.bind(call_1.callBgPage), call_1.callBgPage.sendFelogUsageEvent.bind(call_1.callBgPage), call_1.callBgPage.setUserId.bind(call_1.callBgPage), call_1.callBgPage.setContainerId.bind(call_1.callBgPage), call_1.callBgPage.sendTimes.bind(call_1.callBgPage), Config.getGlobal().appConfig.felog.sendUsageMetrics, telemetry_2.PerformanceMetrics.create(window.performance), Config.getGlobal().appConfig.felog.sendPerfMetrics, call_1.callBgPage.sendFelogManyEvents.bind(call_1.callBgPage), call_1.callBgPage.sendFelogCrashLogs.bind(call_1.callBgPage)), 
    newConfig_1.isBg() && (log.info("Installing unhandled error loggers..."), window.addEventListener("error", function(e) {
        return exports.felog.unhandledBgPageException(e);
    }), window.addEventListener("unhandledrejection", function(e) {
        return exports.felog.unhandledBgPageRejection(e);
    }));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), function(SiteCategory) {
        SiteCategory.gdocs = "gdocs", SiteCategory.other = "other";
    }(exports.SiteCategory || (exports.SiteCategory = {}));
}, , , function(module, exports) {
    module.exports = function(array, predicate) {
        for (var index = -1, length = null == array ? 0 : array.length, resIndex = 0, result = []; ++index < length; ) {
            var value = array[index];
            predicate(value, index, array) && (result[resIndex++] = value);
        }
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var Set = __webpack_require__(26)(__webpack_require__(12), "Set");
    module.exports = Set;
}, function(module, exports, __webpack_require__) {
    __webpack_require__(278);
    var algorithms = {
        superfasthash: __webpack_require__(279),
        murmurhash3: __webpack_require__(280)
    };
    module.exports = {
        createHash: function(algorithm) {
            algorithm = algorithm.replace(/![a-zA-z0-9]/g, "").toLowerCase();
            try {
                return algorithms[algorithm];
            } catch (e) {
                throw new Error(e);
            }
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var StorageMigrationResult, InternalStorageMigrationResult, stdlib_1 = __webpack_require__(3), isEqual = __webpack_require__(171);
    function createMigrationAwareApi(api, preserveValue) {
        return {
            get: api.get.bind(api),
            set: api.set.bind(api),
            getAll: api.getAll.bind(api),
            remove: api.remove.bind(api),
            removeAll: function() {
                return __awaiter(this, void 0, void 0, function() {
                    var all;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return [ 4, api.getAll() ];

                          case 1:
                            return all = _a.sent(), [ 4, api.removeAll() ];

                          case 2:
                            return _a.sent(), [ 4, Promise.all(Object.keys(all).filter(preserveValue).map(function(k) {
                                return api.set(k, all[k]);
                            })) ];

                          case 3:
                            return _a.sent(), [ 2 ];
                        }
                    });
                });
            }
        };
    }
    !function(StorageMigrationResult) {
        StorageMigrationResult[StorageMigrationResult.success = 0] = "success", StorageMigrationResult[StorageMigrationResult.successWithEmpty = 1] = "successWithEmpty", 
        StorageMigrationResult[StorageMigrationResult.alreadyMigrated = 2] = "alreadyMigrated";
    }(StorageMigrationResult = exports.StorageMigrationResult || (exports.StorageMigrationResult = {})), 
    function(InternalStorageMigrationResult) {
        InternalStorageMigrationResult[InternalStorageMigrationResult.nonEmptyMigration = 0] = "nonEmptyMigration", 
        InternalStorageMigrationResult[InternalStorageMigrationResult.emptyMigration = 1] = "emptyMigration";
    }(InternalStorageMigrationResult || (InternalStorageMigrationResult = {})), exports.createMigrationAwareApi = createMigrationAwareApi;
    var StorageMigration = function() {
        function StorageMigration(_name, _source, _destination, _destValuesToKeep) {
            void 0 === _destValuesToKeep && (_destValuesToKeep = []);
            var _this = this;
            this._name = _name, this._source = _source, this._destination = _destination, this._destValuesToKeep = _destValuesToKeep, 
            this._migrationFlagSuccessfulValue = "ok", this._migrationFlagUniqueKey = "104ccd8c-9919-9ae4-931f-782fb197486c", 
            this._migrationFlagKey = "__migration-" + this._migrationFlagUniqueKey + ":(" + this._name + ")", 
            this._migrationInProgress = !1, this.migrationAwareDestination = createMigrationAwareApi(this._destination, function(k) {
                return k === _this._migrationFlagKey;
            });
        }
        return StorageMigration.prototype._getMigrated = function() {
            var _this = this;
            return this._destination.get(this._migrationFlagKey).then(function(x) {
                return x === _this._migrationFlagSuccessfulValue;
            });
        }, StorageMigration.prototype._setMigrated = function() {
            return __awaiter(this, void 0, void 0, function() {
                var actualStatus;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return [ 4, this._destination.set(this._migrationFlagKey, this._migrationFlagSuccessfulValue) ];

                      case 1:
                        return _a.sent(), [ 4, this._destination.get(this._migrationFlagKey) ];

                      case 2:
                        if ((actualStatus = _a.sent()) !== this._migrationFlagSuccessfulValue) throw new Error("Could not verify status write, actual value: " + actualStatus);
                        return [ 2 ];
                    }
                });
            });
        }, StorageMigration.prototype._runMigration = function() {
            return __awaiter(this, void 0, void 0, function() {
                var payload_1, sourceIsEmpty, _a, _b, err_1, _this = this;
                return __generator(this, function(_c) {
                    switch (_c.label) {
                      case 0:
                        stdlib_1.assert(!this._migrationInProgress, "migration already in progress"), this._migrationInProgress = !0, 
                        _c.label = 1;

                      case 1:
                        return _c.trys.push([ 1, 7, , 8 ]), [ 4, this._source.getAll() ];

                      case 2:
                        return payload_1 = _c.sent(), sourceIsEmpty = 0 === Object.keys(payload_1).length, 
                        [ 4, Promise.all(this._destValuesToKeep.map(function(k) {
                            return _this._destination.get(k).then(function(v) {
                                null != v && (payload_1[k] = v);
                            });
                        })) ];

                      case 3:
                        return _c.sent(), [ 4, this._destination.removeAll() ];

                      case 4:
                        return _c.sent(), [ 4, Promise.all(Object.keys(payload_1).filter(function(k) {
                            return null != payload_1[k];
                        }).map(function(k) {
                            return _this._destination.set(k, payload_1[k]);
                        })) ];

                      case 5:
                        return _c.sent(), _a = isEqual, _b = [ payload_1 ], [ 4, this._destination.getAll() ];

                      case 6:
                        if (!_a.apply(void 0, _b.concat([ _c.sent() ]))) throw new Error("Could not verify write");
                        return this._migrationInProgress = !1, [ 2, sourceIsEmpty ? InternalStorageMigrationResult.emptyMigration : InternalStorageMigrationResult.nonEmptyMigration ];

                      case 7:
                        throw err_1 = _c.sent(), this._migrationInProgress = !1, err_1;

                      case 8:
                        return [ 2 ];
                    }
                });
            });
        }, StorageMigration.prototype.ensureMigrationCompleted = function() {
            return __awaiter(this, void 0, void 0, function() {
                var internalMigrationResult;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return [ 4, this._getMigrated() ];

                      case 1:
                        return _a.sent() ? [ 2, StorageMigrationResult.alreadyMigrated ] : [ 3, 2 ];

                      case 2:
                        return [ 4, this._runMigration() ];

                      case 3:
                        return internalMigrationResult = _a.sent(), [ 4, this._setMigrated() ];

                      case 4:
                        switch (_a.sent(), internalMigrationResult) {
                          case InternalStorageMigrationResult.nonEmptyMigration:
                            return [ 2, StorageMigrationResult.success ];

                          case InternalStorageMigrationResult.emptyMigration:
                            return [ 2, StorageMigrationResult.successWithEmpty ];

                          default:
                            throw internalMigrationResult, new Error("Match not exhaustive: " + internalMigrationResult);
                        }
                        _a.label = 5;

                      case 5:
                        return [ 2 ];
                    }
                });
            });
        }, StorageMigration;
    }();
    exports.StorageMigration = StorageMigration;
}, function(module, exports, __webpack_require__) {
    var apply = __webpack_require__(197), nativeMax = Math.max;
    module.exports = function(func, start, transform) {
        return start = nativeMax(void 0 === start ? func.length - 1 : start, 0), function() {
            for (var args = arguments, index = -1, length = nativeMax(args.length - start, 0), array = Array(length); ++index < length; ) array[index] = args[start + index];
            index = -1;
            for (var otherArgs = Array(start + 1); ++index < start; ) otherArgs[index] = args[index];
            return otherArgs[start] = transform(array), apply(func, this, otherArgs);
        };
    };
}, function(module, exports) {
    module.exports = function(func, thisArg, args) {
        switch (args.length) {
          case 0:
            return func.call(thisArg);

          case 1:
            return func.call(thisArg, args[0]);

          case 2:
            return func.call(thisArg, args[0], args[1]);

          case 3:
            return func.call(thisArg, args[0], args[1], args[2]);
        }
        return func.apply(thisArg, args);
    };
}, function(module, exports, __webpack_require__) {
    var baseSetToString = __webpack_require__(287), setToString = __webpack_require__(289)(baseSetToString);
    module.exports = setToString;
}, function(module, exports, __webpack_require__) {
    var eq = __webpack_require__(36), isArrayLike = __webpack_require__(29), isIndex = __webpack_require__(64), isObject = __webpack_require__(9);
    module.exports = function(value, index, object) {
        if (!isObject(object)) return !1;
        var type = typeof index;
        return !!("number" == type ? isArrayLike(object) && isIndex(index, object.length) : "string" == type && index in object) && eq(object[index], value);
    };
}, function(module, exports, __webpack_require__) {
    var isObject = __webpack_require__(9), isSymbol = __webpack_require__(51), NAN = NaN, reTrim = /^\s+|\s+$/g, reIsBadHex = /^[-+]0x[0-9a-f]+$/i, reIsBinary = /^0b[01]+$/i, reIsOctal = /^0o[0-7]+$/i, freeParseInt = parseInt;
    module.exports = function(value) {
        if ("number" == typeof value) return value;
        if (isSymbol(value)) return NAN;
        if (isObject(value)) {
            var other = "function" == typeof value.valueOf ? value.valueOf() : value;
            value = isObject(other) ? other + "" : other;
        }
        if ("string" != typeof value) return 0 === value ? value : +value;
        value = value.replace(reTrim, "");
        var isBinary = reIsBinary.test(value);
        return isBinary || reIsOctal.test(value) ? freeParseInt(value.slice(2), isBinary ? 2 : 8) : reIsBadHex.test(value) ? NAN : +value;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.t = {
        SET_ACTIVE_TAB: "tabs/SET_ACTIVE_TAB"
    }, exports.setActiveTab = function(data) {
        return {
            type: exports.t.SET_ACTIVE_TAB,
            data: data
        };
    };
}, function(module, exports, __webpack_require__) {
    var arrayPush = __webpack_require__(106), isFlattenable = __webpack_require__(399);
    module.exports = function baseFlatten(array, depth, predicate, isStrict, result) {
        var index = -1, length = array.length;
        for (predicate || (predicate = isFlattenable), result || (result = []); ++index < length; ) {
            var value = array[index];
            depth > 0 && predicate(value) ? depth > 1 ? baseFlatten(value, depth - 1, predicate, isStrict, result) : arrayPush(result, value) : isStrict || (result[result.length] = value);
        }
        return result;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var tslib_1 = __webpack_require__(204), utils_1 = __webpack_require__(152), AbstractMetricsStorage = function() {
        function AbstractMetricsStorage(name, timersSink, countersSink) {
            this.name = name, this.timersSink = timersSink, this.countersSink = countersSink, 
            utils_1.validateName(name);
        }
        return AbstractMetricsStorage.prototype.getMetric = function(name) {
            return this._createChild(name);
        }, AbstractMetricsStorage.prototype.getTimer = function(name) {
            return this._createChild(name);
        }, AbstractMetricsStorage.prototype.getCounter = function(name) {
            return this._createChild(name);
        }, Object.defineProperty(AbstractMetricsStorage.prototype, "parent", {
            get: function() {
                var dot = this.name.lastIndexOf("."), name = this.name.substring(0, -1 === dot ? 0 : dot);
                return "" === name ? void 0 : new AbstractMetricsStorage(name, this.timersSink, this.countersSink);
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(AbstractMetricsStorage.prototype, "root", {
            get: function() {
                var dot = this.name.indexOf("."), name = this.name.substring(0, -1 === dot ? 0 : dot);
                return "" === name ? this : new AbstractMetricsStorage(name, this.timersSink, this.countersSink);
            },
            enumerable: !0,
            configurable: !0
        }), AbstractMetricsStorage.prototype._createName = function(name) {
            return this.name + "." + name;
        }, AbstractMetricsStorage.prototype.start = function() {
            var start = Date.now(), self = this;
            return {
                stop: function() {
                    self.recordTime(Date.now() - start);
                }
            };
        }, AbstractMetricsStorage.prototype.recordTime = function(time) {
            this.timersSink(this.name, time);
        }, AbstractMetricsStorage.prototype.timing = function(fn) {
            var tn = this.start();
            try {
                return fn();
            } finally {
                try {
                    tn.stop();
                } catch (e) {}
            }
        }, AbstractMetricsStorage.prototype.increment = function(step) {
            void 0 === step && (step = 1), this.countersSink(this.name, step);
        }, AbstractMetricsStorage.prototype.decrement = function(step) {
            void 0 === step && (step = 1), this.increment(-step);
        }, AbstractMetricsStorage.prototype._createChild = function(name) {
            return new AbstractMetricsStorage(this._createName(name), this.timersSink, this.countersSink);
        }, AbstractMetricsStorage;
    }();
    exports.AbstractMetricsStorage = AbstractMetricsStorage;
    var MetricsPrinter = function(_super) {
        function MetricsPrinter(fn) {
            return _super.call(this, "MP", function(name, value) {
                return fn("TIMER: " + name + " = " + value);
            }, function(name, value) {
                return fn("COUNTER: " + name + " = " + value);
            }) || this;
        }
        return tslib_1.__extends(MetricsPrinter, _super), MetricsPrinter;
    }(AbstractMetricsStorage);
    exports.MetricsPrinter = MetricsPrinter;
    var DEFAULT_SEND_TIMEOUT_MS = 7500, MAX_SEND_ATTEMPTS = 3, MetricsStorage = function(_super) {
        function MetricsStorage(name, baseUrl, _fetch, _sendTimeout) {
            void 0 === _sendTimeout && (_sendTimeout = DEFAULT_SEND_TIMEOUT_MS);
            var _this = _super.call(this, name, function(n, v) {
                return _this._reportTimer(n, v);
            }, function(n, v) {
                return _this._reportCounter(n, v);
            }) || this;
            return _this._fetch = _fetch, _this._sendTimeout = _sendTimeout, _this._countersBuffer = {}, 
            _this._timersBuffer = new Array(), _this._sendTimer = void 0, _this._sendData = function() {
                var data = [ _this._timersBuffer.join("&"), Object.keys(_this._countersBuffer).map(function(key) {
                    return key + "=" + _this._countersBuffer[key];
                }).join("&") ].filter(function(s) {
                    return s.length;
                }).join("&"), url = _this._baseUrl + data;
                _this._timersBuffer.length = 0, _this._countersBuffer = {}, _this._sendTimer = void 0;
                var attempt = 0, send = function() {
                    _this._fetch(url, {
                        mode: "no-cors",
                        cache: "no-cache"
                    }).catch(function(error) {
                        attempt++ < MAX_SEND_ATTEMPTS ? setTimeout(send, 5e3 * attempt) : console.error("Cannot send timesereies data", error, url);
                    });
                };
                send();
            }, _this._baseUrl = baseUrl + "/ts?", _this;
        }
        return tslib_1.__extends(MetricsStorage, _super), MetricsStorage.createRoot = function(name, baseUrl, fetch) {
            return new MetricsStorage(name, baseUrl, fetch);
        }, MetricsStorage.prototype._reportTimer = function(name, value) {
            this._timersBuffer.push("t." + name + "=" + value), this._startSending();
        }, MetricsStorage.prototype._reportCounter = function(name, value) {
            var key = "c." + name;
            this._countersBuffer[key] = (this._countersBuffer[key] || 0) + value, this._startSending();
        }, MetricsStorage.prototype._startSending = function() {
            this._sendTimer || (this._sendTimer = setTimeout(this._sendData, this._sendTimeout));
        }, MetricsStorage;
    }(AbstractMetricsStorage);
    exports.MetricsStorage = MetricsStorage;
    var MetricsConfig = function() {
        function MetricsConfig() {}
        return MetricsConfig.getRootMetric = function() {
            return MetricsConfig._metricsRoot || (console.warn("[WARNING] Using default timeseries implementation."), 
            MetricsConfig._metricsRoot = new MetricsPrinter(console.log)), MetricsConfig._metricsRoot;
        }, MetricsConfig.configure = function(root) {
            MetricsConfig._metricsRoot = root;
        }, MetricsConfig;
    }();
    exports.MetricsConfig = MetricsConfig;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    Object.defineProperty(__webpack_exports__, "__esModule", {
        value: !0
    }), __webpack_exports__.__extends = function(d, b) {
        function __() {
            this.constructor = d;
        }
        extendStatics(d, b), d.prototype = null === b ? Object.create(b) : (__.prototype = b.prototype, 
        new __());
    }, __webpack_require__.d(__webpack_exports__, "__assign", function() {
        return __assign;
    }), __webpack_exports__.__rest = function(s, e) {
        var t = {};
        for (var p in s) Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0 && (t[p] = s[p]);
        if (null != s && "function" == typeof Object.getOwnPropertySymbols) for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) e.indexOf(p[i]) < 0 && (t[p[i]] = s[p[i]]);
        return t;
    }, __webpack_exports__.__decorate = function(decorators, target, key, desc) {
        var d, c = arguments.length, r = c < 3 ? target : null === desc ? desc = Object.getOwnPropertyDescriptor(target, key) : desc;
        if ("object" == typeof Reflect && "function" == typeof Reflect.decorate) r = Reflect.decorate(decorators, target, key, desc); else for (var i = decorators.length - 1; i >= 0; i--) (d = decorators[i]) && (r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r);
        return c > 3 && r && Object.defineProperty(target, key, r), r;
    }, __webpack_exports__.__param = function(paramIndex, decorator) {
        return function(target, key) {
            decorator(target, key, paramIndex);
        };
    }, __webpack_exports__.__metadata = function(metadataKey, metadataValue) {
        if ("object" == typeof Reflect && "function" == typeof Reflect.metadata) return Reflect.metadata(metadataKey, metadataValue);
    }, __webpack_exports__.__awaiter = function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __webpack_exports__.__generator = function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    }, __webpack_exports__.__exportStar = function(m, exports) {
        for (var p in m) exports.hasOwnProperty(p) || (exports[p] = m[p]);
    }, __webpack_exports__.__values = __values, __webpack_exports__.__read = __read, 
    __webpack_exports__.__spread = function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    }, __webpack_exports__.__await = __await, __webpack_exports__.__asyncGenerator = function(thisArg, _arguments, generator) {
        if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
        var i, g = generator.apply(thisArg, _arguments || []), q = [];
        return i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function() {
            return this;
        }, i;
        function verb(n) {
            g[n] && (i[n] = function(v) {
                return new Promise(function(a, b) {
                    q.push([ n, v, a, b ]) > 1 || resume(n, v);
                });
            });
        }
        function resume(n, v) {
            try {
                (r = g[n](v)).value instanceof __await ? Promise.resolve(r.value.v).then(fulfill, reject) : settle(q[0][2], r);
            } catch (e) {
                settle(q[0][3], e);
            }
            var r;
        }
        function fulfill(value) {
            resume("next", value);
        }
        function reject(value) {
            resume("throw", value);
        }
        function settle(f, v) {
            f(v), q.shift(), q.length && resume(q[0][0], q[0][1]);
        }
    }, __webpack_exports__.__asyncDelegator = function(o) {
        var i, p;
        return i = {}, verb("next"), verb("throw", function(e) {
            throw e;
        }), verb("return"), i[Symbol.iterator] = function() {
            return this;
        }, i;
        function verb(n, f) {
            o[n] && (i[n] = function(v) {
                return (p = !p) ? {
                    value: __await(o[n](v)),
                    done: "return" === n
                } : f ? f(v) : v;
            });
        }
    }, __webpack_exports__.__asyncValues = function(o) {
        if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
        var m = o[Symbol.asyncIterator];
        return m ? m.call(o) : __values(o);
    }, __webpack_exports__.__makeTemplateObject = function(cooked, raw) {
        Object.defineProperty ? Object.defineProperty(cooked, "raw", {
            value: raw
        }) : cooked.raw = raw;
        return cooked;
    }, __webpack_exports__.__importStar = function(mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (null != mod) for (var k in mod) Object.hasOwnProperty.call(mod, k) && (result[k] = mod[k]);
        return result.default = mod, result;
    }, __webpack_exports__.__importDefault = function(mod) {
        return mod && mod.__esModule ? mod : {
            default: mod
        };
    };
    var extendStatics = Object.setPrototypeOf || {
        __proto__: []
    } instanceof Array && function(d, b) {
        d.__proto__ = b;
    } || function(d, b) {
        for (var p in b) b.hasOwnProperty(p) && (d[p] = b[p]);
    };
    var __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
        return t;
    };
    function __values(o) {
        var m = "function" == typeof Symbol && o[Symbol.iterator], i = 0;
        return m ? m.call(o) : {
            next: function() {
                return o && i >= o.length && (o = void 0), {
                    value: o && o[i++],
                    done: !o
                };
            }
        };
    }
    function __read(o, n) {
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
    }
    function __await(v) {
        return this instanceof __await ? (this.v = v, this) : new __await(v);
    }
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var isObject = __webpack_require__(9), util_1 = __webpack_require__(2), config_1 = __webpack_require__(11), message = __webpack_require__(15), cookie_1 = __webpack_require__(360), extension_api_1 = __webpack_require__(66), log = __webpack_require__(1).Logger.create("lib.request"), AJAX_TIMEOUT = 1e4;
    function transformOptions(opts, isBG) {
        return __awaiter(this, void 0, void 0, function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    if (opts.data && (opts.query || "post" !== opts.method) && (opts.url += "?" + paramStr(opts.data)), 
                    opts.data && "post" === opts.method && !opts.query && !opts.body) {
                        try {
                            opts.body = JSON.stringify(opts.data);
                        } catch (e) {
                            opts.body = {}, log.warn("", e);
                        }
                        opts.headers = opts.headers || {}, opts.headers["Content-Type"] = opts.headers["Content-Type"] || "application/json", 
                        delete opts.data;
                    }
                    return opts.credentials = "include", isBG ? [ 4, function(opts) {
                        return new cookie_1.CookiesHelper(extension_api_1.getGlobalExtensionApi()).getCSRFToken().then(function(v) {
                            return v && (opts.headers = opts.headers || {}, opts.headers["X-CSRF-Token"] = v), 
                            opts;
                        });
                    }(opts) ] : [ 3, 2 ];

                  case 1:
                    return [ 2, _a.sent() ];

                  case 2:
                    return [ 2, opts ];
                }
            });
        });
    }
    function bgFetch(opts) {
        var url = opts.url;
        if (delete opts.url, !url) return Promise.reject(new Error("Url is not defined in fetch request"));
        return Promise.race([ window.fetch(url, opts).then(function(resp) {
            return resp.ok ? resp[opts.isText ? "text" : "json"]() : resp.text().then(function(body) {
                throw {
                    name: "RequestError",
                    body: body,
                    statusCode: resp.status,
                    message: resp.statusText
                };
            });
        }).then(function(res) {
            if ("string" != typeof res && res && res.error) throw new Error(res.error);
            return res;
        }), util_1.delay(opts.timeout || AJAX_TIMEOUT).then(function() {
            throw new Error("Fetch request to " + url + " rejected by timeout");
        }) ]);
    }
    function paramStr(data) {
        var req = "", _loop_1 = function(item) {
            if (Array.isArray(data[item])) {
                if (data[item].length) {
                    var items = data[item].map(function(val) {
                        return item + "=" + val;
                    }).join("&");
                    req += (req.length ? "&" : "") + items;
                }
            } else req += (req.length ? "&" : "") + item + "=" + encodeURIComponent(data[item]);
        };
        for (var item in data) _loop_1(item);
        return req;
    }
    util_1.isBg() && message.on("fetch", function(data, cb) {
        return bgFetch(data).then(cb, function(error) {
            return cb({
                error: error.message
            });
        });
    }), exports.transformOptions = transformOptions, exports.fetch = function(url, opts) {
        return void 0 === opts && (opts = {}), __awaiter(this, void 0, void 0, function() {
            var data;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return opts.url = url, [ 4, transformOptions(opts, util_1.isBg()) ];

                  case 1:
                    return _a.sent(), util_1.isBg() || config_1.isTestsMode() ? [ 2, bgFetch(opts) ] : [ 4, message.promiseBackground("fetch", opts) ];

                  case 2:
                    if (data = _a.sent(), isObject(data) && data.error) throw new Error(data.error);
                    return [ 2, data ];
                }
            });
        });
    }, exports.paramStr = paramStr;
}, , , , , , , , , , , function(module, exports, __webpack_require__) {
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
    });
    var message = __webpack_require__(15), util_1 = __webpack_require__(2), tracking_1 = __webpack_require__(7), logger_1 = __webpack_require__(1), promise_1 = __webpack_require__(63), bgonly_1 = __webpack_require__(460), on_1 = __webpack_require__(1149), appLogger = logger_1.Logger.create("lib.tracking");
    function fire(msg) {
        for (var data = [], _i = 1; _i < arguments.length; _i++) data[_i - 1] = arguments[_i];
        if (!on_1.on[msg]) return appLogger.error("No handler specified for message: " + msg);
        util_1.asyncCall(function() {
            return on_1.on[msg].apply(on_1.on, __spread(data));
        }, 20);
    }
    exports.gnarSpecInstance = promise_1.SafePromise.createCompletionSource(), exports.gnar = new Proxy({}, {
        get: function(_, method) {
            return function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return exports.gnarSpecInstance.promise.then(function(gnarSpec) {
                    var _a;
                    tracking_1.logCall("gnar", __spread([ method ], args)), (_a = gnarSpec)[method].apply(_a, __spread(args));
                }).catch(function(err) {
                    appLogger.error(err);
                });
            };
        }
    }), exports.initBg = function(gnarSpecClass) {
        bgonly_1.init(gnarSpecClass).then(function(spec) {
            spec ? exports.gnarSpecInstance.resolve(spec) : (tracking_1.felog.bgTrackingInitFail(), 
            exports.gnarSpecInstance.reject("failed to send tracking event: gnarSpec init failed"));
        }).catch(function(_) {
            tracking_1.felog.bgTrackingInitFail(), exports.gnarSpecInstance.reject("failed to send tracking event: tracking init failed");
        }), message.on("gnar-track", function(_a) {
            var _b, props = _a.props, method = _a.method;
            return (_b = exports.gnar)[method].apply(_b, __spread(props));
        }), message.on("tracker-init", bgonly_1.processCookiesFromGrammarly), message.on("tracking-fire", function(_a) {
            var msg = _a.msg, data = _a.data;
            return fire.apply(void 0, __spread([ msg ], data));
        }), message.on("tracking-call", function(_a, cb) {
            var msg = _a.msg, data = _a.data;
            void 0 === cb && (cb = util_1._f), tracking_1.call.apply(void 0, __spread([ msg ], data)), 
            cb();
        });
    }, exports.fire = fire;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    try {
        window.firefox = browser;
    } catch (e) {
        window.firefox = window.browser;
    }
    window.edge = window.browser, window.chrome = window.chrome, exports.default = void 0;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __rest = this && this.__rest || function(s, e) {
        var t = {};
        for (var p in s) Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0 && (t[p] = s[p]);
        if (null != s && "function" == typeof Object.getOwnPropertySymbols) {
            var i = 0;
            for (p = Object.getOwnPropertySymbols(s); i < p.length; i++) e.indexOf(p[i]) < 0 && (t[p[i]] = s[p[i]]);
        }
        return t;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var bg_1 = __webpack_require__(103), content_1 = __webpack_require__(132), chrome_1 = __webpack_require__(281), chrome_util_1 = __webpack_require__(133), web_extensions_1 = __webpack_require__(108), util_1 = __webpack_require__(2), Config = __webpack_require__(10), stdlib_1 = __webpack_require__(3), ChromeContentScriptPort = function() {
        function ChromeContentScriptPort(name) {
            this.port = chrome.runtime.connect({
                name: name
            });
        }
        return ChromeContentScriptPort.prototype.onMessage = function(cb) {
            this.port.onMessage.addListener(cb);
        }, ChromeContentScriptPort.prototype.onDisconnect = function(cb) {
            this.port.onDisconnect.addListener(cb);
        }, ChromeContentScriptPort.prototype.postMessage = function(data) {
            this.port.postMessage(data);
        }, ChromeContentScriptPort;
    }(), ChromeBackgroundPort = function() {
        function ChromeBackgroundPort(_port) {
            this._port = _port, this.sender = {};
            var sender = _port.sender, name = _port.name;
            this.name = name, sender && (this.sender.url = sender.url, sender.tab && sender.tab.url && sender.tab.id && (this.sender.tab = {
                url: sender.tab.url,
                id: sender.tab.id,
                active: sender.tab.active
            }));
        }
        return ChromeBackgroundPort.prototype.onMessage = function(cb) {
            this._port.onMessage.addListener(cb);
        }, ChromeBackgroundPort.prototype.onDisconnect = function(cb) {
            this._port.onDisconnect.addListener(cb);
        }, ChromeBackgroundPort.prototype.postMessage = function(data) {
            this._port.postMessage(data);
        }, ChromeBackgroundPort;
    }(), ChromeApi = function() {
        return function() {
            this.tabs = new chrome_1.ChromeTabsApiImpl(), this.notification = {
                kind: "web-extension",
                create: function(options) {
                    return stdlib_1.SafePromise.create(function(resolve, reject) {
                        var onClicked = options.onClicked, onButtonClicked = options.onButtonClicked, opts = __rest(options, [ "onClicked", "onButtonClicked" ]), cn = chrome.notifications, id = util_1.guid();
                        cn.create(id, Object.assign({
                            type: "basic"
                        }, opts), function() {
                            chrome_util_1.handleChromeError(function() {
                                void 0 !== onClicked && cn.onClicked.addListener(onClicked), void 0 !== onButtonClicked && cn.onButtonClicked.addListener(onButtonClicked), 
                                resolve(id);
                            }, reject);
                        });
                    });
                },
                clear: function(id) {
                    return stdlib_1.SafePromise.create(function(resolve, reject) {
                        chrome.notifications.clear(id, function(wasCleared) {
                            chrome_util_1.handleChromeError(function() {
                                return resolve(wasCleared);
                            }, reject);
                        });
                    });
                }
            }, this.cookies = {
                kind: "web-extension",
                get: function(details) {
                    return stdlib_1.SafePromise.create(function(resolve, reject) {
                        return chrome.cookies.get(details, function(cookie) {
                            return chrome_util_1.handleChromeError(function() {
                                return resolve(cookie);
                            }, reject);
                        });
                    });
                },
                remove: function(details) {
                    return new Promise(function(resolve, reject) {
                        return chrome.cookies.remove(details, function() {
                            return chrome_util_1.handleChromeError(function() {
                                return resolve(null);
                            }, reject);
                        });
                    });
                },
                getAll: function(details) {
                    return stdlib_1.SafePromise.create(function(resolve, reject) {
                        return chrome.cookies.getAll(details, function(cookie) {
                            return chrome_util_1.handleChromeError(function() {
                                return resolve(cookie);
                            }, reject);
                        });
                    });
                },
                set: function(details) {
                    return stdlib_1.SafePromise.create(function(resolve, reject) {
                        return chrome.cookies.set(details, function(cookie) {
                            return chrome_util_1.handleChromeError(function() {
                                return resolve(cookie);
                            }, reject);
                        });
                    });
                },
                watch: function(details, cb) {
                    chrome.cookies.onChanged.addListener(function(changeInfo) {
                        var cookie = changeInfo.cookie, cause = changeInfo.cause;
                        !cookie || !cookie.name || details.path && details.path !== cookie.path || details.name !== cookie.name || details.domain && -1 === cookie.domain.indexOf(details.domain) || ("explicit" === cause && cb(cookie), 
                        "expired_overwrite" === cause && cb());
                    });
                }
            }, this.preferences = web_extensions_1.preferencesApi.windowLocalStorage, this.button = {
                kind: "web-extension",
                setBadge: function(text) {
                    chrome.browserAction.setBadgeText({
                        text: text
                    });
                },
                setIconByName: function(name) {
                    var postfix = name ? "-" + name : "";
                    chrome.browserAction.setIcon({
                        path: {
                            16: "./src/icon/icon16" + postfix + ".png",
                            32: "./src/icon/icon32" + postfix + ".png"
                        }
                    });
                },
                setBadgeBackgroundColor: function(color) {
                    chrome.browserAction.setBadgeBackgroundColor({
                        color: color
                    });
                }
            }, this.management = {
                uninstallSelf: function() {
                    chrome.management.uninstallSelf();
                }
            }, this.message = "bg" === Config.getGlobal().bundleInfo.context ? new bg_1.GenericBackgroundMessageApiImpl(function(cb) {
                return chrome.runtime.onConnect.addListener(function(port) {
                    return cb(new ChromeBackgroundPort(port));
                });
            }, this.tabs.getActiveTab.bind(this.tabs), this.tabs.getAllTabs.bind(this.tabs)) : new content_1.GenericContentScriptMessageApiImpl(function(name) {
                return new ChromeContentScriptPort(name);
            });
        };
    }();
    exports.createApi = function() {
        return new ChromeApi();
    };
}, function(module, exports) {
    module.exports = function(fromRight) {
        return function(object, iteratee, keysFunc) {
            for (var index = -1, iterable = Object(object), props = keysFunc(object), length = props.length; length--; ) {
                var key = props[fromRight ? length : ++index];
                if (!1 === iteratee(iterable[key], key, iterable)) break;
            }
            return object;
        };
    };
}, function(module, exports) {
    module.exports = function(n, iteratee) {
        for (var index = -1, result = Array(n); ++index < n; ) result[index] = iteratee(index);
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), isObjectLike = __webpack_require__(17), argsTag = "[object Arguments]";
    module.exports = function(value) {
        return isObjectLike(value) && baseGetTag(value) == argsTag;
    };
}, function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), objectProto = Object.prototype, hasOwnProperty = objectProto.hasOwnProperty, nativeObjectToString = objectProto.toString, symToStringTag = Symbol ? Symbol.toStringTag : void 0;
    module.exports = function(value) {
        var isOwn = hasOwnProperty.call(value, symToStringTag), tag = value[symToStringTag];
        try {
            value[symToStringTag] = void 0;
            var unmasked = !0;
        } catch (e) {}
        var result = nativeObjectToString.call(value);
        return unmasked && (isOwn ? value[symToStringTag] = tag : delete value[symToStringTag]), 
        result;
    };
}, function(module, exports) {
    var nativeObjectToString = Object.prototype.toString;
    module.exports = function(value) {
        return nativeObjectToString.call(value);
    };
}, function(module, exports) {
    module.exports = function() {
        return !1;
    };
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), isLength = __webpack_require__(78), isObjectLike = __webpack_require__(17), typedArrayTags = {};
    typedArrayTags["[object Float32Array]"] = typedArrayTags["[object Float64Array]"] = typedArrayTags["[object Int8Array]"] = typedArrayTags["[object Int16Array]"] = typedArrayTags["[object Int32Array]"] = typedArrayTags["[object Uint8Array]"] = typedArrayTags["[object Uint8ClampedArray]"] = typedArrayTags["[object Uint16Array]"] = typedArrayTags["[object Uint32Array]"] = !0, 
    typedArrayTags["[object Arguments]"] = typedArrayTags["[object Array]"] = typedArrayTags["[object ArrayBuffer]"] = typedArrayTags["[object Boolean]"] = typedArrayTags["[object DataView]"] = typedArrayTags["[object Date]"] = typedArrayTags["[object Error]"] = typedArrayTags["[object Function]"] = typedArrayTags["[object Map]"] = typedArrayTags["[object Number]"] = typedArrayTags["[object Object]"] = typedArrayTags["[object RegExp]"] = typedArrayTags["[object Set]"] = typedArrayTags["[object String]"] = typedArrayTags["[object WeakMap]"] = !1, 
    module.exports = function(value) {
        return isObjectLike(value) && isLength(value.length) && !!typedArrayTags[baseGetTag(value)];
    };
}, function(module, exports, __webpack_require__) {
    var nativeKeys = __webpack_require__(123)(Object.keys, Object);
    module.exports = nativeKeys;
}, function(module, exports, __webpack_require__) {
    var baseIsMatch = __webpack_require__(228), getMatchData = __webpack_require__(265), matchesStrictComparable = __webpack_require__(130);
    module.exports = function(source) {
        var matchData = getMatchData(source);
        return 1 == matchData.length && matchData[0][2] ? matchesStrictComparable(matchData[0][0], matchData[0][1]) : function(object) {
            return object === source || baseIsMatch(object, source, matchData);
        };
    };
}, function(module, exports, __webpack_require__) {
    var Stack = __webpack_require__(57), baseIsEqual = __webpack_require__(82), COMPARE_PARTIAL_FLAG = 1, COMPARE_UNORDERED_FLAG = 2;
    module.exports = function(object, source, matchData, customizer) {
        var index = matchData.length, length = index, noCustomizer = !customizer;
        if (null == object) return !length;
        for (object = Object(object); index--; ) {
            var data = matchData[index];
            if (noCustomizer && data[2] ? data[1] !== object[data[0]] : !(data[0] in object)) return !1;
        }
        for (;++index < length; ) {
            var key = (data = matchData[index])[0], objValue = object[key], srcValue = data[1];
            if (noCustomizer && data[2]) {
                if (void 0 === objValue && !(key in object)) return !1;
            } else {
                var stack = new Stack();
                if (customizer) var result = customizer(objValue, srcValue, key, object, source, stack);
                if (!(void 0 === result ? baseIsEqual(srcValue, objValue, COMPARE_PARTIAL_FLAG | COMPARE_UNORDERED_FLAG, customizer, stack) : result)) return !1;
            }
        }
        return !0;
    };
}, function(module, exports) {
    module.exports = function() {
        this.__data__ = [], this.size = 0;
    };
}, function(module, exports, __webpack_require__) {
    var assocIndexOf = __webpack_require__(48), splice = Array.prototype.splice;
    module.exports = function(key) {
        var data = this.__data__, index = assocIndexOf(data, key);
        return !(index < 0 || (index == data.length - 1 ? data.pop() : splice.call(data, index, 1), 
        --this.size, 0));
    };
}, function(module, exports, __webpack_require__) {
    var assocIndexOf = __webpack_require__(48);
    module.exports = function(key) {
        var data = this.__data__, index = assocIndexOf(data, key);
        return index < 0 ? void 0 : data[index][1];
    };
}, function(module, exports, __webpack_require__) {
    var assocIndexOf = __webpack_require__(48);
    module.exports = function(key) {
        return assocIndexOf(this.__data__, key) > -1;
    };
}, function(module, exports, __webpack_require__) {
    var assocIndexOf = __webpack_require__(48);
    module.exports = function(key, value) {
        var data = this.__data__, index = assocIndexOf(data, key);
        return index < 0 ? (++this.size, data.push([ key, value ])) : data[index][1] = value, 
        this;
    };
}, function(module, exports, __webpack_require__) {
    var ListCache = __webpack_require__(47);
    module.exports = function() {
        this.__data__ = new ListCache(), this.size = 0;
    };
}, function(module, exports) {
    module.exports = function(key) {
        var data = this.__data__, result = data.delete(key);
        return this.size = data.size, result;
    };
}, function(module, exports) {
    module.exports = function(key) {
        return this.__data__.get(key);
    };
}, function(module, exports) {
    module.exports = function(key) {
        return this.__data__.has(key);
    };
}, function(module, exports, __webpack_require__) {
    var ListCache = __webpack_require__(47), Map = __webpack_require__(80), MapCache = __webpack_require__(81), LARGE_ARRAY_SIZE = 200;
    module.exports = function(key, value) {
        var data = this.__data__;
        if (data instanceof ListCache) {
            var pairs = data.__data__;
            if (!Map || pairs.length < LARGE_ARRAY_SIZE - 1) return pairs.push([ key, value ]), 
            this.size = ++data.size, this;
            data = this.__data__ = new MapCache(pairs);
        }
        return data.set(key, value), this.size = data.size, this;
    };
}, function(module, exports, __webpack_require__) {
    var isFunction = __webpack_require__(41), isMasked = __webpack_require__(240), isObject = __webpack_require__(9), toSource = __webpack_require__(124), reIsHostCtor = /^\[object .+?Constructor\]$/, funcProto = Function.prototype, objectProto = Object.prototype, funcToString = funcProto.toString, hasOwnProperty = objectProto.hasOwnProperty, reIsNative = RegExp("^" + funcToString.call(hasOwnProperty).replace(/[\\^$.*+?()[\]{}|]/g, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
    module.exports = function(value) {
        return !(!isObject(value) || isMasked(value)) && (isFunction(value) ? reIsNative : reIsHostCtor).test(toSource(value));
    };
}, function(module, exports, __webpack_require__) {
    var uid, coreJsData = __webpack_require__(241), maskSrcKey = (uid = /[^.]+$/.exec(coreJsData && coreJsData.keys && coreJsData.keys.IE_PROTO || "")) ? "Symbol(src)_1." + uid : "";
    module.exports = function(func) {
        return !!maskSrcKey && maskSrcKey in func;
    };
}, function(module, exports, __webpack_require__) {
    var coreJsData = __webpack_require__(12)["__core-js_shared__"];
    module.exports = coreJsData;
}, function(module, exports) {
    module.exports = function(object, key) {
        return null == object ? void 0 : object[key];
    };
}, function(module, exports, __webpack_require__) {
    var Hash = __webpack_require__(244), ListCache = __webpack_require__(47), Map = __webpack_require__(80);
    module.exports = function() {
        this.size = 0, this.__data__ = {
            hash: new Hash(),
            map: new (Map || ListCache)(),
            string: new Hash()
        };
    };
}, function(module, exports, __webpack_require__) {
    var hashClear = __webpack_require__(245), hashDelete = __webpack_require__(246), hashGet = __webpack_require__(247), hashHas = __webpack_require__(248), hashSet = __webpack_require__(249);
    function Hash(entries) {
        var index = -1, length = null == entries ? 0 : entries.length;
        for (this.clear(); ++index < length; ) {
            var entry = entries[index];
            this.set(entry[0], entry[1]);
        }
    }
    Hash.prototype.clear = hashClear, Hash.prototype.delete = hashDelete, Hash.prototype.get = hashGet, 
    Hash.prototype.has = hashHas, Hash.prototype.set = hashSet, module.exports = Hash;
}, function(module, exports, __webpack_require__) {
    var nativeCreate = __webpack_require__(49);
    module.exports = function() {
        this.__data__ = nativeCreate ? nativeCreate(null) : {}, this.size = 0;
    };
}, function(module, exports) {
    module.exports = function(key) {
        var result = this.has(key) && delete this.__data__[key];
        return this.size -= result ? 1 : 0, result;
    };
}, function(module, exports, __webpack_require__) {
    var nativeCreate = __webpack_require__(49), HASH_UNDEFINED = "__lodash_hash_undefined__", hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(key) {
        var data = this.__data__;
        if (nativeCreate) {
            var result = data[key];
            return result === HASH_UNDEFINED ? void 0 : result;
        }
        return hasOwnProperty.call(data, key) ? data[key] : void 0;
    };
}, function(module, exports, __webpack_require__) {
    var nativeCreate = __webpack_require__(49), hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(key) {
        var data = this.__data__;
        return nativeCreate ? void 0 !== data[key] : hasOwnProperty.call(data, key);
    };
}, function(module, exports, __webpack_require__) {
    var nativeCreate = __webpack_require__(49), HASH_UNDEFINED = "__lodash_hash_undefined__";
    module.exports = function(key, value) {
        var data = this.__data__;
        return this.size += this.has(key) ? 0 : 1, data[key] = nativeCreate && void 0 === value ? HASH_UNDEFINED : value, 
        this;
    };
}, function(module, exports, __webpack_require__) {
    var getMapData = __webpack_require__(50);
    module.exports = function(key) {
        var result = getMapData(this, key).delete(key);
        return this.size -= result ? 1 : 0, result;
    };
}, function(module, exports) {
    module.exports = function(value) {
        var type = typeof value;
        return "string" == type || "number" == type || "symbol" == type || "boolean" == type ? "__proto__" !== value : null === value;
    };
}, function(module, exports, __webpack_require__) {
    var getMapData = __webpack_require__(50);
    module.exports = function(key) {
        return getMapData(this, key).get(key);
    };
}, function(module, exports, __webpack_require__) {
    var getMapData = __webpack_require__(50);
    module.exports = function(key) {
        return getMapData(this, key).has(key);
    };
}, function(module, exports, __webpack_require__) {
    var getMapData = __webpack_require__(50);
    module.exports = function(key, value) {
        var data = getMapData(this, key), size = data.size;
        return data.set(key, value), this.size += data.size == size ? 0 : 1, this;
    };
}, function(module, exports, __webpack_require__) {
    var Stack = __webpack_require__(57), equalArrays = __webpack_require__(125), equalByTag = __webpack_require__(259), equalObjects = __webpack_require__(261), getTag = __webpack_require__(58), isArray = __webpack_require__(8), isBuffer = __webpack_require__(35), isTypedArray = __webpack_require__(40), COMPARE_PARTIAL_FLAG = 1, argsTag = "[object Arguments]", arrayTag = "[object Array]", objectTag = "[object Object]", hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(object, other, bitmask, customizer, equalFunc, stack) {
        var objIsArr = isArray(object), othIsArr = isArray(other), objTag = objIsArr ? arrayTag : getTag(object), othTag = othIsArr ? arrayTag : getTag(other), objIsObj = (objTag = objTag == argsTag ? objectTag : objTag) == objectTag, othIsObj = (othTag = othTag == argsTag ? objectTag : othTag) == objectTag, isSameTag = objTag == othTag;
        if (isSameTag && isBuffer(object)) {
            if (!isBuffer(other)) return !1;
            objIsArr = !0, objIsObj = !1;
        }
        if (isSameTag && !objIsObj) return stack || (stack = new Stack()), objIsArr || isTypedArray(object) ? equalArrays(object, other, bitmask, customizer, equalFunc, stack) : equalByTag(object, other, objTag, bitmask, customizer, equalFunc, stack);
        if (!(bitmask & COMPARE_PARTIAL_FLAG)) {
            var objIsWrapped = objIsObj && hasOwnProperty.call(object, "__wrapped__"), othIsWrapped = othIsObj && hasOwnProperty.call(other, "__wrapped__");
            if (objIsWrapped || othIsWrapped) {
                var objUnwrapped = objIsWrapped ? object.value() : object, othUnwrapped = othIsWrapped ? other.value() : other;
                return stack || (stack = new Stack()), equalFunc(objUnwrapped, othUnwrapped, bitmask, customizer, stack);
            }
        }
        return !!isSameTag && (stack || (stack = new Stack()), equalObjects(object, other, bitmask, customizer, equalFunc, stack));
    };
}, function(module, exports) {
    var HASH_UNDEFINED = "__lodash_hash_undefined__";
    module.exports = function(value) {
        return this.__data__.set(value, HASH_UNDEFINED), this;
    };
}, function(module, exports) {
    module.exports = function(value) {
        return this.__data__.has(value);
    };
}, function(module, exports) {
    module.exports = function(array, predicate) {
        for (var index = -1, length = null == array ? 0 : array.length; ++index < length; ) if (predicate(array[index], index, array)) return !0;
        return !1;
    };
}, function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), Uint8Array = __webpack_require__(128), eq = __webpack_require__(36), equalArrays = __webpack_require__(125), mapToArray = __webpack_require__(260), setToArray = __webpack_require__(166), COMPARE_PARTIAL_FLAG = 1, COMPARE_UNORDERED_FLAG = 2, boolTag = "[object Boolean]", dateTag = "[object Date]", errorTag = "[object Error]", mapTag = "[object Map]", numberTag = "[object Number]", regexpTag = "[object RegExp]", setTag = "[object Set]", stringTag = "[object String]", symbolTag = "[object Symbol]", arrayBufferTag = "[object ArrayBuffer]", dataViewTag = "[object DataView]", symbolProto = Symbol ? Symbol.prototype : void 0, symbolValueOf = symbolProto ? symbolProto.valueOf : void 0;
    module.exports = function(object, other, tag, bitmask, customizer, equalFunc, stack) {
        switch (tag) {
          case dataViewTag:
            if (object.byteLength != other.byteLength || object.byteOffset != other.byteOffset) return !1;
            object = object.buffer, other = other.buffer;

          case arrayBufferTag:
            return !(object.byteLength != other.byteLength || !equalFunc(new Uint8Array(object), new Uint8Array(other)));

          case boolTag:
          case dateTag:
          case numberTag:
            return eq(+object, +other);

          case errorTag:
            return object.name == other.name && object.message == other.message;

          case regexpTag:
          case stringTag:
            return object == other + "";

          case mapTag:
            var convert = mapToArray;

          case setTag:
            var isPartial = bitmask & COMPARE_PARTIAL_FLAG;
            if (convert || (convert = setToArray), object.size != other.size && !isPartial) return !1;
            var stacked = stack.get(object);
            if (stacked) return stacked == other;
            bitmask |= COMPARE_UNORDERED_FLAG, stack.set(object, other);
            var result = equalArrays(convert(object), convert(other), bitmask, customizer, equalFunc, stack);
            return stack.delete(object), result;

          case symbolTag:
            if (symbolValueOf) return symbolValueOf.call(object) == symbolValueOf.call(other);
        }
        return !1;
    };
}, function(module, exports) {
    module.exports = function(map) {
        var index = -1, result = Array(map.size);
        return map.forEach(function(value, key) {
            result[++index] = [ key, value ];
        }), result;
    };
}, function(module, exports, __webpack_require__) {
    var getAllKeys = __webpack_require__(167), COMPARE_PARTIAL_FLAG = 1, hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(object, other, bitmask, customizer, equalFunc, stack) {
        var isPartial = bitmask & COMPARE_PARTIAL_FLAG, objProps = getAllKeys(object), objLength = objProps.length;
        if (objLength != getAllKeys(other).length && !isPartial) return !1;
        for (var index = objLength; index--; ) {
            var key = objProps[index];
            if (!(isPartial ? key in other : hasOwnProperty.call(other, key))) return !1;
        }
        var stacked = stack.get(object);
        if (stacked && stack.get(other)) return stacked == other;
        var result = !0;
        stack.set(object, other), stack.set(other, object);
        for (var skipCtor = isPartial; ++index < objLength; ) {
            var objValue = object[key = objProps[index]], othValue = other[key];
            if (customizer) var compared = isPartial ? customizer(othValue, objValue, key, other, object, stack) : customizer(objValue, othValue, key, object, other, stack);
            if (!(void 0 === compared ? objValue === othValue || equalFunc(objValue, othValue, bitmask, customizer, stack) : compared)) {
                result = !1;
                break;
            }
            skipCtor || (skipCtor = "constructor" == key);
        }
        if (result && !skipCtor) {
            var objCtor = object.constructor, othCtor = other.constructor;
            objCtor != othCtor && "constructor" in object && "constructor" in other && !("function" == typeof objCtor && objCtor instanceof objCtor && "function" == typeof othCtor && othCtor instanceof othCtor) && (result = !1);
        }
        return stack.delete(object), stack.delete(other), result;
    };
}, function(module, exports, __webpack_require__) {
    var DataView = __webpack_require__(26)(__webpack_require__(12), "DataView");
    module.exports = DataView;
}, function(module, exports, __webpack_require__) {
    var Promise = __webpack_require__(26)(__webpack_require__(12), "Promise");
    module.exports = Promise;
}, function(module, exports, __webpack_require__) {
    var WeakMap = __webpack_require__(26)(__webpack_require__(12), "WeakMap");
    module.exports = WeakMap;
}, function(module, exports, __webpack_require__) {
    var isStrictComparable = __webpack_require__(129), keys = __webpack_require__(32);
    module.exports = function(object) {
        for (var result = keys(object), length = result.length; length--; ) {
            var key = result[length], value = object[key];
            result[length] = [ key, value, isStrictComparable(value) ];
        }
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var baseIsEqual = __webpack_require__(82), get = __webpack_require__(267), hasIn = __webpack_require__(272), isKey = __webpack_require__(84), isStrictComparable = __webpack_require__(129), matchesStrictComparable = __webpack_require__(130), toKey = __webpack_require__(42), COMPARE_PARTIAL_FLAG = 1, COMPARE_UNORDERED_FLAG = 2;
    module.exports = function(path, srcValue) {
        return isKey(path) && isStrictComparable(srcValue) ? matchesStrictComparable(toKey(path), srcValue) : function(object) {
            var objValue = get(object, path);
            return void 0 === objValue && objValue === srcValue ? hasIn(object, path) : baseIsEqual(srcValue, objValue, COMPARE_PARTIAL_FLAG | COMPARE_UNORDERED_FLAG);
        };
    };
}, function(module, exports, __webpack_require__) {
    var baseGet = __webpack_require__(93);
    module.exports = function(object, path, defaultValue) {
        var result = null == object ? void 0 : baseGet(object, path);
        return void 0 === result ? defaultValue : result;
    };
}, function(module, exports, __webpack_require__) {
    var memoizeCapped = __webpack_require__(269), rePropName = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, reEscapeChar = /\\(\\)?/g, stringToPath = memoizeCapped(function(string) {
        var result = [];
        return 46 === string.charCodeAt(0) && result.push(""), string.replace(rePropName, function(match, number, quote, subString) {
            result.push(quote ? subString.replace(reEscapeChar, "$1") : number || match);
        }), result;
    });
    module.exports = stringToPath;
}, function(module, exports, __webpack_require__) {
    var memoize = __webpack_require__(270), MAX_MEMOIZE_SIZE = 500;
    module.exports = function(func) {
        var result = memoize(func, function(key) {
            return cache.size === MAX_MEMOIZE_SIZE && cache.clear(), key;
        }), cache = result.cache;
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var MapCache = __webpack_require__(81), FUNC_ERROR_TEXT = "Expected a function";
    function memoize(func, resolver) {
        if ("function" != typeof func || null != resolver && "function" != typeof resolver) throw new TypeError(FUNC_ERROR_TEXT);
        var memoized = function() {
            var args = arguments, key = resolver ? resolver.apply(this, args) : args[0], cache = memoized.cache;
            if (cache.has(key)) return cache.get(key);
            var result = func.apply(this, args);
            return memoized.cache = cache.set(key, result) || cache, result;
        };
        return memoized.cache = new (memoize.Cache || MapCache)(), memoized;
    }
    memoize.Cache = MapCache, module.exports = memoize;
}, function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), arrayMap = __webpack_require__(85), isArray = __webpack_require__(8), isSymbol = __webpack_require__(51), INFINITY = 1 / 0, symbolProto = Symbol ? Symbol.prototype : void 0, symbolToString = symbolProto ? symbolProto.toString : void 0;
    module.exports = function baseToString(value) {
        if ("string" == typeof value) return value;
        if (isArray(value)) return arrayMap(value, baseToString) + "";
        if (isSymbol(value)) return symbolToString ? symbolToString.call(value) : "";
        var result = value + "";
        return "0" == result && 1 / value == -INFINITY ? "-0" : result;
    };
}, function(module, exports, __webpack_require__) {
    var baseHasIn = __webpack_require__(273), hasPath = __webpack_require__(274);
    module.exports = function(object, path) {
        return null != object && hasPath(object, path, baseHasIn);
    };
}, function(module, exports) {
    module.exports = function(object, key) {
        return null != object && key in Object(object);
    };
}, function(module, exports, __webpack_require__) {
    var castPath = __webpack_require__(83), isArguments = __webpack_require__(45), isArray = __webpack_require__(8), isIndex = __webpack_require__(64), isLength = __webpack_require__(78), toKey = __webpack_require__(42);
    module.exports = function(object, path, hasFunc) {
        for (var index = -1, length = (path = castPath(path, object)).length, result = !1; ++index < length; ) {
            var key = toKey(path[index]);
            if (!(result = null != object && hasFunc(object, key))) break;
            object = object[key];
        }
        return result || ++index != length ? result : !!(length = null == object ? 0 : object.length) && isLength(length) && isIndex(key, length) && (isArray(object) || isArguments(object));
    };
}, function(module, exports, __webpack_require__) {
    var baseProperty = __webpack_require__(276), basePropertyDeep = __webpack_require__(277), isKey = __webpack_require__(84), toKey = __webpack_require__(42);
    module.exports = function(path) {
        return isKey(path) ? baseProperty(toKey(path)) : basePropertyDeep(path);
    };
}, function(module, exports) {
    module.exports = function(key) {
        return function(object) {
            return null == object ? void 0 : object[key];
        };
    };
}, function(module, exports, __webpack_require__) {
    var baseGet = __webpack_require__(93);
    module.exports = function(path) {
        return function(object) {
            return baseGet(object, path);
        };
    };
}, function(module, exports, __webpack_require__) {
    (function(process) {
        function normalizeArray(parts, allowAboveRoot) {
            for (var up = 0, i = parts.length - 1; i >= 0; i--) {
                var last = parts[i];
                "." === last ? parts.splice(i, 1) : ".." === last ? (parts.splice(i, 1), up++) : up && (parts.splice(i, 1), 
                up--);
            }
            if (allowAboveRoot) for (;up--; up) parts.unshift("..");
            return parts;
        }
        var splitPathRe = /^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/, splitPath = function(filename) {
            return splitPathRe.exec(filename).slice(1);
        };
        function filter(xs, f) {
            if (xs.filter) return xs.filter(f);
            for (var res = [], i = 0; i < xs.length; i++) f(xs[i], i, xs) && res.push(xs[i]);
            return res;
        }
        exports.resolve = function() {
            for (var resolvedPath = "", resolvedAbsolute = !1, i = arguments.length - 1; i >= -1 && !resolvedAbsolute; i--) {
                var path = i >= 0 ? arguments[i] : process.cwd();
                if ("string" != typeof path) throw new TypeError("Arguments to path.resolve must be strings");
                path && (resolvedPath = path + "/" + resolvedPath, resolvedAbsolute = "/" === path.charAt(0));
            }
            return (resolvedAbsolute ? "/" : "") + (resolvedPath = normalizeArray(filter(resolvedPath.split("/"), function(p) {
                return !!p;
            }), !resolvedAbsolute).join("/")) || ".";
        }, exports.normalize = function(path) {
            var isAbsolute = exports.isAbsolute(path), trailingSlash = "/" === substr(path, -1);
            return (path = normalizeArray(filter(path.split("/"), function(p) {
                return !!p;
            }), !isAbsolute).join("/")) || isAbsolute || (path = "."), path && trailingSlash && (path += "/"), 
            (isAbsolute ? "/" : "") + path;
        }, exports.isAbsolute = function(path) {
            return "/" === path.charAt(0);
        }, exports.join = function() {
            var paths = Array.prototype.slice.call(arguments, 0);
            return exports.normalize(filter(paths, function(p, index) {
                if ("string" != typeof p) throw new TypeError("Arguments to path.join must be strings");
                return p;
            }).join("/"));
        }, exports.relative = function(from, to) {
            function trim(arr) {
                for (var start = 0; start < arr.length && "" === arr[start]; start++) ;
                for (var end = arr.length - 1; end >= 0 && "" === arr[end]; end--) ;
                return start > end ? [] : arr.slice(start, end - start + 1);
            }
            from = exports.resolve(from).substr(1), to = exports.resolve(to).substr(1);
            for (var fromParts = trim(from.split("/")), toParts = trim(to.split("/")), length = Math.min(fromParts.length, toParts.length), samePartsLength = length, i = 0; i < length; i++) if (fromParts[i] !== toParts[i]) {
                samePartsLength = i;
                break;
            }
            var outputParts = [];
            for (i = samePartsLength; i < fromParts.length; i++) outputParts.push("..");
            return (outputParts = outputParts.concat(toParts.slice(samePartsLength))).join("/");
        }, exports.sep = "/", exports.delimiter = ":", exports.dirname = function(path) {
            var result = splitPath(path), root = result[0], dir = result[1];
            return root || dir ? (dir && (dir = dir.substr(0, dir.length - 1)), root + dir) : ".";
        }, exports.basename = function(path, ext) {
            var f = splitPath(path)[2];
            return ext && f.substr(-1 * ext.length) === ext && (f = f.substr(0, f.length - ext.length)), 
            f;
        }, exports.extname = function(path) {
            return splitPath(path)[3];
        };
        var substr = "b" === "ab".substr(-1) ? function(str, start, len) {
            return str.substr(start, len);
        } : function(str, start, len) {
            return start < 0 && (start = str.length + start), str.substr(start, len);
        };
    }).call(exports, __webpack_require__(60));
}, function(module, exports, __webpack_require__) {
    "use strict";
    var util = __webpack_require__(131);
    function getU16Int(u8IntArray, index) {
        return u8IntArray[index] << 8 | u8IntArray[index + 1];
    }
    module.exports = {
        hash: function(inputString) {
            var rem, u8IntArray = util.toU8IntArray(inputString + ""), hash = 0;
            if (!inputString) return hash.toString(16);
            var len = u8IntArray.length, pointer = 0;
            rem = 3 & len, len >>>= 2;
            for (var i = 0; i < len; i++) hash = (hash += getU16Int(u8IntArray, pointer)) << 16 ^ getU16Int(u8IntArray, pointer + 2) << 11 ^ hash, 
            pointer += 4, hash += hash >> 11;
            switch (rem) {
              case 3:
                hash += getU16Int(u8IntArray, pointer), hash ^= hash << 16, hash ^= u8IntArray[pointer + 2] << 18, 
                hash += hash >> 11;
                break;

              case 2:
                hash += getU16Int(u8IntArray, pointer), hash ^= hash << 11, hash += hash >> 17;
                break;

              case 1:
                hash += u8IntArray[pointer], hash ^= hash << 10, hash += hash >> 1;
            }
            return hash ^= hash << 3, hash += hash >> 5, hash ^= hash << 4, hash += hash >> 17, 
            hash ^= hash << 25, hash += hash >> 6, util.intToUnsignedHex(hash);
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var util = __webpack_require__(131);
    function _x86Multiply(m, n) {
        return (65535 & m) * n + (((m >>> 16) * n & 65535) << 16);
    }
    function _x86Rotl(m, n) {
        return m << n | m >>> 32 - n;
    }
    function _x86Fmix(h) {
        return h = _x86Multiply(h ^= h >>> 16, 2246822507), h = _x86Multiply(h ^= h >>> 13, 3266489909), 
        h ^= h >>> 16;
    }
    function _x64Add(m, n) {
        m = [ m[0] >>> 16, 65535 & m[0], m[1] >>> 16, 65535 & m[1] ], n = [ n[0] >>> 16, 65535 & n[0], n[1] >>> 16, 65535 & n[1] ];
        var o = [ 0, 0, 0, 0 ];
        return o[3] += m[3] + n[3], o[2] += o[3] >>> 16, o[3] &= 65535, o[2] += m[2] + n[2], 
        o[1] += o[2] >>> 16, o[2] &= 65535, o[1] += m[1] + n[1], o[0] += o[1] >>> 16, o[1] &= 65535, 
        o[0] += m[0] + n[0], o[0] &= 65535, [ o[0] << 16 | o[1], o[2] << 16 | o[3] ];
    }
    function _x64Multiply(m, n) {
        m = [ m[0] >>> 16, 65535 & m[0], m[1] >>> 16, 65535 & m[1] ], n = [ n[0] >>> 16, 65535 & n[0], n[1] >>> 16, 65535 & n[1] ];
        var o = [ 0, 0, 0, 0 ];
        return o[3] += m[3] * n[3], o[2] += o[3] >>> 16, o[3] &= 65535, o[2] += m[2] * n[3], 
        o[1] += o[2] >>> 16, o[2] &= 65535, o[2] += m[3] * n[2], o[1] += o[2] >>> 16, o[2] &= 65535, 
        o[1] += m[1] * n[3], o[0] += o[1] >>> 16, o[1] &= 65535, o[1] += m[2] * n[2], o[0] += o[1] >>> 16, 
        o[1] &= 65535, o[1] += m[3] * n[1], o[0] += o[1] >>> 16, o[1] &= 65535, o[0] += m[0] * n[3] + m[1] * n[2] + m[2] * n[1] + m[3] * n[0], 
        o[0] &= 65535, [ o[0] << 16 | o[1], o[2] << 16 | o[3] ];
    }
    function _x64Rotl(m, n) {
        return 32 === (n %= 64) ? [ m[1], m[0] ] : n < 32 ? [ m[0] << n | m[1] >>> 32 - n, m[1] << n | m[0] >>> 32 - n ] : (n -= 32, 
        [ m[1] << n | m[0] >>> 32 - n, m[0] << n | m[1] >>> 32 - n ]);
    }
    function _x64LeftShift(m, n) {
        return 0 === (n %= 64) ? m : n < 32 ? [ m[0] << n | m[1] >>> 32 - n, m[1] << n ] : [ m[1] << n - 32, 0 ];
    }
    function _x64Xor(m, n) {
        return [ m[0] ^ n[0], m[1] ^ n[1] ];
    }
    function _x64Fmix(h) {
        return h = _x64Xor(h = _x64Multiply(h = _x64Xor(h = _x64Multiply(h = _x64Xor(h, [ 0, h[0] >>> 1 ]), [ 4283543511, 3981806797 ]), [ 0, h[0] >>> 1 ]), [ 3301882366, 444984403 ]), [ 0, h[0] >>> 1 ]);
    }
    var x64Hash128 = function(key, seed) {
        key = "" + key || "";
        var u8IntArray = util.toU8IntArray(key);
        seed = seed || 0;
        for (var remainder = (key = {
            charCodeAt: function(index) {
                return u8IntArray[index];
            },
            length: u8IntArray.length
        }).length % 16, bytes = key.length - remainder, h1 = [ 0, seed ], h2 = [ 0, seed ], k1 = [ 0, 0 ], k2 = [ 0, 0 ], c1 = [ 2277735313, 289559509 ], c2 = [ 1291169091, 658871167 ], i = 0; i < bytes; i += 16) k1 = [ 255 & key.charCodeAt(i + 4) | (255 & key.charCodeAt(i + 5)) << 8 | (255 & key.charCodeAt(i + 6)) << 16 | (255 & key.charCodeAt(i + 7)) << 24, 255 & key.charCodeAt(i) | (255 & key.charCodeAt(i + 1)) << 8 | (255 & key.charCodeAt(i + 2)) << 16 | (255 & key.charCodeAt(i + 3)) << 24 ], 
        k2 = [ 255 & key.charCodeAt(i + 12) | (255 & key.charCodeAt(i + 13)) << 8 | (255 & key.charCodeAt(i + 14)) << 16 | (255 & key.charCodeAt(i + 15)) << 24, 255 & key.charCodeAt(i + 8) | (255 & key.charCodeAt(i + 9)) << 8 | (255 & key.charCodeAt(i + 10)) << 16 | (255 & key.charCodeAt(i + 11)) << 24 ], 
        h1 = _x64Add(_x64Multiply(h1 = _x64Add(h1 = _x64Rotl(h1 = _x64Xor(h1, k1 = _x64Multiply(k1 = _x64Rotl(k1 = _x64Multiply(k1, c1), 31), c2)), 27), h2), [ 0, 5 ]), [ 0, 1390208809 ]), 
        h2 = _x64Add(_x64Multiply(h2 = _x64Add(h2 = _x64Rotl(h2 = _x64Xor(h2, k2 = _x64Multiply(k2 = _x64Rotl(k2 = _x64Multiply(k2, c2), 33), c1)), 31), h1), [ 0, 5 ]), [ 0, 944331445 ]);
        switch (k1 = [ 0, 0 ], k2 = [ 0, 0 ], remainder) {
          case 15:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 14) ], 48));

          case 14:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 13) ], 40));

          case 13:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 12) ], 32));

          case 12:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 11) ], 24));

          case 11:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 10) ], 16));

          case 10:
            k2 = _x64Xor(k2, _x64LeftShift([ 0, key.charCodeAt(i + 9) ], 8));

          case 9:
            h2 = _x64Xor(h2, k2 = _x64Multiply(k2 = _x64Rotl(k2 = _x64Multiply(k2 = _x64Xor(k2, [ 0, key.charCodeAt(i + 8) ]), c2), 33), c1));

          case 8:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 7) ], 56));

          case 7:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 6) ], 48));

          case 6:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 5) ], 40));

          case 5:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 4) ], 32));

          case 4:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 3) ], 24));

          case 3:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 2) ], 16));

          case 2:
            k1 = _x64Xor(k1, _x64LeftShift([ 0, key.charCodeAt(i + 1) ], 8));

          case 1:
            h1 = _x64Xor(h1, k1 = _x64Multiply(k1 = _x64Rotl(k1 = _x64Multiply(k1 = _x64Xor(k1, [ 0, key.charCodeAt(i) ]), c1), 31), c2));
        }
        return h1 = _x64Xor(h1, [ 0, key.length ]), h2 = _x64Add(h2 = _x64Xor(h2, [ 0, key.length ]), h1 = _x64Add(h1, h2)), 
        h1 = _x64Fmix(h1), h2 = _x64Add(h2 = _x64Fmix(h2), h1 = _x64Add(h1, h2)), ("00000000" + (h1[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (h1[1] >>> 0).toString(16)).slice(-8) + ("00000000" + (h2[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (h2[1] >>> 0).toString(16)).slice(-8);
    };
    module.exports = {
        x86Hash32: function(key, seed) {
            key = "" + key || "";
            var u8IntArray = util.toU8IntArray(key);
            seed = seed || 0;
            for (var remainder = (key = {
                charCodeAt: function(index) {
                    return u8IntArray[index];
                },
                length: u8IntArray.length
            }).length % 4, bytes = key.length - remainder, h1 = seed, k1 = 0, c1 = 3432918353, c2 = 461845907, i = 0; i < bytes; i += 4) h1 = _x86Multiply(h1 = _x86Rotl(h1 ^= k1 = _x86Multiply(k1 = _x86Rotl(k1 = _x86Multiply(k1 = 255 & key.charCodeAt(i) | (255 & key.charCodeAt(i + 1)) << 8 | (255 & key.charCodeAt(i + 2)) << 16 | (255 & key.charCodeAt(i + 3)) << 24, c1), 15), c2), 13), 5) + 3864292196;
            switch (k1 = 0, remainder) {
              case 3:
                k1 ^= (255 & key.charCodeAt(i + 2)) << 16;

              case 2:
                k1 ^= (255 & key.charCodeAt(i + 1)) << 8;

              case 1:
                h1 ^= k1 = _x86Multiply(k1 = _x86Rotl(k1 = _x86Multiply(k1 ^= 255 & key.charCodeAt(i), c1), 15), c2);
            }
            return ((h1 = _x86Fmix(h1 ^= key.length)) >>> 0).toString(16);
        },
        x86Hash128: function(key, seed) {
            key = "" + key || "";
            var u8IntArray = util.toU8IntArray(key);
            seed = seed || 0;
            for (var remainder = (key = {
                charCodeAt: function(index) {
                    return u8IntArray[index];
                },
                length: u8IntArray.length
            }).length % 16, bytes = key.length - remainder, h1 = seed, h2 = seed, h3 = seed, h4 = seed, k1 = 0, k2 = 0, k3 = 0, k4 = 0, c1 = 597399067, c2 = 2869860233, c3 = 951274213, c4 = 2716044179, i = 0; i < bytes; i += 16) k1 = 255 & key.charCodeAt(i) | (255 & key.charCodeAt(i + 1)) << 8 | (255 & key.charCodeAt(i + 2)) << 16 | (255 & key.charCodeAt(i + 3)) << 24, 
            k2 = 255 & key.charCodeAt(i + 4) | (255 & key.charCodeAt(i + 5)) << 8 | (255 & key.charCodeAt(i + 6)) << 16 | (255 & key.charCodeAt(i + 7)) << 24, 
            k3 = 255 & key.charCodeAt(i + 8) | (255 & key.charCodeAt(i + 9)) << 8 | (255 & key.charCodeAt(i + 10)) << 16 | (255 & key.charCodeAt(i + 11)) << 24, 
            k4 = 255 & key.charCodeAt(i + 12) | (255 & key.charCodeAt(i + 13)) << 8 | (255 & key.charCodeAt(i + 14)) << 16 | (255 & key.charCodeAt(i + 15)) << 24, 
            h1 = _x86Rotl(h1 ^= k1 = _x86Multiply(k1 = _x86Rotl(k1 = _x86Multiply(k1, c1), 15), c2), 19), 
            h1 = _x86Multiply(h1 += h2, 5) + 1444728091, h2 = _x86Rotl(h2 ^= k2 = _x86Multiply(k2 = _x86Rotl(k2 = _x86Multiply(k2, c2), 16), c3), 17), 
            h2 = _x86Multiply(h2 += h3, 5) + 197830471, h3 = _x86Rotl(h3 ^= k3 = _x86Multiply(k3 = _x86Rotl(k3 = _x86Multiply(k3, c3), 17), c4), 15), 
            h3 = _x86Multiply(h3 += h4, 5) + 2530024501, h4 = _x86Rotl(h4 ^= k4 = _x86Multiply(k4 = _x86Rotl(k4 = _x86Multiply(k4, c4), 18), c1), 13), 
            h4 = _x86Multiply(h4 += h1, 5) + 850148119;
            switch (k1 = 0, k2 = 0, k3 = 0, k4 = 0, remainder) {
              case 15:
                k4 ^= key.charCodeAt(i + 14) << 16;

              case 14:
                k4 ^= key.charCodeAt(i + 13) << 8;

              case 13:
                h4 ^= k4 = _x86Multiply(k4 = _x86Rotl(k4 = _x86Multiply(k4 ^= key.charCodeAt(i + 12), c4), 18), c1);

              case 12:
                k3 ^= key.charCodeAt(i + 11) << 24;

              case 11:
                k3 ^= key.charCodeAt(i + 10) << 16;

              case 10:
                k3 ^= key.charCodeAt(i + 9) << 8;

              case 9:
                h3 ^= k3 = _x86Multiply(k3 = _x86Rotl(k3 = _x86Multiply(k3 ^= key.charCodeAt(i + 8), c3), 17), c4);

              case 8:
                k2 ^= key.charCodeAt(i + 7) << 24;

              case 7:
                k2 ^= key.charCodeAt(i + 6) << 16;

              case 6:
                k2 ^= key.charCodeAt(i + 5) << 8;

              case 5:
                h2 ^= k2 = _x86Multiply(k2 = _x86Rotl(k2 = _x86Multiply(k2 ^= key.charCodeAt(i + 4), c2), 16), c3);

              case 4:
                k1 ^= key.charCodeAt(i + 3) << 24;

              case 3:
                k1 ^= key.charCodeAt(i + 2) << 16;

              case 2:
                k1 ^= key.charCodeAt(i + 1) << 8;

              case 1:
                h1 ^= k1 = _x86Multiply(k1 = _x86Rotl(k1 = _x86Multiply(k1 ^= key.charCodeAt(i), c1), 15), c2);
            }
            return h1 ^= key.length, h1 += h2 ^= key.length, h1 += h3 ^= key.length, h2 += h1 += h4 ^= key.length, 
            h3 += h1, h4 += h1, h1 = _x86Fmix(h1), h1 += h2 = _x86Fmix(h2), h1 += h3 = _x86Fmix(h3), 
            h2 += h1 += h4 = _x86Fmix(h4), h3 += h1, h4 += h1, ("00000000" + (h1 >>> 0).toString(16)).slice(-8) + ("00000000" + (h2 >>> 0).toString(16)).slice(-8) + ("00000000" + (h3 >>> 0).toString(16)).slice(-8) + ("00000000" + (h4 >>> 0).toString(16)).slice(-8);
        },
        x64Hash64: function(key, seed) {
            return x64Hash128(key, seed).slice(8);
        },
        x64Hash128: x64Hash128,
        hash: function(key, seed) {
            return x64Hash128(key, seed);
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var chrome_util_1 = __webpack_require__(133), stdlib_1 = __webpack_require__(3), ChromeTabsApiImpl = function() {
        function ChromeTabsApiImpl() {
            this.kind = "web-extension";
        }
        return ChromeTabsApiImpl.prototype.open = function(url, activateOnOpen) {
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                chrome.tabs.create({
                    url: url,
                    active: activateOnOpen
                }, function(tab) {
                    chrome_util_1.handleChromeError(function() {
                        return resolve(tab);
                    }, reject);
                });
            });
        }, ChromeTabsApiImpl.prototype.updateCurrent = function(url) {
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                chrome.tabs.update({
                    url: url
                }, function(tab) {
                    chrome_util_1.handleChromeError(function() {
                        return resolve(tab);
                    }, reject);
                });
            });
        }, ChromeTabsApiImpl.prototype.getActiveTab = function() {
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                var ct = chrome.tabs;
                ct.query({
                    active: !0,
                    lastFocusedWindow: !0
                }, function(tabs) {
                    chrome_util_1.handleChromeError(function() {
                        tabs && tabs.length ? resolve(tabs[0]) : ct.query({
                            active: !0
                        }, function(tabs) {
                            chrome_util_1.handleChromeError(function() {
                                resolve(tabs[0]);
                            }, reject);
                        });
                    }, reject);
                });
            });
        }, ChromeTabsApiImpl.prototype.getAllTabs = function() {
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                return chrome.tabs.query({}, function(tabs) {
                    return chrome_util_1.handleChromeError(function() {
                        return resolve(tabs);
                    }, reject);
                });
            });
        }, ChromeTabsApiImpl.prototype.getActiveTabUrl = function() {
            var _this = this;
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                return _this.getActiveTab().then(function(tab) {
                    return chrome_util_1.handleChromeError(function() {
                        return resolve(tab && tab.url);
                    }, reject);
                });
            });
        }, ChromeTabsApiImpl.prototype.onActiveTabChange = function(listener, error) {
            var _this = this, resolveWithCheck = function(tab) {
                chrome_util_1.handleChromeError(function() {
                    tab && listener(tab);
                }, error);
            };
            chrome.tabs.onActivated.addListener(function(activeTab) {
                return chrome.tabs.get(activeTab.tabId, function(tab) {
                    return resolveWithCheck(tab);
                });
            }), chrome.tabs.onUpdated.addListener(function(tabId, reason) {
                _this.getActiveTab().then(function(tab) {
                    tab && tab.id === tabId && (reason.url || reason.favIconUrl || "complete" === reason.status) && chrome.tabs.get(tabId, function(active) {
                        return resolveWithCheck(active);
                    });
                });
            }), chrome.windows.onFocusChanged.addListener(function(windowId) {
                return chrome.tabs.query({
                    active: !0,
                    windowId: windowId,
                    lastFocusedWindow: !0
                }, function(tabs) {
                    return resolveWithCheck(tabs[0]);
                });
            }), this.getActiveTab().then(function(tab) {
                return resolveWithCheck(tab);
            });
        }, ChromeTabsApiImpl.prototype.reload = function(tabId) {
            return stdlib_1.SafePromise.create(function(resolve, reject) {
                var cb = function() {
                    return chrome_util_1.handleChromeError(function() {
                        return resolve();
                    }, reject);
                };
                tabId ? chrome.tabs.reload(tabId, {}, cb) : chrome.tabs.reload(cb);
            });
        }, ChromeTabsApiImpl;
    }();
    exports.ChromeTabsApiImpl = ChromeTabsApiImpl;
}, function(module, exports, __webpack_require__) {
    var Stack = __webpack_require__(57), assignMergeValue = __webpack_require__(134), baseFor = __webpack_require__(120), baseMergeDeep = __webpack_require__(283), isObject = __webpack_require__(9), keysIn = __webpack_require__(43), safeGet = __webpack_require__(136);
    module.exports = function baseMerge(object, source, srcIndex, customizer, stack) {
        object !== source && baseFor(source, function(srcValue, key) {
            if (isObject(srcValue)) stack || (stack = new Stack()), baseMergeDeep(object, source, key, srcIndex, baseMerge, customizer, stack); else {
                var newValue = customizer ? customizer(safeGet(object, key), srcValue, key + "", object, source, stack) : void 0;
                void 0 === newValue && (newValue = srcValue), assignMergeValue(object, key, newValue);
            }
        }, keysIn);
    };
}, function(module, exports, __webpack_require__) {
    var assignMergeValue = __webpack_require__(134), cloneBuffer = __webpack_require__(173), cloneTypedArray = __webpack_require__(174), copyArray = __webpack_require__(175), initCloneObject = __webpack_require__(176), isArguments = __webpack_require__(45), isArray = __webpack_require__(8), isArrayLikeObject = __webpack_require__(111), isBuffer = __webpack_require__(35), isFunction = __webpack_require__(41), isObject = __webpack_require__(9), isPlainObject = __webpack_require__(177), isTypedArray = __webpack_require__(40), safeGet = __webpack_require__(136), toPlainObject = __webpack_require__(284);
    module.exports = function(object, source, key, srcIndex, mergeFunc, customizer, stack) {
        var objValue = safeGet(object, key), srcValue = safeGet(source, key), stacked = stack.get(srcValue);
        if (stacked) assignMergeValue(object, key, stacked); else {
            var newValue = customizer ? customizer(objValue, srcValue, key + "", object, source, stack) : void 0, isCommon = void 0 === newValue;
            if (isCommon) {
                var isArr = isArray(srcValue), isBuff = !isArr && isBuffer(srcValue), isTyped = !isArr && !isBuff && isTypedArray(srcValue);
                newValue = srcValue, isArr || isBuff || isTyped ? isArray(objValue) ? newValue = objValue : isArrayLikeObject(objValue) ? newValue = copyArray(objValue) : isBuff ? (isCommon = !1, 
                newValue = cloneBuffer(srcValue, !0)) : isTyped ? (isCommon = !1, newValue = cloneTypedArray(srcValue, !0)) : newValue = [] : isPlainObject(srcValue) || isArguments(srcValue) ? (newValue = objValue, 
                isArguments(objValue) ? newValue = toPlainObject(objValue) : (!isObject(objValue) || srcIndex && isFunction(objValue)) && (newValue = initCloneObject(srcValue))) : isCommon = !1;
            }
            isCommon && (stack.set(srcValue, newValue), mergeFunc(newValue, srcValue, srcIndex, customizer, stack), 
            stack.delete(srcValue)), assignMergeValue(object, key, newValue);
        }
    };
}, function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), keysIn = __webpack_require__(43);
    module.exports = function(value) {
        return copyObject(value, keysIn(value));
    };
}, function(module, exports, __webpack_require__) {
    var isObject = __webpack_require__(9), isPrototype = __webpack_require__(56), nativeKeysIn = __webpack_require__(286), hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(object) {
        if (!isObject(object)) return nativeKeysIn(object);
        var isProto = isPrototype(object), result = [];
        for (var key in object) ("constructor" != key || !isProto && hasOwnProperty.call(object, key)) && result.push(key);
        return result;
    };
}, function(module, exports) {
    module.exports = function(object) {
        var result = [];
        if (null != object) for (var key in Object(object)) result.push(key);
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var constant = __webpack_require__(288), defineProperty = __webpack_require__(135), identity = __webpack_require__(52), baseSetToString = defineProperty ? function(func, string) {
        return defineProperty(func, "toString", {
            configurable: !0,
            enumerable: !1,
            value: constant(string),
            writable: !0
        });
    } : identity;
    module.exports = baseSetToString;
}, function(module, exports) {
    module.exports = function(value) {
        return function() {
            return value;
        };
    };
}, function(module, exports) {
    var HOT_COUNT = 800, HOT_SPAN = 16, nativeNow = Date.now;
    module.exports = function(func) {
        var count = 0, lastCalled = 0;
        return function() {
            var stamp = nativeNow(), remaining = HOT_SPAN - (stamp - lastCalled);
            if (lastCalled = stamp, remaining > 0) {
                if (++count >= HOT_COUNT) return arguments[0];
            } else count = 0;
            return func.apply(void 0, arguments);
        };
    };
}, , , , , , , , , , function(module, exports, __webpack_require__) {
    var root = __webpack_require__(12);
    module.exports = function() {
        return root.Date.now();
    };
}, function(module, exports) {
    try {
        module.exports = function(obj) {
            var topics = {};
            return (obj = obj || {}).emit = function(topic, data) {
                topic = processTopic(topic);
                var listeners = topics[topic];
                if (listeners) for (var _listeners = listeners.concat(), i = 0; i < _listeners.length; i++) _listeners[i](data);
            }, obj.emitArgs = function(topic) {
                topic = processTopic(topic);
                var listeners = topics[topic], args = [].slice.call(arguments, 1);
                if (listeners) for (var _listeners = listeners.concat(), i = 0; i < _listeners.length; i++) _listeners[i].apply(null, args);
            }, obj.on = function(topic, cb) {
                return topic = processTopic(topic), topics[topic] = topics[topic] || [], topics[topic].push(cb), 
                {
                    un: function() {
                        obj.un(topic, cb);
                    }
                };
            }, obj.off = obj.un = function(topic, cb) {
                topic = processTopic(topic);
                var listeners = topics[topic];
                if (listeners) {
                    var index = listeners.indexOf(cb);
                    index > -1 && (listeners.splice(index, 1), listeners.length > 0 || delete topics[topic]);
                }
            }, obj.one = function(topic, cb) {
                var listener = obj.on(topic, function() {
                    listener.un(), cb.apply(null, arguments);
                });
            }, obj.delegate = function(delegateTo, topic, delegateTopic) {
                topic = processTopic(topic), obj.on(topic, function(data) {
                    delegateTo.emit(delegateTopic || topic, data);
                });
            }, obj;
            function processTopic(topic) {
                return topic.join ? topic.join(" ") : topic;
            }
        };
    } catch (e) {}
}, function(module, exports, __webpack_require__) {
    var arrayEach = __webpack_require__(92), baseEach = __webpack_require__(181), castFunction = __webpack_require__(303), isArray = __webpack_require__(8);
    module.exports = function(collection, iteratee) {
        return (isArray(collection) ? arrayEach : baseEach)(collection, castFunction(iteratee));
    };
}, function(module, exports, __webpack_require__) {
    var isArrayLike = __webpack_require__(29);
    module.exports = function(eachFunc, fromRight) {
        return function(collection, iteratee) {
            if (null == collection) return collection;
            if (!isArrayLike(collection)) return eachFunc(collection, iteratee);
            for (var length = collection.length, index = fromRight ? length : -1, iterable = Object(collection); (fromRight ? index-- : ++index < length) && !1 !== iteratee(iterable[index], index, iterable); ) ;
            return collection;
        };
    };
}, function(module, exports, __webpack_require__) {
    var identity = __webpack_require__(52);
    module.exports = function(value) {
        return "function" == typeof value ? value : identity;
    };
}, function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), createAssigner = __webpack_require__(112), keysIn = __webpack_require__(43), assignIn = createAssigner(function(object, source) {
        copyObject(source, keysIn(source), object);
    });
    module.exports = assignIn;
}, , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(obj) {
        return typeof obj;
    } : function(obj) {
        return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
    };
    exports.printBuffer = function(buffer, options) {
        var logger = options.logger, actionTransformer = options.actionTransformer, _options$titleFormatt = options.titleFormatter, titleFormatter = void 0 === _options$titleFormatt ? function(options) {
            var timestamp = options.timestamp, duration = options.duration;
            return function(action, time, took) {
                var parts = [ "action" ];
                return parts.push("%c" + String(action.type)), timestamp && parts.push("%c@ " + time), 
                duration && parts.push("%c(in " + took.toFixed(2) + " ms)"), parts.join(" ");
            };
        }(options) : _options$titleFormatt, collapsed = options.collapsed, colors = options.colors, level = options.level, diff = options.diff;
        buffer.forEach(function(logEntry, key) {
            var started = logEntry.started, startedTime = logEntry.startedTime, action = logEntry.action, prevState = logEntry.prevState, error = logEntry.error, took = logEntry.took, nextState = logEntry.nextState, nextEntry = buffer[key + 1];
            nextEntry && (nextState = nextEntry.prevState, took = nextEntry.started - started);
            var formattedAction = actionTransformer(action), isCollapsed = "function" == typeof collapsed ? collapsed(function() {
                return nextState;
            }, action, logEntry) : collapsed, formattedTime = (0, _helpers.formatTime)(startedTime), titleCSS = colors.title ? "color: " + colors.title(formattedAction) + ";" : "", headerCSS = [ "color: gray; font-weight: lighter;" ];
            headerCSS.push(titleCSS), options.timestamp && headerCSS.push("color: gray; font-weight: lighter;"), 
            options.duration && headerCSS.push("color: gray; font-weight: lighter;");
            var title = titleFormatter(formattedAction, formattedTime, took);
            try {
                isCollapsed ? colors.title ? logger.groupCollapsed.apply(logger, [ "%c " + title ].concat(headerCSS)) : logger.groupCollapsed(title) : colors.title ? logger.group.apply(logger, [ "%c " + title ].concat(headerCSS)) : logger.group(title);
            } catch (e) {
                logger.log(title);
            }
            var prevStateLevel = getLogLevel(level, formattedAction, [ prevState ], "prevState"), actionLevel = getLogLevel(level, formattedAction, [ formattedAction ], "action"), errorLevel = getLogLevel(level, formattedAction, [ error, prevState ], "error"), nextStateLevel = getLogLevel(level, formattedAction, [ nextState ], "nextState");
            prevStateLevel && (colors.prevState ? logger[prevStateLevel]("%c prev state", "color: " + colors.prevState(prevState) + "; font-weight: bold", prevState) : logger[prevStateLevel]("prev state", prevState)), 
            actionLevel && (colors.action ? logger[actionLevel]("%c action    ", "color: " + colors.action(formattedAction) + "; font-weight: bold", formattedAction) : logger[actionLevel]("action    ", formattedAction)), 
            error && errorLevel && (colors.error ? logger[errorLevel]("%c error     ", "color: " + colors.error(error, prevState) + "; font-weight: bold;", error) : logger[errorLevel]("error     ", error)), 
            nextStateLevel && (colors.nextState ? logger[nextStateLevel]("%c next state", "color: " + colors.nextState(nextState) + "; font-weight: bold", nextState) : logger[nextStateLevel]("next state", nextState)), 
            diff && (0, _diff2.default)(prevState, nextState, logger, isCollapsed);
            try {
                logger.groupEnd();
            } catch (e) {
                logger.log("—— log end ——");
            }
        });
    };
    var obj, _helpers = __webpack_require__(142), _diff = __webpack_require__(307), _diff2 = (obj = _diff) && obj.__esModule ? obj : {
        default: obj
    };
    function getLogLevel(level, action, payload, type) {
        switch (void 0 === level ? "undefined" : _typeof(level)) {
          case "object":
            return "function" == typeof level[type] ? level[type].apply(level, function(arr) {
                if (Array.isArray(arr)) {
                    for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];
                    return arr2;
                }
                return Array.from(arr);
            }(payload)) : level[type];

          case "function":
            return level(action);

          default:
            return level;
        }
    }
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.default = function(prevState, newState, logger, isCollapsed) {
        var diff = (0, _deepDiff2.default)(prevState, newState);
        try {
            isCollapsed ? logger.groupCollapsed("diff") : logger.group("diff");
        } catch (e) {
            logger.log("diff");
        }
        diff ? diff.forEach(function(elem) {
            var kind = elem.kind, output = function(diff) {
                var kind = diff.kind, path = diff.path, lhs = diff.lhs, rhs = diff.rhs, index = diff.index, item = diff.item;
                switch (kind) {
                  case "E":
                    return [ path.join("."), lhs, "→", rhs ];

                  case "N":
                    return [ path.join("."), rhs ];

                  case "D":
                    return [ path.join(".") ];

                  case "A":
                    return [ path.join(".") + "[" + index + "]", item ];

                  default:
                    return [];
                }
            }(elem);
            logger.log.apply(logger, [ "%c " + dictionary[kind].text, function(kind) {
                return "color: " + dictionary[kind].color + "; font-weight: bold";
            }(kind) ].concat(function(arr) {
                {
                    if (Array.isArray(arr)) {
                        for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];
                        return arr2;
                    }
                    return Array.from(arr);
                }
            }(output)));
        }) : logger.log("—— no diff ——");
        try {
            logger.groupEnd();
        } catch (e) {
            logger.log("—— diff end —— ");
        }
    };
    var obj, _deepDiff = __webpack_require__(308), _deepDiff2 = (obj = _deepDiff) && obj.__esModule ? obj : {
        default: obj
    };
    var dictionary = {
        E: {
            color: "#2196F3",
            text: "CHANGED:"
        },
        N: {
            color: "#4CAF50",
            text: "ADDED:"
        },
        D: {
            color: "#F44336",
            text: "DELETED:"
        },
        A: {
            color: "#2196F3",
            text: "ARRAY:"
        }
    };
    module.exports = exports.default;
}, function(module, exports, __webpack_require__) {
    (function(global) {
        var __WEBPACK_AMD_DEFINE_RESULT__;
        !function(root, factory) {
            "use strict";
            void 0 === (__WEBPACK_AMD_DEFINE_RESULT__ = function() {
                return factory();
            }.apply(exports, [])) || (module.exports = __WEBPACK_AMD_DEFINE_RESULT__);
        }(0, function(undefined) {
            "use strict";
            var $scope, conflict, conflictResolution = [];
            function inherits(ctor, superCtor) {
                ctor.super_ = superCtor, ctor.prototype = Object.create(superCtor.prototype, {
                    constructor: {
                        value: ctor,
                        enumerable: !1,
                        writable: !0,
                        configurable: !0
                    }
                });
            }
            function Diff(kind, path) {
                Object.defineProperty(this, "kind", {
                    value: kind,
                    enumerable: !0
                }), path && path.length && Object.defineProperty(this, "path", {
                    value: path,
                    enumerable: !0
                });
            }
            function DiffEdit(path, origin, value) {
                DiffEdit.super_.call(this, "E", path), Object.defineProperty(this, "lhs", {
                    value: origin,
                    enumerable: !0
                }), Object.defineProperty(this, "rhs", {
                    value: value,
                    enumerable: !0
                });
            }
            function DiffNew(path, value) {
                DiffNew.super_.call(this, "N", path), Object.defineProperty(this, "rhs", {
                    value: value,
                    enumerable: !0
                });
            }
            function DiffDeleted(path, value) {
                DiffDeleted.super_.call(this, "D", path), Object.defineProperty(this, "lhs", {
                    value: value,
                    enumerable: !0
                });
            }
            function DiffArray(path, index, item) {
                DiffArray.super_.call(this, "A", path), Object.defineProperty(this, "index", {
                    value: index,
                    enumerable: !0
                }), Object.defineProperty(this, "item", {
                    value: item,
                    enumerable: !0
                });
            }
            function arrayRemove(arr, from, to) {
                var rest = arr.slice((to || from) + 1 || arr.length);
                return arr.length = from < 0 ? arr.length + from : from, arr.push.apply(arr, rest), 
                arr;
            }
            function realTypeOf(subject) {
                var type = typeof subject;
                return "object" !== type ? type : subject === Math ? "math" : null === subject ? "null" : Array.isArray(subject) ? "array" : "[object Date]" === Object.prototype.toString.call(subject) ? "date" : void 0 !== subject.toString && /^\/.*\//.test(subject.toString()) ? "regexp" : "object";
            }
            function deepDiff(lhs, rhs, changes, prefilter, path, key, stack) {
                var currentPath = (path = path || []).slice(0);
                if (void 0 !== key) {
                    if (prefilter) {
                        if ("function" == typeof prefilter && prefilter(currentPath, key)) return;
                        if ("object" == typeof prefilter) {
                            if (prefilter.prefilter && prefilter.prefilter(currentPath, key)) return;
                            if (prefilter.normalize) {
                                var alt = prefilter.normalize(currentPath, key, lhs, rhs);
                                alt && (lhs = alt[0], rhs = alt[1]);
                            }
                        }
                    }
                    currentPath.push(key);
                }
                "regexp" === realTypeOf(lhs) && "regexp" === realTypeOf(rhs) && (lhs = lhs.toString(), 
                rhs = rhs.toString());
                var ltype = typeof lhs, rtype = typeof rhs;
                if ("undefined" === ltype) "undefined" !== rtype && changes(new DiffNew(currentPath, rhs)); else if ("undefined" === rtype) changes(new DiffDeleted(currentPath, lhs)); else if (realTypeOf(lhs) !== realTypeOf(rhs)) changes(new DiffEdit(currentPath, lhs, rhs)); else if ("[object Date]" === Object.prototype.toString.call(lhs) && "[object Date]" === Object.prototype.toString.call(rhs) && lhs - rhs != 0) changes(new DiffEdit(currentPath, lhs, rhs)); else if ("object" === ltype && null !== lhs && null !== rhs) {
                    if ((stack = stack || []).indexOf(lhs) < 0) {
                        if (stack.push(lhs), Array.isArray(lhs)) {
                            var i;
                            lhs.length;
                            for (i = 0; i < lhs.length; i++) i >= rhs.length ? changes(new DiffArray(currentPath, i, new DiffDeleted(undefined, lhs[i]))) : deepDiff(lhs[i], rhs[i], changes, prefilter, currentPath, i, stack);
                            for (;i < rhs.length; ) changes(new DiffArray(currentPath, i, new DiffNew(undefined, rhs[i++])));
                        } else {
                            var akeys = Object.keys(lhs), pkeys = Object.keys(rhs);
                            akeys.forEach(function(k, i) {
                                var other = pkeys.indexOf(k);
                                other >= 0 ? (deepDiff(lhs[k], rhs[k], changes, prefilter, currentPath, k, stack), 
                                pkeys = arrayRemove(pkeys, other)) : deepDiff(lhs[k], undefined, changes, prefilter, currentPath, k, stack);
                            }), pkeys.forEach(function(k) {
                                deepDiff(undefined, rhs[k], changes, prefilter, currentPath, k, stack);
                            });
                        }
                        stack.length = stack.length - 1;
                    }
                } else lhs !== rhs && ("number" === ltype && isNaN(lhs) && isNaN(rhs) || changes(new DiffEdit(currentPath, lhs, rhs)));
            }
            function accumulateDiff(lhs, rhs, prefilter, accum) {
                return accum = accum || [], deepDiff(lhs, rhs, function(diff) {
                    diff && accum.push(diff);
                }, prefilter), accum.length ? accum : undefined;
            }
            function applyChange(target, source, change) {
                if (target && source && change && change.kind) {
                    for (var it = target, i = -1, last = change.path ? change.path.length - 1 : 0; ++i < last; ) void 0 === it[change.path[i]] && (it[change.path[i]] = "number" == typeof change.path[i] ? [] : {}), 
                    it = it[change.path[i]];
                    switch (change.kind) {
                      case "A":
                        !function applyArrayChange(arr, index, change) {
                            if (change.path && change.path.length) {
                                var i, it = arr[index], u = change.path.length - 1;
                                for (i = 0; i < u; i++) it = it[change.path[i]];
                                switch (change.kind) {
                                  case "A":
                                    applyArrayChange(it[change.path[i]], change.index, change.item);
                                    break;

                                  case "D":
                                    delete it[change.path[i]];
                                    break;

                                  case "E":
                                  case "N":
                                    it[change.path[i]] = change.rhs;
                                }
                            } else switch (change.kind) {
                              case "A":
                                applyArrayChange(arr[index], change.index, change.item);
                                break;

                              case "D":
                                arr = arrayRemove(arr, index);
                                break;

                              case "E":
                              case "N":
                                arr[index] = change.rhs;
                            }
                            return arr;
                        }(change.path ? it[change.path[i]] : it, change.index, change.item);
                        break;

                      case "D":
                        delete it[change.path[i]];
                        break;

                      case "E":
                      case "N":
                        it[change.path[i]] = change.rhs;
                    }
                }
            }
            return $scope = "object" == typeof global && global ? global : "undefined" != typeof window ? window : {}, 
            (conflict = $scope.DeepDiff) && conflictResolution.push(function() {
                void 0 !== conflict && $scope.DeepDiff === accumulateDiff && ($scope.DeepDiff = conflict, 
                conflict = undefined);
            }), inherits(DiffEdit, Diff), inherits(DiffNew, Diff), inherits(DiffDeleted, Diff), 
            inherits(DiffArray, Diff), Object.defineProperties(accumulateDiff, {
                diff: {
                    value: accumulateDiff,
                    enumerable: !0
                },
                observableDiff: {
                    value: deepDiff,
                    enumerable: !0
                },
                applyDiff: {
                    value: function(target, source, filter) {
                        target && source && deepDiff(target, source, function(change) {
                            filter && !filter(target, source, change) || applyChange(target, source, change);
                        });
                    },
                    enumerable: !0
                },
                applyChange: {
                    value: applyChange,
                    enumerable: !0
                },
                revertChange: {
                    value: function(target, source, change) {
                        if (target && source && change && change.kind) {
                            var i, u, it = target;
                            for (u = change.path.length - 1, i = 0; i < u; i++) void 0 === it[change.path[i]] && (it[change.path[i]] = {}), 
                            it = it[change.path[i]];
                            switch (change.kind) {
                              case "A":
                                !function revertArrayChange(arr, index, change) {
                                    if (change.path && change.path.length) {
                                        var i, it = arr[index], u = change.path.length - 1;
                                        for (i = 0; i < u; i++) it = it[change.path[i]];
                                        switch (change.kind) {
                                          case "A":
                                            revertArrayChange(it[change.path[i]], change.index, change.item);
                                            break;

                                          case "D":
                                          case "E":
                                            it[change.path[i]] = change.lhs;
                                            break;

                                          case "N":
                                            delete it[change.path[i]];
                                        }
                                    } else switch (change.kind) {
                                      case "A":
                                        revertArrayChange(arr[index], change.index, change.item);
                                        break;

                                      case "D":
                                      case "E":
                                        arr[index] = change.lhs;
                                        break;

                                      case "N":
                                        arr = arrayRemove(arr, index);
                                    }
                                    return arr;
                                }(it[change.path[i]], change.index, change.item);
                                break;

                              case "D":
                              case "E":
                                it[change.path[i]] = change.lhs;
                                break;

                              case "N":
                                delete it[change.path[i]];
                            }
                        }
                    },
                    enumerable: !0
                },
                isConflict: {
                    value: function() {
                        return void 0 !== conflict;
                    },
                    enumerable: !0
                },
                noConflict: {
                    value: function() {
                        return conflictResolution && (conflictResolution.forEach(function(it) {
                            it();
                        }), conflictResolution = null), accumulateDiff;
                    },
                    enumerable: !0
                }
            }), accumulateDiff;
        });
    }).call(exports, __webpack_require__(34));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.default = {
        level: "log",
        logger: console,
        logErrors: !0,
        collapsed: void 0,
        predicate: void 0,
        duration: !1,
        timestamp: !0,
        stateTransformer: function(state) {
            return state;
        },
        actionTransformer: function(action) {
            return action;
        },
        errorTransformer: function(error) {
            return error;
        },
        colors: {
            title: function() {
                return "inherit";
            },
            prevState: function() {
                return "#9E9E9E";
            },
            action: function() {
                return "#03A9F4";
            },
            nextState: function() {
                return "#4CAF50";
            },
            error: function() {
                return "#F20404";
            }
        },
        diff: !1,
        diffPredicate: void 0,
        transformer: void 0
    }, module.exports = exports.default;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var __WEBPACK_IMPORTED_MODULE_0__Symbol_js__ = __webpack_require__(145), __WEBPACK_IMPORTED_MODULE_1__getRawTag_js__ = __webpack_require__(313), __WEBPACK_IMPORTED_MODULE_2__objectToString_js__ = __webpack_require__(314), nullTag = "[object Null]", undefinedTag = "[object Undefined]", symToStringTag = __WEBPACK_IMPORTED_MODULE_0__Symbol_js__.a ? __WEBPACK_IMPORTED_MODULE_0__Symbol_js__.a.toStringTag : void 0;
    __webpack_exports__.a = function(value) {
        return null == value ? void 0 === value ? undefinedTag : nullTag : symToStringTag && symToStringTag in Object(value) ? Object(__WEBPACK_IMPORTED_MODULE_1__getRawTag_js__.a)(value) : Object(__WEBPACK_IMPORTED_MODULE_2__objectToString_js__.a)(value);
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var __WEBPACK_IMPORTED_MODULE_0__freeGlobal_js__ = __webpack_require__(312), freeSelf = "object" == typeof self && self && self.Object === Object && self, root = __WEBPACK_IMPORTED_MODULE_0__freeGlobal_js__.a || freeSelf || Function("return this")();
    __webpack_exports__.a = root;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    (function(global) {
        var freeGlobal = "object" == typeof global && global && global.Object === Object && global;
        __webpack_exports__.a = freeGlobal;
    }).call(__webpack_exports__, __webpack_require__(34));
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var __WEBPACK_IMPORTED_MODULE_0__Symbol_js__ = __webpack_require__(145), objectProto = Object.prototype, hasOwnProperty = objectProto.hasOwnProperty, nativeObjectToString = objectProto.toString, symToStringTag = __WEBPACK_IMPORTED_MODULE_0__Symbol_js__.a ? __WEBPACK_IMPORTED_MODULE_0__Symbol_js__.a.toStringTag : void 0;
    __webpack_exports__.a = function(value) {
        var isOwn = hasOwnProperty.call(value, symToStringTag), tag = value[symToStringTag];
        try {
            value[symToStringTag] = void 0;
            var unmasked = !0;
        } catch (e) {}
        var result = nativeObjectToString.call(value);
        return unmasked && (isOwn ? value[symToStringTag] = tag : delete value[symToStringTag]), 
        result;
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var nativeObjectToString = Object.prototype.toString;
    __webpack_exports__.a = function(value) {
        return nativeObjectToString.call(value);
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    var __WEBPACK_IMPORTED_MODULE_0__overArg_js__ = __webpack_require__(316), getPrototype = Object(__WEBPACK_IMPORTED_MODULE_0__overArg_js__.a)(Object.getPrototypeOf, Object);
    __webpack_exports__.a = getPrototype;
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function(func, transform) {
        return function(arg) {
            return func(transform(arg));
        };
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function(value) {
        return null != value && "object" == typeof value;
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    (function(global, module) {
        var root, __WEBPACK_IMPORTED_MODULE_0__ponyfill_js__ = __webpack_require__(320);
        root = "undefined" != typeof self ? self : "undefined" != typeof window ? window : void 0 !== global ? global : module;
        var result = Object(__WEBPACK_IMPORTED_MODULE_0__ponyfill_js__.a)(root);
        __webpack_exports__.a = result;
    }).call(__webpack_exports__, __webpack_require__(34), __webpack_require__(319)(module));
}, function(module, exports) {
    module.exports = function(originalModule) {
        if (!originalModule.webpackPolyfill) {
            var module = Object.create(originalModule);
            module.children || (module.children = []), Object.defineProperty(module, "loaded", {
                enumerable: !0,
                get: function() {
                    return module.l;
                }
            }), Object.defineProperty(module, "id", {
                enumerable: !0,
                get: function() {
                    return module.i;
                }
            }), Object.defineProperty(module, "exports", {
                enumerable: !0
            }), module.webpackPolyfill = 1;
        }
        return module;
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function(root) {
        var result, Symbol = root.Symbol;
        "function" == typeof Symbol ? Symbol.observable ? result = Symbol.observable : (result = Symbol("observable"), 
        Symbol.observable = result) : result = "@@observable";
        return result;
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function(reducers) {
        for (var reducerKeys = Object.keys(reducers), finalReducers = {}, i = 0; i < reducerKeys.length; i++) {
            var key = reducerKeys[i];
            0, "function" == typeof reducers[key] && (finalReducers[key] = reducers[key]);
        }
        var finalReducerKeys = Object.keys(finalReducers);
        0;
        var shapeAssertionError = void 0;
        try {
            !function(reducers) {
                Object.keys(reducers).forEach(function(key) {
                    var reducer = reducers[key], initialState = reducer(void 0, {
                        type: __WEBPACK_IMPORTED_MODULE_0__createStore__.a.INIT
                    });
                    if (void 0 === initialState) throw new Error('Reducer "' + key + "\" returned undefined during initialization. If the state passed to the reducer is undefined, you must explicitly return the initial state. The initial state may not be undefined. If you don't want to set a value for this reducer, you can use null instead of undefined.");
                    var type = "@@redux/PROBE_UNKNOWN_ACTION_" + Math.random().toString(36).substring(7).split("").join(".");
                    if (void 0 === reducer(void 0, {
                        type: type
                    })) throw new Error('Reducer "' + key + "\" returned undefined when probed with a random type. Don't try to handle " + __WEBPACK_IMPORTED_MODULE_0__createStore__.a.INIT + ' or other actions in "redux/*" namespace. They are considered private. Instead, you must return the current state for any unknown actions, unless it is undefined, in which case you must return the initial state, regardless of the action type. The initial state may not be undefined, but can be null.');
                });
            }(finalReducers);
        } catch (e) {
            shapeAssertionError = e;
        }
        return function() {
            var state = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}, action = arguments[1];
            if (shapeAssertionError) throw shapeAssertionError;
            for (var hasChanged = !1, nextState = {}, _i = 0; _i < finalReducerKeys.length; _i++) {
                var _key = finalReducerKeys[_i], reducer = finalReducers[_key], previousStateForKey = state[_key], nextStateForKey = reducer(previousStateForKey, action);
                if (void 0 === nextStateForKey) {
                    var errorMessage = getUndefinedStateErrorMessage(_key, action);
                    throw new Error(errorMessage);
                }
                nextState[_key] = nextStateForKey, hasChanged = hasChanged || nextStateForKey !== previousStateForKey;
            }
            return hasChanged ? nextState : state;
        };
    };
    var __WEBPACK_IMPORTED_MODULE_0__createStore__ = __webpack_require__(144);
    __webpack_require__(113), __webpack_require__(146);
    function getUndefinedStateErrorMessage(key, action) {
        var actionType = action && action.type;
        return "Given action " + (actionType && '"' + actionType.toString() + '"' || "an action") + ', reducer "' + key + '" returned undefined. To ignore an action, you must explicitly return the previous state. If you want this reducer to hold no value, you can return null instead of undefined.';
    }
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    function bindActionCreator(actionCreator, dispatch) {
        return function() {
            return dispatch(actionCreator.apply(void 0, arguments));
        };
    }
    __webpack_exports__.a = function(actionCreators, dispatch) {
        if ("function" == typeof actionCreators) return bindActionCreator(actionCreators, dispatch);
        if ("object" != typeof actionCreators || null === actionCreators) throw new Error("bindActionCreators expected an object or a function, instead received " + (null === actionCreators ? "null" : typeof actionCreators) + '. Did you write "import ActionCreators from" instead of "import * as ActionCreators from"?');
        for (var keys = Object.keys(actionCreators), boundActionCreators = {}, i = 0; i < keys.length; i++) {
            var key = keys[i], actionCreator = actionCreators[key];
            "function" == typeof actionCreator && (boundActionCreators[key] = bindActionCreator(actionCreator, dispatch));
        }
        return boundActionCreators;
    };
}, function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    __webpack_exports__.a = function() {
        for (var _len = arguments.length, middlewares = Array(_len), _key = 0; _key < _len; _key++) middlewares[_key] = arguments[_key];
        return function(createStore) {
            return function(reducer, preloadedState, enhancer) {
                var store = createStore(reducer, preloadedState, enhancer), _dispatch = store.dispatch, chain = [], middlewareAPI = {
                    getState: store.getState,
                    dispatch: function(action) {
                        return _dispatch(action);
                    }
                };
                return chain = middlewares.map(function(middleware) {
                    return middleware(middlewareAPI);
                }), _dispatch = __WEBPACK_IMPORTED_MODULE_0__compose__.a.apply(void 0, chain)(store.dispatch), 
                _extends({}, store, {
                    dispatch: _dispatch
                });
            };
        };
    };
    var __WEBPACK_IMPORTED_MODULE_0__compose__ = __webpack_require__(147), _extends = Object.assign || function(target) {
        for (var i = 1; i < arguments.length; i++) {
            var source = arguments[i];
            for (var key in source) Object.prototype.hasOwnProperty.call(source, key) && (target[key] = source[key]);
        }
        return target;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    }, __spread = this && this.__spread || function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var createLogger = __webpack_require__(183), redux_1 = __webpack_require__(143), redux_saga_1 = __webpack_require__(148), reducer_1 = __webpack_require__(330), reducer_2 = __webpack_require__(331), reducer_3 = __webpack_require__(184), reducer_4 = __webpack_require__(332), config_1 = __webpack_require__(11), actions_1 = __webpack_require__(151), actions_2 = __webpack_require__(151);
    exports.pureActions = actions_2.pureActions;
    var effects_1 = __webpack_require__(99), AuthSagaRunners = function() {
        return function(_store, _userSagas) {
            var _this = this;
            this._store = _store, this._userSagas = _userSagas, this.refreshUser = function() {
                for (var _a, args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                return (_a = _this._store).runSaga.apply(_a, __spread([ _this._userSagas.externalUpdateUser.bind(_this._userSagas) ], args)).done;
            }, this.signin = function(data) {
                var _a = data.form, reqData = {
                    email_login: {
                        email: _a.email,
                        password: _a.password
                    }
                };
                return _this._store.runSaga(_this._userSagas.authRequest.bind(_this._userSagas), config_1.URLS.authSignin, reqData, data.placement, "signin").done;
            }, this.signup = function(data) {
                var _a = data.form, reqData = {
                    email_signup: {
                        name: _a.name,
                        email: _a.email,
                        password: _a.password
                    },
                    custom_fields: "true" === data.disableMarketingEmails ? {
                        disableMarketingEmails: "true"
                    } : {}
                };
                return _this._store.runSaga(_this._userSagas.authRequest.bind(_this._userSagas), config_1.URLS.authSignup, reqData, data.placement, "signup").done;
            };
        };
    }();
    exports.AuthSagaRunners = AuthSagaRunners;
    var TabsSagaRunner = function() {
        return function(_store, _tabsSagas) {
            var _this = this;
            this._store = _store, this._tabsSagas = _tabsSagas, this.sendStateToTabs = function() {
                return _this._store.runSaga(_this._tabsSagas.sendStateToTabs.bind(_this._tabsSagas));
            };
        };
    }();
    exports.TabsSagaRunner = TabsSagaRunner;
    var StoreControllerImpl = function() {
        function StoreControllerImpl(_userSagas, _settingsSagas, _tabsSagas, _connectionSagas, _pageConfig) {
            var _this = this;
            this._userSagas = _userSagas, this._settingsSagas = _settingsSagas, this._tabsSagas = _tabsSagas, 
            this._connectionSagas = _connectionSagas, this._pageConfig = _pageConfig;
            var sagaMiddleware = redux_saga_1.default(_userSagas.start.bind(_userSagas), _settingsSagas.start.bind(_settingsSagas), _connectionSagas.start.bind(_connectionSagas));
            this.store = function(sagaMiddleware) {
                var reducer = redux_1.combineReducers({
                    user: reducer_3.userReducer,
                    tabs: reducer_4.tabsReducer,
                    settings: reducer_2.settingsReducer,
                    connection: reducer_1.connectionReducer
                }), logger = createLogger({
                    level: "debug",
                    colors: {
                        title: function() {
                            return "green";
                        }
                    }
                });
                return redux_1.createStore(reducer, {}, redux_1.applyMiddleware(sagaMiddleware, logger));
            }(sagaMiddleware), this.runSaga = sagaMiddleware.run, this.initStore = function() {
                return sagaMiddleware.run(_this._startupFlow.bind(_this)).done.then(function() {
                    _this.store.subscribe(function() {
                        sagaMiddleware.run(_tabsSagas.sendStateToTabs.bind(_tabsSagas)), sagaMiddleware.run(_settingsSagas.processEmailConnectednessData.bind(_settingsSagas));
                    });
                });
            }, this.actions = redux_1.bindActionCreators(actions_1.pureActions, this.store.dispatch);
        }
        return StoreControllerImpl.prototype._startupFlow = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, [ effects_1.call([ this._settingsSagas, this._settingsSagas.setInitialSettings ]), effects_1.call([ this._pageConfig, this._pageConfig.init ]), effects_1.call([ this._userSagas, this._userSagas.updateUser ], {
                        failoverFromCache: !0
                    }) ] ];

                  case 1:
                    return _a.sent(), [ 4, effects_1.fork([ this._connectionSagas, this._connectionSagas.monitorIsIncognito ]) ];

                  case 2:
                    return _a.sent(), [ 4, effects_1.call([ this._tabsSagas, this._tabsSagas.start ]) ];

                  case 3:
                    return _a.sent(), [ 2 ];
                }
            });
        }, StoreControllerImpl;
    }();
    exports.StoreControllerImpl = StoreControllerImpl;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.NOT_ITERATOR_ERROR = void 0, exports.storeIO = function(store) {
        if ((0, _utils.warnDeprecated)("storeIO is deprecated, to run Saga dynamically, use 'run' method of the middleware"), 
        store[IO]) return store[IO];
        var storeEmitter = (0, _emitter2.default)(), _dispatch = store.dispatch;
        return store.dispatch = function(action) {
            var result = _dispatch(action);
            return storeEmitter.emit(action), result;
        }, store[IO] = {
            subscribe: storeEmitter.subscribe,
            dispatch: store.dispatch,
            getState: store.getState
        }, store[IO];
    }, exports.runSaga = function(iterator, _ref) {
        var subscribe = _ref.subscribe, dispatch = _ref.dispatch, getState = _ref.getState, monitor = arguments.length <= 2 || void 0 === arguments[2] ? _utils.noop : arguments[2];
        return (0, _utils.check)(iterator, _utils.is.iterator, NOT_ITERATOR_ERROR), (0, 
        _proc2.default)(iterator, subscribe, dispatch, getState, monitor);
    };
    var _utils = __webpack_require__(21), _proc2 = _interopRequireDefault(__webpack_require__(87)), _emitter2 = _interopRequireDefault(__webpack_require__(149));
    function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
            default: obj
        };
    }
    var NOT_ITERATOR_ERROR = exports.NOT_ITERATOR_ERROR = "runSaga must be called on an iterator", IO = (0, 
    _utils.sym)("IO");
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var _slicedToArray = function() {
        return function(arr, i) {
            if (Array.isArray(arr)) return arr;
            if (Symbol.iterator in Object(arr)) return function(arr, i) {
                var _arr = [], _n = !0, _d = !1, _e = void 0;
                try {
                    for (var _s, _i = arr[Symbol.iterator](); !(_n = (_s = _i.next()).done) && (_arr.push(_s.value), 
                    !i || _arr.length !== i); _n = !0) ;
                } catch (err) {
                    _d = !0, _e = err;
                } finally {
                    try {
                        !_n && _i.return && _i.return();
                    } finally {
                        if (_d) throw _e;
                    }
                }
                return _arr;
            }(arr, i);
            throw new TypeError("Invalid attempt to destructure non-iterable instance");
        };
    }();
    exports.takeEvery = function(pattern, worker) {
        for (var _len = arguments.length, args = Array(_len > 2 ? _len - 2 : 0), _key = 2; _key < _len; _key++) args[_key - 2] = arguments[_key];
        return fsmIterator({
            take: [ {
                done: !1,
                value: (0, _io.take)(pattern)
            }, "fork" ],
            fork: [ function(action) {
                return {
                    done: !1,
                    value: _io.fork.apply(void 0, [ worker ].concat(args, [ action ]))
                };
            }, "take" ]
        }, "take", "takeEvery(" + pattern + ", " + worker.name + ")");
    }, exports.takeLatest = function(pattern, worker) {
        for (var _len2 = arguments.length, args = Array(_len2 > 2 ? _len2 - 2 : 0), _key2 = 2; _key2 < _len2; _key2++) args[_key2 - 2] = arguments[_key2];
        var yieldTake = {
            done: !1,
            value: (0, _io.take)(pattern)
        }, currentTask = void 0, currentAction = void 0;
        return fsmIterator({
            take: [ yieldTake, function() {
                return currentTask ? "cancel" : "fork";
            }, function(action) {
                return currentAction = action;
            } ],
            cancel: [ function() {
                return {
                    done: !1,
                    value: (0, _io.cancel)(currentTask)
                };
            }, "fork" ],
            fork: [ function() {
                return {
                    done: !1,
                    value: _io.fork.apply(void 0, [ worker ].concat(args, [ currentAction ]))
                };
            }, "take", function(task) {
                return currentTask = task;
            } ]
        }, "take", "takeLatest(" + pattern + ", " + worker.name + ")");
    };
    var obj, _utils = __webpack_require__(21), _io = __webpack_require__(54), _SagaCancellationException = __webpack_require__(55), _SagaCancellationException2 = (obj = _SagaCancellationException) && obj.__esModule ? obj : {
        default: obj
    };
    var resume = function(fnOrValue, arg) {
        return _utils.is.func(fnOrValue) ? fnOrValue(arg) : fnOrValue;
    }, done = {
        done: !0
    };
    function fsmIterator(fsm, nextState) {
        var name = arguments.length <= 2 || void 0 === arguments[2] ? "iterator" : arguments[2], aborted = void 0, updateState = void 0;
        function next(arg, error) {
            if (aborted) return done;
            if (error) {
                if (aborted = !0, !(error instanceof _SagaCancellationException2.default)) throw error;
                return done;
            }
            updateState && updateState(arg);
            var _fsm$nextState = _slicedToArray(fsm[nextState], 3), output = _fsm$nextState[0], transition = _fsm$nextState[1], _updateState = _fsm$nextState[2];
            return updateState = _updateState, nextState = resume(transition, arg), resume(output, arg);
        }
        var iterator = {
            name: name,
            next: next,
            throw: function(error) {
                return next(null, error);
            }
        };
        return "undefined" != typeof Symbol && (iterator[Symbol.iterator] = function() {
            return iterator;
        }), iterator;
    }
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.GET_STATE_DEPRECATED_WARNING = exports.RUN_SAGA_DYNAMIC_ERROR = exports.sagaArgError = void 0, 
    exports.default = function() {
        for (var _len = arguments.length, sagas = Array(_len), _key = 0; _key < _len; _key++) sagas[_key] = arguments[_key];
        var runSagaDynamically = void 0;
        function sagaMiddleware(_ref) {
            var getState = _ref.getState, dispatch = _ref.dispatch, sagaEmitter = (0, _emitter2.default)(), monitor = _utils.isDev ? function(action) {
                return (0, _utils.asap)(function() {
                    return dispatch(action);
                });
            } : void 0, getStateDeprecated = function() {
                return (0, _utils.warnDeprecated)(GET_STATE_DEPRECATED_WARNING), getState();
            };
            function runSaga(saga) {
                for (var _len2 = arguments.length, args = Array(_len2 > 1 ? _len2 - 1 : 0), _key2 = 1; _key2 < _len2; _key2++) args[_key2 - 1] = arguments[_key2];
                return (0, _proc2.default)(saga.apply(void 0, [ getStateDeprecated ].concat(args)), sagaEmitter.subscribe, dispatch, getState, monitor, 0, saga.name);
            }
            return runSagaDynamically = runSaga, sagas.forEach(runSaga), function(next) {
                return function(action) {
                    var result = next(action);
                    return action[_monitorActions.MONITOR_ACTION] || sagaEmitter.emit(action), result;
                };
            };
        }
        return sagas.forEach(function(saga, idx) {
            return (0, _utils.check)(saga, _utils.is.func, sagaArgError("createSagaMiddleware", idx, saga));
        }), sagaMiddleware.run = function(saga) {
            for (var _len3 = arguments.length, args = Array(_len3 > 1 ? _len3 - 1 : 0), _key3 = 1; _key3 < _len3; _key3++) args[_key3 - 1] = arguments[_key3];
            if (!runSagaDynamically) throw new Error(RUN_SAGA_DYNAMIC_ERROR);
            (0, _utils.check)(saga, _utils.is.func, sagaArgError("sagaMiddleware.run", 0, saga));
            var task = runSagaDynamically.apply(void 0, [ saga ].concat(args));
            return task.done.catch(function(err) {
                if (!(err instanceof _SagaCancellationException2.default)) throw err;
            }), task;
        }, sagaMiddleware;
    };
    var _utils = __webpack_require__(21), _proc2 = _interopRequireDefault(__webpack_require__(87)), _emitter2 = _interopRequireDefault(__webpack_require__(149)), _monitorActions = __webpack_require__(88), _SagaCancellationException2 = _interopRequireDefault(__webpack_require__(55));
    function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
            default: obj
        };
    }
    var sagaArgError = exports.sagaArgError = function(fn, pos, saga) {
        return "\n  " + fn + " can only be called on Generator functions\n  Argument " + saga + " at position " + pos + " is not function!\n";
    }, RUN_SAGA_DYNAMIC_ERROR = exports.RUN_SAGA_DYNAMIC_ERROR = "Before running a Saga dynamically using middleware.run, you must mount the Saga middleware on the Store using applyMiddleware", GET_STATE_DEPRECATED_WARNING = exports.GET_STATE_DEPRECATED_WARNING = "\n  Using the 'getState' param of Sagas to access the state is deprecated since 0.9.1\n  To access the Store's state use 'yield select()' instead\n  For more infos see http://yelouafi.github.io/redux-saga/docs/api/index.html#selectselector-args\n";
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.monitorActions = exports.createMockTask = exports.MANUAL_CANCEL = exports.PARALLEL_AUTO_CANCEL = exports.RACE_AUTO_CANCEL = exports.CANCEL = exports.asap = exports.arrayOfDeffered = exports.deferred = exports.asEffect = exports.is = exports.noop = exports.TASK = void 0;
    var _utils = __webpack_require__(21), _io = __webpack_require__(54), _proc = __webpack_require__(87), _testUtils = __webpack_require__(329), monitorActions = function(obj) {
        {
            if (obj && obj.__esModule) return obj;
            var newObj = {};
            if (null != obj) for (var key in obj) Object.prototype.hasOwnProperty.call(obj, key) && (newObj[key] = obj[key]);
            return newObj.default = obj, newObj;
        }
    }(__webpack_require__(88));
    exports.TASK = _utils.TASK, exports.noop = _utils.noop, exports.is = _utils.is, 
    exports.asEffect = _io.asEffect, exports.deferred = _utils.deferred, exports.arrayOfDeffered = _utils.arrayOfDeffered, 
    exports.asap = _utils.asap, exports.CANCEL = _proc.CANCEL, exports.RACE_AUTO_CANCEL = _proc.RACE_AUTO_CANCEL, 
    exports.PARALLEL_AUTO_CANCEL = _proc.PARALLEL_AUTO_CANCEL, exports.MANUAL_CANCEL = _proc.MANUAL_CANCEL, 
    exports.createMockTask = _testUtils.createMockTask, exports.monitorActions = monitorActions;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.createMockTask = function() {
        var _ref, running = !0, _result = void 0, _error = void 0;
        return _defineProperty(_ref = {}, _utils.TASK, !0), _defineProperty(_ref, "isRunning", function() {
            return running;
        }), _defineProperty(_ref, "result", function() {
            return _result;
        }), _defineProperty(_ref, "error", function() {
            return _error;
        }), _defineProperty(_ref, "setRunning", function(b) {
            return running = b;
        }), _defineProperty(_ref, "setResult", function(r) {
            return _result = r;
        }), _defineProperty(_ref, "setError", function(e) {
            return _error = e;
        }), _ref;
    };
    var _utils = __webpack_require__(21);
    function _defineProperty(obj, key, value) {
        return key in obj ? Object.defineProperty(obj, key, {
            value: value,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : obj[key] = value, obj;
    }
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var actions_1 = __webpack_require__(98);
    exports.defaultConnection = {
        networkOffline: !window.navigator.onLine,
        cookiesDisabled: !1 === navigator.cookieEnabled,
        online: !0
    }, exports.connectionReducer = function(state, _a) {
        void 0 === state && (state = exports.defaultConnection);
        var type = _a.type, data = _a.data, online = _a.online;
        switch (type) {
          case actions_1.t.ONLINE_STATE:
            return Object.assign({}, state, {
                online: online
            });

          case actions_1.t.UPDATE_CONNECTION:
            return Object.assign({}, state, data);

          default:
            return state;
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Config = __webpack_require__(10), actions_1 = __webpack_require__(89), newsVersion = Config.getGlobal().appConfig.newsVersion;
    exports.settingsReducer = function(settings, _a) {
        void 0 === settings && (settings = {});
        var _c, _d, _e, _f, _g, type = _a.type, _b = _a.data, data = void 0 === _b ? {} : _b, domain = _a.domain, enabledDefs = _a.enabledDefs, enabled = _a.enabled, showNews = _a.showNews, propKey = _a.propKey, loginReminderType = _a.loginReminderType, domainSetting = settings[domain] || {};
        switch (type) {
          case actions_1.t.SETTINGS_INITIAL:
            return Object.assign({}, settings, data);

          case actions_1.t.TOGGLE_DEFS:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    enabledDefs: enabledDefs
                })
            });

          case actions_1.t.TOGGLE_SITE:
            return Object.assign({}, settings, ((_c = {})[domain] = Object.assign({}, domainSetting, {
                enabled: enabled,
                disabledDate: !0 === enabled ? null : Date.now()
            }), _c));

          case actions_1.t.TOGGLE_FIELD:
            return Object.assign({}, settings, ((_d = {})[domain] = Object.assign({}, settings[domain], {
                disabledFields: Object.assign({}, domainSetting.disabledFields, data)
            }), _d));

          case actions_1.t.SHOW_NEWS:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    showNews: showNews
                })
            });

          case actions_1.t.SHOW_ONBOARDING:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    showOnboarding: !0
                })
            });

          case actions_1.t.SEEN_ONBOARDING:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    showOnboarding: !1
                })
            });

          case actions_1.t.SEEN_GDOCS_OPT_IN:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    seenGdocsOptIn: !0
                })
            });

          case actions_1.t.SEEN_GDOCS_LARGE_DOCUMENT_WARNING:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    seenGdocsLargeDocumentWarning: !0
                })
            });

          case actions_1.t.SET_GDOCS_INITIAL_DISABLE:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    gdocsWasInitiallyDisabled: !0
                })
            });

          case actions_1.t.SEEN_NEWS:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    seenNewsVersion: newsVersion
                })
            });

          case actions_1.t.SET_DAPI_PROP:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, (_e = {}, _e[propKey] = data, _e))
            });

          case actions_1.t.DISABLE_REMINDER_NOTIFICATION:
            return Object.assign({}, settings, ((_f = {})[domain] = Object.assign({}, domainSetting, {
                disableReminderNotification: !0
            }), _f));

          case actions_1.t.SHOW_DISABLE_REMINDER:
            return Object.assign({}, settings, ((_g = {})[domain] = Object.assign({}, domainSetting, {
                disabledDate: Date.now()
            }), _g));

          case actions_1.t.EDGE_POPUP_FROM_GBUTTON:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    showEdgePopupFromGButton: !0
                })
            });

          case actions_1.t.SHOW_LOGIN_REMINDER:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    loginReminderType: loginReminderType,
                    showLoginReminder: !0
                })
            });

          case actions_1.t.HIDE_LOGIN_REMINDER:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    showLoginReminder: !1
                })
            });

          case actions_1.t.DISABLE_LOGIN_REMINDER:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    loginReminderDisabled: !0,
                    showLoginReminder: !1
                })
            });

          case actions_1.t.DISABLE_EMAIL_SUMMARIZATION:
            return Object.assign({}, settings, {
                common: Object.assign({}, settings.common, {
                    emailSummarizationDisabled: !0
                })
            });

          default:
            return settings;
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var actions_1 = __webpack_require__(201);
    exports.tabsReducer = function(state, _a) {
        void 0 === state && (state = {});
        var type = _a.type, data = _a.data;
        switch (type) {
          case actions_1.t.SET_ACTIVE_TAB:
            return Object.assign({}, state, {
                active: data
            });

          default:
            return state;
        }
    };
}, function(module, exports, __webpack_require__) {
    var arrayPush = __webpack_require__(106), getPrototype = __webpack_require__(59), getSymbols = __webpack_require__(107), stubArray = __webpack_require__(169), getSymbolsIn = Object.getOwnPropertySymbols ? function(object) {
        for (var result = []; object; ) arrayPush(result, getSymbols(object)), object = getPrototype(object);
        return result;
    } : stubArray;
    module.exports = getSymbolsIn;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var timeseries_impl_1 = __webpack_require__(203), log_1 = __webpack_require__(28), util_1 = __webpack_require__(2), DefaultFelogClient = function() {
        function DefaultFelogClient(_baseUrl, _appName, _appVersion, _env, _fetch) {
            this._baseUrl = _baseUrl, this._appName = _appName, this._appVersion = _appVersion, 
            this._env = _env, this._fetch = _fetch, this._context = {
                userId: void 0,
                containerId: void 0
            }, this._sessionId = util_1.guid(), this._metrics = timeseries_impl_1.MetricsStorage.createRoot(this._env + "." + this._appName, this._baseUrl, this._fetch);
        }
        return DefaultFelogClient.prototype.setUserId = function(userId) {
            this._context = Object.assign({}, this._context, {
                userId: userId
            });
        }, DefaultFelogClient.prototype.setContainerId = function(containerId) {
            this._context = Object.assign({}, this._context, {
                containerId: containerId
            });
        }, DefaultFelogClient.prototype.getContext = function() {
            return this._context;
        }, DefaultFelogClient.prototype.sendEvent = function(e) {
            var payload = log_1.createEventPayload(e, {
                appName: this._appName,
                appVersion: this._appVersion,
                env: this._env,
                context: this.getContext()
            });
            return this._fetch(log_1.felogRequestUrl(payload, this._baseUrl), {
                mode: "no-cors",
                method: "get",
                cache: "no-cache"
            }).then(function(_) {}).catch(function(_) {});
        }, DefaultFelogClient.prototype.sendManyEvents = function(events, isCrash) {
            var _this = this, payloadEvents = events.map(function(event) {
                return log_1.createEventPayload({
                    logger: event.logger,
                    message: event.message,
                    level: event.level,
                    extra: event.extra,
                    extra_performance: event.extra_performance,
                    timestamp: event.timestamp
                }, {
                    appName: _this._appName,
                    appVersion: _this._appVersion,
                    sessionId: _this._sessionId,
                    env: _this._env,
                    context: _this.getContext()
                });
            });
            return this._fetch(this._baseUrl + "/" + (isCrash ? "crash" : "log"), {
                mode: "cors",
                headers: {
                    "Content-Type": "application/json"
                },
                method: "post",
                cache: "no-cache",
                body: JSON.stringify(payloadEvents)
            }).then(function(_) {}).catch(function(_) {});
        }, DefaultFelogClient.prototype.sendUsageEvent = function(logger, message, level, usageData) {
            var usage = {
                domain: usageData.domain,
                accountType: usageData.accountType,
                fieldType: usageData.fieldType,
                fieldSupported: usageData.fieldSupported
            };
            if (this._context.containerId || this._context.userId) {
                var str = (this._context.containerId || this._context.userId) + usageData.domain;
                usage.groupInfo = util_1.normalizedHashCode(str, 1e9);
            }
            var payload = log_1.createEventPayload({
                logger: logger,
                message: message,
                level: level,
                extra_usage: usageData
            }, {
                appName: this._appName,
                appVersion: this._appVersion,
                env: this._env
            });
            return this._fetch(log_1.felogUsageRequestUrl(payload, this._baseUrl), {
                mode: "no-cors",
                method: "get",
                cache: "no-cache"
            }).then(function(_) {}).catch(function(_) {});
        }, DefaultFelogClient.prototype.sendCounter = function(name, delta) {
            this._metrics.getCounter(name).increment(delta);
        }, DefaultFelogClient.prototype.sendTimer = function(name, time) {
            this._metrics.getTimer(name).recordTime(time);
        }, DefaultFelogClient;
    }();
    exports.DefaultFelogClient = DefaultFelogClient;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var log_1 = __webpack_require__(28), SumoLogicClient = function() {
        function SumoLogicClient(_baseUrl, _appName, _appVersion, _env, _fetch) {
            this._baseUrl = _baseUrl, this._appName = _appName, this._appVersion = _appVersion, 
            this._env = _env, this._fetch = _fetch, this._context = {
                userId: void 0,
                containerId: void 0
            };
        }
        return SumoLogicClient.prototype.setUserId = function(userId) {
            this._context = Object.assign({}, this._context, {
                userId: userId
            });
        }, SumoLogicClient.prototype.setContainerId = function(containerId) {
            this._context = Object.assign({}, this._context, {
                containerId: containerId
            });
        }, SumoLogicClient.prototype.getContext = function() {
            return this._context;
        }, SumoLogicClient.prototype.send = function(e) {
            var payload = log_1.createEventPayload(e, {
                appName: this._appName,
                appVersion: this._appVersion,
                env: this._env,
                context: this.getContext()
            });
            return this._fetch(this._baseUrl, {
                mode: "no-cors",
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                cache: "no-cache",
                body: JSON.stringify(payload)
            });
        }, SumoLogicClient;
    }();
    exports.SumoLogicClient = SumoLogicClient;
}, , , function(module, exports) {
    module.exports = function(array, predicate, fromIndex, fromRight) {
        for (var length = array.length, index = fromIndex + (fromRight ? 1 : -1); fromRight ? index-- : ++index < length; ) if (predicate(array[index], index, array)) return index;
        return -1;
    };
}, , , , , , , , , , , , , , , , , , , function(module, exports, __webpack_require__) {
    var baseFlatten = __webpack_require__(202);
    module.exports = function(array) {
        return null != array && array.length ? baseFlatten(array, 1) : [];
    };
}, function(module, exports, __webpack_require__) {
    var Stack = __webpack_require__(57), arrayEach = __webpack_require__(92), assignValue = __webpack_require__(178), baseAssign = __webpack_require__(401), baseAssignIn = __webpack_require__(402), cloneBuffer = __webpack_require__(173), copyArray = __webpack_require__(175), copySymbols = __webpack_require__(403), copySymbolsIn = __webpack_require__(404), getAllKeys = __webpack_require__(167), getAllKeysIn = __webpack_require__(359), getTag = __webpack_require__(58), initCloneArray = __webpack_require__(405), initCloneByTag = __webpack_require__(406), initCloneObject = __webpack_require__(176), isArray = __webpack_require__(8), isBuffer = __webpack_require__(35), isMap = __webpack_require__(410), isObject = __webpack_require__(9), isSet = __webpack_require__(412), keys = __webpack_require__(32), CLONE_DEEP_FLAG = 1, CLONE_FLAT_FLAG = 2, CLONE_SYMBOLS_FLAG = 4, argsTag = "[object Arguments]", funcTag = "[object Function]", genTag = "[object GeneratorFunction]", objectTag = "[object Object]", cloneableTags = {};
    cloneableTags[argsTag] = cloneableTags["[object Array]"] = cloneableTags["[object ArrayBuffer]"] = cloneableTags["[object DataView]"] = cloneableTags["[object Boolean]"] = cloneableTags["[object Date]"] = cloneableTags["[object Float32Array]"] = cloneableTags["[object Float64Array]"] = cloneableTags["[object Int8Array]"] = cloneableTags["[object Int16Array]"] = cloneableTags["[object Int32Array]"] = cloneableTags["[object Map]"] = cloneableTags["[object Number]"] = cloneableTags[objectTag] = cloneableTags["[object RegExp]"] = cloneableTags["[object Set]"] = cloneableTags["[object String]"] = cloneableTags["[object Symbol]"] = cloneableTags["[object Uint8Array]"] = cloneableTags["[object Uint8ClampedArray]"] = cloneableTags["[object Uint16Array]"] = cloneableTags["[object Uint32Array]"] = !0, 
    cloneableTags["[object Error]"] = cloneableTags[funcTag] = cloneableTags["[object WeakMap]"] = !1, 
    module.exports = function baseClone(value, bitmask, customizer, key, object, stack) {
        var result, isDeep = bitmask & CLONE_DEEP_FLAG, isFlat = bitmask & CLONE_FLAT_FLAG, isFull = bitmask & CLONE_SYMBOLS_FLAG;
        if (customizer && (result = object ? customizer(value, key, object, stack) : customizer(value)), 
        void 0 !== result) return result;
        if (!isObject(value)) return value;
        var isArr = isArray(value);
        if (isArr) {
            if (result = initCloneArray(value), !isDeep) return copyArray(value, result);
        } else {
            var tag = getTag(value), isFunc = tag == funcTag || tag == genTag;
            if (isBuffer(value)) return cloneBuffer(value, isDeep);
            if (tag == objectTag || tag == argsTag || isFunc && !object) {
                if (result = isFlat || isFunc ? {} : initCloneObject(value), !isDeep) return isFlat ? copySymbolsIn(value, baseAssignIn(result, value)) : copySymbols(value, baseAssign(result, value));
            } else {
                if (!cloneableTags[tag]) return object ? value : {};
                result = initCloneByTag(value, tag, isDeep);
            }
        }
        stack || (stack = new Stack());
        var stacked = stack.get(value);
        if (stacked) return stacked;
        if (stack.set(value, result), isSet(value)) return value.forEach(function(subValue) {
            result.add(baseClone(subValue, bitmask, customizer, subValue, value, stack));
        }), result;
        if (isMap(value)) return value.forEach(function(subValue, key) {
            result.set(key, baseClone(subValue, bitmask, customizer, key, value, stack));
        }), result;
        var keysFunc = isFull ? isFlat ? getAllKeysIn : getAllKeys : isFlat ? keysIn : keys, props = isArr ? void 0 : keysFunc(value);
        return arrayEach(props || value, function(subValue, key) {
            props && (subValue = value[key = subValue]), assignValue(result, key, baseClone(subValue, bitmask, customizer, key, value, stack));
        }), result;
    };
}, function(module, exports, __webpack_require__) {
    var baseGetAllKeys = __webpack_require__(168), getSymbolsIn = __webpack_require__(333), keysIn = __webpack_require__(43);
    module.exports = function(object) {
        return baseGetAllKeys(object, keysIn, getSymbolsIn);
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var config_1 = __webpack_require__(11), log = __webpack_require__(1).Logger.create("Cookies"), CookiesHelper = function() {
        return function(_api) {
            var _this = this;
            this._api = _api, this._rootPath = "/", this._grammarlyUrl = "https://" + config_1.GRAMMARLY_DOMAIN + this._rootPath, 
            this._grauthCookieName = "grauth", this._csrfTokenCookieName = "csrf-token", this._grInstallSourceCookieName = "grInstallSource", 
            this._grChromeStoreInstallUtmName = "grChromeStoreInstallUTM", this.getToken = function() {
                return _this._api.cookies.get({
                    name: _this._grauthCookieName,
                    url: _this._grammarlyUrl
                }).then(function(x) {
                    return x ? x.value : null;
                });
            }, this.getCSRFToken = function() {
                return __awaiter(_this, void 0, void 0, function() {
                    var cookie, error_1;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return _a.trys.push([ 0, 2, , 3 ]), [ 4, this._api.cookies.get({
                                name: this._csrfTokenCookieName,
                                url: this._grammarlyUrl
                            }) ];

                          case 1:
                            return [ 2, (cookie = _a.sent()) ? cookie.value : null ];

                          case 2:
                            return error_1 = _a.sent(), log.warn("failed to get a CSRFToken cookie", error_1), 
                            [ 2, null ];

                          case 3:
                            return [ 2 ];
                        }
                    });
                });
            }, this.watchToken = function(cb) {
                return _this._api.cookies.watch({
                    domain: config_1.GRAMMARLY_DOMAIN,
                    name: _this._grauthCookieName,
                    url: _this._grammarlyUrl,
                    path: _this._rootPath
                }, cb);
            }, this.getInstallSource = function() {
                return _this._api.cookies.get({
                    name: _this._grInstallSourceCookieName,
                    url: _this._grammarlyUrl
                });
            }, this.getChromeStoreInstallUTM = function() {
                return _this._api.cookies.get({
                    name: _this._grChromeStoreInstallUtmName,
                    url: _this._grammarlyUrl
                });
            }, this.getAllGrammarlyCookies = function() {
                return _this._api.cookies.getAll({
                    domain: config_1.GRAMMARLY_DOMAIN,
                    path: _this._rootPath
                });
            };
        };
    }();
    exports.CookiesHelper = CookiesHelper;
}, , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.MessageTypes = {
        server: "socket-server",
        client: "socket-client",
        serverIframe: "socket-server-iframe",
        iframeMode: "iframe-mode"
    };
}, function(module, exports, __webpack_require__) {
    var baseIndexOf = __webpack_require__(431);
    module.exports = function(array, value) {
        return !(null == array || !array.length) && baseIndexOf(array, value, 0) > -1;
    };
}, function(module, exports) {
    module.exports = function(array, value, comparator) {
        for (var index = -1, length = null == array ? 0 : array.length; ++index < length; ) if (comparator(value, array[index])) return !0;
        return !1;
    };
}, , , , , , function(module, exports, __webpack_require__) {
    try {
        module.exports = __webpack_require__(442);
    } catch (e) {}
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var emitter = __webpack_require__(18), Emitter = function() {
        return function(obj) {
            void 0 === obj && (obj = {});
            var _this = this;
            this.on = function(event, callback) {
                return _this._internalEmitter.on(event, callback);
            }, this.one = function(event, callback) {
                return _this._internalEmitter.one(event, callback);
            }, this.off = function(event, callback) {
                return _this._internalEmitter.off(event, callback);
            }, this.emit = function(event, data) {
                return _this._internalEmitter.emit(event, data);
            }, this.delegate = function(obj, event, delegateEvent) {
                return _this._internalEmitter.delegate(obj, event, delegateEvent);
            }, this._internalEmitter = emitter(obj);
        };
    }();
    exports.Emitter = Emitter;
}, , , , , , , , , , , , , , , , , , , , , , , , , , , function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), isArguments = __webpack_require__(45), isArray = __webpack_require__(8), spreadableSymbol = Symbol ? Symbol.isConcatSpreadable : void 0;
    module.exports = function(value) {
        return isArray(value) || isArguments(value) || !!(spreadableSymbol && value && value[spreadableSymbol]);
    };
}, , function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), keys = __webpack_require__(32);
    module.exports = function(object, source) {
        return object && copyObject(source, keys(source), object);
    };
}, function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), keysIn = __webpack_require__(43);
    module.exports = function(object, source) {
        return object && copyObject(source, keysIn(source), object);
    };
}, function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), getSymbols = __webpack_require__(107);
    module.exports = function(source, object) {
        return copyObject(source, getSymbols(source), object);
    };
}, function(module, exports, __webpack_require__) {
    var copyObject = __webpack_require__(37), getSymbolsIn = __webpack_require__(333);
    module.exports = function(source, object) {
        return copyObject(source, getSymbolsIn(source), object);
    };
}, function(module, exports) {
    var hasOwnProperty = Object.prototype.hasOwnProperty;
    module.exports = function(array) {
        var length = array.length, result = new array.constructor(length);
        return length && "string" == typeof array[0] && hasOwnProperty.call(array, "index") && (result.index = array.index, 
        result.input = array.input), result;
    };
}, function(module, exports, __webpack_require__) {
    var cloneArrayBuffer = __webpack_require__(110), cloneDataView = __webpack_require__(407), cloneRegExp = __webpack_require__(408), cloneSymbol = __webpack_require__(409), cloneTypedArray = __webpack_require__(174), boolTag = "[object Boolean]", dateTag = "[object Date]", mapTag = "[object Map]", numberTag = "[object Number]", regexpTag = "[object RegExp]", setTag = "[object Set]", stringTag = "[object String]", symbolTag = "[object Symbol]", arrayBufferTag = "[object ArrayBuffer]", dataViewTag = "[object DataView]", float32Tag = "[object Float32Array]", float64Tag = "[object Float64Array]", int8Tag = "[object Int8Array]", int16Tag = "[object Int16Array]", int32Tag = "[object Int32Array]", uint8Tag = "[object Uint8Array]", uint8ClampedTag = "[object Uint8ClampedArray]", uint16Tag = "[object Uint16Array]", uint32Tag = "[object Uint32Array]";
    module.exports = function(object, tag, isDeep) {
        var Ctor = object.constructor;
        switch (tag) {
          case arrayBufferTag:
            return cloneArrayBuffer(object);

          case boolTag:
          case dateTag:
            return new Ctor(+object);

          case dataViewTag:
            return cloneDataView(object, isDeep);

          case float32Tag:
          case float64Tag:
          case int8Tag:
          case int16Tag:
          case int32Tag:
          case uint8Tag:
          case uint8ClampedTag:
          case uint16Tag:
          case uint32Tag:
            return cloneTypedArray(object, isDeep);

          case mapTag:
            return new Ctor();

          case numberTag:
          case stringTag:
            return new Ctor(object);

          case regexpTag:
            return cloneRegExp(object);

          case setTag:
            return new Ctor();

          case symbolTag:
            return cloneSymbol(object);
        }
    };
}, function(module, exports, __webpack_require__) {
    var cloneArrayBuffer = __webpack_require__(110);
    module.exports = function(dataView, isDeep) {
        var buffer = isDeep ? cloneArrayBuffer(dataView.buffer) : dataView.buffer;
        return new dataView.constructor(buffer, dataView.byteOffset, dataView.byteLength);
    };
}, function(module, exports) {
    var reFlags = /\w*$/;
    module.exports = function(regexp) {
        var result = new regexp.constructor(regexp.source, reFlags.exec(regexp));
        return result.lastIndex = regexp.lastIndex, result;
    };
}, function(module, exports, __webpack_require__) {
    var Symbol = __webpack_require__(33), symbolProto = Symbol ? Symbol.prototype : void 0, symbolValueOf = symbolProto ? symbolProto.valueOf : void 0;
    module.exports = function(symbol) {
        return symbolValueOf ? Object(symbolValueOf.call(symbol)) : {};
    };
}, function(module, exports, __webpack_require__) {
    var baseIsMap = __webpack_require__(411), baseUnary = __webpack_require__(79), nodeUtil = __webpack_require__(105), nodeIsMap = nodeUtil && nodeUtil.isMap, isMap = nodeIsMap ? baseUnary(nodeIsMap) : baseIsMap;
    module.exports = isMap;
}, function(module, exports, __webpack_require__) {
    var getTag = __webpack_require__(58), isObjectLike = __webpack_require__(17), mapTag = "[object Map]";
    module.exports = function(value) {
        return isObjectLike(value) && getTag(value) == mapTag;
    };
}, function(module, exports, __webpack_require__) {
    var baseIsSet = __webpack_require__(413), baseUnary = __webpack_require__(79), nodeUtil = __webpack_require__(105), nodeIsSet = nodeUtil && nodeUtil.isSet, isSet = nodeIsSet ? baseUnary(nodeIsSet) : baseIsSet;
    module.exports = isSet;
}, function(module, exports, __webpack_require__) {
    var getTag = __webpack_require__(58), isObjectLike = __webpack_require__(17), setTag = "[object Set]";
    module.exports = function(value) {
        return isObjectLike(value) && getTag(value) == setTag;
    };
}, , , , , , , , , , , , function(module, exports, __webpack_require__) {
    "use strict";
    function encode(value) {
        try {
            return encodeURIComponent(value);
        } catch (e) {
            return null;
        }
    }
    function decode(value) {
        try {
            return decodeURIComponent(value);
        } catch (e) {
            return null;
        }
    }
    module.exports = function(name, value, options) {
        if (arguments.length < 2) return function(name) {
            var cookies = function(str) {
                var obj = {}, pairs = str.split(/ *; */);
                if (!pairs[0]) return obj;
                var _iteratorNormalCompletion = !0, _didIteratorError = !1, _iteratorError = void 0;
                try {
                    for (var _step, _iterator = pairs[Symbol.iterator](); !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = !0) {
                        var pair = _step.value;
                        pair = pair.split("="), obj[decode(pair[0])] = decode(pair[1]);
                    }
                } catch (err) {
                    _didIteratorError = !0, _iteratorError = err;
                } finally {
                    try {
                        !_iteratorNormalCompletion && _iterator.return && _iterator.return();
                    } finally {
                        if (_didIteratorError) throw _iteratorError;
                    }
                }
                return obj;
            }(document.cookie);
            return name ? cookies[name] : cookies;
        }(name);
        !function(name, value) {
            var options = void 0 === arguments[2] ? {} : arguments[2], str = encode(name) + "=" + encode(value);
            null == value && (options.maxage = -1);
            options.maxage && (options.expires = new Date(+new Date() + options.maxage));
            options.path && (str += "; path=" + options.path);
            options.domain && (str += "; domain=" + options.domain);
            options.expires && (str += "; expires=" + options.expires.toUTCString());
            options.secure && (str += "; secure");
            document.cookie = str;
        }(name, value, options);
    };
}, , , , , , function(module, exports, __webpack_require__) {
    var baseFindIndex = __webpack_require__(338), baseIsNaN = __webpack_require__(432), strictIndexOf = __webpack_require__(433);
    module.exports = function(array, value, fromIndex) {
        return value == value ? strictIndexOf(array, value, fromIndex) : baseFindIndex(array, baseIsNaN, fromIndex);
    };
}, function(module, exports) {
    module.exports = function(value) {
        return value != value;
    };
}, function(module, exports) {
    module.exports = function(array, value, fromIndex) {
        for (var index = fromIndex - 1, length = array.length; ++index < length; ) if (array[index] === value) return index;
        return -1;
    };
}, , , , , , , , , function(module, exports, __webpack_require__) {
    var emitter = __webpack_require__(18);
    "function" != typeof Object.assign && (Object.assign = function(target) {
        "use strict";
        if (null == target) throw new TypeError("Cannot convert undefined or null to object");
        for (var output = Object(target), index = 1; index < arguments.length; index++) {
            var source = arguments[index];
            if (null != source) for (var nextKey in source) source.hasOwnProperty(nextKey) && (output[nextKey] = source[nextKey]);
        }
        return output;
    });
    try {
        module.exports = function(options) {
            var socket, reconnectTimer, idleTimer, emiterQueueId, playTimerId, reconnectInProgress, DEBUG = !options.silentLogs, WebSocketClass = window.WebSocket || window.MozWebSocket, standByStatus = !1, activityTimer = null, connected = !1, closedByMe = !1, closeWhenConnected = !1, reconnectTime = 1e3, initialReconnectTime = 1e3, maxReconnectTime = 6e4, messageQueue = [], emiterQueue = [], isPaused = !1;
            options = Object.assign({}, {
                url: null,
                connectionTimeout: 1e3,
                idleTimeout: 3e5,
                useQueue: !1,
                useStandBy: !1,
                playDelay: 50,
                resetQueueOnReconnect: !1
            }, options);
            var ws = emitter({
                connect: connect,
                reconnect: function() {
                    reconnectInProgress || (reconnectInProgress = !0, ws.isConnected() ? (ws.one("disconnect", function() {
                        setTimeout(ws.connect.bind(null, !0), 0);
                    }), closedByMe = !0, ws.close()) : ws.connect(!0));
                },
                send: function(message) {
                    if (standByStatus) !function(message) {
                        if (hasPingPong(message)) return !1;
                        standByStatus && (standByStatus = !1, connect(!0));
                    }(message); else {
                        var strMessage = JSON.stringify(message);
                        messageQueue.push(strMessage), dequeue();
                    }
                },
                close: function() {
                    if (closedByMe = !0, log("explicit close requested"), !connected) return closeWhenConnected = !0;
                    try {
                        socket && socket.close(), reconnectTimer && (clearTimeout(reconnectTimer), reconnectTimer = null);
                    } catch (e) {
                        logError("socket closing bug", e.stack || e);
                    }
                    connected = !1, activityTimer && clearTimeout(activityTimer);
                },
                isConnected: function() {
                    return connected;
                },
                release: function() {
                    clearTimeout(reconnectTimer);
                },
                toString: function() {
                    return "[object WebSocket]";
                },
                wsPlay: function() {
                    clearTimeout(playTimerId), playTimerId = setTimeout(function() {
                        isPaused = !1, emiterWorker();
                    }, options.playDelay);
                },
                wsPause: function() {
                    clearTimeout(playTimerId), isPaused = !0;
                }
            });
            return ws;
            function connect(isReconnect) {
                ws.isConnected() || (log("connect to url: " + options.url), socket = new WebSocketClass(options.url), 
                closedByMe = !1, connected = !1, socket.onopen = function() {
                    reconnectTime = initialReconnectTime, connected = !0, closeWhenConnected && (closeWhenConnected = !1, 
                    ws.close()), isReconnect && options.resetQueueOnReconnect ? messageQueue = [] : dequeue(), 
                    ws.emit("connect"), isReconnect && (ws.emit("reconnect"), reconnectInProgress = !1);
                }, socket.onmessage = function(msg) {
                    DEBUG && console.log("%c Received: %s", "color: #46af91;", msg.data), activity(msg.data), 
                    function(msg) {
                        try {
                            msg = JSON.parse(msg);
                        } catch (e) {
                            logError(e.stack || e, msg);
                        }
                        options.useQueue ? (emiterQueue.push(msg), emiterWorker()) : ws.emit("message", msg);
                    }(msg.data);
                }, socket.onclose = function(reason) {
                    connected = !1, ws.emit("disconnect", reason), closedByMe || handleError("disconnected");
                }, socket.onerror = handleError, window.app && app.one("offline", function() {
                    connected && (ws.close(), app.one("online", function() {
                        ws.connect();
                    }));
                }));
            }
            function activity(msg) {
                options.useStandBy && msg && !hasPingPong(msg) && (clearTimeout(activityTimer), 
                activityTimer = setTimeout(function() {
                    ws.close(), standByStatus = !0, activityTimer = !1;
                }, options.useStandBy));
            }
            function hasPingPong(msg) {
                if (msg && "ping" == msg) return !0;
                var message, result = !1;
                try {
                    message = JSON.parse(msg);
                } catch (e) {}
                return message && ("ping" == message || message.action && "pong" == message.action) && (result = !0), 
                result;
            }
            function dequeue() {
                if (socket) for (;socket.readyState == WebSocketClass.OPEN && messageQueue.length; ) message = messageQueue.shift(), 
                DEBUG && console.log("%c Sending %s", "color:rgba(10, 10, 10, 0.6); font-size: 10px", message), 
                activity(message), socket.send(message), idleTimer && clearTimeout(idleTimer), idleTimer = setTimeout(ping, options.idleTimeout);
                var message;
            }
            function ping() {
                idleTimer = null, ws.send("ping");
            }
            function handleError(data) {
                logError("websocket error", data), ws.emit("error", data), data && data.target && [ WebSocketClass.CLOSING, WebSocketClass.CLOSED ].indexOf(data.target.readyState) > -1 || reconnectTimer || (connected && ws.close(), 
                log("try to reconnect in " + reconnectTime / 1e3 + "s"), reconnectTimer = setTimeout(function() {
                    reconnectTime = Math.min(maxReconnectTime, 1.5 * reconnectTime), reconnectTimer = null, 
                    connect(!0);
                }, reconnectTime));
            }
            function log() {
                DEBUG && console.log.apply(console, arguments);
            }
            function logError() {
                console.error.apply(console, arguments);
            }
            function emiterWorker() {
                emiterQueueId || isPaused || (emiterQueueId = 0 !== emiterQueue.length ? setTimeout(function() {
                    isPaused || ws.emit("message", emiterQueue.shift()), emiterQueueId = null, emiterWorker();
                }, options.useQueue) : null);
            }
        };
    } catch (e) {}
}, function(module, exports, __webpack_require__) {
    var castPath = __webpack_require__(83), last = __webpack_require__(444), parent = __webpack_require__(445), toKey = __webpack_require__(42);
    module.exports = function(object, path) {
        return path = castPath(path, object), null == (object = parent(object, path)) || delete object[toKey(last(path))];
    };
}, function(module, exports) {
    module.exports = function(array) {
        var length = null == array ? 0 : array.length;
        return length ? array[length - 1] : void 0;
    };
}, function(module, exports, __webpack_require__) {
    var baseGet = __webpack_require__(93), baseSlice = __webpack_require__(446);
    module.exports = function(object, path) {
        return path.length < 2 ? object : baseGet(object, baseSlice(path, 0, -1));
    };
}, function(module, exports) {
    module.exports = function(array, start, end) {
        var index = -1, length = array.length;
        start < 0 && (start = -start > length ? 0 : length + start), (end = end > length ? length : end) < 0 && (end += length), 
        length = start > end ? 0 : end - start >>> 0, start >>>= 0;
        for (var result = Array(length); ++index < length; ) result[index] = array[index + start];
        return result;
    };
}, , , , , , , , , , , , , , function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    }, _this = this;
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Config = __webpack_require__(10), pageCookie = __webpack_require__(425), location_1 = __webpack_require__(16), tracker_1 = __webpack_require__(187), logger_1 = __webpack_require__(188), gnarclientweb_1 = __webpack_require__(1140), telemetry_ts_1 = __webpack_require__(1144), stdlib_1 = __webpack_require__(3);
    exports.init = function(GnarSpec) {
        return __awaiter(this, void 0, void 0, function() {
            var client;
            return __generator(this, function(_a) {
                try {
                    return client = function(cfg) {
                        var fetchFn = window.fetch.bind(window);
                        __webpack_require__(1148);
                        var logger = telemetry_ts_1.LoggingImpl.DefaultLogAppender.createRootLogger("gnar", telemetry_ts_1.Logging.LogLevel.INFO, new telemetry_ts_1.LoggingImpl.GetFelogClient(cfg.appConfig.url.newFelog, cfg.appConfig.felog.appName, cfg.buildInfo.version, cfg.bundleInfo.env, fetchFn)), metrics = telemetry_ts_1.TimeSeriesImpl.MetricsStorage.createRoot("gnar", cfg.appConfig.url.newFelog, fetchFn), browser = cfg.bundleInfo.browser, gnarConfig = cfg.appConfig.gnar, cookieStorage = "chrome" === browser ? new gnarclientweb_1.ChromeCookieStorage(gnarConfig.url, gnarConfig.domain) : "firefox" === browser ? new gnarclientweb_1.WebExtensionsCookieStorage(gnarConfig.url, gnarConfig.domain) : "edge" === browser || "safari" === browser ? new gnarclientweb_1.BackendStorage(fetchFn, gnarConfig.url) : stdlib_1.assertNever(browser), cidManager = new gnarclientweb_1.ContainerIdManager(cookieStorage, [ new gnarclientweb_1.CookieStorage(gnarConfig.domain), new gnarclientweb_1.LocalStorage(), new gnarclientweb_1.MemoryStorage() ], logger.getLogger("containerId"), metrics.getCounter("containerId"), "chrome" === browser ? 1e3 : 5e3);
                        return {
                            ga: new gnarclientweb_1.GoogleAnalyticsClient(gnarConfig.googleAnalyticsId, new gnarclientweb_1.GAClientIdManager(cookieStorage, [ new gnarclientweb_1.CookieStorage(gnarConfig.domain), new gnarclientweb_1.LocalStorage(), new gnarclientweb_1.MemoryStorage() ], logger.getLogger("gaClientId"), metrics.getCounter("gaClientId"), "chrome" === browser ? 1e3 : 5e3), !1),
                            gnar: new gnarclientweb_1.GnarClientImpl(gnarConfig.url, gnarConfig.appName, cfg.buildInfo.version, fetchFn, cidManager, logger, metrics, !0)
                        };
                    }(Config.getGlobal()), tracker_1.tracker.gnar = client.gnar, tracker_1.tracker.ga = client.ga, 
                    [ 2, new GnarSpec(client.gnar) ];
                } catch (error) {
                    return logger_1.felog.gnarClientInitFail(error && error.message), [ 2, void 0 ];
                }
                return [ 2 ];
            });
        });
    }, exports.processCookiesFromGrammarly = function(_a) {
        var dapi = _a.dapi, cookieOptions = {
            path: "/",
            domain: location_1.getDomain(),
            expires: new Date(new Date().setFullYear(new Date().getFullYear() + 1))
        };
        name = "__fngrprnt__", value = dapi, value && name && (pageCookie(name, null), pageCookie(name, value, cookieOptions));
        var name, value;
    }, exports.getContainerIdOrUndefined = function() {
        return __awaiter(_this, void 0, void 0, function() {
            var _a;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return _b.trys.push([ 0, 4, , 5 ]), tracker_1.tracker.gnar ? [ 4, tracker_1.tracker.gnar.getContainerId() ] : [ 3, 2 ];

                  case 1:
                    return _a = _b.sent(), [ 3, 3 ];

                  case 2:
                    _a = void 0, _b.label = 3;

                  case 3:
                    return [ 2, _a ];

                  case 4:
                    return _b.sent(), [ 2, void 0 ];

                  case 5:
                    return [ 2 ];
                }
            });
        });
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var _localforage, log = __webpack_require__(1).Logger.create("lib.page-config.localforage");
    try {
        (_localforage = __webpack_require__(1151)).config({
            name: "Grammarly",
            version: 1,
            size: 4194304,
            storeName: "configuration"
        });
    } catch (e) {
        log.error("Fallback to memory storage", e);
        var storage_1 = {};
        _localforage = {
            getItem: function(key) {
                return Promise.resolve(storage_1[key]);
            },
            setItem: function(key, value) {
                return storage_1[key] = value, Promise.resolve(value);
            },
            clear: function() {
                storage_1 = {}, Promise.resolve(!0);
            }
        };
    }
    exports.localforage = _localforage;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    }, __spread = this && this.__spread || function() {
        for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
        return ar;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var timers_1 = __webpack_require__(102), tracking_1 = __webpack_require__(7), log = __webpack_require__(1).Logger.create("lib.profiler"), Profiler = function() {
        function Profiler() {
            var _this = this;
            this.timings = {}, this.track = function(cb) {
                for (var args = [], _i = 1; _i < arguments.length; _i++) args[_i - 1] = arguments[_i];
                return __awaiter(_this, void 0, void 0, function() {
                    return __generator(this, function(_a) {
                        return [ 2, this._track.apply(this, __spread([ !1, cb ], args)) ];
                    });
                });
            }, this.trackAsync = function(cb) {
                for (var args = [], _i = 1; _i < arguments.length; _i++) args[_i - 1] = arguments[_i];
                return __awaiter(_this, void 0, void 0, function() {
                    return __generator(this, function(_a) {
                        return [ 2, this._track.apply(this, __spread([ !0, cb ], args)) ];
                    });
                });
            }, this._track = function(async, cb) {
                for (var args = [], _i = 2; _i < arguments.length; _i++) args[_i - 2] = arguments[_i];
                return __awaiter(_this, void 0, void 0, function() {
                    var name;
                    return __generator(this, function(_b) {
                        switch (_b.label) {
                          case 0:
                            name = cb.name + (async ? "__sync" : ""), timers_1.timers.start(name), _b.label = 1;

                          case 1:
                            return _b.trys.push([ 1, 5, 6, 7 ]), async ? [ 4, cb.apply(void 0, __spread(args)) ] : [ 3, 3 ];

                          case 2:
                            return _b.sent(), [ 3, 4 ];

                          case 3:
                            cb.apply(void 0, __spread(args)), _b.label = 4;

                          case 4:
                            return [ 3, 7 ];

                          case 5:
                            throw _b.sent();

                          case 6:
                            return this.timings[name] = timers_1.timers.stop(name), [ 7 ];

                          case 7:
                            return [ 2 ];
                        }
                    });
                });
            };
        }
        return Profiler.start = function(name) {
            timers_1.timers.start(name);
        }, Profiler.stop = function(name, max) {
            void 0 === max && (max = 3e4);
            var time = timers_1.timers.stop(name);
            return time > max && (log.warn("profiler_" + name + "_time_exceeded " + time), "pageConfig_init" === name && tracking_1.felog.tooLongPageConfigInit(time), 
            "updateUser" === name && tracking_1.felog.tooLongUserUpdateTime(time)), time;
        }, Profiler.prototype.start = function(name) {
            timers_1.timers.start(name);
        }, Profiler.prototype.stop = function(name) {
            this.timings[name] = timers_1.timers.stop(name);
        }, Profiler;
    }();
    exports.Profiler = Profiler;
}, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    exports.alphanumeric = function alphanumeric(num, res) {
        if (void 0 === res && (res = ""), num <= 0) return res;
        var random = Math.floor(Math.random() * (allowed.length - 1));
        return alphanumeric(num - 1, res + allowed.charAt(random));
    }, exports.getNextPingDate = function() {
        var now = new Date();
        return now.getHours() > 2 && now.setDate(now.getDate() + 1), now.setHours(3), now.setMinutes(Math.floor(60 * Math.random())), 
        now.getTime();
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), function(LogLevel) {
        LogLevel[LogLevel.TRACE = 0] = "TRACE", LogLevel[LogLevel.DEBUG = 1] = "DEBUG", 
        LogLevel[LogLevel.INFO = 2] = "INFO", LogLevel[LogLevel.WARN = 3] = "WARN", LogLevel[LogLevel.ERROR = 4] = "ERROR", 
        LogLevel[LogLevel.FATAL = 5] = "FATAL", LogLevel[LogLevel.OFF = 6] = "OFF";
    }(exports.LogLevel || (exports.LogLevel = {})), function(LogLevel) {
        LogLevel.fromString = function(levelString) {
            switch (levelString) {
              case "TRACE":
                return LogLevel.TRACE;

              case "DEBUG":
                return LogLevel.DEBUG;

              case "INFO":
                return LogLevel.INFO;

              case "WARN":
                return LogLevel.WARN;

              case "ERROR":
                return LogLevel.ERROR;

              case "FATAL":
                return LogLevel.FATAL;

              case "OFF":
                return LogLevel.OFF;

              default:
                throw new TypeError("Unrecognized log level string '" + levelString + "'");
            }
        };
    }(exports.LogLevel || (exports.LogLevel = {}));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var RingBuffer = function() {
        function RingBuffer(capacity, allowOverflow) {
            if (void 0 === allowOverflow && (allowOverflow = !1), this.capacity = capacity, 
            this.allowOverflow = allowOverflow, this._start = 0, this._end = 0, this._isFull = !1, 
            this.toJSON = this.toArray, capacity <= 0) throw new Error("Invalid capacity " + capacity);
            this._buffer = new Array(capacity);
        }
        return Object.defineProperty(RingBuffer.prototype, "size", {
            get: function() {
                return this._isFull ? this._buffer.length : (this._end - this._start + this._buffer.length) % this._buffer.length;
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(RingBuffer.prototype, "isEmpty", {
            get: function() {
                return 0 === this.size;
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(RingBuffer.prototype, "isFull", {
            get: function() {
                return this._isFull;
            },
            enumerable: !0,
            configurable: !0
        }), RingBuffer.prototype.push = function(element) {
            if (this.isFull) {
                if (!this.allowOverflow) throw new Error("Buffer is full");
                ++this._start, this._start === this.capacity && (this._start = 0);
            }
            this._buffer[this._end++] = element, this._end === this.capacity && (this._end = 0), 
            this._start === this._end && (this._isFull = !0);
        }, RingBuffer.prototype.pop = function() {
            if (!this.isEmpty) {
                var t = this._buffer[this._start];
                return this._buffer[this._start] = void 0, this._start++, this._start === this.capacity && (this._start = 0), 
                this._isFull = !1, t;
            }
        }, Object.defineProperty(RingBuffer.prototype, "first", {
            get: function() {
                return this.isEmpty ? void 0 : this._buffer[this._start];
            },
            enumerable: !0,
            configurable: !0
        }), Object.defineProperty(RingBuffer.prototype, "last", {
            get: function() {
                return this.isEmpty ? void 0 : this._buffer[0 === this._end ? this.capacity - 1 : this._end - 1];
            },
            enumerable: !0,
            configurable: !0
        }), RingBuffer.prototype.clear = function() {
            this._buffer = new Array(this.capacity), this._start = this._end = 0, this._isFull = !1;
        }, RingBuffer.prototype.toArray = function() {
            var res;
            if (this.isEmpty) res = new Array(0); else if (this._start < this._end) res = this._buffer.slice(this._start, this._end); else {
                res = new Array(this.size);
                for (var j = 0, i = this._start; i < this.capacity; ++i, ++j) res[j] = this._buffer[i];
                for (i = 0; i < this._end; ++i, ++j) res[j] = this._buffer[i];
            }
            return res;
        }, RingBuffer;
    }();
    exports.RingBuffer = RingBuffer;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    }, _this = this;
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var stdlib_1 = __webpack_require__(3), util_1 = __webpack_require__(2);
    exports.isIncognito = function() {
        return __awaiter(_this, void 0, void 0, function() {
            var _a;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return (_a = util_1.isChrome() || util_1.isFF()) ? [ 4, stdlib_1.SafePromise.create(function(res) {
                        chrome && chrome.extension ? chrome.extension.isAllowedIncognitoAccess(res) : res(!1);
                    }) ] : [ 3, 2 ];

                  case 1:
                    _a = _b.sent(), _b.label = 2;

                  case 2:
                    return [ 2, _a ];
                }
            });
        });
    }, exports.getNextPingDate = function() {
        var now = new Date();
        return now.getHours() > 2 && now.setDate(now.getDate() + 1), now.setHours(3), now.setMinutes(Math.floor(60 * Math.random())), 
        now.getTime();
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    }, _this = this;
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var log = __webpack_require__(1).Logger.create("universal.bg.prefs"), pget = function(prop, preferences) {
        return __awaiter(_this, void 0, void 0, function() {
            var value, e_1;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 2, , 3 ]), [ 4, preferences.get(prop) ];

                  case 1:
                    return "undefined" === (value = _a.sent()) ? [ 2, void 0 ] : [ 2, value && JSON.parse(value) ];

                  case 2:
                    throw (e_1 = _a.sent()) && e_1.toString().includes("SyntaxError") ? (preferences.remove(prop), 
                    new Error("'" + prop + "' has unparseable value, removing")) : e_1;

                  case 3:
                    return [ 2 ];
                }
            });
        });
    }, PrefsImpl = function() {
        return function(_api) {
            var _this = this;
            this._api = _api, this.get = function(props) {
                return __awaiter(_this, void 0, void 0, function() {
                    var isArray, result, values_1, e_2, _this = this;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            isArray = Array.isArray(props), _a.label = 1;

                          case 1:
                            return _a.trys.push([ 1, 6, , 7 ]), isArray ? (props = props, [ 4, Promise.all(props.map(function(prop) {
                                return pget(prop, _this._api);
                            })) ]) : [ 3, 3 ];

                          case 2:
                            return values_1 = _a.sent(), result = props.reduce(function(obj, prop, i) {
                                return Object.assign(obj, ((_a = {})[prop] = values_1[i], _a));
                                var _a;
                            }, {}), [ 3, 5 ];

                          case 3:
                            return [ 4, pget(props = props, this._api) ];

                          case 4:
                            result = _a.sent(), _a.label = 5;

                          case 5:
                            return [ 3, 7 ];

                          case 6:
                            return e_2 = _a.sent(), isArray && (result = {}), log.warn("prefs get error:", e_2), 
                            [ 3, 7 ];

                          case 7:
                            return [ 2, result ];
                        }
                    });
                });
            }, this.set = function(name, value) {
                return __awaiter(_this, void 0, void 0, function() {
                    var e_3, _this = this;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return null === name || "object" != typeof name ? [ 3, 2 ] : [ 4, Promise.all(Object.keys(name).map(function(key) {
                                return _this.set(key, name[key]);
                            })) ];

                          case 1:
                            return _a.sent(), [ 3, 5 ];

                          case 2:
                            return _a.trys.push([ 2, 4, , 5 ]), value = void 0 === value ? "undefined" : JSON.stringify(value), 
                            [ 4, this._api.set(name, value) ];

                          case 3:
                            return _a.sent(), [ 3, 5 ];

                          case 4:
                            return e_3 = _a.sent(), log.warn("prefs set error", e_3), [ 3, 5 ];

                          case 5:
                            return [ 2 ];
                        }
                    });
                });
            }, this.all = function() {
                return __awaiter(_this, void 0, void 0, function() {
                    var prefs, key, v;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return [ 4, this._api.getAll() ];

                          case 1:
                            for (key in prefs = _a.sent()) if ("undefined" === prefs[key]) prefs[key] = void 0; else try {
                                v = prefs[key], prefs[key] = v && JSON.parse(v);
                            } catch (e) {}
                            return [ 2, prefs ];
                        }
                    });
                });
            }, this.remove = function(key) {
                try {
                    return _this._api.remove(key);
                } catch (e) {
                    return log.warn("prefs remove error", e), Promise.resolve();
                }
            }, this.clearAll = function() {
                try {
                    return _this._api.removeAll().catch(function(e) {
                        return log.warn("prefs clearAll error", e);
                    });
                } catch (e) {
                    return log.warn("prefs clearAll error", e), Promise.resolve();
                }
            };
        };
    }();
    exports.PrefsImpl = PrefsImpl;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var effects_1 = __webpack_require__(99), redux_saga_1 = __webpack_require__(148), actions_1 = __webpack_require__(98), connectionSelectors = __webpack_require__(670), settingsSelectors = __webpack_require__(671), settingsActions = __webpack_require__(89), actions = __webpack_require__(114), reducer_1 = __webpack_require__(184), selectors = __webpack_require__(1153), helpers_1 = __webpack_require__(1154), util_1 = __webpack_require__(2), profiler_1 = __webpack_require__(462), experiment_1 = __webpack_require__(672), tracking_1 = __webpack_require__(216), log = __webpack_require__(1).Logger.create("universal.bg.state.user.sagas");
    exports.SERIALIZED_USER_INFO_PROP_NAME = "serializedUserInfo";
    var UserSagas = function() {
        function UserSagas(_settingsSagas, _prefs, _telemetry, _cookiesHelper, _getContainerIdOrUndefined, _reconnectAllSockets) {
            this._settingsSagas = _settingsSagas, this._prefs = _prefs, this._telemetry = _telemetry, 
            this._cookiesHelper = _cookiesHelper, this._getContainerIdOrUndefined = _getContainerIdOrUndefined, 
            this._reconnectAllSockets = _reconnectAllSockets;
        }
        return UserSagas.prototype.start = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return util_1.isEdge() ? [ 3, 2 ] : [ 4, [ effects_1.fork([ this, this.listenCookieChanges ]), redux_saga_1.takeLatest(actions.t.SESSION_INVALIDATE, this.updateUser.bind(this)), redux_saga_1.takeLatest(actions.t.UPDATE_GROUPS, this.updateGroups.bind(this)) ] ];

                  case 1:
                    return _a.sent(), [ 3, 4 ];

                  case 2:
                    return [ 4, [ redux_saga_1.takeLatest(actions.t.SESSION_INVALIDATE, this.updateUser.bind(this)), redux_saga_1.takeLatest(actions.t.UPDATE_GROUPS, this.updateGroups.bind(this)) ] ];

                  case 3:
                    _a.sent(), _a.label = 4;

                  case 4:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.updateUser = function(_a) {
            var loginDate, containerId, authData, mimicData, statsData, grauth, user, oldUser, dialectStrong, userLoggedIn, newDialectStrong, dialectWeak, dialect, _c, authDegradation, cookiesDisabled, error_1, cachedUser, _b = void 0 === _a ? {} : _a, lazy = _b.lazy, failoverFromCache = _b.failoverFromCache, reason = _b.reason;
            return __generator(this, function(_d) {
                switch (_d.label) {
                  case 0:
                    return [ 3, 4 ];

                  case 1:
                    return _d.sent() ? [ 4, effects_1.call(this._prefs.get, "user") ] : [ 3, 4 ];

                  case 2:
                    return cachedUser = _d.sent(), [ 4, effects_1.put(actions.setUser(cachedUser)) ];

                  case 3:
                    return _d.sent(), [ 2, log.info("updateUser: SKIP AUTH") ];

                  case 4:
                    profiler_1.Profiler.start("updateUser"), _d.label = 5;

                  case 5:
                    return _d.trys.push([ 5, 41, , 48 ]), lazy ? [ 4, effects_1.call(this._prefs.get, "loginDate") ] : [ 3, 7 ];

                  case 6:
                    if (loginDate = _d.sent(), !helpers_1.isItTimeToRefresh(loginDate)) return log.info("AUTH SERVICE | user session still fresh"), 
                    profiler_1.Profiler.stop("updateUser"), [ 2 ];
                    _d.label = 7;

                  case 7:
                    return [ 4, effects_1.fork([ this, this.trackCookieHeaderSize ]) ];

                  case 8:
                    return _d.sent(), [ 4, effects_1.call(this._getContainerIdOrUndefined) ];

                  case 9:
                    return containerId = _d.sent(), [ 4, effects_1.call(helpers_1.fetchUser, containerId) ];

                  case 10:
                    return authData = _d.sent(), [ 4, effects_1.call([ this, this.getMimic ], containerId) ];

                  case 11:
                    return mimicData = _d.sent(), [ 4, effects_1.call([ this, this.getStats ], containerId) ];

                  case 12:
                    return statsData = _d.sent(), [ 4, effects_1.call([ this, this.getGrauthFromCookie ]) ];

                  case 13:
                    return grauth = _d.sent(), [ 4, effects_1.call(helpers_1.prepareUser, authData, mimicData, statsData, grauth) ];

                  case 14:
                    return user = _d.sent(), [ 4, effects_1.select(selectors.current) ];

                  case 15:
                    return oldUser = _d.sent(), [ 4, effects_1.select(settingsSelectors.getDapiProp, "dialectStrong") ];

                  case 16:
                    return dialectStrong = _d.sent(), userLoggedIn = !1 === user.anonymous && !0 === oldUser.anonymous && void 0 !== oldUser.grauth && void 0 !== oldUser.email, 
                    [ 4, effects_1.put(actions.setUser(user)) ];

                  case 17:
                    return _d.sent(), !0 !== userLoggedIn ? [ 3, 19 ] : [ 4, effects_1.call([ this._settingsSagas, this._settingsSagas.setAnonymousPropsToDapi ]) ];

                  case 18:
                    _d.sent(), _d.label = 19;

                  case 19:
                    return user.id === oldUser.id ? [ 3, 21 ] : [ 4, effects_1.call([ this._settingsSagas, this._settingsSagas.initializeDapiProps ]) ];

                  case 20:
                    return _d.sent(), [ 3, 23 ];

                  case 21:
                    return [ 4, effects_1.call([ this._settingsSagas, this._settingsSagas.resetStrongDialectFromDapi ]) ];

                  case 22:
                    _d.sent(), _d.label = 23;

                  case 23:
                    return [ 4, effects_1.select(settingsSelectors.getDapiProp, "dialectStrong") ];

                  case 24:
                    return newDialectStrong = _d.sent(), !user.settings.dialectStrong || newDialectStrong ? [ 3, 26 ] : [ 4, effects_1.put(settingsActions.setDapiProp("dialectStrong", user.settings.dialectStrong)) ];

                  case 25:
                    _d.sent(), newDialectStrong = user.settings.dialectStrong, _d.label = 26;

                  case 26:
                    return !oldUser.id || user.id === oldUser.id && user.type === oldUser.type && newDialectStrong === dialectStrong ? [ 3, 29 ] : [ 4, effects_1.select(settingsSelectors.getDapiProp, "dialectWeak") ];

                  case 27:
                    return dialectWeak = _d.sent(), dialect = newDialectStrong || dialectStrong || dialectWeak, 
                    [ 4, effects_1.call(this._reconnectAllSockets, dialect) ];

                  case 28:
                    _d.sent(), log.warn("DAPI SERVICE | user changed, reseting capi session witha a dialect: ", dialect), 
                    _d.label = 29;

                  case 29:
                    return [ 4, effects_1.call(this._prefs.set, {
                        user: user,
                        loginDate: new Date()
                    }) ];

                  case 30:
                    return _d.sent(), [ 4, effects_1.select(connectionSelectors.current) ];

                  case 31:
                    return _c = _d.sent(), authDegradation = _c.authDegradation, cookiesDisabled = _c.cookiesDisabled, 
                    [ 4, effects_1.call(tracking_1.fire, "session-invalidate", user, oldUser, reason, cookiesDisabled, containerId) ];

                  case 32:
                    return _d.sent(), authDegradation ? [ 4, effects_1.put(actions_1.updateConnection({
                        authDegradation: !1
                    })) ] : [ 3, 34 ];

                  case 33:
                    _d.sent(), _d.label = 34;

                  case 34:
                    return void 0 === containerId ? [ 3, 36 ] : [ 4, effects_1.call([ this._telemetry, this._telemetry.setContainerId ], containerId) ];

                  case 35:
                    _d.sent(), _d.label = 36;

                  case 36:
                    return user.id === oldUser.id ? [ 3, 38 ] : [ 4, effects_1.call([ this._telemetry, this._telemetry.setUserId ], user.id) ];

                  case 37:
                    _d.sent(), _d.label = 38;

                  case 38:
                    return [ 4, effects_1.fork([ this, this.checkReminderNotification ], user, oldUser) ];

                  case 39:
                    return _d.sent(), [ 4, effects_1.fork([ this, this.storeLoginReminderInfo ], user) ];

                  case 40:
                    return _d.sent(), [ 3, 48 ];

                  case 41:
                    return error_1 = _d.sent(), redux_saga_1.isCancelError(error_1) ? (profiler_1.Profiler.stop("updateUser"), 
                    [ 2 ]) : [ 4, effects_1.call(this._prefs.set, {
                        loginDate: 0
                    }) ];

                  case 42:
                    return _d.sent(), [ 4, effects_1.put(actions_1.updateConnection({
                        authDegradation: !0
                    })) ];

                  case 43:
                    return _d.sent(), [ 4, effects_1.call(this._telemetry.fetchUserFail, reason, error_1.body, error_1.statusCode) ];

                  case 44:
                    return _d.sent(), log.warn("Update user failed. Message: ", error_1), failoverFromCache ? [ 4, effects_1.call(this._prefs.get, "user") ] : [ 3, 47 ];

                  case 45:
                    return cachedUser = _d.sent(), [ 4, effects_1.put(actions.setUser(cachedUser || reducer_1.defaultUser)) ];

                  case 46:
                    _d.sent(), _d.label = 47;

                  case 47:
                    return [ 3, 48 ];

                  case 48:
                    return profiler_1.Profiler.stop("updateUser"), [ 2 ];
                }
            });
        }, UserSagas.prototype.getMimic = function(containerId) {
            var error_2;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 2, , 4 ]), [ 4, effects_1.call(helpers_1.fetchMimic, containerId) ];

                  case 1:
                    return [ 2, _a.sent() ];

                  case 2:
                    return error_2 = _a.sent(), log.warn("DAPI SERVICE | fetch mimic fail. Message: ", error_2.message), 
                    [ 4, effects_1.call(this._telemetry.fetchMimicFail, error_2.body, error_2.statusCode) ];

                  case 3:
                    return _a.sent(), [ 2, {} ];

                  case 4:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.getStats = function(containerId) {
            var error_3;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 2, , 4 ]), [ 4, effects_1.call(helpers_1.fetchStats, containerId) ];

                  case 1:
                    return [ 2, _a.sent() ];

                  case 2:
                    return error_3 = _a.sent(), log.warn("DAPI SERVICE | fetch stats fail. Message: ", error_3.message), 
                    [ 4, effects_1.call(this._telemetry.fetchStatsFail, error_3.body, error_3.statusCode) ];

                  case 3:
                    return _a.sent(), [ 2, {} ];

                  case 4:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.getGrauthFromCookie = function() {
            var error_4;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 2, , 4 ]), [ 4, effects_1.call(this._cookiesHelper.getToken) ];

                  case 1:
                    return [ 2, _a.sent() ];

                  case 2:
                    return error_4 = _a.sent(), log.warn("AUTH SERVICE | fetch cookie fail. Message: ", error_4.message), 
                    [ 4, effects_1.call(this._telemetry.fetchCookieFail) ];

                  case 3:
                    return _a.sent(), [ 2, "bad_cookie" ];

                  case 4:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.trackCookieHeaderSize = function() {
            var cookies, total, _a, name_1, length_1, error_5;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return _b.trys.push([ 0, 4, , 5 ]), [ 4, effects_1.call(this._cookiesHelper.getAllGrammarlyCookies) ];

                  case 1:
                    return cookies = _b.sent(), (total = cookies.reduce(function(total, _a) {
                        return total + _a.value.length;
                    }, 0)) > helpers_1.MAX_COOKIE_HEADER_LENGTH ? (_a = cookies.reduce(function(prev, next) {
                        return prev.value.length > next.value.length ? prev : next;
                    }, {
                        name: "",
                        value: ""
                    }), name_1 = _a.name, length_1 = _a.value.length, [ 4, effects_1.call(tracking_1.fire, "cookie-overflow", total, {
                        name: name_1,
                        length: length_1
                    }) ]) : [ 3, 3 ];

                  case 2:
                    _b.sent(), _b.label = 3;

                  case 3:
                    return [ 3, 5 ];

                  case 4:
                    return error_5 = _b.sent(), log.warn("fetch grammarly cookies fail. Message: ", error_5.message), 
                    [ 3, 5 ];

                  case 5:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.externalUpdateUser = function(_, lazy, reason) {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call([ this, this.updateUser ], {
                        lazy: lazy,
                        reason: reason
                    }) ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, UserSagas.prototype.authRequest = function(_, url, data, placement, type) {
            var response, e_1;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 4, , 6 ]), [ 4, effects_1.call(helpers_1.authRequestHelper, url, data) ];

                  case 1:
                    return response = _a.sent(), [ 4, effects_1.call([ this, this.updateUser ], {
                        reason: type
                    }) ];

                  case 2:
                    return _a.sent(), [ 4, effects_1.call([ tracking_1.gnar, "signin" === type ? tracking_1.gnar.signInFormSuccess : tracking_1.gnar.signUpFormSuccess ], placement) ];

                  case 3:
                    return _a.sent(), [ 2, response ];

                  case 4:
                    return e_1 = _a.sent(), log.warn("auth error", e_1), [ 4, effects_1.call([ tracking_1.gnar, "signin" === type ? tracking_1.gnar.signInFormFail : tracking_1.gnar.signUpFormFail ], placement) ];

                  case 5:
                    return _a.sent(), [ 2, {
                        error: e_1.message || e_1.body
                    } ];

                  case 6:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.listenCookieChanges = function() {
            var channel, task;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(helpers_1.createCookieChannel, this._cookiesHelper.watchToken) ];

                  case 1:
                    channel = _a.sent(), _a.label = 2;

                  case 2:
                    return [ 4, effects_1.call(channel.take) ];

                  case 3:
                    return _a.sent(), task ? [ 4, effects_1.cancel(task) ] : [ 3, 5 ];

                  case 4:
                    _a.sent(), _a.label = 5;

                  case 5:
                    return [ 4, effects_1.fork([ this, this.cookieChange ]) ];

                  case 6:
                    return task = _a.sent(), [ 3, 2 ];

                  case 7:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.updateGroups = function() {
            var containerId, mimicData, experiments;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._getContainerIdOrUndefined) ];

                  case 1:
                    return containerId = _a.sent(), [ 4, effects_1.call([ this, this.getMimic ], containerId) ];

                  case 2:
                    return mimicData = _a.sent(), [ 4, effects_1.call(experiment_1.UserExperiments.create, mimicData.groups) ];

                  case 3:
                    return experiments = _a.sent(), [ 4, effects_1.put(actions.setGroups({
                        mimic: mimicData,
                        experiments: experiments
                    })) ];

                  case 4:
                    return _a.sent(), [ 2 ];
                }
            });
        }, UserSagas.prototype.cookieChange = function() {
            var newGrauth, grauth, error_6;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 6, , 8 ]), [ 4, effects_1.call(util_1.delay, helpers_1.LOGIN_BY_COOKIE_CHANGE_TIMEOUT) ];

                  case 1:
                    return _a.sent(), [ 4, effects_1.call([ this, this.getGrauthFromCookie ]) ];

                  case 2:
                    return newGrauth = _a.sent(), [ 4, effects_1.select(selectors.current) ];

                  case 3:
                    return grauth = _a.sent().grauth, newGrauth === grauth ? [ 3, 5 ] : [ 4, effects_1.put(actions.sessionInvalidate("cookieChange")) ];

                  case 4:
                    _a.sent(), _a.label = 5;

                  case 5:
                    return [ 3, 8 ];

                  case 6:
                    return error_6 = _a.sent(), [ 4, effects_1.call(this._telemetry.frequentCookieChanges, redux_saga_1.isCancelError(error_6)) ];

                  case 7:
                    return _a.sent(), [ 3, 8 ];

                  case 8:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.storeLoginReminderInfo = function(user) {
            var userInfo, userType, isDataStored, serializedUserInfo;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.get, exports.SERIALIZED_USER_INFO_PROP_NAME) ];

                  case 1:
                    return userInfo = _a.sent(), userType = user.type.toLowerCase(), isDataStored = !(!userInfo || userInfo.type !== userType), 
                    !1 !== user.anonymous || !1 !== isDataStored ? [ 3, 3 ] : (serializedUserInfo = {
                        type: userType
                    }, [ 4, effects_1.call(this._prefs.set, {
                        serializedUserInfo: serializedUserInfo
                    }) ]);

                  case 2:
                    _a.sent(), _a.label = 3;

                  case 3:
                    return [ 2 ];
                }
            });
        }, UserSagas.prototype.checkReminderNotification = function(user) {
            var isAnonymous, loginReminderDisabled, showLoginReminder, userInfo, onboardingShowed;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return isAnonymous = !0 === user.anonymous, [ 4, effects_1.select(settingsSelectors.getLoginReminderDisabled) ];

                  case 1:
                    return loginReminderDisabled = _a.sent(), [ 4, effects_1.select(settingsSelectors.getShowLoginReminder) ];

                  case 2:
                    return (showLoginReminder = _a.sent()) && !1 === isAnonymous ? [ 4, effects_1.put(settingsActions.hideLoginReminder()) ] : [ 3, 4 ];

                  case 3:
                    _a.sent(), _a.label = 4;

                  case 4:
                    return !1 === isAnonymous || loginReminderDisabled ? [ 2 ] : [ 4, effects_1.call(this._prefs.get, exports.SERIALIZED_USER_INFO_PROP_NAME) ];

                  case 5:
                    return userInfo = _a.sent(), [ 4, effects_1.select(settingsSelectors.getOnboardingShowed) ];

                  case 6:
                    return onboardingShowed = _a.sent(), !userInfo || !0 !== onboardingShowed || showLoginReminder ? [ 3, 10 ] : [ 4, effects_1.put(settingsActions.showLoginReminder(userInfo.type)) ];

                  case 7:
                    return _a.sent(), [ 4, effects_1.call([ tracking_1.gnar, tracking_1.gnar.loginReminderBadgeShow ]) ];

                  case 8:
                    return _a.sent(), [ 4, effects_1.call(this._telemetry.loginReminderBadgeShow) ];

                  case 9:
                    _a.sent(), _a.label = 10;

                  case 10:
                    return [ 2 ];
                }
            });
        }, UserSagas;
    }();
    exports.UserSagas = UserSagas;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.current = function(state) {
        return state.connection;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.current = function(state) {
        return state.settings;
    }, exports.getUserId = function(state) {
        return state.user.id;
    }, exports.getUserAnonymous = function(state) {
        return state.user.anonymous;
    }, exports.getUserExperiments = function(state) {
        return state.user.experiments;
    }, exports.getDapiProp = function(state, type) {
        return state.settings.common[type];
    }, exports.getLoginReminderType = function(state) {
        return state.settings.common.loginReminderType;
    }, exports.getShowLoginReminder = function(state) {
        return state.settings.common.showLoginReminder;
    }, exports.getLoginReminderDisabled = function(state) {
        return !0 === state.settings.common.loginReminderDisabled;
    }, exports.getOnboardingShowed = function(state) {
        return !1 === state.settings.common.showOnboarding;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var util_1 = __webpack_require__(2);
    !function(UserExperiments) {
        UserExperiments.create = function(groups) {
            return void 0 === groups && (groups = []), {
                googleDocsBeta: util_1.isChrome() && (groups.includes("google_docs_whitelist_enabled") || groups.includes("google_docs_beta_enabled") || groups.includes("google_docs_premium")),
                newExtensionArchitecture: groups.includes("new_extension_architecture"),
                emailSummarization: groups.includes("email_summarization_enabled"),
                connectednessData: !1,
                advancedInlineAlerts: groups.includes("advanced_inline_alerts_enabled"),
                gdprSignupEnabled: groups.includes("gdpr_signup_enabled"),
                fluidEnabled: groups.includes("fluid_slack_dogfood") || groups.includes("fluid_canary1_enabled")
            };
        };
    }(exports.UserExperiments || (exports.UserExperiments = {}));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var defaults_1 = __webpack_require__(109);
    exports.isValid = function(config) {
        if (config && config.pageConfig && Object.keys(config).length && Object.keys(config.pageConfig).length && (!config.protocolVersion || config.protocolVersion === defaults_1.PROTOCOL_VERSION)) return !0;
    }, exports.getInterval = function(ms) {
        return defaults_1.PAGE_CONFIG_UPDATE_INTERVALS.includes(ms) ? ms : defaults_1.PAGE_CONFIG_DEFAULT_INTERVAL;
    };
}, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), __webpack_require__(217), __webpack_require__(1).LogConfig.configure({
        edge: !1,
        prodCs: !1
    }), __webpack_require__(10).initGlobal("chrome", "bg");
    var chrome_1 = __webpack_require__(218), extension_api_1 = __webpack_require__(66);
    __webpack_require__(108).bgPreload(), extension_api_1.initGlobalExtensionApi(chrome_1.createApi());
    var bg_1 = __webpack_require__(1135), chrome_ext_1 = __webpack_require__(1178);
    bg_1.startBgPage(chrome_ext_1.GnarSpec);
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var bg_1 = __webpack_require__(1136);
    exports.startBgPage = bg_1.startBgPage;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), __webpack_require__(1137);
    var Config = __webpack_require__(10);
    "chrome" === Config.getGlobal().bundleInfo.browser && (window.fetch = void 0, __webpack_require__(1138));
    var isBoolean = __webpack_require__(1139), util_1 = __webpack_require__(2), tracking_1 = __webpack_require__(7), tracking_2 = __webpack_require__(216), bgonly_1 = __webpack_require__(460), config_1 = __webpack_require__(11), api_1 = __webpack_require__(1150), extension_api_1 = __webpack_require__(66), notification = __webpack_require__(1155), sagas_1 = __webpack_require__(1156), sagas_2 = __webpack_require__(1160), sagas_3 = __webpack_require__(669), sagas_4 = __webpack_require__(1162), prefs_1 = __webpack_require__(668), web_extensions_1 = __webpack_require__(108), storage_migration_1 = __webpack_require__(195), chrome_1 = __webpack_require__(1165), newConfig_1 = __webpack_require__(25), timers_1 = __webpack_require__(102), message_1 = __webpack_require__(15), profiler_1 = __webpack_require__(462), cookie_1 = __webpack_require__(360), request_1 = __webpack_require__(205), util_2 = __webpack_require__(667), store_1 = __webpack_require__(324), page_config_1 = __webpack_require__(1166), message = __webpack_require__(15), dapi_1 = __webpack_require__(1173), socket_1 = __webpack_require__(1174), url_1 = __webpack_require__(90), logger_1 = __webpack_require__(1), tracking_3 = __webpack_require__(216), log = logger_1.Logger.create("lib.bg.bg"), BG_START_TIMER = "bg_start_timer", profiler = new profiler_1.Profiler(), extensionApi = extension_api_1.getGlobalExtensionApi(), cookiesHelper = new cookie_1.CookiesHelper(extensionApi);
    function runPrefsMigrations() {
        return newConfig_1.isFF() ? (log.trace("Migrating preferences data..."), web_extensions_1.preferencesApi.ensureMigrationCompleted().then(function(r) {
            log.trace("Preferences data migration successful!"), r === storage_migration_1.StorageMigrationResult.success && tracking_1.felog.storageMigrationSucceeded();
        }, function(err) {
            log.error("XXX Preferences migration failed"), tracking_1.felog.storageMigrationFailed(err);
        })) : Promise.resolve();
    }
    function checkUpdate(prefs, pageConfig, seenNews, showOnboarding) {
        return __awaiter(this, void 0, void 0, function() {
            var version, previousVersion, enabledDefs;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return version = config_1.getVersion(), [ 4, prefs.get("version") ];

                  case 1:
                    return previousVersion = _a.sent(), version === previousVersion ? [ 2 ] : [ 4, prefs.set("version", version) ];

                  case 2:
                    return _a.sent(), [ 4, prefs.get("version") ];

                  case 3:
                    return _a.sent() !== version ? [ 2 ] : previousVersion ? [ 3, 6 ] : [ 4, function(prefs, pageConfig, showOnboarding) {
                        return __awaiter(this, void 0, void 0, function() {
                            var source;
                            return __generator(this, function(_a) {
                                switch (_a.label) {
                                  case 0:
                                    chrome_1.loadContentScripts(extensionApi, pageConfig), source = "unknown", _a.label = 1;

                                  case 1:
                                    return _a.trys.push([ 1, 3, , 4 ]), [ 4, function() {
                                        return __awaiter(this, void 0, void 0, function() {
                                            var installSource;
                                            return __generator(this, function(_a) {
                                                switch (_a.label) {
                                                  case 0:
                                                    return util_1.isSafari() || util_1.isEdge() ? [ 2, "webstore" ] : [ 4, cookiesHelper.getInstallSource() ];

                                                  case 1:
                                                    return null === (installSource = _a.sent()) ? [ 2, "webstore" ] : "funnel" === installSource.value ? [ 2, "funnel" ] : "blog" === installSource.value ? [ 2, "blog" ] : "editor" === installSource.value ? [ 2, "editor" ] : [ 2, "webstore" ];
                                                }
                                            });
                                        });
                                    }() ];

                                  case 2:
                                    return source = _a.sent(), [ 3, 4 ];

                                  case 3:
                                    return _a.sent(), tracking_1.felog.cannotGetInstallSource(), [ 3, 4 ];

                                  case 4:
                                    return installSource = source, tracking_1.felog.extensionInstall(source), tracking_3.gnar.install(installSource), 
                                    [ 4, prefs.get("enableWelcomePageForQA") ];

                                  case 5:
                                    return _a.sent(), [ 4, function(funnel) {
                                        return __awaiter(this, void 0, void 0, function() {
                                            var chromeStoreInstallUtmCookie, chromeInstallUtmValue, url, tabs;
                                            return __generator(this, function(_a) {
                                                switch (_a.label) {
                                                  case 0:
                                                    return util_1.isChrome() && funnel ? [ 2 ] : [ 4, cookiesHelper.getChromeStoreInstallUTM() ];

                                                  case 1:
                                                    return chromeStoreInstallUtmCookie = _a.sent(), chromeInstallUtmValue = !!chromeStoreInstallUtmCookie && "true" === chromeStoreInstallUtmCookie.value, 
                                                    url = util_1.isChrome() ? url_1.getExtensionSuccessURL(chromeInstallUtmValue) : url_1.getAfterInstallURL(funnel), 
                                                    tabs = extensionApi.tabs, [ 2, funnel ? tabs.updateCurrent(url) : tabs.open(url, !0) ];
                                                }
                                            });
                                        });
                                    }("funnel" === source) ];

                                  case 6:
                                    _a.sent(), _a.label = 7;

                                  case 7:
                                    return showOnboarding(), [ 2 ];
                                }
                                var installSource;
                            });
                        });
                    }(prefs, pageConfig, showOnboarding) ];

                  case 4:
                    return _a.sent(), [ 4, prefs.set("enabledDefs", !1) ];

                  case 5:
                    return _a.sent(), seenNews(), [ 3, 10 ];

                  case 6:
                    return tracking_1.felog.extensionUpdated(version, previousVersion), tracking_3.gnar.update(previousVersion), 
                    [ 4, prefs.get("enabledDefs") ];

                  case 7:
                    return enabledDefs = _a.sent(), isBoolean(enabledDefs) ? [ 3, 9 ] : [ 4, prefs.set("enabledDefs", !0) ];

                  case 8:
                    _a.sent(), _a.label = 9;

                  case 9:
                    try {
                        version.split(".")[0] !== previousVersion.split(".")[0] && notification.update(extensionApi, pageConfig.toReload);
                    } catch (error) {
                        tracking_1.felog.extensionUpdateFail(previousVersion);
                    }
                    _a.label = 10;

                  case 10:
                    return [ 2 ];
                }
            });
        });
    }
    exports.startBgPage = function(spec) {
        timers_1.timers.start(BG_START_TIMER), function(gnarSpec) {
            return __awaiter(this, void 0, void 0, function() {
                var prefs, dapi, connectionSagas, userStateOrNull, pageConfig, socketManager, reconnectSockets, settingsSagas, tabsSagas, userSagas, storeController, authSagaRunners, tabsSagaRunner, fakeCapi;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return prefs = new prefs_1.PrefsImpl(extensionApi.preferences), dapi = new dapi_1.DapiImpl(request_1.fetch), 
                        [ 4, runPrefsMigrations() ];

                      case 1:
                        return _a.sent(), connectionSagas = new sagas_1.ConnectionSagas(prefs, message_1.emitTabs, tracking_1.felog, util_2.isIncognito, util_2.getNextPingDate), 
                        userStateOrNull = function() {
                            return null;
                        }, pageConfig = new page_config_1.PageConfigImpl(prefs, function() {
                            return userStateOrNull();
                        }), reconnectSockets = function(dialect) {
                            socketManager && socketManager.reconnectAll(dialect);
                        }, settingsSagas = new sagas_2.SettingsSagas(prefs, dapi, reconnectSockets, message_1.emitFocusedTab), 
                        tabsSagas = new sagas_4.TabsSagas(connectionSagas, message_1.emitTo, message_1.emitFocusedTab, extensionApi, pageConfig), 
                        userSagas = new sagas_3.UserSagas(settingsSagas, prefs, tracking_1.felog, cookiesHelper, bgonly_1.getContainerIdOrUndefined, reconnectSockets), 
                        storeController = new store_1.StoreControllerImpl(userSagas, settingsSagas, tabsSagas, connectionSagas, pageConfig), 
                        userStateOrNull = function() {
                            return storeController.store.getState().user;
                        }, authSagaRunners = new store_1.AuthSagaRunners(storeController, userSagas), tabsSagaRunner = new store_1.TabsSagaRunner(storeController, tabsSagas), 
                        profiler.track(tracking_2.initBg, gnarSpec), fakeCapi = new socket_1.FakeCapi(), 
                        socketManager = new socket_1.BackgroundSocketManager(tracking_1.felog, function() {
                            return storeController.store.getState().connection;
                        }, storeController.actions.updateConnection, authSagaRunners.refreshUser, cookiesHelper.getToken, message, fakeCapi), 
                        profiler.track(function() {
                            return api_1.api(storeController.store, authSagaRunners, storeController.actions, prefs, socketManager.getLog, fakeCapi, extensionApi, tabsSagaRunner);
                        }), [ 4, profiler.trackAsync(storeController.initStore) ];

                      case 2:
                        return _a.sent(), [ 4, profiler.trackAsync(checkUpdate, prefs, pageConfig, storeController.actions.seenNews, storeController.actions.showOnboarding) ];

                      case 3:
                        return _a.sent(), profiler.track(function() {
                            return chrome_1.loadContentScripts(extensionApi, pageConfig, config_1.GRAMMARLY_DOMAIN);
                        }), profiler.track(function() {
                            return chrome_1.loadProxy(extensionApi, pageConfig);
                        }), (time = timers_1.timers.stop(BG_START_TIMER)) > 3e4 && tracking_1.felog.bgPageInitTimeout(time), 
                        [ 4, function(prefs) {
                            return __awaiter(this, void 0, void 0, function() {
                                var bgFails;
                                return __generator(this, function(_a) {
                                    switch (_a.label) {
                                      case 0:
                                        return [ 4, prefs.get("bgInitFail") ];

                                      case 1:
                                        return (bgFails = _a.sent()) ? (tracking_1.felog.bgPageInitFail(bgFails), [ 4, prefs.set("bgInitFail", 0) ]) : [ 2 ];

                                      case 2:
                                        return _a.sent(), [ 2 ];
                                    }
                                });
                            });
                        }(prefs) ];

                      case 4:
                        return _a.sent(), [ 2 ];
                    }
                    var time;
                });
            });
        }(spec).catch(function(error) {
            tracking_1.felog.bgPageStartFail(error && error.message, error && error.stack), 
            log.error("bg page start fail", error);
        }), chrome_1.setupForcedUpdate(), "prod" !== Config.getGlobal().bundleInfo.env && "qa" === Config.getGlobal().bundleInfo.env && __webpack_require__(1177).startSendingBgLogsToActiveTab();
    }, exports.runPrefsMigrations = runPrefsMigrations;
}, function(module, exports) {
    window.IS_BG = !0;
}, function(module, exports) {
    !function() {
        "use strict";
        if (!self.fetch) {
            Headers.prototype.append = function(name, value) {
                name = normalizeName(name), value = normalizeValue(value);
                var list = this.map[name];
                list || (list = [], this.map[name] = list), list.push(value);
            }, Headers.prototype.delete = function(name) {
                delete this.map[normalizeName(name)];
            }, Headers.prototype.get = function(name) {
                var values = this.map[normalizeName(name)];
                return values ? values[0] : null;
            }, Headers.prototype.getAll = function(name) {
                return this.map[normalizeName(name)] || [];
            }, Headers.prototype.has = function(name) {
                return this.map.hasOwnProperty(normalizeName(name));
            }, Headers.prototype.set = function(name, value) {
                this.map[normalizeName(name)] = [ normalizeValue(value) ];
            }, Headers.prototype.forEach = function(callback, thisArg) {
                Object.getOwnPropertyNames(this.map).forEach(function(name) {
                    this.map[name].forEach(function(value) {
                        callback.call(thisArg, value, name, this);
                    }, this);
                }, this);
            };
            var support = {
                blob: "FileReader" in self && "Blob" in self && function() {
                    try {
                        return new Blob(), !0;
                    } catch (e) {
                        return !1;
                    }
                }(),
                formData: "FormData" in self
            }, methods = [ "DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT" ];
            Body.call(Request.prototype), Body.call(Response.prototype), self.Headers = Headers, 
            self.Request = Request, self.Response = Response, self.fetch = function(input, init) {
                var request;
                return request = Request.prototype.isPrototypeOf(input) && !init ? input : new Request(input, init), 
                new Promise(function(resolve, reject) {
                    var xhr = new XMLHttpRequest();
                    xhr.onload = function() {
                        var status = 1223 === xhr.status ? 204 : xhr.status;
                        if (status < 100 || status > 599) reject(new TypeError("Network request failed")); else {
                            var options = {
                                status: status,
                                statusText: xhr.statusText,
                                headers: function(xhr) {
                                    var head = new Headers();
                                    return xhr.getAllResponseHeaders().trim().split("\n").forEach(function(header) {
                                        var split = header.trim().split(":"), key = split.shift().trim(), value = split.join(":").trim();
                                        head.append(key, value);
                                    }), head;
                                }(xhr),
                                url: "responseURL" in xhr ? xhr.responseURL : /^X-Request-URL:/m.test(xhr.getAllResponseHeaders()) ? xhr.getResponseHeader("X-Request-URL") : void 0
                            }, body = "response" in xhr ? xhr.response : xhr.responseText;
                            resolve(new Response(body, options));
                        }
                    }, xhr.onerror = function() {
                        reject(new TypeError("Network request failed"));
                    }, xhr.open(request.method, request.url, !0), "include" === request.credentials && (xhr.withCredentials = !0), 
                    "responseType" in xhr && support.blob && (xhr.responseType = "blob"), request.headers.forEach(function(value, name) {
                        xhr.setRequestHeader(name, value);
                    }), xhr.send(void 0 === request._bodyInit ? null : request._bodyInit);
                });
            }, self.fetch.polyfill = !0;
        }
        function normalizeName(name) {
            if ("string" != typeof name && (name = name.toString()), /[^a-z0-9\-#$%&'*+.\^_`|~]/i.test(name)) throw new TypeError("Invalid character in header field name");
            return name.toLowerCase();
        }
        function normalizeValue(value) {
            return "string" != typeof value && (value = value.toString()), value;
        }
        function Headers(headers) {
            this.map = {}, headers instanceof Headers ? headers.forEach(function(value, name) {
                this.append(name, value);
            }, this) : headers && Object.getOwnPropertyNames(headers).forEach(function(name) {
                this.append(name, headers[name]);
            }, this);
        }
        function consumed(body) {
            if (body.bodyUsed) return Promise.reject(new TypeError("Already read"));
            body.bodyUsed = !0;
        }
        function fileReaderReady(reader) {
            return new Promise(function(resolve, reject) {
                reader.onload = function() {
                    resolve(reader.result);
                }, reader.onerror = function() {
                    reject(reader.error);
                };
            });
        }
        function readBlobAsArrayBuffer(blob) {
            var reader = new FileReader();
            return reader.readAsArrayBuffer(blob), fileReaderReady(reader);
        }
        function Body() {
            return this.bodyUsed = !1, this._initBody = function(body) {
                if (this._bodyInit = body, "string" == typeof body) this._bodyText = body; else if (support.blob && Blob.prototype.isPrototypeOf(body)) this._bodyBlob = body; else if (support.formData && FormData.prototype.isPrototypeOf(body)) this._bodyFormData = body; else {
                    if (body) throw new Error("unsupported BodyInit type");
                    this._bodyText = "";
                }
            }, support.blob ? (this.blob = function() {
                var rejected = consumed(this);
                if (rejected) return rejected;
                if (this._bodyBlob) return Promise.resolve(this._bodyBlob);
                if (this._bodyFormData) throw new Error("could not read FormData body as blob");
                return Promise.resolve(new Blob([ this._bodyText ]));
            }, this.arrayBuffer = function() {
                return this.blob().then(readBlobAsArrayBuffer);
            }, this.text = function() {
                var blob, reader, rejected = consumed(this);
                if (rejected) return rejected;
                if (this._bodyBlob) return blob = this._bodyBlob, (reader = new FileReader()).readAsText(blob), 
                fileReaderReady(reader);
                if (this._bodyFormData) throw new Error("could not read FormData body as text");
                return Promise.resolve(this._bodyText);
            }) : this.text = function() {
                var rejected = consumed(this);
                return rejected || Promise.resolve(this._bodyText);
            }, support.formData && (this.formData = function() {
                return this.text().then(decode);
            }), this.json = function() {
                return this.text().then(JSON.parse);
            }, this;
        }
        function Request(url, options) {
            var method, upcased;
            if (options = options || {}, this.url = url, this.credentials = options.credentials || "omit", 
            this.headers = new Headers(options.headers), this.method = (method = options.method || "GET", 
            upcased = method.toUpperCase(), methods.indexOf(upcased) > -1 ? upcased : method), 
            this.mode = options.mode || null, this.referrer = null, ("GET" === this.method || "HEAD" === this.method) && options.body) throw new TypeError("Body not allowed for GET or HEAD requests");
            this._initBody(options.body);
        }
        function decode(body) {
            var form = new FormData();
            return body.trim().split("&").forEach(function(bytes) {
                if (bytes) {
                    var split = bytes.split("="), name = split.shift().replace(/\+/g, " "), value = split.join("=").replace(/\+/g, " ");
                    form.append(decodeURIComponent(name), decodeURIComponent(value));
                }
            }), form;
        }
        function Response(bodyInit, options) {
            options || (options = {}), this._initBody(bodyInit), this.type = "default", this.url = null, 
            this.status = options.status, this.ok = this.status >= 200 && this.status < 300, 
            this.statusText = options.statusText, this.headers = options.headers instanceof Headers ? options.headers : new Headers(options.headers), 
            this.url = options.url || "";
        }
    }();
}, function(module, exports, __webpack_require__) {
    var baseGetTag = __webpack_require__(23), isObjectLike = __webpack_require__(17), boolTag = "[object Boolean]";
    module.exports = function(value) {
        return !0 === value || !1 === value || isObjectLike(value) && baseGetTag(value) == boolTag;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __assign = this && this.__assign || Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
        return t;
    }, __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var util_1 = __webpack_require__(664), value_manager_1 = __webpack_require__(1141);
    exports.ValueManager = value_manager_1.ValueManager, exports.BaseStorage = value_manager_1.BaseStorage, 
    exports.MemoryStorage = value_manager_1.MemoryStorage, exports.ContainerIdManager = value_manager_1.ContainerIdManager, 
    exports.GAClientIdManager = value_manager_1.GAClientIdManager, exports.LocalStorage = value_manager_1.LocalStorage, 
    exports.CookieStorage = value_manager_1.CookieStorage, exports.ChromeCookieStorage = value_manager_1.ChromeCookieStorage, 
    exports.WebExtensionsCookieStorage = value_manager_1.WebExtensionsCookieStorage, 
    exports.BackendStorage = value_manager_1.BackendStorage;
    var analytics_1 = __webpack_require__(1143);
    exports.GoogleAnalyticsClient = analytics_1.GoogleAnalyticsClient;
    var reservedPropNames = [ "client", "clientVersion", "userId", "isTest", "containerId", "instanceId", "batchId" ], GnarClientImpl = function() {
        function GnarClientImpl(_url, _client, _clientVersion, _fetch, _containerIdManager, _logger, _metric, _storePingTimestamp) {
            void 0 === _storePingTimestamp && (_storePingTimestamp = !1), this._client = _client, 
            this._clientVersion = _clientVersion, this._fetch = _fetch, this._containerIdManager = _containerIdManager, 
            this._logger = _logger, this._metric = _metric, this._storePingTimestamp = _storePingTimestamp, 
            this._instanceId = util_1.alphanumeric(8), this._batchId = 0, this._isUserReady = !1, 
            this._queue = [], this._eventsUrl = _url + "/events", this._liteUrl = _url + "/lite", 
            this._pingMaybe();
        }
        return GnarClientImpl.prototype.track = function(props, options) {
            if (void 0 === options && (options = {
                lite: !1
            }), 0 !== props.eventName.indexOf(this._client + "/")) throw new Error("Event name " + props.eventName + " should start with '" + this._client + "/'");
            return Object.keys(props).forEach(function(key) {
                if (-1 !== reservedPropNames.indexOf(key)) throw new Error("Event data should not contain '" + key + "' prop.");
            }), this._isUserReady || options.lite && !options.sendUser ? (props.eventName !== this._client + "/ping" && this._pingMaybe(), 
            this._send(props, options)) : this._enqueue(props, options);
        }, GnarClientImpl.prototype.setUser = function(id, isTest) {
            if (null === id || "" === id) throw new Error("Invalid userId: " + id);
            var shouldSendPing = this._userId && this._userId !== id && !(/^-/.test(id) && /^-/.test(this._userId));
            this._isTest = isTest, this._userId = id, shouldSendPing && this._pingMaybe(!0), 
            this._isUserReady || (this._execQueue(), this._isUserReady = !0);
        }, GnarClientImpl.prototype.getContainerId = function() {
            return this._containerIdManager.getContainerId();
        }, GnarClientImpl.prototype._setNextPingTimestamp = function() {
            var ts = util_1.getNextPingDate();
            if (this._nextPingTimestamp = ts, this._storePingTimestamp) try {
                localStorage.setItem("gnar_nextPingTimestamp", ts.toString());
            } catch (error) {
                this._metric.getCounter("nextPingDate.write.failure").increment(), this._logger.warn("nextPingDate.write.failed", error);
            }
        }, GnarClientImpl.prototype._getNextPingTimestamp = function() {
            var ts = this._nextPingTimestamp;
            if (void 0 !== ts || !this._storePingTimestamp) return ts;
            try {
                var stored = localStorage.getItem("gnar_nextPingTimestamp");
                ts = null === stored ? void 0 : parseInt(stored, 10);
            } catch (error) {
                ts = void 0, this._metric.getCounter("nextPingDate.read.failure").increment(), this._logger.warn("nextPingDate.read.failed", error);
            }
            return ts;
        }, GnarClientImpl.prototype._shouldPing = function(force) {
            if (force) return !0;
            var ts = this._getNextPingTimestamp();
            return void 0 === ts || ts < Date.now();
        }, GnarClientImpl.prototype._pingMaybe = function(force) {
            if (void 0 === force && (force = !1), this._shouldPing(force)) {
                this._setNextPingTimestamp();
                var props = {
                    eventName: this._client + "/ping",
                    referrer: document.referrer,
                    url: document.location.href
                };
                this.track(props);
            }
        }, GnarClientImpl.prototype.pingMaybe = function() {
            this._pingMaybe();
        }, GnarClientImpl.prototype._enqueue = function(props, options) {
            var _this = this;
            return new Promise(function(resolve, reject) {
                _this._queue.push([ props, options, {
                    resolve: resolve,
                    reject: reject
                } ]);
            });
        }, GnarClientImpl.prototype._execQueue = function() {
            var _this = this;
            this._queue.forEach(function(_a) {
                var props = _a[0], options = _a[1], _b = _a[2], resolve = _b.resolve, reject = _b.reject;
                _this._send(props, options).then(function() {
                    return resolve();
                }).catch(function(error) {
                    return reject(error);
                });
            }), this._queue = [];
        }, GnarClientImpl.prototype._withClientProps = function(props) {
            return __assign({}, props, {
                client: this._client,
                clientVersion: this._clientVersion
            });
        }, GnarClientImpl.prototype._withUserProps = function(props) {
            return __awaiter(this, void 0, void 0, function() {
                var _a, _b;
                return __generator(this, function(_c) {
                    switch (_c.label) {
                      case 0:
                        return _a = [ {}, props ], _b = {}, [ 4, this.getContainerId() ];

                      case 1:
                        return [ 2, __assign.apply(void 0, _a.concat([ (_b.containerId = _c.sent(), _b.userId = this._userId, 
                        _b.isTest = this._isTest, _b) ])) ];
                    }
                });
            });
        }, GnarClientImpl.prototype._withBrowserProps = function(props) {
            return __assign({}, props, {
                userAgent: navigator.userAgent,
                screenWidth: screen.width,
                screenHeight: screen.height
            });
        }, GnarClientImpl.prototype._withInstanceProps = function(props) {
            var batchId = this._batchId++;
            return __assign({}, props, {
                instanceId: this._instanceId,
                batchId: batchId
            });
        }, GnarClientImpl.prototype._send = function(props, options) {
            return __awaiter(this, void 0, void 0, function() {
                var error_1;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return _a.trys.push([ 0, 4, , 5 ]), props = this._withClientProps(props), (!options.lite || options.lite && options.sendInstance) && (props = this._withInstanceProps(props)), 
                        !options.lite || options.lite && options.sendUser ? [ 4, this._withUserProps(props) ] : [ 3, 2 ];

                      case 1:
                        props = _a.sent(), _a.label = 2;

                      case 2:
                        return (!options.lite || options.lite && options.sendBrowser) && (props = this._withBrowserProps(props)), 
                        [ 4, this._doSend(options.lite ? this._liteUrl : this._eventsUrl, props) ];

                      case 3:
                        return [ 2, _a.sent() ];

                      case 4:
                        throw error_1 = _a.sent(), this._metric.getCounter("send.failure").increment(), 
                        this._logger.warn("send.failed", error_1), error_1;

                      case 5:
                        return [ 2 ];
                    }
                });
            });
        }, GnarClientImpl.prototype._doSend = function(url, props) {
            return this._fetch(url, {
                mode: "cors",
                credentials: "include",
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    events: [ props ]
                })
            }).then(function(response) {
                return response.ok ? Promise.resolve() : Promise.reject(new Error(response.statusText));
            });
        }, GnarClientImpl;
    }();
    exports.GnarClientImpl = GnarClientImpl;
    var MemoryGnarClient = function() {
        function MemoryGnarClient() {
            this.history = [];
        }
        return MemoryGnarClient.prototype.track = function(props) {
            return this.history.push(props), Promise.resolve();
        }, MemoryGnarClient.prototype.pingMaybe = function() {}, MemoryGnarClient.prototype.setUser = function() {}, 
        MemoryGnarClient.prototype.getContainerId = function() {
            return Promise.resolve("dummy_container_id");
        }, MemoryGnarClient;
    }();
    exports.MemoryGnarClient = MemoryGnarClient;
    var LocalStorageGnarClient = function() {
        function LocalStorageGnarClient() {}
        return LocalStorageGnarClient.prototype.track = function(props) {
            try {
                var data = JSON.parse(localStorage.getItem("trackingGnar")) || [];
                data.push(props), localStorage.setItem("trackingGnar", JSON.stringify(data));
            } catch (error) {}
            return Promise.resolve();
        }, LocalStorageGnarClient.prototype.pingMaybe = function() {}, LocalStorageGnarClient.prototype.setUser = function() {}, 
        LocalStorageGnarClient.prototype.getContainerId = function() {
            return Promise.resolve("dummy_container_id");
        }, LocalStorageGnarClient;
    }();
    exports.LocalStorageGnarClient = LocalStorageGnarClient;
}, function(module, exports, __webpack_require__) {
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
    }), __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var cookie_1 = __webpack_require__(1142), util_1 = __webpack_require__(664), cookieExpiration = function() {
        return new Date().setFullYear(new Date().getFullYear() + 10);
    }, testCookieExpiration = function() {
        return new Date().setMinutes(new Date().getMinutes() + 10);
    }, cookieDomainRegExp = /^\.\w+\.\w+/;
    function success(value) {
        return {
            type: "success",
            value: value
        };
    }
    function failure(error) {
        return {
            type: "failure",
            error: error
        };
    }
    function lift(promise) {
        return promise.then(success, failure);
    }
    function retry(times, backoffMillis, f) {
        var res = f();
        return times > 0 ? res.catch(function(_) {
            return new Promise(function(resolve, _) {
                return setTimeout(resolve, backoffMillis);
            }).then(function(_) {
                return retry(times - 1, backoffMillis, f);
            });
        }) : res;
    }
    var ValueManager = function() {
        function ValueManager(primaryStorage, secondaryStorages, _logger, _metric, _cacheSuccessTimeoutMillis, _cacheFailureTimeoutMillis, _getTime) {
            void 0 === secondaryStorages && (secondaryStorages = []), void 0 === _cacheSuccessTimeoutMillis && (_cacheSuccessTimeoutMillis = 3e5), 
            void 0 === _cacheFailureTimeoutMillis && (_cacheFailureTimeoutMillis = 0), void 0 === _getTime && (_getTime = function() {
                return Date.now();
            }), this.primaryStorage = primaryStorage, this.secondaryStorages = secondaryStorages, 
            this._logger = _logger, this._metric = _metric, this._cacheSuccessTimeoutMillis = _cacheSuccessTimeoutMillis, 
            this._cacheFailureTimeoutMillis = _cacheFailureTimeoutMillis, this._getTime = _getTime, 
            this._allStorages = [ primaryStorage ].concat(secondaryStorages);
        }
        return ValueManager.prototype._expireCache = function(timeoutMillis) {
            0 === timeoutMillis ? this._cacheExpireTimestamp = 0 : timeoutMillis > 0 && (this._cacheExpireTimestamp = this._getTime() + timeoutMillis);
        }, ValueManager.prototype.getValue = function() {
            var _this = this;
            if (void 0 !== this._cache && (void 0 === this._cacheExpireTimestamp || this._getTime() < this._cacheExpireTimestamp)) return this._cache;
            var timer = this._metric.getTimer("doGet" + this.valueLabel() + ".timer").start(), result = this._valueFromStorage();
            return result && (this._cache = result, this._cacheExpireTimestamp = void 0, result.then(function(_) {
                return _this._expireCache(_this._cacheSuccessTimeoutMillis);
            }, function(_) {
                return _this._expireCache(_this._cacheFailureTimeoutMillis);
            })), result.then(function(_) {
                timer.stop(), _this._metric.getCounter("doGet" + _this.valueLabel() + ".success").increment();
            }, function(error) {
                timer.stop(), _this._metric.getCounter("doGet" + _this.valueLabel() + ".failure").increment(), 
                _this._logger.warn("doGet" + _this.valueLabel() + ".failed", error);
            }), result;
        }, ValueManager.prototype._valueFromStorage = function() {
            var _this = this;
            return Promise.all(this._allStorages.map(function(storage) {
                return lift(storage.safeGetValue(_this.key()));
            })).then(function(getResults) {
                var primaryGetResult = getResults[0];
                if ("failure" === primaryGetResult.type) return Promise.reject("getting value from primary storage '" + _this.primaryStorage.name + "' has failed: " + primaryGetResult.error);
                var nonEmptyResult = getResults.find(function(result) {
                    return "success" === result.type && void 0 !== result.value;
                });
                if (void 0 === nonEmptyResult) return Promise.resolve(void 0);
                var retrievedValue = nonEmptyResult.value, recovered = "success" === primaryGetResult.type && void 0 === primaryGetResult.value && void 0 !== nonEmptyResult, storagesToFill = getResults.reduce(function(acc, result, index) {
                    return "success" === result.type && result.value !== retrievedValue ? acc.concat(index) : acc;
                }, []);
                return _this.setValue(retrievedValue, recovered, !1, storagesToFill);
            });
        }, ValueManager.prototype.setValue = function(value, recovered, generated, storageList) {
            var _this = this;
            void 0 === recovered && (recovered = !1), void 0 === generated && (generated = !1), 
            void 0 === storageList && (storageList = Array.from(Array(this._allStorages.length).keys()));
            var setPromises = storageList.map(function(index) {
                return lift(_this._allStorages[index].safeSetValue(_this.key(), value));
            }), result = Promise.all(setPromises).then(function(setResults) {
                if (recovered || generated) {
                    var primarySetResult = setResults[0];
                    if ("success" !== primarySetResult.type) return Promise.reject("setting " + _this.valueLabel() + " to primary storage has failed: \n                " + primarySetResult.error);
                }
                return Promise.resolve(value);
            });
            return result.then(function(_) {
                recovered ? _this._metric.getCounter("recovered").increment() : generated && _this._metric.getCounter("generated").increment();
            }), result;
        }, ValueManager;
    }();
    exports.ValueManager = ValueManager;
    var ContainerIdManager = function(_super) {
        function ContainerIdManager() {
            var _this = null !== _super && _super.apply(this, arguments) || this;
            return _this.containerIdLength = 12, _this.getContainerId = function() {
                return _super.prototype.getValue.call(_this).then(function(r) {
                    return __awaiter(_this, void 0, void 0, function() {
                        return __generator(this, function(_a) {
                            switch (_a.label) {
                              case 0:
                                return void 0 !== r ? [ 3, 2 ] : [ 4, _super.prototype.setValue.call(this, this.generateContainerId(), !1, !0) ];

                              case 1:
                                return [ 2, _a.sent() ];

                              case 2:
                                return [ 2, r ];
                            }
                        });
                    });
                });
            }, _this;
        }
        return __extends(ContainerIdManager, _super), ContainerIdManager.prototype.key = function() {
            return "gnar_containerId";
        }, ContainerIdManager.prototype.valueLabel = function() {
            return "ContainerId";
        }, ContainerIdManager.prototype.generateContainerId = function() {
            return util_1.alphanumeric(this.containerIdLength);
        }, ContainerIdManager;
    }(ValueManager);
    exports.ContainerIdManager = ContainerIdManager;
    var GAClientIdManager = function(_super) {
        function GAClientIdManager() {
            return null !== _super && _super.apply(this, arguments) || this;
        }
        return __extends(GAClientIdManager, _super), GAClientIdManager.prototype.key = function() {
            return "ga_clientId";
        }, GAClientIdManager.prototype.valueLabel = function() {
            return "GAClientId";
        }, GAClientIdManager.prototype.setId = function(value) {
            _super.prototype.setValue.call(this, value, !1, !0);
        }, GAClientIdManager;
    }(ValueManager);
    exports.GAClientIdManager = GAClientIdManager;
    var BaseStorage = function() {
        function BaseStorage(name) {
            this.name = name;
        }
        return BaseStorage.prototype.safeSetValue = function(key, value) {
            var _this = this;
            return this.ensureAvailable(key).then(function() {
                return _this.setValue(key, value);
            });
        }, BaseStorage.prototype.safeGetValue = function(key) {
            var _this = this;
            return this.ensureAvailable(key).then(function() {
                return _this.getValue(key);
            }).then(function(cid) {
                return "" === cid ? void 0 : cid;
            });
        }, BaseStorage;
    }();
    exports.BaseStorage = BaseStorage;
    var ChromeCookieStorage = function(_super) {
        function ChromeCookieStorage(_url, _domain) {
            var _this = _super.call(this, "chromeCookie") || this;
            if (_this._url = _url, _this._domain = _domain, !cookieDomainRegExp.test(_domain)) throw new Error('Incorrect cookie domain provided.\n        Use top-level domain, starting from "."');
            return _this;
        }
        return __extends(ChromeCookieStorage, _super), ChromeCookieStorage.prototype._hasRuntimeError = function() {
            return window.chrome && window.chrome.runtime && window.chrome.runtime.lastError;
        }, ChromeCookieStorage.prototype.ensureAvailable = function() {
            var _this = this;
            return retry(2, 1e3, function() {
                return new Promise(function(resolve, reject) {
                    var value = util_1.alphanumeric(10);
                    try {
                        window.chrome.cookies.set({
                            name: value,
                            value: value,
                            url: _this._url,
                            domain: _this._domain,
                            expirationDate: testCookieExpiration() / 1e3
                        }, function(cookie) {
                            var error = _this._hasRuntimeError();
                            !cookie && error && reject("chrome.cookie.set failed with an error: " + error.message), 
                            cookie && cookie.value === value ? resolve() : reject(new Error("ChromeCookieStorage is unavailable.\n              Availability test failed.\n              Tried to set " + value + ", the result is " + (cookie ? cookie.value : cookie) + "."));
                        });
                    } catch (e) {
                        reject(e);
                    }
                });
            });
        }, ChromeCookieStorage.prototype.getValue = function(key) {
            var _this = this;
            return new Promise(function(resolve, reject) {
                try {
                    window.chrome.cookies.get({
                        url: _this._url,
                        name: key
                    }, function(cookie) {
                        var error = _this._hasRuntimeError();
                        !cookie && error && reject("chrome.cookie.get failed with an error: " + error.message), 
                        resolve(cookie ? cookie.value : void 0);
                    });
                } catch (e) {
                    reject(e);
                }
            });
        }, ChromeCookieStorage.prototype.setValue = function(key, value) {
            var _this = this;
            return new Promise(function(resolve, reject) {
                try {
                    window.chrome.cookies.set({
                        name: key,
                        value: value,
                        url: _this._url,
                        domain: _this._domain,
                        expirationDate: cookieExpiration() / 1e3
                    }, function(cookie) {
                        var error = _this._hasRuntimeError();
                        !cookie && error && reject("chrome.cookie.set failed with an error: " + error.message), 
                        cookie && cookie.value === value || reject(new Error("setValue for " + key + " failed.\n            Tried to set " + value + ", the result is " + (cookie ? cookie.value : cookie) + ".")), 
                        resolve();
                    });
                } catch (e) {
                    reject(e);
                }
            });
        }, ChromeCookieStorage;
    }(BaseStorage);
    exports.ChromeCookieStorage = ChromeCookieStorage;
    var WebExtensionsCookieStorage = function(_super) {
        function WebExtensionsCookieStorage(_url, _domain) {
            var _this = _super.call(this, "webExtensionsCookie") || this;
            if (_this._url = _url, _this._domain = _domain, !cookieDomainRegExp.test(_domain)) throw new Error('Incorrect cookie domain provided.\n        Use top-level domain, starting from "."');
            return _this;
        }
        return __extends(WebExtensionsCookieStorage, _super), WebExtensionsCookieStorage.prototype.ensureAvailable = function() {
            var _this = this;
            return retry(2, 1e3, function() {
                return new Promise(function(resolve, reject) {
                    var value = util_1.alphanumeric(10);
                    window.browser.cookies.set({
                        name: value,
                        value: value,
                        url: _this._url,
                        domain: _this._domain,
                        expirationDate: testCookieExpiration() / 1e3
                    }).then(function() {
                        window.browser.cookies.get({
                            url: _this._url,
                            name: value
                        }).then(function(cookie) {
                            cookie && cookie.value === value ? resolve() : reject(new Error("WebExtensionsCookieStorage is unavailable.\n              Availability test failed.\n              Tried to set " + value + ", the result is " + (cookie ? cookie.value : cookie) + "."));
                        }).catch(function(error) {
                            reject("browser.cookies.get failed with an error: " + error.message);
                        });
                    }).catch(function(error) {
                        reject("browser.cookies.set failed with an error: " + error.message);
                    });
                });
            });
        }, WebExtensionsCookieStorage.prototype.getValue = function(key) {
            var _this = this;
            return new Promise(function(resolve, reject) {
                window.browser.cookies.get({
                    url: _this._url,
                    name: key
                }).then(function(cookie) {
                    resolve(cookie ? cookie.value : void 0);
                }).catch(function(error) {
                    reject("browser.cookies.get failed with an error: " + error.message);
                });
            });
        }, WebExtensionsCookieStorage.prototype.setValue = function(key, value) {
            var _this = this;
            return new Promise(function(resolve, reject) {
                window.browser.cookies.set({
                    name: key,
                    value: value,
                    url: _this._url,
                    domain: _this._domain,
                    expirationDate: cookieExpiration() / 1e3
                }).then(function(cookie) {
                    cookie && cookie.value === value || reject(new Error("setValue failed.\n          Tried to set " + value + ", the result is " + (cookie ? cookie.value : cookie) + ".")), 
                    resolve();
                }).catch(function(error) {
                    reject("browser.cookies.set failed with an error: " + error.message);
                });
            });
        }, WebExtensionsCookieStorage;
    }(BaseStorage);
    exports.WebExtensionsCookieStorage = WebExtensionsCookieStorage;
    var LocalStorage = function(_super) {
        function LocalStorage() {
            return _super.call(this, "localStorage") || this;
        }
        return __extends(LocalStorage, _super), LocalStorage.prototype.ensureAvailable = function(key) {
            var testKey = key + "_test", value = util_1.alphanumeric(10);
            return new Promise(function(resolve, reject) {
                localStorage.setItem(testKey, value), localStorage.getItem(testKey) !== value ? reject(new Error("LocalStorage is unavailable.\n          Availability test failed.\n          Tried to set " + value + ", \n          the result is " + localStorage.getItem(testKey) + ".")) : resolve(), 
                localStorage.removeItem(testKey);
            });
        }, LocalStorage.prototype.getValue = function(key) {
            var value = localStorage.getItem(key);
            return new Promise(function(resolve, _) {
                return resolve(null === value ? void 0 : value);
            });
        }, LocalStorage.prototype.setValue = function(key, value) {
            return new Promise(function(resolve, _) {
                localStorage.setItem(key, value), resolve();
            });
        }, LocalStorage;
    }(BaseStorage);
    exports.LocalStorage = LocalStorage;
    var CookieStorage = function(_super) {
        function CookieStorage(_domain) {
            var _this = _super.call(this, "cookie") || this;
            if (_this._domain = _domain, !cookieDomainRegExp.test(_domain)) throw new Error('Incorrect cookie domain provided.\n        Use top-level domain, starting from "."');
            return _this;
        }
        return __extends(CookieStorage, _super), CookieStorage.prototype._getCookieOptions = function() {
            return {
                path: "/",
                domain: this._domain,
                expires: new Date(cookieExpiration())
            };
        }, CookieStorage.prototype.ensureAvailable = function() {
            var value = util_1.alphanumeric(10);
            return new Promise(function(resolve, reject) {
                cookie_1.default(value, value), cookie_1.default(value) !== value ? reject(new Error("CookieStorage is unavailable.\n          Availability test failed.\n          Tried to set " + value + ", the result is " + cookie_1.default(value) + ".")) : resolve(), 
                cookie_1.default(value, null);
            });
        }, CookieStorage.prototype.getValue = function(key) {
            return new Promise(function(resolve, _) {
                return resolve(cookie_1.default(key));
            });
        }, CookieStorage.prototype.setValue = function(key, value) {
            var _this = this;
            return new Promise(function(resolve, _) {
                cookie_1.default(key, value, _this._getCookieOptions()), resolve();
            });
        }, CookieStorage;
    }(BaseStorage);
    exports.CookieStorage = CookieStorage;
    var BackendStorage = function(_super) {
        function BackendStorage(_fetch, _url) {
            var _this = _super.call(this, "backend") || this;
            return _this._fetch = _fetch, _this._url = _url, _this._baseUrl = _url + "/cookies", 
            _this;
        }
        return __extends(BackendStorage, _super), BackendStorage.prototype.ensureAvailable = function(key) {
            var _this = this, testKey = key + "_test", value = util_1.alphanumeric(10), maxAge = (testCookieExpiration() - Date.now()) / 1e3, getUrl = this._baseUrl + "?name=" + testKey, postUrl = getUrl + "&value=" + value + "&maxAge=" + maxAge;
            return this._doSend(postUrl, "post").then(function(response) {
                if (!response.ok) throw new Error("BackendStorage is unavailable.\n          Availability test failed.\n          Tried to set " + value + ". Request failed.\n        ");
            }).then(function() {
                return _this._doSend(getUrl, "get").then(function(response) {
                    if (response.ok) return response.json().then(function(obj) {
                        if (obj.value !== value) throw new Error("BackendStorage is unavailable.\n                Availability test failed.\n                Tried to get " + testKey + " from server.\n                Got " + obj.value + " instead of " + value + ".");
                    });
                    throw new Error("BackendStorage is unavailable.\n            Availability test failed.\n            Tried to get " + testKey + " from server. Request failed.");
                });
            });
        }, BackendStorage.prototype._doSend = function(url, method) {
            return this._fetch(url, {
                credentials: "include",
                method: method
            });
        }, BackendStorage.prototype.getValue = function(key) {
            var url = this._baseUrl + "?name=" + key;
            return this._doSend(url, "get").then(function(response) {
                return response.json();
            }).then(function(obj) {
                return obj.value;
            });
        }, BackendStorage.prototype.setValue = function(key, value) {
            var maxAge = (cookieExpiration() - Date.now()) / 1e3, url = this._baseUrl + "?name=" + key + "&value=" + value + "&maxAge=" + maxAge;
            return this._doSend(url, "post").then(function() {});
        }, BackendStorage;
    }(BaseStorage);
    exports.BackendStorage = BackendStorage;
    var MemoryStorage = function(_super) {
        function MemoryStorage(_value) {
            void 0 === _value && (_value = void 0);
            var _this = _super.call(this, "memory") || this;
            return _this._value = _value, _this;
        }
        return __extends(MemoryStorage, _super), MemoryStorage.prototype.ensureAvailable = function() {
            return Promise.resolve();
        }, MemoryStorage.prototype.getValue = function(_) {
            return Promise.resolve(this._value);
        }, MemoryStorage.prototype.setValue = function(_, value) {
            return this._value = value, Promise.resolve();
        }, MemoryStorage;
    }(BaseStorage);
    exports.MemoryStorage = MemoryStorage;
}, function(module, exports, __webpack_require__) {
    "use strict";
    function encode(value) {
        try {
            return encodeURIComponent(value);
        } catch (e) {
            return null;
        }
    }
    function decode(value) {
        try {
            return decodeURIComponent(value);
        } catch (e) {
            return null;
        }
    }
    exports.__esModule = !0, exports.default = function(name, value, options) {
        if (arguments.length < 2) return function(name) {
            var cookies = function(str) {
                var obj = {}, pairs = str.split(/ *; */);
                if (!pairs[0]) return obj;
                for (var _iterator = pairs, _isArray = Array.isArray(_iterator), _i = 0, _iterator = _isArray ? _iterator : _iterator[Symbol.iterator](); ;) {
                    var _ref;
                    if (_isArray) {
                        if (_i >= _iterator.length) break;
                        _ref = _iterator[_i++];
                    } else {
                        if ((_i = _iterator.next()).done) break;
                        _ref = _i.value;
                    }
                    var pair = _ref;
                    pair = pair.split("="), obj[decode(pair[0])] = decode(pair[1]);
                }
                return obj;
            }(document.cookie);
            return name ? cookies[name] : cookies;
        }(name);
        !function(name, value) {
            var options = arguments.length <= 2 || void 0 === arguments[2] ? {} : arguments[2], str = encode(name) + "=" + encode(value);
            null == value && (options.maxage = -1);
            options.maxage && (options.expires = new Date(+new Date() + options.maxage));
            options.path && (str += "; path=" + options.path);
            options.domain && (str += "; domain=" + options.domain);
            options.expires && (str += "; expires=" + options.expires.toUTCString());
            options.secure && (str += "; secure");
            document.cookie = str;
        }(name, value, options);
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var initGA = function() {
        var i, s, o, g, r, a, m;
        i = window, s = document, o = "script", g = "//www.google-analytics.com/analytics.js", 
        r = "ga", i.GoogleAnalyticsObject = r, i[r] = i[r] || function() {
            (i[r].q = i[r].q || []).push(arguments);
        }, i[r].l = new Date().getTime(), a = s.createElement(o), m = s.getElementsByTagName(o)[0], 
        a.async = 1, a.src = g, m.parentNode.insertBefore(a, m);
    }, GoogleAnalyticsClient = function() {
        function GoogleAnalyticsClient(trackingId, clientIdManager, shouldInitGA) {
            void 0 === shouldInitGA && (shouldInitGA = !0);
            var _this = this;
            this._isReady = !1, this._gaQueue = [], shouldInitGA && initGA(), clientIdManager.getValue().then(function(clientId) {
                for (clientId ? ga("create", trackingId, "auto", {
                    clientId: clientId
                }) : (ga("create", trackingId, "auto"), ga(function(tracker) {
                    tracker && clientIdManager.setId(tracker.get("clientId"));
                })); _this._gaQueue.length > 0; ) ga.apply(null, _this._gaQueue.shift());
                _this._isReady = !0;
            });
        }
        return GoogleAnalyticsClient.prototype.setUserId = function(userId) {
            /^-/.test(userId) || this.ga("set", "userId", userId);
        }, GoogleAnalyticsClient.prototype.ga = function() {
            for (var _ = [], _i = 0; _i < arguments.length; _i++) _[_i] = arguments[_i];
            this._isReady ? ga.apply(null, arguments) : this._gaQueue.push(arguments);
        }, GoogleAnalyticsClient;
    }();
    exports.GoogleAnalyticsClient = GoogleAnalyticsClient;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Logging = __webpack_require__(665);
    exports.Logging = Logging;
    var LoggingImpl = __webpack_require__(1145);
    exports.LoggingImpl = LoggingImpl;
    var TimeSeries = __webpack_require__(1147);
    exports.TimeSeries = TimeSeries;
    var TimeSeriesImpl = __webpack_require__(203);
    exports.TimeSeriesImpl = TimeSeriesImpl;
    var utils_1 = __webpack_require__(152);
    exports.EventProps = utils_1.EventProps, function(Monitoring) {
        var Logging = function() {
            function Logging() {}
            return Object.defineProperty(Logging, "root", {
                get: function() {
                    return LoggingImpl.LoggingConfig.getRootLogger();
                },
                enumerable: !0,
                configurable: !0
            }), Logging.getLogger = function(name, level) {
                return Logging.root.getLogger(name, level);
            }, Logging;
        }();
        Monitoring.Logging = Logging;
        var TimeSeries = function() {
            function TimeSeries() {}
            return Object.defineProperty(TimeSeries, "root", {
                get: function() {
                    return TimeSeriesImpl.MetricsConfig.getRootMetric();
                },
                enumerable: !0,
                configurable: !0
            }), TimeSeries;
        }();
        Monitoring.TimeSeries = TimeSeries;
    }(exports.Monitoring || (exports.Monitoring = {}));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var tslib_1 = __webpack_require__(204), utils_1 = __webpack_require__(152), log4ts_1 = __webpack_require__(665), utils_2 = __webpack_require__(152), crash_logger_1 = __webpack_require__(1146), ring_buffer_1 = __webpack_require__(666), TreeContext = function() {
        function TreeContext(parent) {
            this.parent = parent, this.context = void 0;
        }
        return TreeContext.prototype.get = function() {
            var parentContext = this.parent && this.parent.get(), context = this.context;
            return parentContext || context ? Object.assign({}, parentContext, context) : void 0;
        }, TreeContext.prototype.add = function(ctx) {
            this.context = Object.assign({}, this.context, ctx);
        }, TreeContext.prototype.remove = function(keys) {
            var _this = this;
            this.context && keys.forEach(function(k) {
                k in _this.context && delete _this.context[k];
            });
        }, TreeContext.prototype.clear = function() {
            this.context = void 0;
        }, TreeContext;
    }();
    exports.TreeContext = TreeContext;
    var AbstractLogger = function() {
        function AbstractLogger(name, level, context) {
            this.name = name, this.level = level, this.context = context, utils_1.validateName(name);
        }
        return AbstractLogger.prototype.isEnabled = function(level) {
            return level >= this.level;
        }, AbstractLogger.prototype.handler = function(message, extra) {
            var _this = this;
            return {
                trace: function(error) {
                    throw _this.trace(message, error, extra), error;
                },
                debug: function(error) {
                    throw _this.debug(message, error, extra), error;
                },
                info: function(error) {
                    throw _this.info(message, error, extra), error;
                },
                warn: function(error) {
                    throw _this.warn(message, error, extra), error;
                },
                error: function(error) {
                    throw _this.error(message, error, extra), error;
                },
                fatal: function(error) {
                    throw _this.fatal(message, error, extra), error;
                }
            };
        }, AbstractLogger.prototype.trace = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.TRACE, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.debug = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.DEBUG, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.info = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.INFO, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.warn = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.WARN, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.error = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.ERROR, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.fatal = function(message, exceptionOrExtra, extra) {
            this.log(log4ts_1.LogLevel.FATAL, message, exceptionOrExtra, extra);
        }, AbstractLogger.prototype.log = function(level, message, exceptionOrExtra, extra) {
            this.isEnabled(level) && (exceptionOrExtra && extra || utils_2.ErrorLike.isErrorLike(exceptionOrExtra) ? this.logImpl(level, message, exceptionOrExtra, extra) : this.logImpl(level, message, void 0, extra || exceptionOrExtra));
        }, AbstractLogger;
    }();
    exports.AbstractLogger = AbstractLogger;
    var LogEvent = function() {
        return function(level, message, logger, timestamp, exception, extra, context) {
            this.level = level, this.message = message, this.logger = logger, this.timestamp = timestamp, 
            this.exception = exception, this.extra = extra, this.context = context;
        };
    }();
    exports.LogEvent = LogEvent;
    var SimpleLogger = function(_super) {
        function SimpleLogger(name, level, appender, context) {
            var _this = _super.call(this, name, level, context || new TreeContext()) || this;
            return _this.appender = appender, _this;
        }
        return tslib_1.__extends(SimpleLogger, _super), SimpleLogger.prototype.getLogger = function(name, level) {
            return new SimpleLogger(this.name + "." + name, level || this.level, this.appender, new TreeContext(this.context));
        }, SimpleLogger.prototype.logImpl = function(level, message, exception, extra) {
            var event = new LogEvent(level, message, this.name, Date.now(), exception, extra, this.context.get());
            try {
                this.appender(event);
            } catch (exception) {
                console.trace("Failed processing log event", exception);
                try {
                    ConsoleLogger.printToConsole(event);
                } catch (e) {
                    console.error("No luck. Can't print the event", e);
                }
            }
        }, SimpleLogger;
    }(AbstractLogger);
    exports.SimpleLogger = SimpleLogger;
    var ConsoleLogger = function(_super) {
        function ConsoleLogger(name, level, context) {
            return _super.call(this, name, level, ConsoleLogger.printToConsole, context) || this;
        }
        return tslib_1.__extends(ConsoleLogger, _super), ConsoleLogger.printToConsole = function(event) {
            console.log;
            (event.level <= log4ts_1.LogLevel.TRACE || event.level <= log4ts_1.LogLevel.DEBUG ? console.debug || console.log : event.level <= log4ts_1.LogLevel.INFO ? console.log : event.level <= log4ts_1.LogLevel.WARN ? console.warn : console.error).apply(console, [ "[" + event.logger + "]: " + log4ts_1.LogLevel[event.level] + " : " + event.message, event.exception, event.extra ].filter(function(x) {
                return !!x;
            }));
        }, ConsoleLogger;
    }(SimpleLogger);
    exports.ConsoleLogger = ConsoleLogger;
    var DummyFelogClient = function() {
        function DummyFelogClient() {}
        return DummyFelogClient.prototype.append = function(_1) {
            return Promise.resolve();
        }, DummyFelogClient;
    }();
    exports.DummyFelogClient = DummyFelogClient;
    var FelogClientBase = function() {
        function FelogClientBase(_appName, _appVersion, _env, _fetch, _wrapExtra) {
            void 0 === _wrapExtra && (_wrapExtra = !0), this._appName = _appName, this._appVersion = _appVersion, 
            this._env = _env, this._fetch = _fetch, this._wrapExtra = _wrapExtra;
        }
        return FelogClientBase.prototype.append = function(event) {
            return this._fetch(this._prepareData(event));
        }, FelogClientBase.toObject = function(obj) {
            return null == obj || obj instanceof Object && !Array.isArray(obj) ? obj && obj.toJSON ? obj.toJSON() : obj : {
                details: obj
            };
        }, FelogClientBase.prototype._parseException = function(ex) {
            if (ex) {
                var _a = FelogClientBase.toObject(ex), _b = _a.name, name_1 = void 0 === _b ? "UnknownError" : _b, _c = _a.message, message = void 0 === _c ? "Unknown error message" : _c, stack = _a.stack, exceptionDetails = tslib_1.__rest(_a, [ "name", "message", "stack" ]);
                return {
                    exceptionPart: {
                        exception: {
                            name: name_1,
                            message: message,
                            stack: stack
                        }
                    },
                    exceptionDetailsPart: Object.keys(exceptionDetails).length > 0 ? {
                        exceptionDetails: exceptionDetails
                    } : {}
                };
            }
            return {
                exceptionPart: {},
                exceptionDetailsPart: {}
            };
        }, FelogClientBase.prototype._prepareData = function(event) {
            var contextPart = event.context ? {
                context: event.context
            } : {}, _a = this._parseException(event.exception), exceptionPart = _a.exceptionPart, exceptionDetailsPart = _a.exceptionDetailsPart, extraObject = FelogClientBase.toObject(event.extra), details = JSON.stringify(this._wrapExtra ? Object.assign({}, exceptionDetailsPart, extraObject) : exceptionDetailsPart), data = Object.assign({
                message: event.message,
                logger: event.logger,
                level: log4ts_1.LogLevel[event.level],
                application: this._appName,
                version: this._appVersion,
                env: this._env
            }, contextPart, exceptionPart, "{}" !== details && {
                details: details
            }, !this._wrapExtra && extraObject && {
                extra: extraObject
            });
            return JSON.stringify(data, null, "");
        }, FelogClientBase;
    }();
    exports.FelogClientBase = FelogClientBase;
    var PostFelogClient = function(_super) {
        function PostFelogClient(url, appName, appVersion, env, fetch, wrapExtra) {
            return void 0 === wrapExtra && (wrapExtra = !0), _super.call(this, appName, appVersion, env, function(body) {
                return fetch(url, {
                    method: "POST",
                    cache: "no-cache",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: body
                }).then(function() {});
            }, wrapExtra) || this;
        }
        return tslib_1.__extends(PostFelogClient, _super), PostFelogClient;
    }(FelogClientBase);
    exports.PostFelogClient = PostFelogClient;
    var GetFelogClient = function(_super) {
        function GetFelogClient(url, appName, appVersion, env, fetch, wrapExtra) {
            void 0 === wrapExtra && (wrapExtra = !0);
            var baseUrl = url + "/log?json=";
            return _super.call(this, appName, appVersion, env, function(data) {
                return fetch(baseUrl + encodeURIComponent(data), {
                    mode: "no-cors",
                    method: "get",
                    cache: "no-cache"
                }).then(function() {});
            }, wrapExtra) || this;
        }
        return tslib_1.__extends(GetFelogClient, _super), GetFelogClient;
    }(FelogClientBase);
    exports.GetFelogClient = GetFelogClient;
    var DefaultLogAppender = function() {
        function DefaultLogAppender() {}
        return DefaultLogAppender.createRootLogger = function(name, appendLevel, appender, crashAppender, copyToConsole) {
            void 0 === copyToConsole && (copyToConsole = !1);
            var defaultSink = function(event) {
                event.level >= appendLevel && (copyToConsole && ConsoleLogger.printToConsole(event), 
                appender.append(event).catch(DefaultLogAppender._onError));
            }, rootLoggerContext = new TreeContext(), sink = defaultSink;
            if (crashAppender) {
                var crashLogger = new SimpleLogger(name + ".crashLogs", log4ts_1.LogLevel.TRACE, function(event) {
                    crashAppender.append(event).catch(DefaultLogAppender._onError);
                }, new TreeContext(rootLoggerContext));
                sink = new crash_logger_1.CrashLogWrapper(500, log4ts_1.LogLevel.ERROR, defaultSink, crashLogger).sink;
            }
            return new SimpleLogger(name, appendLevel, sink, rootLoggerContext);
        }, DefaultLogAppender._onError = function(error) {
            return ConsoleLogger.printToConsole(new LogEvent(log4ts_1.LogLevel.WARN, "Error while logging message to the server.", "Fallback", 0, void 0, error));
        }, DefaultLogAppender;
    }();
    exports.DefaultLogAppender = DefaultLogAppender;
    var QItem = function() {
        return function(event) {
            var _this = this;
            this.event = event, this.promise = new Promise(function(resolve, __reject) {
                _this.resolve = resolve;
            }).then(function() {});
        };
    }(), DEFAULT_LOG_QUEUE_SIZE = 300, DEFAULT_RETRY_INTERVAL = 1e4, LogQueue = function() {
        function LogQueue(_sink, size, _retryInterval) {
            void 0 === size && (size = DEFAULT_LOG_QUEUE_SIZE), void 0 === _retryInterval && (_retryInterval = DEFAULT_RETRY_INTERVAL), 
            this._sink = _sink, this._retryInterval = _retryInterval, this._currentItem = null, 
            this._skippedCounter = null, this._buffer = new ring_buffer_1.RingBuffer(size, !1);
        }
        return LogQueue.prototype.append = function(event) {
            if (this._buffer.isFull) return this._incSkippedCounter(), Promise.reject(new Error("Outgoing message buffer is full"));
            var item = new QItem(event);
            return this._buffer.push(item), this._doAppend(), item.promise;
        }, LogQueue.prototype._incSkippedCounter = function() {
            this._skippedCounter || (this._skippedCounter = new LogEvent(log4ts_1.LogLevel.WARN, "Messages was skipped due to buffer overflow", "log4ts_impl.LogQueue", Date.now(), void 0, {
                count: 0
            })), this._skippedCounter.extra.count++;
        }, LogQueue.prototype._doAppend = function() {
            var _this = this;
            if (!this._buffer.isEmpty && !this._currentItem) {
                var item = this._buffer.first, sinkPromise = this._sink.append(item.event);
                this._currentItem = item, sinkPromise.then(function() {
                    item.resolve();
                    var i = _this._buffer.pop();
                    if (i !== item && i === _this._currentItem) throw new Error("Illegal state");
                    _this._currentItem = null, _this._skippedCounter && (_this.append(_this._skippedCounter), 
                    _this._skippedCounter = null), _this._doAppend();
                }).catch(function(__error) {
                    _this._retryAppend(item);
                });
            }
        }, LogQueue.prototype._retryAppend = function(item) {
            var _this = this;
            setTimeout(function() {
                var extra = item.event.extra || {};
                extra.appendRetries || (extra = item.event.extra = Object.assign({
                    appendRetries: 1
                }, FelogClientBase.toObject(extra))), ++extra.appendRetries, _this._currentItem = null, 
                _this._doAppend();
            }, this._retryInterval);
        }, LogQueue;
    }();
    exports.LogQueue = LogQueue;
    var LoggingConfig = function() {
        function LoggingConfig() {}
        return LoggingConfig.getRootLogger = function() {
            return LoggingConfig._rootLogger || (LoggingConfig._rootLogger = LoggingConfig._createDefaultRootLogger(), 
            LoggingConfig._rootLogger.warn("Using DEFAULT root logger")), LoggingConfig._rootLogger;
        }, LoggingConfig.configure = function(rootLogger) {
            LoggingConfig._rootLogger = rootLogger, LoggingConfig._rootLogger.debug("ROOT logger changed", rootLogger);
        }, LoggingConfig._createDefaultRootLogger = function() {
            return new ConsoleLogger("DEFAULT", log4ts_1.LogLevel.DEBUG);
        }, LoggingConfig;
    }();
    exports.LoggingConfig = LoggingConfig;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var ring_buffer_1 = __webpack_require__(666), CrashLogWrapper = function() {
        function CrashLogWrapper(cacheSize, trigger, _eventsSink, _crashLogger) {
            var _this = this;
            this._eventsSink = _eventsSink, this._crashLogger = _crashLogger, this._crashLogged = !1, 
            this.sink = function(event) {
                _this._buffer.push(event), _this._eventsSink(event), _this._trigger(event) && _this._sendCrashLog(event);
            }, this._buffer = new ring_buffer_1.RingBuffer(cacheSize, !0), this._trigger = "function" == typeof trigger ? trigger : function(event) {
                return event.level >= trigger;
            };
        }
        return Object.defineProperty(CrashLogWrapper.prototype, "logs", {
            get: function() {
                return this._buffer.toArray();
            },
            enumerable: !0,
            configurable: !0
        }), CrashLogWrapper.prototype._sendCrashLog = function(triggeredBy) {
            if (!this._crashLogged || this._buffer.size > this._buffer.capacity / 2) {
                var crashLog = void 0;
                try {
                    crashLog = JSON.stringify(this.logs, void 0, 0);
                } catch (err) {
                    crashLog = err;
                }
                this._crashLogger.log(triggeredBy.level, "CrashLog", {
                    events: crashLog,
                    first: !this._crashLogged,
                    trigger: {
                        message: triggeredBy.message,
                        logger: triggeredBy.logger
                    }
                }), this._crashLogged = !0, this._buffer.clear();
            }
        }, CrashLogWrapper;
    }();
    exports.CrashLogWrapper = CrashLogWrapper;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
}, function(module, exports) {
    !function() {
        var $c = function(a) {
            this.w = a || [];
        };
        $c.prototype.set = function(a) {
            this.w[a] = !0;
        }, $c.prototype.encode = function() {
            for (var a = [], b = 0; b < this.w.length; b++) this.w[b] && (a[Math.floor(b / 6)] ^= 1 << b % 6);
            for (b = 0; b < a.length; b++) a[b] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".charAt(a[b] || 0);
            return a.join("") + "~";
        };
        var vd = new $c();
        function J(a) {
            vd.set(a);
        }
        var Td = function(a) {
            a = Dd(a), a = new $c(a);
            for (var b = vd.w.slice(), c = 0; c < a.w.length; c++) b[c] = b[c] || a.w[c];
            return new $c(b).encode();
        }, Dd = function(a) {
            return a = a.get(Gd), ka(a) || (a = []), a;
        }, ea = function(a) {
            return "function" == typeof a;
        }, ka = function(a) {
            return "[object Array]" == Object.prototype.toString.call(Object(a));
        }, qa = function(a) {
            return null != a && -1 < (a.constructor + "").indexOf("String");
        }, D = function(a, b) {
            return 0 == a.indexOf(b);
        }, sa = function(a) {
            return a ? a.replace(/^[\s\xa0]+|[\s\xa0]+$/g, "") : "";
        }, ra = function() {
            for (var a = O.navigator.userAgent + (M.cookie ? M.cookie : "") + (M.referrer ? M.referrer : ""), b = a.length, c = O.history.length; 0 < c; ) a += c-- ^ b++;
            return [ hd() ^ 2147483647 & La(a), Math.round(new Date().getTime() / 1e3) ].join(".");
        }, ta = function(a) {
            var b = M.createElement("img");
            return b.width = 1, b.height = 1, b.src = a, b;
        }, ua = function() {}, K = function(a) {
            return encodeURIComponent instanceof Function ? encodeURIComponent(a) : (J(28), 
            a);
        }, L = function(a, b, c, d) {
            try {
                a.addEventListener ? a.addEventListener(b, c, !!d) : a.attachEvent && a.attachEvent("on" + b, c);
            } catch (e) {
                J(27);
            }
        }, f = /^[\w\-:/.?=&%!]+$/, wa = function(a, b, c) {
            a && (c ? (c = "", b && f.test(b) && (c = ' id="' + b + '"'), f.test(a) && M.write("<script" + c + ' src="' + a + '"><\/script>')) : ((c = M.createElement("script")).type = "text/javascript", 
            c.async = !0, c.src = a, b && (c.id = b), (a = M.getElementsByTagName("script")[0]).parentNode.insertBefore(c, a)));
        }, be = function(a, b) {
            return E(M.location[b ? "href" : "search"], a);
        }, E = function(a, b) {
            return (a = a.match("(?:&|#|\\?)" + K(b).replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1") + "=([^&#]*)")) && 2 == a.length ? a[1] : "";
        }, xa = function() {
            var a = "" + M.location.hostname;
            return 0 == a.indexOf("www.") ? a.substring(4) : a;
        }, de = function(a, b) {
            var c = a.indexOf(b);
            return (5 == c || 6 == c) && ("/" == (a = a.charAt(c + b.length)) || "?" == a || "" == a || ":" == a);
        }, za = function(a, b) {
            if (1 == b.length && null != b[0] && "object" == typeof b[0]) return b[0];
            for (var c = {}, d = Math.min(a.length + 1, b.length), e = 0; e < d; e++) {
                if ("object" == typeof b[e]) {
                    for (var g in b[e]) b[e].hasOwnProperty(g) && (c[g] = b[e][g]);
                    break;
                }
                e < a.length && (c[a[e]] = b[e]);
            }
            return c;
        }, ee = function() {
            this.keys = [], this.values = {}, this.m = {};
        };
        ee.prototype.set = function(a, b, c) {
            this.keys.push(a), c ? this.m[":" + a] = b : this.values[":" + a] = b;
        }, ee.prototype.get = function(a) {
            return this.m.hasOwnProperty(":" + a) ? this.m[":" + a] : this.values[":" + a];
        }, ee.prototype.map = function(a) {
            for (var b = 0; b < this.keys.length; b++) {
                var c = this.keys[b], d = this.get(c);
                d && a(c, d);
            }
        };
        var oc, Fa, Ga, fb, Ab, O = window, M = document, va = function(a, b) {
            return setTimeout(a, b);
        }, F = window, Ea = document, G = function(a) {
            var b = F._gaUserPrefs;
            if (b && b.ioo && b.ioo() || a && !0 === F["ga-disable-" + a]) return !0;
            try {
                var c = F.external;
                if (c && c._gaUserPrefs && "oo" == c._gaUserPrefs) return !0;
            } catch (g) {}
            a = [], b = Ea.cookie.split(";"), c = /^\s*AMP_TOKEN=\s*(.*?)\s*$/;
            for (var d = 0; d < b.length; d++) {
                var e = b[d].match(c);
                e && a.push(e[1]);
            }
            for (b = 0; b < a.length; b++) if ("$OPT_OUT" == decodeURIComponent(a[b])) return !0;
            return !1;
        }, Ca = function(a) {
            var b = [], c = M.cookie.split(";");
            a = new RegExp("^\\s*" + a + "=\\s*(.*?)\\s*$");
            for (var d = 0; d < c.length; d++) {
                var e = c[d].match(a);
                e && b.push(e[1]);
            }
            return b;
        }, zc = function(a, b, c, d, e, g) {
            if (!(e = !G(e) && !(eb.test(M.location.hostname) || "/" == c && vc.test(d)))) return !1;
            if (b && 1200 < b.length && (b = b.substring(0, 1200)), c = a + "=" + b + "; path=" + c + "; ", 
            g && (c += "expires=" + new Date(new Date().getTime() + g).toGMTString() + "; "), 
            d && "none" !== d && (c += "domain=" + d + ";"), d = M.cookie, M.cookie = c, !(d = d != M.cookie)) a: {
                for (a = Ca(a), d = 0; d < a.length; d++) if (b == a[d]) {
                    d = !0;
                    break a;
                }
                d = !1;
            }
            return d;
        }, Cc = function(a) {
            return encodeURIComponent ? encodeURIComponent(a).replace(/\(/g, "%28").replace(/\)/g, "%29") : a;
        }, vc = /^(www\.)?google(\.com?)?(\.[a-z]{2})?$/, eb = /(^|\.)doubleclick\.net$/i, Id = /^.*Version\/?(\d+)[^\d].*$/i, ne = function() {
            if (void 0 !== O.__ga4__) return O.__ga4__;
            if (void 0 === oc) {
                var a = O.navigator.userAgent;
                if (a) {
                    var b = a;
                    try {
                        b = decodeURIComponent(a);
                    } catch (c) {}
                    (a = !(0 <= b.indexOf("Chrome") || 0 <= b.indexOf("CriOS") || !(0 <= b.indexOf("Safari/") || 0 <= b.indexOf("Safari,")))) && (a = 11 <= ((b = Id.exec(b)) ? Number(b[1]) : -1)), 
                    oc = a;
                } else oc = !1;
            }
            return oc;
        }, ja = /^https?:\/\/[^/]*cdn\.ampproject\.org\//, Ub = [], ic = function() {
            Z.D([ ua ]);
        }, tc = function(a, b) {
            var c = Ca("AMP_TOKEN");
            return 1 < c.length ? (J(55), !1) : "$OPT_OUT" == (c = decodeURIComponent(c[0] || "")) || "$ERROR" == c || G(b) ? (J(62), 
            !1) : ja.test(M.referrer) || "$NOT_FOUND" != c ? void 0 !== Ab ? (J(56), va(function() {
                a(Ab);
            }, 0), !0) : Fa ? (Ub.push(a), !0) : "$RETRIEVING" == c ? (J(57), va(function() {
                tc(a, b);
            }, 1e4), !0) : (Fa = !0, c && "$" != c[0] || (xc("$RETRIEVING", 3e4), setTimeout(Mc, 3e4), 
            c = ""), !!Pc(c, b) && (Ub.push(a), !0)) : (J(68), !1);
        }, Pc = function(a, b, c) {
            if (!window.JSON) return J(58), !1;
            var d = O.XMLHttpRequest;
            if (!d) return J(59), !1;
            var e = new d();
            return "withCredentials" in e ? (e.open("POST", (c || "https://ampcid.google.com/v1/publisher:getClientId") + "?key=AIzaSyA65lEHUEizIsNtlbNo-l2K18dT680nsaM", !0), 
            e.withCredentials = !0, e.setRequestHeader("Content-Type", "text/plain"), e.onload = function() {
                if (Fa = !1, 4 == e.readyState) {
                    try {
                        200 != e.status && (J(61), Qc("", "$ERROR", 3e4));
                        var d = JSON.parse(e.responseText);
                        d.optOut ? (J(63), Qc("", "$OPT_OUT", 31536e6)) : d.clientId ? Qc(d.clientId, d.securityToken, 31536e6) : !c && d.alternateUrl ? (Ga && clearTimeout(Ga), 
                        Fa = !0, Pc(a, b, d.alternateUrl)) : (J(64), Qc("", "$NOT_FOUND", 36e5));
                    } catch (ca) {
                        J(65), Qc("", "$ERROR", 3e4);
                    }
                    e = null;
                }
            }, d = {
                originScope: "AMP_ECID_GOOGLE"
            }, a && (d.securityToken = a), e.send(JSON.stringify(d)), Ga = va(function() {
                J(66), Qc("", "$ERROR", 3e4);
            }, 1e4), !0) : (J(60), !1);
        }, Mc = function() {
            Fa = !1;
        }, xc = function(a, b) {
            if (void 0 === fb) {
                fb = "";
                for (var c = id(), d = 0; d < c.length; d++) {
                    var e = c[d];
                    if (zc("AMP_TOKEN", encodeURIComponent(a), "/", e, "", b)) return void (fb = e);
                }
            }
            zc("AMP_TOKEN", encodeURIComponent(a), "/", fb, "", b);
        }, Qc = function(a, b, c) {
            for (Ga && clearTimeout(Ga), b && xc(b, c), Ab = a, b = Ub, Ub = [], c = 0; c < b.length; c++) b[c](a);
        }, oe = function() {
            return (Ba || "https:" == M.location.protocol ? "https:" : "http:") + "//www.google-analytics.com";
        }, ba = function(a, b, c) {
            if (c = c || ua, 2036 >= b.length) wc(a, b, c); else {
                if (!(8192 >= b.length)) throw ge("len", b.length), new function(a) {
                    this.name = "len", this.message = a + "-8192";
                }(b.length);
                x(a, b, c) || wd(a, b, c) || wc(a, b, c);
            }
        }, pe = function(a, b, c, d) {
            wd(a + "?" + b, "", d = d || ua, c);
        }, wc = function(a, b, c) {
            var d = ta(a + "?" + b);
            d.onload = d.onerror = function() {
                d.onload = null, d.onerror = null, c();
            };
        }, wd = function(a, b, c, d) {
            var e = O.XMLHttpRequest;
            if (!e) return !1;
            var g = new e();
            return "withCredentials" in g && (a = a.replace(/^http:/, "https:"), g.open("POST", a, !0), 
            g.withCredentials = !0, g.setRequestHeader("Content-Type", "text/plain"), g.onreadystatechange = function() {
                if (4 == g.readyState) {
                    if (d) try {
                        var a = g.responseText;
                        if (1 > a.length) ge("xhr", "ver", "0"), c(); else if ("1" != a.charAt(0)) ge("xhr", "ver", String(a.length)), 
                        c(); else if (3 < d.count++) ge("xhr", "tmr", "" + d.count), c(); else if (1 == a.length) c(); else {
                            var b = a.charAt(1);
                            if ("d" == b) pe("https://stats.g.doubleclick.net/j/collect", d.U, d, c); else if ("g" == b) {
                                var e = "https://www.google.%/ads/ga-audiences".replace("%", "com");
                                wc(e, d.google, c);
                                var w = a.substring(2);
                                if (w) if (/^[a-z.]{1,6}$/.test(w)) {
                                    var ha = "https://www.google.%/ads/ga-audiences".replace("%", w);
                                    wc(ha, d.google, ua);
                                } else ge("tld", "bcc", w);
                            } else ge("xhr", "brc", b), c();
                        }
                    } catch (ue) {
                        ge("xhr", "rsp"), c();
                    } else c();
                    g = null;
                }
            }, g.send(b), !0);
        }, x = function(a, b, c) {
            return !!O.navigator.sendBeacon && (!!O.navigator.sendBeacon(a, b) && (c(), !0));
        }, ge = function(a, b, c) {
            1 <= 100 * Math.random() || G("?") || (a = [ "t=error", "_e=" + a, "_v=j67", "sr=1" ], 
            b && a.push("_f=" + b), c && a.push("_m=" + K(c.substring(0, 100))), a.push("aip=1"), 
            a.push("z=" + hd()), wc("https://www.google-analytics.com/u/d", a.join("&"), ua));
        }, h = function(a) {
            var b = O.gaData = O.gaData || {};
            return b[a] = b[a] || {};
        }, Ha = function() {
            this.M = [];
        };
        function Ja(a) {
            if (100 != a.get(Ka) && La(P(a, Q)) % 1e4 >= 100 * R(a, Ka)) throw "abort";
        }
        function Ma(a) {
            if (G(P(a, Na))) throw "abort";
        }
        function Oa() {
            var a = M.location.protocol;
            if ("http:" != a && "https:" != a) throw "abort";
        }
        function Pa(a) {
            try {
                O.navigator.sendBeacon ? J(42) : O.XMLHttpRequest && "withCredentials" in new O.XMLHttpRequest() && J(40);
            } catch (c) {}
            a.set(ld, Td(a), !0), a.set(Ac, R(a, Ac) + 1);
            var b = [];
            Qa.map(function(c, d) {
                d.F && (null != (c = a.get(c)) && c != d.defaultValue && ("boolean" == typeof c && (c *= 1), 
                b.push(d.F + "=" + K("" + c))));
            }), b.push("z=" + Bd()), a.set(Ra, b.join("&"), !0);
        }
        function Sa(a) {
            var b = P(a, gd) || oe() + "/collect", c = a.get(qe), d = P(a, fa);
            if (!d && a.get(Vd) && (d = "beacon"), c) pe(b, P(a, Ra), c, a.get(Ia)); else if (d) {
                c = d, d = P(a, Ra);
                var e = a.get(Ia);
                e = e || ua, "image" == c ? wc(b, d, e) : "xhr" == c && wd(b, d, e) || "beacon" == c && x(b, d, e) || ba(b, d, e);
            } else ba(b, P(a, Ra), a.get(Ia));
            b = a.get(Na), c = (b = h(b)).hitcount, b.hitcount = c ? c + 1 : 1, b = a.get(Na), 
            delete h(b).pending_experiments, a.set(Ia, ua, !0);
        }
        function Hc(a) {
            (O.gaData = O.gaData || {}).expId && a.set(Nc, (O.gaData = O.gaData || {}).expId), 
            (O.gaData = O.gaData || {}).expVar && a.set(Oc, (O.gaData = O.gaData || {}).expVar);
            var b = a.get(Na);
            if (b = h(b).pending_experiments) {
                var c = [];
                for (d in b) b.hasOwnProperty(d) && b[d] && c.push(encodeURIComponent(d) + "." + encodeURIComponent(b[d]));
                var d = c.join("!");
            } else d = void 0;
            d && a.set(m, d, !0);
        }
        function cd() {
            if (O.navigator && "preview" == O.navigator.loadPurpose) throw "abort";
        }
        function yd(a) {
            var b = O.gaDevIds;
            ka(b) && 0 != b.length && a.set("&did", b.join(","), !0);
        }
        function vb(a) {
            if (!a.get(Na)) throw "abort";
        }
        Ha.prototype.add = function(a) {
            this.M.push(a);
        }, Ha.prototype.D = function(a) {
            try {
                for (var b = 0; b < this.M.length; b++) {
                    var c = a.get(this.M[b]);
                    c && ea(c) && c.call(O, a);
                }
            } catch (d) {}
            (b = a.get(Ia)) != ua && ea(b) && (a.set(Ia, ua, !0), setTimeout(b, 10));
        };
        var hd = function() {
            return Math.round(2147483647 * Math.random());
        }, Bd = function() {
            try {
                var a = new Uint32Array(1);
                return O.crypto.getRandomValues(a), 2147483647 & a[0];
            } catch (b) {
                return hd();
            }
        };
        function Ta(a) {
            var b = R(a, Ua);
            500 <= b && J(15);
            var c = P(a, Va);
            if ("transaction" != c && "item" != c) {
                c = R(a, Wa);
                var d = new Date().getTime(), e = R(a, Xa);
                if (0 == e && a.set(Xa, d), 0 < (e = Math.round(2 * (d - e) / 1e3)) && (c = Math.min(c + e, 20), 
                a.set(Xa, d)), 0 >= c) throw "abort";
                a.set(Wa, --c);
            }
            a.set(Ua, ++b);
        }
        var Ya = function() {
            this.data = new ee();
        }, Qa = new ee(), Za = [];
        Ya.prototype.get = function(a) {
            var b = $a(a), c = this.data.get(a);
            return b && null == c && (c = ea(b.defaultValue) ? b.defaultValue() : b.defaultValue), 
            b && b.Z ? b.Z(this, a, c) : c;
        };
        var P = function(a, b) {
            return null == (a = a.get(b)) ? "" : "" + a;
        }, R = function(a, b) {
            return null == (a = a.get(b)) || "" === a ? 0 : 1 * a;
        };
        Ya.prototype.set = function(a, b, c) {
            if (a) if ("object" == typeof a) for (var d in a) a.hasOwnProperty(d) && ab(this, d, a[d], c); else ab(this, a, b, c);
        };
        var ab = function(a, b, c, d) {
            if (null != c) switch (b) {
              case Na:
                wb.test(c);
            }
            var e = $a(b);
            e && e.o ? e.o(a, b, c, d) : a.data.set(b, c, d);
        }, bb = function(a, b, c, d, e) {
            this.name = a, this.F = b, this.Z = d, this.o = e, this.defaultValue = c;
        }, $a = function(a) {
            var b = Qa.get(a);
            if (!b) for (var c = 0; c < Za.length; c++) {
                var d = Za[c], e = d[0].exec(a);
                if (e) {
                    b = d[1](e), Qa.set(b.name, b);
                    break;
                }
            }
            return b;
        }, S = function(a, b, c, d, e) {
            return a = new bb(a, b, c, d, e), Qa.set(a.name, a), a.name;
        }, cb = function(a, b) {
            Za.push([ new RegExp("^" + a + "$"), b ]);
        }, T = function(a, b, c) {
            return S(a, b, c, void 0, db);
        }, db = function() {}, gb = qa(window.GoogleAnalyticsObject) && sa(window.GoogleAnalyticsObject) || "ga", jd = /^(?:utma\.)?\d+\.\d+$/, kd = /^amp-[\w.-]{22,64}$/, Ba = !1, hb = T("apiVersion", "v"), ib = T("clientVersion", "_v");
        S("anonymizeIp", "aip");
        var jb = S("adSenseId", "a"), Va = S("hitType", "t"), Ia = S("hitCallback"), Ra = S("hitPayload");
        S("nonInteraction", "ni"), S("currencyCode", "cu"), S("dataSource", "ds");
        var Vd = S("useBeacon", void 0, !1), fa = S("transport");
        S("sessionControl", "sc", ""), S("sessionGroup", "sg"), S("queueTime", "qt");
        var Ac = S("_s", "_s");
        S("screenName", "cd");
        var kb = S("location", "dl", ""), lb = S("referrer", "dr"), mb = S("page", "dp", "");
        S("hostname", "dh");
        var nb = S("language", "ul"), ob = S("encoding", "de");
        S("title", "dt", function() {
            return M.title || void 0;
        }), cb("contentGroup([0-9]+)", function(a) {
            return new bb(a[0], "cg" + a[1]);
        });
        var pb = S("screenColors", "sd"), qb = S("screenResolution", "sr"), rb = S("viewportSize", "vp"), sb = S("javaEnabled", "je"), tb = S("flashVersion", "fl");
        S("campaignId", "ci"), S("campaignName", "cn"), S("campaignSource", "cs"), S("campaignMedium", "cm"), 
        S("campaignKeyword", "ck"), S("campaignContent", "cc");
        var ub = S("eventCategory", "ec"), xb = S("eventAction", "ea"), yb = S("eventLabel", "el"), zb = S("eventValue", "ev"), Bb = S("socialNetwork", "sn"), Cb = S("socialAction", "sa"), Db = S("socialTarget", "st"), Eb = S("l1", "plt"), Fb = S("l2", "pdt"), Gb = S("l3", "dns"), Hb = S("l4", "rrt"), Ib = S("l5", "srt"), Jb = S("l6", "tcp"), Kb = S("l7", "dit"), Lb = S("l8", "clt"), Mb = S("timingCategory", "utc"), Nb = S("timingVar", "utv"), Ob = S("timingLabel", "utl"), Pb = S("timingValue", "utt");
        S("appName", "an"), S("appVersion", "av", ""), S("appId", "aid", ""), S("appInstallerId", "aiid", ""), 
        S("exDescription", "exd"), S("exFatal", "exf");
        var Nc = S("expId", "xid"), Oc = S("expVar", "xvar"), m = S("exp", "exp"), Rc = S("_utma", "_utma"), Sc = S("_utmz", "_utmz"), Tc = S("_utmht", "_utmht"), Ua = S("_hc", void 0, 0), Xa = S("_ti", void 0, 0), Wa = S("_to", void 0, 20);
        cb("dimension([0-9]+)", function(a) {
            return new bb(a[0], "cd" + a[1]);
        }), cb("metric([0-9]+)", function(a) {
            return new bb(a[0], "cm" + a[1]);
        }), S("linkerParam", void 0, void 0, function(a) {
            var b = a.get(Q), c = a.get(I) || "";
            if (b = "_ga=2." + K(pa(c + b, 0) + "." + c + "-" + b), (c = a.get(ce)) && a.get(je)) {
                var d = R(a, fe);
                1e3 * d + R(a, he) <= new Date().getTime() ? (J(76), a = "") : (J(44), a = "&_gac=1." + K([ pa(c, 0), d, c ].join(".")));
            } else a = "";
            return b + a;
        }, db);
        var ld = S("usage", "_u"), Gd = S("_um");
        S("forceSSL", void 0, void 0, function() {
            return Ba;
        }, function(a, b, c) {
            J(34), Ba = !!c;
        });
        var ed = S("_j1", "jid"), ia = S("_j2", "gjid");
        cb("\\&(.*)", function(a) {
            var b = new bb(a[0], a[1]), c = function(a) {
                var b;
                return Qa.map(function(c, d) {
                    d.F == a && (b = d);
                }), b && b.name;
            }(a[0].substring(1));
            return c && (b.Z = function(a) {
                return a.get(c);
            }, b.o = function(a, b, g, ca) {
                a.set(c, g, ca);
            }, b.F = void 0), b;
        });
        var Qb = T("_oot"), dd = S("previewTask"), Rb = S("checkProtocolTask"), md = S("validationTask"), Sb = S("checkStorageTask"), Uc = S("historyImportTask"), Tb = S("samplerTask"), Vb = S("_rlt"), Wb = S("buildHitTask"), Xb = S("sendHitTask"), Vc = S("ceTask"), zd = S("devIdTask"), Cd = S("timingTask"), Ld = S("displayFeaturesTask"), oa = S("customTask"), V = T("name"), Q = T("clientId", "cid"), n = T("clientIdTime"), xd = T("storedClientId"), Ad = S("userId", "uid"), Na = T("trackingId", "tid"), U = T("cookieName", void 0, "_ga"), W = T("cookieDomain"), Yb = T("cookiePath", void 0, "/"), Zb = T("cookieExpires", void 0, 63072e3), Hd = T("cookieUpdate", void 0, !0), $b = T("legacyCookieDomain"), Wc = T("legacyHistoryImport", void 0, !0), ac = T("storage", void 0, "cookie"), bc = T("allowLinker", void 0, !1), cc = T("allowAnchor", void 0, !0), Ka = T("sampleRate", "sf", 100), dc = T("siteSpeedSampleRate", void 0, 1), ec = T("alwaysSendReferrer", void 0, !1), I = T("_gid", "_gid"), la = T("_gcn"), Kd = T("useAmpClientId"), ce = T("_gclid"), fe = T("_gt"), he = T("_ge", void 0, 7776e6), ie = T("_gclsrc"), je = T("storeGac", void 0, !0), gd = S("transportUrl"), Md = S("_r", "_r"), qe = S("_dp");
        function X(a, b, c, d) {
            b[a] = function() {
                try {
                    return d && J(d), c.apply(this, arguments);
                } catch (e) {
                    throw ge("exc", a, e && e.name), e;
                }
            };
        }
        var gc = function(a) {
            var b = {};
            if (Ec(b) || Fc(b)) {
                var c = b[Eb];
                null == c || 1 / 0 == c || isNaN(c) || (0 < c ? (Y(b, Gb), Y(b, Jb), Y(b, Ib), Y(b, Fb), 
                Y(b, Hb), Y(b, Kb), Y(b, Lb), va(function() {
                    a(b);
                }, 10)) : L(O, "load", function() {
                    gc(a);
                }, !1));
            }
        }, Ec = function(a) {
            var b = O.performance || O.webkitPerformance;
            if (!(b = b && b.timing)) return !1;
            var c = b.navigationStart;
            return 0 != c && (a[Eb] = b.loadEventStart - c, a[Gb] = b.domainLookupEnd - b.domainLookupStart, 
            a[Jb] = b.connectEnd - b.connectStart, a[Ib] = b.responseStart - b.requestStart, 
            a[Fb] = b.responseEnd - b.responseStart, a[Hb] = b.fetchStart - c, a[Kb] = b.domInteractive - c, 
            a[Lb] = b.domContentLoadedEventStart - c, !0);
        }, Fc = function(a) {
            if (O.top != O) return !1;
            var b = O.external, c = b && b.onloadT;
            return b && !b.isValidLoadTime && (c = void 0), 2147483648 < c && (c = void 0), 
            0 < c && b.setPageReadyTime(), null != c && (a[Eb] = c, !0);
        }, Y = function(a, b) {
            var c = a[b];
            (isNaN(c) || 1 / 0 == c || 0 > c) && (a[b] = void 0);
        }, Fd = function(a) {
            return function(b) {
                if ("pageview" == b.get(Va) && !a.I) {
                    a.I = !0;
                    var c = function(a) {
                        var b = Math.min(R(a, dc), 100);
                        return !(La(P(a, Q)) % 100 >= b);
                    }(b), d = 0 < E(b.get(kb), "gclid").length;
                    (c || d) && gc(function(b) {
                        c && a.send("timing", b), d && a.send("adtiming", b);
                    });
                }
            };
        }, hc = !1, mc = function(a) {
            if ("cookie" == P(a, ac)) {
                if (a.get(Hd) || P(a, xd) != P(a, Q)) {
                    var b = 1e3 * R(a, Zb);
                    ma(a, Q, U, b);
                }
                if (ma(a, I, la, 864e5), a.get(je)) {
                    var c = a.get(ce);
                    if (c) {
                        var d = Math.min(R(a, he), 1e3 * R(a, Zb));
                        d = Math.min(d, 1e3 * R(a, fe) + d - new Date().getTime()), a.data.set(he, d), b = {};
                        var e = a.get(fe), g = a.get(ie), ca = kc(P(a, Yb)), l = lc(P(a, W)), k = P(a, Na);
                        g && "aw.ds" != g ? b && (b.ua = !0) : (c = [ "1", e, Cc(c) ].join("."), 0 < d && (b && (b.ta = !0), 
                        zc("_gac_" + Cc(k), c, ca, l, k, d))), le(b);
                    }
                } else J(75);
                (a = "none" === lc(P(a, W))) && (a = M.location.hostname, a = eb.test(a) || vc.test(a)), 
                a && J(30);
            }
        }, ma = function(a, b, c, d) {
            var e = nd(a, b);
            if (e) {
                c = P(a, c);
                var g = kc(P(a, Yb)), ca = lc(P(a, W)), l = P(a, Na);
                if ("auto" != ca) zc(c, e, g, ca, l, d) && (hc = !0); else {
                    J(32);
                    for (var k = id(), w = 0; w < k.length; w++) if (ca = k[w], a.data.set(W, ca), e = nd(a, b), 
                    zc(c, e, g, ca, l, d)) return void (hc = !0);
                    a.data.set(W, "auto");
                }
            }
        }, nc = function(a) {
            if ("cookie" == P(a, ac) && !hc && (mc(a), !hc)) throw "abort";
        }, Yc = function(a) {
            if (a.get(Wc)) {
                var b = P(a, W), c = P(a, $b) || xa(), d = Xc("__utma", c, b);
                d && (J(19), a.set(Tc, new Date().getTime(), !0), a.set(Rc, d.R), (b = Xc("__utmz", c, b)) && d.hash == b.hash && a.set(Sc, b.R));
            }
        }, nd = function(a, b) {
            b = Cc(P(a, b));
            var c = lc(P(a, W)).split(".").length;
            return 1 < (a = jc(P(a, Yb))) && (c += "-" + a), b ? [ "GA1", c, b ].join(".") : "";
        }, Xd = function(a, b) {
            return na(b, P(a, W), P(a, Yb));
        }, na = function(a, b, c) {
            if (!a || 1 > a.length) J(12); else {
                for (var d = [], e = 0; e < a.length; e++) {
                    var g = a[e], ca = g.split("."), l = ca.shift();
                    ("GA1" == l || "1" == l) && 1 < ca.length ? (1 == (g = ca.shift().split("-")).length && (g[1] = "1"), 
                    g[0] *= 1, g[1] *= 1, ca = {
                        H: g,
                        s: ca.join(".")
                    }) : ca = kd.test(g) ? {
                        H: [ 0, 0 ],
                        s: g
                    } : void 0, ca && d.push(ca);
                }
                if (1 == d.length) return J(13), d[0].s;
                if (0 != d.length) return J(14), 1 == (d = Gc(d, lc(b).split(".").length, 0)).length ? d[0].s : (1 < (d = Gc(d, jc(c), 1)).length && J(41), 
                d[0] && d[0].s);
                J(12);
            }
        }, Gc = function(a, b, c) {
            for (var g, d = [], e = [], ca = 0; ca < a.length; ca++) {
                var l = a[ca];
                l.H[c] == b ? d.push(l) : null == g || l.H[c] < g ? (e = [ l ], g = l.H[c]) : l.H[c] == g && e.push(l);
            }
            return 0 < d.length ? d : e;
        }, lc = function(a) {
            return 0 == a.indexOf(".") ? a.substr(1) : a;
        }, id = function() {
            var a = [], b = xa().split(".");
            if (4 == b.length) {
                var c = b[b.length - 1];
                if (parseInt(c, 10) == c) return [ "none" ];
            }
            for (c = b.length - 2; 0 <= c; c--) a.push(b.slice(c).join("."));
            return a.push("none"), a;
        }, kc = function(a) {
            return a ? (1 < a.length && a.lastIndexOf("/") == a.length - 1 && (a = a.substr(0, a.length - 1)), 
            0 != a.indexOf("/") && (a = "/" + a), a) : "/";
        }, jc = function(a) {
            return "/" == (a = kc(a)) ? 1 : a.split("/").length;
        }, le = function(a) {
            a.ta && J(77), a.na && J(74), a.pa && J(73), a.ua && J(69);
        };
        function Xc(a, b, c) {
            "none" == b && (b = "");
            var d = [], e = Ca(a);
            a = "__utma" == a ? 6 : 2;
            for (var g = 0; g < e.length; g++) {
                var ca = ("" + e[g]).split(".");
                ca.length >= a && d.push({
                    hash: ca[0],
                    R: e[g],
                    O: ca
                });
            }
            if (0 != d.length) return 1 == d.length ? d[0] : Zc(b, d) || Zc(c, d) || Zc(null, d) || d[0];
        }
        function Zc(a, b) {
            if (null == a) var c = a = 1; else c = La(a), a = La(D(a, ".") ? a.substring(1) : "." + a);
            for (var d = 0; d < b.length; d++) if (b[d].hash == c || b[d].hash == a) return b[d];
        }
        var od = new RegExp(/^https?:\/\/([^\/:]+)/), pd = /(.*)([?&#])(?:_ga=[^&#]*)(?:&?)(.*)/, me = /(.*)([?&#])(?:_gac=[^&#]*)(?:&?)(.*)/;
        function Ic(a, b) {
            var c = new Date(), d = O.navigator, e = d.plugins || [];
            for (a = [ a, d.userAgent, c.getTimezoneOffset(), c.getYear(), c.getDate(), c.getHours(), c.getMinutes() + b ], 
            b = 0; b < e.length; ++b) a.push(e[b].description);
            return La(a.join("."));
        }
        function pa(a, b) {
            var c = new Date(), d = O.navigator, e = c.getHours() + Math.floor((c.getMinutes() + b) / 60);
            return La([ a, d.userAgent, d.language || "", c.getTimezoneOffset(), c.getYear(), c.getDate() + Math.floor(e / 24), (24 + e) % 24, (60 + c.getMinutes() + b) % 60 ].join("."));
        }
        var Dc = function(a) {
            J(48), this.target = a, this.T = !1;
        };
        Dc.prototype.ca = function(a, b) {
            if (a.tagName) {
                if ("a" == a.tagName.toLowerCase()) return void (a.href && (a.href = qd(this, a.href, b)));
                if ("form" == a.tagName.toLowerCase()) return rd(this, a);
            }
            if ("string" == typeof a) return qd(this, a, b);
        };
        var qd = function(a, b, c) {
            var d = pd.exec(b);
            d && 3 <= d.length && (b = d[1] + (d[3] ? d[2] + d[3] : "")), (d = me.exec(b)) && 3 <= d.length && (b = d[1] + (d[3] ? d[2] + d[3] : "")), 
            a = a.target.get("linkerParam");
            var e = b.indexOf("?");
            return d = b.indexOf("#"), c ? b += (-1 == d ? "#" : "&") + a : (c = -1 == e ? "?" : "&", 
            b = -1 == d ? b + (c + a) : b.substring(0, d) + c + a + b.substring(d)), (b = b.replace(/&+_ga=/, "&_ga=")).replace(/&+_gac=/, "&_gac=");
        }, rd = function(a, b) {
            if (b && b.action) if ("get" == b.method.toLowerCase()) {
                a = a.target.get("linkerParam").split("&");
                for (var c = 0; c < a.length; c++) {
                    var d = a[c].split("="), e = d[1];
                    d = d[0];
                    for (var g = b.childNodes || [], ca = !1, l = 0; l < g.length; l++) if (g[l].name == d) {
                        g[l].setAttribute("value", e), ca = !0;
                        break;
                    }
                    ca || ((g = M.createElement("input")).setAttribute("type", "hidden"), g.setAttribute("name", d), 
                    g.setAttribute("value", e), b.appendChild(g));
                }
            } else "post" == b.method.toLowerCase() && (b.action = qd(a, b.action));
        };
        function sd(a, b) {
            if (b == M.location.hostname) return !1;
            for (var c = 0; c < a.length; c++) if (a[c] instanceof RegExp) {
                if (a[c].test(b)) return !0;
            } else if (0 <= b.indexOf(a[c])) return !0;
            return !1;
        }
        function ke(a, b) {
            return b != Ic(a, 0) && b != Ic(a, -1) && b != Ic(a, -2) && b != pa(a, 0) && b != pa(a, -1) && b != pa(a, -2);
        }
        Dc.prototype.S = function(a, b, c) {
            function d(c) {
                try {
                    c = c || O.event;
                    a: {
                        var d = c.target || c.srcElement;
                        for (c = 100; d && 0 < c; ) {
                            if (d.href && d.nodeName.match(/^a(?:rea)?$/i)) {
                                var g = d;
                                break a;
                            }
                            d = d.parentNode, c--;
                        }
                        g = {};
                    }
                    ("http:" == g.protocol || "https:" == g.protocol) && sd(a, g.hostname || "") && g.href && (g.href = qd(e, g.href, b));
                } catch (k) {
                    J(26);
                }
            }
            var e = this;
            this.T || (this.T = !0, L(M, "mousedown", d, !1), L(M, "keyup", d, !1)), c && L(M, "submit", function(b) {
                if ((b = (b = b || O.event).target || b.srcElement) && b.action) {
                    var c = b.action.match(od);
                    c && sd(a, c[1]) && rd(e, b);
                }
            });
        };
        var ad, p = /^(GTM|OPT)-[A-Z0-9]+$/, q = /;_gaexp=[^;]*/g, r = /;((__utma=)|([^;=]+=GAX?\d+\.))[^;]*/g, Aa = /^https?:\/\/[\w\-.]+\.google.com(:\d+)?\/optimize\/opt-launch\.html\?.*$/, Jd = function(a, b, c) {
            this.aa = b, (b = c) || (b = (b = P(a, V)) && "t0" != b ? Wd.test(b) ? "_gat_" + Cc(P(a, Na)) : "_gat_" + Cc(b) : "_gat"), 
            this.Y = b, this.ra = null;
        }, Pd = function(a, b, c) {
            b.get(c) || ("1" == Ca(a.Y)[0] ? b.set(c, "", !0) : b.set(c, "" + hd(), !0));
        }, Qd = function(a, b) {
            b.get(ed) && zc(a.Y, "1", b.get(Yb), b.get(W), b.get(Na), 6e4);
        }, re = function(a, b, c) {
            var d = new ee(), e = function(a) {
                $a(a).F && d.set($a(a).F, b.get(a));
            };
            e(hb), e(ib), e(Na), e(Q), e(ed), 0 != c && 1 != c || (e(Ad), e(ia), e(I)), d.set($a(ld).F, Td(b));
            var g = "";
            return d.map(function(a, b) {
                g += K(a) + "=", g += K("" + b) + "&";
            }), g += "z=" + hd(), 0 == c ? g = a.aa + g : 1 == c ? g = "t=dc&aip=1&_r=3&" + g : 2 == c && (g = "t=sr&aip=1&_r=4&slf_rd=1&" + g), 
            g;
        }, H = function(a, b) {
            return null === a.ra && (a.ra = 1 === function(a) {
                var c, b = new function() {
                    this.V = 100, this.$ = this.fa = !1, this.oa = "detourexp", this.ea = 1;
                }();
                if (b.fa && b.$) return 0;
                if (b.$ = !0, a) {
                    if (b.oa && void 0 !== a.get(b.oa)) return R(a, b.oa);
                    if (0 == a.get(dc)) return 0;
                }
                return 0 == b.V ? 0 : (void 0 === c && (c = Bd()), 0 == c % b.V ? Math.floor(c / b.V) % b.ea + 1 : 0);
            }(b), a.ra && J(33)), a.ra;
        }, Wd = /^gtm\d+$/, fd = function(a, b) {
            if (!(a = a.b).get("dcLoaded")) {
                var d, c = new $c(Dd(a));
                c.set(29), a.set(Gd, c.w), (b = b || {})[U] && (d = Cc(b[U])), function(a, b) {
                    var c = b.get(Wb);
                    b.set(Wb, function(b) {
                        Pd(a, b, ed), Pd(a, b, ia);
                        var d = c(b);
                        return Qd(a, b), d;
                    });
                    var d = b.get(Xb);
                    b.set(Xb, function(b) {
                        var c = d(b);
                        if (b.get(ed)) {
                            if (ne() !== H(a, b)) {
                                J(80);
                                var e = {
                                    U: re(a, b, 1),
                                    google: re(a, b, 2),
                                    count: 0
                                };
                                pe("https://stats.g.doubleclick.net/j/collect", e.U, e);
                            } else ta(re(a, b, 0));
                            b.set(ed, "", !0);
                        }
                        return c;
                    });
                }(b = new Jd(a, "https://stats.g.doubleclick.net/r/collect?t=dc&aip=1&_r=3&", d), a), 
                a.set("dcLoaded", !0);
            }
        }, Sd = function(a) {
            if (!a.get("dcLoaded") && "cookie" == a.get(ac)) {
                var b = new Jd(a);
                if (Pd(b, a, ed), Pd(b, a, ia), Qd(b, a), a.get(ed)) {
                    var c = ne() !== H(b, a);
                    a.set(Md, 1, !0), c ? (J(79), a.set(gd, oe() + "/j/collect", !0), a.set(qe, {
                        U: re(b, a, 1),
                        google: re(b, a, 2),
                        count: 0
                    }, !0)) : a.set(gd, oe() + "/r/collect", !0);
                }
            }
        }, wb = /^(UA|YT|MO|GP)-(\d+)-(\d+)$/, pc = function(a) {
            function b(a, b) {
                d.b.data.set(a, b);
            }
            function c(a, c) {
                b(a, c), d.filters.add(a);
            }
            var d = this;
            this.b = new Ya(), this.filters = new Ha(), b(V, a[V]), b(Na, sa(a[Na])), b(U, a[U]), 
            b(W, a[W] || xa()), b(Yb, a[Yb]), b(Zb, a[Zb]), b(Hd, a[Hd]), b($b, a[$b]), b(Wc, a[Wc]), 
            b(bc, a[bc]), b(cc, a[cc]), b(Ka, a[Ka]), b(dc, a[dc]), b(ec, a[ec]), b(ac, a[ac]), 
            b(Ad, a[Ad]), b(n, a[n]), b(Kd, a[Kd]), b(je, a[je]), b(hb, 1), b(ib, "j67"), c(Qb, Ma), 
            c(oa, ua), c(dd, cd), c(Rb, Oa), c(md, vb), c(Sb, nc), c(Uc, Yc), c(Tb, Ja), c(Vb, Ta), 
            c(Vc, Hc), c(zd, yd), c(Ld, Sd), c(Wb, Pa), c(Xb, Sa), c(Cd, Fd(this)), Kc(this.b), 
            Jc(this.b, a[Q]), this.b.set(jb, function() {
                var a = O.gaGlobal = O.gaGlobal || {};
                return a.hid = a.hid || hd();
            }()), function(a, b, c) {
                if (!ad) {
                    var d = M.location.hash, e = O.name, g = /^#?gaso=([^&]*)/;
                    (e = (d = (d = d && d.match(g) || e && e.match(g)) ? d[1] : Ca("GASO")[0] || "") && d.match(/^(?:!([-0-9a-z.]{1,40})!)?([-.\w]{10,1200})$/i)) && (zc("GASO", "" + d, c, b, a, 0), 
                    window._udo || (window._udo = b), window._utcp || (window._utcp = c), a = e[1], 
                    wa("https://www.google.com/analytics/web/inpage/pub/inpage.js?" + (a ? "prefix=" + a + "&" : "") + hd(), "_gasojs")), 
                    ad = !0;
                }
            }(this.b.get(Na), this.b.get(W), this.b.get(Yb));
        }, Jc = function(a, b) {
            var c = P(a, U);
            if (a.data.set(la, "_ga" == c ? "_gid" : c + "_gid"), "cookie" == P(a, ac)) {
                if (hc = !1, c = Ca(P(a, U)), !(c = Xd(a, c))) {
                    c = P(a, W);
                    var d = P(a, $b) || xa();
                    null != (c = Xc("__utma", d, c)) ? (J(10), c = c.O[1] + "." + c.O[2]) : c = void 0;
                }
                if (c && (hc = !0), d = c && !a.get(Hd)) if (2 != (d = c.split(".")).length) d = !1; else if (d = Number(d[1])) {
                    var e = R(a, Zb);
                    d = d + e < new Date().getTime() / 1e3;
                } else d = !1;
                if (d && (c = void 0), c && (a.data.set(xd, c), a.data.set(Q, c), c = Ca(P(a, la)), 
                (c = Xd(a, c)) && a.data.set(I, c)), a.get(je) && (c = a.get(ce), d = a.get(ie), 
                !c || d && "aw.ds" != d)) {
                    if (c = {}, M) {
                        d = [], e = M.cookie.split(";");
                        for (var g = /^\s*_gac_(UA-\d+-\d+)=\s*(.+?)\s*$/, ca = 0; ca < e.length; ca++) {
                            var l = e[ca].match(g);
                            l && d.push({
                                ja: l[1],
                                value: l[2]
                            });
                        }
                        if (e = {}, d && d.length) for (g = 0; g < d.length; g++) "1" != (ca = d[g].value.split("."))[0] || 3 != ca.length ? c && (c.na = !0) : ca[1] && (e[d[g].ja] ? c && (c.pa = !0) : e[d[g].ja] = [], 
                        e[d[g].ja].push({
                            timestamp: ca[1],
                            qa: ca[2]
                        }));
                        d = e;
                    } else d = {};
                    d = d[P(a, Na)], le(c), d && 0 != d.length && (c = d[0], a.data.set(fe, c.timestamp), 
                    a.data.set(ce, c.qa));
                }
            }
            if (a.get(Hd)) a: if (d = be("_ga", a.get(cc))) if (a.get(bc)) if (c = d.indexOf("."), 
            -1 == c) J(22); else {
                if (e = d.substring(0, c), c = (g = d.substring(c + 1)).indexOf("."), d = g.substring(0, c), 
                g = g.substring(c + 1), "1" == e) {
                    if (ke(c = g, d)) {
                        J(23);
                        break a;
                    }
                } else {
                    if ("2" != e) {
                        J(22);
                        break a;
                    }
                    if (e = "", 0 < (c = g.indexOf("-")) ? (e = g.substring(0, c), c = g.substring(c + 1)) : c = g.substring(1), 
                    ke(e + c, d)) {
                        J(53);
                        break a;
                    }
                    e && (J(2), a.data.set(I, e));
                }
                J(11), a.data.set(Q, c), (c = be("_gac", a.get(cc))) && ("1" != (c = c.split("."))[0] || 4 != c.length ? J(72) : ke(c[3], c[1]) ? J(71) : (a.data.set(ce, c[3]), 
                a.data.set(fe, c[2]), J(70)));
            } else J(21);
            b && (J(9), a.data.set(Q, K(b))), a.get(Q) || ((b = (b = O.gaGlobal && O.gaGlobal.vid) && -1 != b.search(jd) ? b : void 0) ? (J(17), 
            a.data.set(Q, b)) : (J(8), a.data.set(Q, ra()))), a.get(I) || (J(3), a.data.set(I, ra())), 
            mc(a);
        }, Kc = function(a) {
            var b = O.navigator, c = O.screen, d = M.location;
            if (a.set(lb, function(a, b) {
                var c = M.referrer;
                if (/^(https?|android-app):\/\//i.test(c)) {
                    if (a) return c;
                    if (a = "//" + M.location.hostname, !de(c, a)) return b && (b = a.replace(/\./g, "-") + ".cdn.ampproject.org", 
                    de(c, b)) ? void 0 : c;
                }
            }(a.get(ec), a.get(Kd))), d) {
                var e = d.pathname || "";
                "/" != e.charAt(0) && (J(31), e = "/" + e), a.set(kb, d.protocol + "//" + d.hostname + e + d.search);
            }
            c && a.set(qb, c.width + "x" + c.height), c && a.set(pb, c.colorDepth + "-bit"), 
            c = M.documentElement;
            var g = (e = M.body) && e.clientWidth && e.clientHeight, ca = [];
            if (c && c.clientWidth && c.clientHeight && ("CSS1Compat" === M.compatMode || !g) ? ca = [ c.clientWidth, c.clientHeight ] : g && (ca = [ e.clientWidth, e.clientHeight ]), 
            c = 0 >= ca[0] || 0 >= ca[1] ? "" : ca.join("x"), a.set(rb, c), a.set(tb, function() {
                var a, b;
                if ((b = (b = O.navigator) ? b.plugins : null) && b.length) for (var c = 0; c < b.length && !a; c++) {
                    var d = b[c];
                    -1 < d.name.indexOf("Shockwave Flash") && (a = d.description);
                }
                if (!a) try {
                    var e = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
                    a = e.GetVariable("$version");
                } catch (g) {}
                if (!a) try {
                    e = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6"), a = "WIN 6,0,21,0", e.AllowScriptAccess = "always", 
                    a = e.GetVariable("$version");
                } catch (g) {}
                if (!a) try {
                    a = (e = new ActiveXObject("ShockwaveFlash.ShockwaveFlash")).GetVariable("$version");
                } catch (g) {}
                return a && (e = a.match(/[\d]+/g)) && 3 <= e.length && (a = e[0] + "." + e[1] + " r" + e[2]), 
                a || void 0;
            }()), a.set(ob, M.characterSet || M.charset), a.set(sb, b && "function" == typeof b.javaEnabled && b.javaEnabled() || !1), 
            a.set(nb, (b && (b.language || b.browserLanguage) || "").toLowerCase()), a.data.set(ce, be("gclid", !0)), 
            a.data.set(ie, be("gclsrc", !0)), a.data.set(fe, Math.round(new Date().getTime() / 1e3)), 
            d && a.get(cc) && (b = M.location.hash)) {
                for (b = b.split(/[?&#]+/), d = [], c = 0; c < b.length; ++c) (D(b[c], "utm_id") || D(b[c], "utm_campaign") || D(b[c], "utm_source") || D(b[c], "utm_medium") || D(b[c], "utm_term") || D(b[c], "utm_content") || D(b[c], "gclid") || D(b[c], "dclid") || D(b[c], "gclsrc")) && d.push(b[c]);
                0 < d.length && (b = "#" + d.join("&"), a.set(kb, a.get(kb) + b));
            }
        };
        pc.prototype.get = function(a) {
            return this.b.get(a);
        }, pc.prototype.set = function(a, b) {
            this.b.set(a, b);
        };
        var qc = {
            pageview: [ mb ],
            event: [ ub, xb, yb, zb ],
            social: [ Bb, Cb, Db ],
            timing: [ Mb, Nb, Pb, Ob ]
        };
        pc.prototype.send = function(a) {
            if (!(1 > arguments.length)) {
                if ("string" == typeof arguments[0]) var b = arguments[0], c = [].slice.call(arguments, 1); else b = arguments[0] && arguments[0][Va], 
                c = arguments;
                b && ((c = za(qc[b] || [], c))[Va] = b, this.b.set(c, void 0, !0), this.filters.D(this.b), 
                this.b.data.m = {});
            }
        }, pc.prototype.ma = function(a, b) {
            var c = this;
            u(a, c, b) || (v(a, function() {
                u(a, c, b);
            }), y(String(c.get(V)), a, void 0, b, !0));
        };
        var Yd, Zd, $d, A, rc = function(a) {
            return "prerender" != M.visibilityState && (a(), !0);
        }, z = function(a) {
            if (!rc(a)) {
                J(16);
                var b = !1, c = function() {
                    if (!b && rc(a)) {
                        b = !0;
                        var d = c, e = M;
                        e.removeEventListener ? e.removeEventListener("visibilitychange", d, !1) : e.detachEvent && e.detachEvent("onvisibilitychange", d);
                    }
                };
                L(M, "visibilitychange", c);
            }
        }, td = /^(?:(\w+)\.)?(?:(\w+):)?(\w+)$/, sc = function(a) {
            if (ea(a[0])) this.u = a[0]; else {
                var b = td.exec(a[0]);
                if (null != b && 4 == b.length && (this.c = b[1] || "t0", this.K = b[2] || "", this.C = b[3], 
                this.a = [].slice.call(a, 1), this.K || (this.A = "create" == this.C, this.i = "require" == this.C, 
                this.g = "provide" == this.C, this.ba = "remove" == this.C), this.i && (3 <= this.a.length ? (this.X = this.a[1], 
                this.W = this.a[2]) : this.a[1] && (qa(this.a[1]) ? this.X = this.a[1] : this.W = this.a[1]))), 
                b = a[1], a = a[2], !this.C) throw "abort";
                if (this.i && (!qa(b) || "" == b)) throw "abort";
                if (this.g && (!qa(b) || "" == b || !ea(a))) throw "abort";
                if (ud(this.c) || ud(this.K)) throw "abort";
                if (this.g && "t0" != this.c) throw "abort";
            }
        };
        function ud(a) {
            return 0 <= a.indexOf(".") || 0 <= a.indexOf(":");
        }
        Yd = new ee(), $d = new ee(), A = new ee(), Zd = {
            ec: 45,
            ecommerce: 46,
            linkid: 47
        };
        var u = function(a, b, c) {
            b == N || b.get(V);
            var d = Yd.get(a);
            return !!ea(d) && (b.plugins_ = b.plugins_ || new ee(), !!b.plugins_.get(a) || (b.plugins_.set(a, new d(b, c || {})), 
            !0));
        }, y = function(a, b, c, d, e) {
            if (!ea(Yd.get(b)) && !$d.get(b)) {
                if (Zd.hasOwnProperty(b) && J(Zd[b]), p.test(b)) {
                    if (J(52), !(a = N.j(a))) return !0;
                    d = {
                        id: b,
                        B: (c = d || {}).dataLayer || "dataLayer",
                        ia: !!a.get("anonymizeIp"),
                        sync: e,
                        G: !1
                    }, a.get("&gtm") == b && (d.G = !0);
                    var g = String(a.get("name"));
                    "t0" != g && (d.target = g), G(String(a.get("trackingId"))) || (d.clientId = String(a.get(Q)), 
                    d.ka = Number(a.get(n)), c = c.palindrome ? r : q, c = (c = M.cookie.replace(/^|(; +)/g, ";").match(c)) ? c.sort().join("").substring(1) : void 0, 
                    d.la = c, d.qa = E(a.b.get(kb) || "", "gclid")), a = d.B, c = new Date().getTime(), 
                    O[a] = O[a] || [], c = {
                        "gtm.start": c
                    }, e || (c.event = "gtm.js"), O[a].push(c), c = function(a) {
                        function b(a, b) {
                            b && (c += "&" + a + "=" + K(b));
                        }
                        var c = "https://www.google-analytics.com/gtm/js?id=" + K(a.id);
                        return "dataLayer" != a.B && b("l", a.B), b("t", a.target), b("cid", a.clientId), 
                        b("cidt", a.ka), b("gac", a.la), b("aip", a.ia), a.sync && b("m", "sync"), b("cycle", a.G), 
                        a.qa && b("gclid", a.qa), Aa.test(M.referrer) && b("cb", String(hd())), c;
                    }(d);
                }
                !c && Zd.hasOwnProperty(b) ? (J(39), c = b + ".js") : J(43), c && (c && 0 <= c.indexOf("/") || (c = (Ba || "https:" == M.location.protocol ? "https:" : "http:") + "//www.google-analytics.com/plugins/ua/" + c), 
                a = (d = ae(c)).protocol, c = M.location.protocol, ("https:" == a || a == c || "http:" == a && "http:" == c) && B(d) && (wa(d.url, void 0, e), 
                $d.set(b, !0)));
            }
        }, v = function(a, b) {
            var c = A.get(a) || [];
            c.push(b), A.set(a, c);
        }, C = function(a, b) {
            Yd.set(a, b), b = A.get(a) || [];
            for (var c = 0; c < b.length; c++) b[c]();
            A.set(a, []);
        }, B = function(a) {
            var b = ae(M.location.href);
            return !!D(a.url, "https://www.google-analytics.com/gtm/js?id=") || !(a.query || 0 <= a.url.indexOf("?") || 0 <= a.path.indexOf("://")) && (a.host == b.host && a.port == b.port || (b = "http:" == a.protocol ? 80 : 443, 
            !("www.google-analytics.com" != a.host || (a.port || b) != b || !D(a.path, "/plugins/"))));
        }, ae = function(a) {
            function b(a) {
                var b = (a.hostname || "").split(":")[0].toLowerCase(), c = (a.protocol || "").toLowerCase();
                return c = 1 * a.port || ("http:" == c ? 80 : "https:" == c ? 443 : ""), a = a.pathname || "", 
                D(a, "/") || (a = "/" + a), [ b, "" + c, a ];
            }
            var c = M.createElement("a");
            c.href = M.location.href;
            var d = (c.protocol || "").toLowerCase(), e = b(c), g = c.search || "", ca = d + "//" + e[0] + (e[1] ? ":" + e[1] : "");
            return D(a, "//") ? a = d + a : D(a, "/") ? a = ca + a : !a || D(a, "?") ? a = ca + e[2] + (a || g) : 0 > a.split("/")[0].indexOf(":") && (a = ca + e[2].substring(0, e[2].lastIndexOf("/")) + "/" + a), 
            c.href = a, d = b(c), {
                protocol: (c.protocol || "").toLowerCase(),
                host: d[0],
                port: d[1],
                path: d[2],
                query: c.search || "",
                url: a || ""
            };
        }, Z = {
            ga: function() {
                Z.f = [];
            }
        };
        Z.ga(), Z.D = function(a) {
            var b = Z.J.apply(Z, arguments);
            for (b = Z.f.concat(b), Z.f = []; 0 < b.length && !Z.v(b[0]) && (b.shift(), !(0 < Z.f.length)); ) ;
            Z.f = Z.f.concat(b);
        }, Z.J = function(a) {
            for (var b = [], c = 0; c < arguments.length; c++) try {
                var d = new sc(arguments[c]);
                d.g ? C(d.a[0], d.a[1]) : (d.i && (d.ha = y(d.c, d.a[0], d.X, d.W)), b.push(d));
            } catch (e) {}
            return b;
        }, Z.v = function(a) {
            try {
                if (a.u) a.u.call(O, N.j("t0")); else {
                    var b = a.c == gb ? N : N.j(a.c);
                    if (a.A) {
                        if ("t0" == a.c && null === (b = N.create.apply(N, a.a))) return !0;
                    } else if (a.ba) N.remove(a.c); else if (b) if (a.i) {
                        if (a.ha && (a.ha = y(a.c, a.a[0], a.X, a.W)), !u(a.a[0], b, a.W)) return !0;
                    } else if (a.K) {
                        var c = a.C, d = a.a, e = b.plugins_.get(a.K);
                        e[c].apply(e, d);
                    } else b[a.C].apply(b, a.a);
                }
            } catch (g) {}
        };
        var N = function(a) {
            J(1), Z.D.apply(Z, [ arguments ]);
        };
        N.h = {}, N.P = [], N.L = 0, N.answer = 42;
        var uc = [ Na, W, V ];
        N.create = function(a) {
            var b = za(uc, [].slice.call(arguments));
            b[V] || (b[V] = "t0");
            var c = "" + b[V];
            if (N.h[c]) return N.h[c];
            a: {
                if (b[Kd]) {
                    if (J(67), b[ac] && "cookie" != b[ac]) {
                        var d = !1;
                        break a;
                    }
                    if (void 0 !== Ab) b[Q] || (b[Q] = Ab); else {
                        b: {
                            d = String(b[W] || xa());
                            var e = String(b[Yb] || "/"), g = Ca(String(b[U] || "_ga"));
                            if (!(d = na(g, d, e)) || jd.test(d)) d = !0; else if (0 == (d = Ca("AMP_TOKEN")).length) d = !0; else {
                                if (1 == d.length && ("$RETRIEVING" == (d = decodeURIComponent(d[0])) || "$OPT_OUT" == d || "$ERROR" == d || "$NOT_FOUND" == d)) {
                                    d = !0;
                                    break b;
                                }
                                d = !1;
                            }
                        }
                        if (d && tc(ic, String(b[Na]))) {
                            d = !0;
                            break a;
                        }
                    }
                }
                d = !1;
            }
            return d ? null : (b = new pc(b), N.h[c] = b, N.P.push(b), b);
        }, N.remove = function(a) {
            for (var b = 0; b < N.P.length; b++) if (N.P[b].get(V) == a) {
                N.P.splice(b, 1), N.h[a] = null;
                break;
            }
        }, N.j = function(a) {
            return N.h[a];
        }, N.getAll = function() {
            return N.P.slice(0);
        }, N.N = function() {
            "ga" != gb && J(49);
            var a = O[gb];
            if (!a || 42 != a.answer) {
                N.L = a && a.l, N.loaded = !0;
                var b = O[gb] = N;
                if (X("create", b, b.create), X("remove", b, b.remove), X("getByName", b, b.j, 5), 
                X("getAll", b, b.getAll, 6), X("get", b = pc.prototype, b.get, 7), X("set", b, b.set, 4), 
                X("send", b, b.send), X("requireSync", b, b.ma), X("get", b = Ya.prototype, b.get), 
                X("set", b, b.set), "https:" != M.location.protocol && !Ba) {
                    a: {
                        b = M.getElementsByTagName("script");
                        for (var c = 0; c < b.length && 100 > c; c++) {
                            var d = b[c].src;
                            if (d && 0 == d.indexOf("https://www.google-analytics.com/analytics")) {
                                b = !0;
                                break a;
                            }
                        }
                        b = !1;
                    }
                    b && (Ba = !0);
                }
                (O.gaplugins = O.gaplugins || {}).Linker = Dc, b = Dc.prototype, C("linker", Dc), 
                X("decorate", b, b.ca, 20), X("autoLink", b, b.S, 25), C("displayfeatures", fd), 
                C("adfeatures", fd), a = a && a.q, ka(a) ? Z.D.apply(N, a) : J(50);
            }
        }, N.da = function() {
            for (var a = N.getAll(), b = 0; b < a.length; b++) a[b].get(V);
        };
        var da = N.N, Nd = O[gb];
        function La(a) {
            var c, b = 1;
            if (a) for (b = 0, c = a.length - 1; 0 <= c; c--) {
                var d = a.charCodeAt(c);
                b = 0 != (d = 266338304 & (b = (b << 6 & 268435455) + d + (d << 14))) ? b ^ d >> 21 : b;
            }
            return b;
        }
        Nd && Nd.r ? da() : z(da), z(function() {
            Z.D([ "provide", "render", ua ]);
        });
    }(window);
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    });
    var _a, util_1 = __webpack_require__(667), call_1 = __webpack_require__(115), tracker_1 = __webpack_require__(187), tracking_1 = __webpack_require__(216), tracking_2 = __webpack_require__(189), logger_1 = __webpack_require__(188), prefs_1 = __webpack_require__(668), extension_api_1 = __webpack_require__(66);
    exports.on = ((_a = {})["daily-ping"] = function(id, cookiesDisabled, getNextPingDate_) {
        return void 0 === getNextPingDate_ && (getNextPingDate_ = util_1.getNextPingDate), 
        __awaiter(this, void 0, void 0, function() {
            var prefs, pingDate, _a, storageNextDate, oldId, newId;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return id ? (call_1.call("gnar.pingMaybe"), [ 4, (prefs = new prefs_1.PrefsImpl(extension_api_1.getGlobalExtensionApi().preferences)).get("pingDate") ]) : [ 2 ];

                  case 1:
                    return "string" != typeof (pingDate = _b.sent()) && (pingDate = ""), _a = __read(pingDate.split("|"), 2), 
                    storageNextDate = _a[0], oldId = _a[1], newId = cookiesDisabled ? "cookiesDisabled" : id, 
                    storageNextDate && storageNextDate > Date.now() && oldId === newId ? [ 2 ] : (logger_1.felog.dailyPing(), 
                    [ 4, prefs.set("pingDate", [ getNextPingDate_(), newId ].join("|")) ]);

                  case 2:
                    return _b.sent(), [ 2 ];
                }
            });
        });
    }, _a.app_signin_success = function(placement) {
        tracking_1.gnar.signInFormSuccess(placement);
    }, _a.app_signup_success = function(placement) {
        tracking_1.gnar.signUpFormSuccess(placement);
    }, _a["signin-error"] = function(error) {
        error.errorType = "Server-Side", call_1.call("gnar.track", "userLoginForm/rejected");
    }, _a["signup-error"] = function(error) {
        error.errorType = "Server-Side", call_1.call("gnar.track", "userAccountSignupForm/rejected");
    }, _a["upgrade-after-register"] = function() {
        return __awaiter(this, void 0, void 0, function() {
            return __generator(this, function(_a) {
                return call_1.call("gnar.track", "Account_Type_Selected"), [ 2 ];
            });
        });
    }, _a["hook-clicked"] = function(placement) {
        call_1.call("gnar.track", "upgradeHookClicked", {
            placement: placement
        }), logger_1.felog.userUpgradeClick(placement);
    }, _a["correct-btn-clicked"] = function(numberOfCriticalAlerts) {
        call_1.call("gnar.track", "gbuttonClicked", {
            numberOfCriticalAlerts: numberOfCriticalAlerts
        }), logger_1.felog.gButtonClick();
    }, _a["btn-disable-in-field"] = function(enabled) {
        call_1.call("gnar.track", "checkingInFieldToggled", {
            enabled: enabled
        }), logger_1.felog.checkingToggledInField(enabled);
    }, _a["button-change-state"] = function() {}, _a["login-attempt"] = function(placement) {
        call_1.call("gnar.track", "signInClicked", {
            placement: placement
        });
    }, _a["show-dictionary"] = function() {
        call_1.call("gnar.track", "showDictionary");
    }, _a["tab-connected"] = function(user, _a, _b, enabledByUserSettings, domain, isGrammarlyEditorPage) {
        var enabled = _a.enabled, cookiesDisabled = _b.cookiesDisabled;
        this["daily-ping"](user.id, cookiesDisabled), enabled || !0 === isGrammarlyEditorPage || logger_1.felog.disabledTabLoad(domain, user.type), 
        !0 === enabled && !1 === enabledByUserSettings && logger_1.felog.disabledTabByUserLoad(domain, user.type);
    }, _a["text-checked"] = function(user, cookiesDisabled) {
        this["daily-ping"](user.id, cookiesDisabled);
    }, _a["session-invalidate"] = function(user, oldUser, reason, cookiesDisabled, _containerId) {
        var id = user.id, anonymous = user.anonymous, isTest = user.isTest;
        id !== oldUser.id && (tracker_1.tracker.gnar && call_1.call("gnar.setUser", id, isTest), 
        tracker_1.tracker.ga && tracker_1.tracker.ga.setUserId(id), this["daily-ping"](id, cookiesDisabled)), 
        reason && logger_1.felog.sessionInvalidated(reason, id !== oldUser.id), oldUser.email && !oldUser.anonymous && anonymous && logger_1.felog.unexpectedAnonymous({
            email: oldUser.email,
            token: oldUser.token,
            grauth: oldUser.grauth,
            tokenEqualsGrauth: oldUser.token === oldUser.grauth,
            cookiesDisabled: cookiesDisabled,
            reason: reason
        });
    }, _a["set-dapi-prop"] = function(propName, value) {
        if ("dialectWeak" === propName) {
            var trackingVal = value + "English";
            tracking_1.gnar.languageSettingUpdate(trackingVal, "capi");
        }
        logger_1.felog.dapiPropInitialized(propName, value);
    }, _a["change-dialect"] = function(_a) {
        var language = _a.language, dialectWeak = _a.dialectWeak, trackingData = {
            language: language
        };
        dialectWeak && (trackingData.sameAsWeak = language === dialectWeak), call_1.call("gnar.track", "languageStrongPreference", trackingData);
    }, _a["change-defs"] = function(data) {
        call_1.call("gnar.track", "definitionsToggled", data), logger_1.felog.toggleExtensionDefs(data.enabled);
    }, _a["checking-toggled"] = function(data) {
        call_1.call("gnar.track", "checkingToggled", data), logger_1.felog.toggleExtension(data.enabled, data.placement);
    }, _a["disable-until-next-visit"] = function() {
        call_1.call("gnar.track", "disableUntilNextVisit"), tracking_1.gnar.disableUntilNextVisitButtonClick("gButton", tracking_2.SiteCategory.other), 
        logger_1.felog.disableUntilNextVisit();
    }, _a["disable-button-click"] = function() {
        tracking_1.gnar.disableButtonClick("gButton"), logger_1.felog.disableButtonClick();
    }, _a["popup-open"] = function() {
        call_1.call("gnar.track", "browserToolbarButtonClicked");
    }, _a["popup-open-on-unsupported"] = function() {
        call_1.call("gnar.track", "browserToolbarButtonClicked/unsupported");
    }, _a["cookie-overflow"] = function(total, biggestCookie) {
        logger_1.felog.cookieOverflow(total, biggestCookie);
    }, _a["onboarding-popup-show"] = function() {
        call_1.call("gnar.track", "onboarding-popup-show"), logger_1.felog.onboardingPopupShow();
    }, _a["onboarding-popup-cancel"] = function() {
        call_1.call("gnar.track", "onboarding-popup-cancel"), logger_1.felog.onboardingPopupCancel();
    }, _a["onboardingTutorial-popup-show"] = function() {
        call_1.call("gnar.track", "onboardingTutorial-popup-show"), logger_1.felog.onboardingTutorialShow();
    }, _a["onboardingTutorialNext-button-click"] = function() {
        call_1.call("gnar.track", "onboardingTutorialNext-button-click");
    }, _a["onboardingTutorialPersonalize-button-click"] = function() {
        call_1.call("gnar.track", "onboardingTutorialPersonalize-button-click");
    }, _a["onboardingTutorialSave-button-click"] = function() {
        call_1.call("gnar.track", "onboardingTutorialSave-button-click");
    }, _a["onboardingTutorialLetsWrite-button-click"] = function() {
        call_1.call("gnar.track", "onboardingTutorialLetsWrite-button-click");
    }, _a);
}, function(module, exports, __webpack_require__) {
    "use strict";
    this && this.__assign || Object.assign;
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    __webpack_require__(99), __webpack_require__(461);
    var message = __webpack_require__(15), tracking = __webpack_require__(7), util_1 = __webpack_require__(2), offline_1 = __webpack_require__(1152), bgonly_1 = __webpack_require__(460), sagas_1 = (__webpack_require__(184), 
    __webpack_require__(16), __webpack_require__(669)), logger_1 = __webpack_require__(1), config_1 = __webpack_require__(11), request_1 = __webpack_require__(205), log = logger_1.Logger.create("lib.bg.api");
    function initAPI(store, auth, actions, prefs, getSocketLog, fakeCapi, extensionApi, tabsSagaRunner) {
        var _a, _this = this, tabs = extensionApi.tabs, API = (extensionApi.management, 
        (_a = {
            dispatch: store.dispatch,
            signin: function(data, cb) {
                return auth.signin(data).then(cb);
            },
            signup: function(data, cb) {
                return auth.signup(data).then(cb);
            }
        })["open-url"] = function(url) {
            return tabs.open(url, !0);
        }, _a["reload-tab"] = function(id) {
            return tabs.reload && tabs.reload(parseInt(id, 10));
        }, _a["create-document"] = function(content) {
            var browser = util_1.getBrowser();
            return request_1.fetch(config_1.URLS.docsApi, {
                data: {
                    content: content
                },
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                    "X-API-Version": "1",
                    "X-Client-Type": "extension_" + browser
                }
            }).then(function(_a) {
                var docId, id = _a.id;
                return docId = id, tabs.open(config_1.URLS.docs + "/" + docId, !0);
            }).catch(function(e) {
                return log.error("request failed", e);
            });
        }, _a["get-containerIdOrUndefined"] = function(_, cb) {
            bgonly_1.getContainerIdOrUndefined().then(cb);
        }, _a["content-script-inited"] = function() {
            tabsSagaRunner.sendStateToTabs();
        }, _a["external:changed-plan"] = function() {
            tracking.felog.externalChangePlan(), actions.sessionInvalidate("changed-plan");
        }, _a["external:changed-dialect"] = function() {
            tracking.felog.externalChangeDialect(), actions.sessionInvalidate("changed-dialect");
        }, _a["external:changed-user"] = function() {
            tracking.felog.externalChangeUser(), actions.sessionInvalidate("changed-user");
        }, _a["external:editor-fix"] = function() {
            actions.incFixed();
        }, _a["external:cleanup"] = function() {
            return __awaiter(_this, void 0, void 0, function() {
                var preserve, values;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return tracking.felog.externalLogout(), preserve = [ "extensionSettings", "extensionInstallDate", "version", sagas_1.SERIALIZED_USER_INFO_PROP_NAME ], 
                        [ 4, prefs.get(preserve) ];

                      case 1:
                        return values = _a.sent(), prefs.clearAll(), [ 4, prefs.set(preserve.reduce(function(obj, key) {
                            return Object.assign({}, obj, ((_a = {})[key] = values[key], _a));
                            var _a;
                        }, {
                            enabledDefs: !1
                        })) ];

                      case 2:
                        return _a.sent(), actions.sessionInvalidate("logout"), [ 2 ];
                    }
                });
            });
        }, _a);
        return API;
    }
    exports.api = function(store, auth, actions, prefs, getSocketLog, fakeCapi, extensionApi, tabsSagaRunner) {
        var API = initAPI(store, auth, actions, prefs, getSocketLog, fakeCapi, extensionApi, tabsSagaRunner);
        Object.keys(API).forEach(function(type) {
            return message.on(type, API[type]);
        }), offline_1.Offline(function() {
            return actions.updateConnection({
                networkOffline: !1
            });
        }, function() {
            return actions.updateConnection({
                networkOffline: !0
            });
        });
    }, exports.initAPI = initAPI;
}, function(module, exports, __webpack_require__) {
    (function(global) {
        var require, f;
        f = function() {
            return function e(t, n, r) {
                function s(o, u) {
                    if (!n[o]) {
                        if (!t[o]) {
                            if (!u && ("function" == typeof require && require)) return require(o, !0);
                            if (i) return i(o, !0);
                            var f = new Error("Cannot find module '" + o + "'");
                            throw f.code = "MODULE_NOT_FOUND", f;
                        }
                        var l = n[o] = {
                            exports: {}
                        };
                        t[o][0].call(l.exports, function(e) {
                            var n = t[o][1][e];
                            return s(n || e);
                        }, l, l.exports, e, t, n, r);
                    }
                    return n[o].exports;
                }
                for (var i = "function" == typeof require && require, o = 0; o < r.length; o++) s(r[o]);
                return s;
            }({
                1: [ function(_dereq_, module, exports) {
                    (function(global) {
                        "use strict";
                        var scheduleDrain, draining, Mutation = global.MutationObserver || global.WebKitMutationObserver;
                        if (Mutation) {
                            var called = 0, observer = new Mutation(nextTick), element = global.document.createTextNode("");
                            observer.observe(element, {
                                characterData: !0
                            }), scheduleDrain = function() {
                                element.data = called = ++called % 2;
                            };
                        } else if (global.setImmediate || void 0 === global.MessageChannel) scheduleDrain = "document" in global && "onreadystatechange" in global.document.createElement("script") ? function() {
                            var scriptEl = global.document.createElement("script");
                            scriptEl.onreadystatechange = function() {
                                nextTick(), scriptEl.onreadystatechange = null, scriptEl.parentNode.removeChild(scriptEl), 
                                scriptEl = null;
                            }, global.document.documentElement.appendChild(scriptEl);
                        } : function() {
                            setTimeout(nextTick, 0);
                        }; else {
                            var channel = new global.MessageChannel();
                            channel.port1.onmessage = nextTick, scheduleDrain = function() {
                                channel.port2.postMessage(0);
                            };
                        }
                        var queue = [];
                        function nextTick() {
                            var i, oldQueue;
                            draining = !0;
                            for (var len = queue.length; len; ) {
                                for (oldQueue = queue, queue = [], i = -1; ++i < len; ) oldQueue[i]();
                                len = queue.length;
                            }
                            draining = !1;
                        }
                        module.exports = function(task) {
                            1 !== queue.push(task) || draining || scheduleDrain();
                        };
                    }).call(this, void 0 !== global ? global : "undefined" != typeof self ? self : "undefined" != typeof window ? window : {});
                }, {} ],
                2: [ function(_dereq_, module, exports) {
                    "use strict";
                    var immediate = _dereq_(1);
                    function INTERNAL() {}
                    var handlers = {}, REJECTED = [ "REJECTED" ], FULFILLED = [ "FULFILLED" ], PENDING = [ "PENDING" ];
                    function Promise(resolver) {
                        if ("function" != typeof resolver) throw new TypeError("resolver must be a function");
                        this.state = PENDING, this.queue = [], this.outcome = void 0, resolver !== INTERNAL && safelyResolveThenable(this, resolver);
                    }
                    function QueueItem(promise, onFulfilled, onRejected) {
                        this.promise = promise, "function" == typeof onFulfilled && (this.onFulfilled = onFulfilled, 
                        this.callFulfilled = this.otherCallFulfilled), "function" == typeof onRejected && (this.onRejected = onRejected, 
                        this.callRejected = this.otherCallRejected);
                    }
                    function unwrap(promise, func, value) {
                        immediate(function() {
                            var returnValue;
                            try {
                                returnValue = func(value);
                            } catch (e) {
                                return handlers.reject(promise, e);
                            }
                            returnValue === promise ? handlers.reject(promise, new TypeError("Cannot resolve promise with itself")) : handlers.resolve(promise, returnValue);
                        });
                    }
                    function getThen(obj) {
                        var then = obj && obj.then;
                        if (obj && ("object" == typeof obj || "function" == typeof obj) && "function" == typeof then) return function() {
                            then.apply(obj, arguments);
                        };
                    }
                    function safelyResolveThenable(self, thenable) {
                        var called = !1;
                        function onError(value) {
                            called || (called = !0, handlers.reject(self, value));
                        }
                        function onSuccess(value) {
                            called || (called = !0, handlers.resolve(self, value));
                        }
                        var result = tryCatch(function() {
                            thenable(onSuccess, onError);
                        });
                        "error" === result.status && onError(result.value);
                    }
                    function tryCatch(func, value) {
                        var out = {};
                        try {
                            out.value = func(value), out.status = "success";
                        } catch (e) {
                            out.status = "error", out.value = e;
                        }
                        return out;
                    }
                    module.exports = Promise, Promise.prototype.catch = function(onRejected) {
                        return this.then(null, onRejected);
                    }, Promise.prototype.then = function(onFulfilled, onRejected) {
                        if ("function" != typeof onFulfilled && this.state === FULFILLED || "function" != typeof onRejected && this.state === REJECTED) return this;
                        var promise = new this.constructor(INTERNAL);
                        this.state !== PENDING ? unwrap(promise, this.state === FULFILLED ? onFulfilled : onRejected, this.outcome) : this.queue.push(new QueueItem(promise, onFulfilled, onRejected));
                        return promise;
                    }, QueueItem.prototype.callFulfilled = function(value) {
                        handlers.resolve(this.promise, value);
                    }, QueueItem.prototype.otherCallFulfilled = function(value) {
                        unwrap(this.promise, this.onFulfilled, value);
                    }, QueueItem.prototype.callRejected = function(value) {
                        handlers.reject(this.promise, value);
                    }, QueueItem.prototype.otherCallRejected = function(value) {
                        unwrap(this.promise, this.onRejected, value);
                    }, handlers.resolve = function(self, value) {
                        var result = tryCatch(getThen, value);
                        if ("error" === result.status) return handlers.reject(self, result.value);
                        var thenable = result.value;
                        if (thenable) safelyResolveThenable(self, thenable); else {
                            self.state = FULFILLED, self.outcome = value;
                            for (var i = -1, len = self.queue.length; ++i < len; ) self.queue[i].callFulfilled(value);
                        }
                        return self;
                    }, handlers.reject = function(self, error) {
                        self.state = REJECTED, self.outcome = error;
                        for (var i = -1, len = self.queue.length; ++i < len; ) self.queue[i].callRejected(error);
                        return self;
                    }, Promise.resolve = function(value) {
                        if (value instanceof this) return value;
                        return handlers.resolve(new this(INTERNAL), value);
                    }, Promise.reject = function(reason) {
                        var promise = new this(INTERNAL);
                        return handlers.reject(promise, reason);
                    }, Promise.all = function(iterable) {
                        var self = this;
                        if ("[object Array]" !== Object.prototype.toString.call(iterable)) return this.reject(new TypeError("must be an array"));
                        var len = iterable.length, called = !1;
                        if (!len) return this.resolve([]);
                        var values = new Array(len), resolved = 0, i = -1, promise = new this(INTERNAL);
                        for (;++i < len; ) allResolver(iterable[i], i);
                        return promise;
                        function allResolver(value, i) {
                            self.resolve(value).then(function(outValue) {
                                values[i] = outValue, ++resolved !== len || called || (called = !0, handlers.resolve(promise, values));
                            }, function(error) {
                                called || (called = !0, handlers.reject(promise, error));
                            });
                        }
                    }, Promise.race = function(iterable) {
                        var self = this;
                        if ("[object Array]" !== Object.prototype.toString.call(iterable)) return this.reject(new TypeError("must be an array"));
                        var len = iterable.length, called = !1;
                        if (!len) return this.resolve([]);
                        var i = -1, promise = new this(INTERNAL);
                        for (;++i < len; ) value = iterable[i], self.resolve(value).then(function(response) {
                            called || (called = !0, handlers.resolve(promise, response));
                        }, function(error) {
                            called || (called = !0, handlers.reject(promise, error));
                        });
                        var value;
                        return promise;
                    };
                }, {
                    1: 1
                } ],
                3: [ function(_dereq_, module, exports) {
                    (function(global) {
                        "use strict";
                        "function" != typeof global.Promise && (global.Promise = _dereq_(2));
                    }).call(this, void 0 !== global ? global : "undefined" != typeof self ? self : "undefined" != typeof window ? window : {});
                }, {
                    2: 2
                } ],
                4: [ function(_dereq_, module, exports) {
                    "use strict";
                    var _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(obj) {
                        return typeof obj;
                    } : function(obj) {
                        return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
                    };
                    var idb = function() {
                        try {
                            if ("undefined" != typeof indexedDB) return indexedDB;
                            if ("undefined" != typeof webkitIndexedDB) return webkitIndexedDB;
                            if ("undefined" != typeof mozIndexedDB) return mozIndexedDB;
                            if ("undefined" != typeof OIndexedDB) return OIndexedDB;
                            if ("undefined" != typeof msIndexedDB) return msIndexedDB;
                        } catch (e) {
                            return;
                        }
                    }();
                    function createBlob(parts, properties) {
                        parts = parts || [], properties = properties || {};
                        try {
                            return new Blob(parts, properties);
                        } catch (e) {
                            if ("TypeError" !== e.name) throw e;
                            for (var builder = new ("undefined" != typeof BlobBuilder ? BlobBuilder : "undefined" != typeof MSBlobBuilder ? MSBlobBuilder : "undefined" != typeof MozBlobBuilder ? MozBlobBuilder : WebKitBlobBuilder)(), i = 0; i < parts.length; i += 1) builder.append(parts[i]);
                            return builder.getBlob(properties.type);
                        }
                    }
                    "undefined" == typeof Promise && _dereq_(3);
                    var Promise$1 = Promise;
                    function executeCallback(promise, callback) {
                        callback && promise.then(function(result) {
                            callback(null, result);
                        }, function(error) {
                            callback(error);
                        });
                    }
                    function executeTwoCallbacks(promise, callback, errorCallback) {
                        "function" == typeof callback && promise.then(callback), "function" == typeof errorCallback && promise.catch(errorCallback);
                    }
                    function normalizeKey(key) {
                        return "string" != typeof key && (console.warn(key + " used as a key, but it is not a string."), 
                        key = String(key)), key;
                    }
                    var supportsBlobs, dbContexts, DETECT_BLOB_SUPPORT_STORE = "local-forage-detect-blob-support", toString = Object.prototype.toString, READ_ONLY = "readonly", READ_WRITE = "readwrite";
                    function _checkBlobSupport(idb) {
                        return "boolean" == typeof supportsBlobs ? Promise$1.resolve(supportsBlobs) : function(idb) {
                            return new Promise$1(function(resolve) {
                                var txn = idb.transaction(DETECT_BLOB_SUPPORT_STORE, READ_WRITE), blob = createBlob([ "" ]);
                                txn.objectStore(DETECT_BLOB_SUPPORT_STORE).put(blob, "key"), txn.onabort = function(e) {
                                    e.preventDefault(), e.stopPropagation(), resolve(!1);
                                }, txn.oncomplete = function() {
                                    var matchedChrome = navigator.userAgent.match(/Chrome\/(\d+)/), matchedEdge = navigator.userAgent.match(/Edge\//);
                                    resolve(matchedEdge || !matchedChrome || parseInt(matchedChrome[1], 10) >= 43);
                                };
                            }).catch(function() {
                                return !1;
                            });
                        }(idb).then(function(value) {
                            return supportsBlobs = value;
                        });
                    }
                    function _deferReadiness(dbInfo) {
                        var dbContext = dbContexts[dbInfo.name], deferredOperation = {};
                        deferredOperation.promise = new Promise$1(function(resolve) {
                            deferredOperation.resolve = resolve;
                        }), dbContext.deferredOperations.push(deferredOperation), dbContext.dbReady ? dbContext.dbReady = dbContext.dbReady.then(function() {
                            return deferredOperation.promise;
                        }) : dbContext.dbReady = deferredOperation.promise;
                    }
                    function _getConnection(dbInfo, upgradeNeeded) {
                        return new Promise$1(function(resolve, reject) {
                            if (dbInfo.db) {
                                if (!upgradeNeeded) return resolve(dbInfo.db);
                                _deferReadiness(dbInfo), dbInfo.db.close();
                            }
                            var dbArgs = [ dbInfo.name ];
                            upgradeNeeded && dbArgs.push(dbInfo.version);
                            var openreq = idb.open.apply(idb, dbArgs);
                            upgradeNeeded && (openreq.onupgradeneeded = function(e) {
                                var db = openreq.result;
                                try {
                                    db.createObjectStore(dbInfo.storeName), e.oldVersion <= 1 && db.createObjectStore(DETECT_BLOB_SUPPORT_STORE);
                                } catch (ex) {
                                    if ("ConstraintError" !== ex.name) throw ex;
                                    console.warn('The database "' + dbInfo.name + '" has been upgraded from version ' + e.oldVersion + " to version " + e.newVersion + ', but the storage "' + dbInfo.storeName + '" already exists.');
                                }
                            }), openreq.onerror = function(e) {
                                e.preventDefault(), reject(openreq.error);
                            }, openreq.onsuccess = function() {
                                resolve(openreq.result), function(dbInfo) {
                                    var deferredOperation = dbContexts[dbInfo.name].deferredOperations.pop();
                                    deferredOperation && deferredOperation.resolve();
                                }(dbInfo);
                            };
                        });
                    }
                    function _decodeBlob(encodedBlob) {
                        return createBlob([ function(bin) {
                            for (var length = bin.length, buf = new ArrayBuffer(length), arr = new Uint8Array(buf), i = 0; i < length; i++) arr[i] = bin.charCodeAt(i);
                            return buf;
                        }(atob(encodedBlob.data)) ], {
                            type: encodedBlob.type
                        });
                    }
                    function _isEncodedBlob(value) {
                        return value && value.__local_forage_encoded_blob;
                    }
                    function _fullyReady(callback) {
                        var self = this, promise = self._initReady().then(function() {
                            var dbContext = dbContexts[self._dbInfo.name];
                            if (dbContext && dbContext.dbReady) return dbContext.dbReady;
                        });
                        return executeTwoCallbacks(promise, callback, callback), promise;
                    }
                    function _tryReconnect(dbInfo) {
                        _deferReadiness(dbInfo);
                        for (var forages = dbContexts[dbInfo.name].forages, i = 0; i < forages.length; i++) forages[i]._dbInfo.db && (forages[i]._dbInfo.db.close(), 
                        forages[i]._dbInfo.db = null);
                        return _getConnection(dbInfo, !1).then(function(db) {
                            for (var j = 0; j < forages.length; j++) forages[j]._dbInfo.db = db;
                        }).catch(function(err) {
                            throw function(dbInfo, err) {
                                var deferredOperation = dbContexts[dbInfo.name].deferredOperations.pop();
                                deferredOperation && deferredOperation.reject(err);
                            }(dbInfo, err), err;
                        });
                    }
                    function createTransaction(dbInfo, mode, callback) {
                        try {
                            var tx = dbInfo.db.transaction(dbInfo.storeName, mode);
                            callback(null, tx);
                        } catch (err) {
                            if (!dbInfo.db || "InvalidStateError" === err.name) return _tryReconnect(dbInfo).then(function() {
                                var tx = dbInfo.db.transaction(dbInfo.storeName, mode);
                                callback(null, tx);
                            });
                            callback(err);
                        }
                    }
                    var asyncStorage = {
                        _driver: "asyncStorage",
                        _initStorage: function(options) {
                            var self = this, dbInfo = {
                                db: null
                            };
                            if (options) for (var i in options) dbInfo[i] = options[i];
                            dbContexts || (dbContexts = {});
                            var dbContext = dbContexts[dbInfo.name];
                            dbContext || (dbContext = {
                                forages: [],
                                db: null,
                                dbReady: null,
                                deferredOperations: []
                            }, dbContexts[dbInfo.name] = dbContext), dbContext.forages.push(self), self._initReady || (self._initReady = self.ready, 
                            self.ready = _fullyReady);
                            var initPromises = [];
                            function ignoreErrors() {
                                return Promise$1.resolve();
                            }
                            for (var j = 0; j < dbContext.forages.length; j++) {
                                var forage = dbContext.forages[j];
                                forage !== self && initPromises.push(forage._initReady().catch(ignoreErrors));
                            }
                            var forages = dbContext.forages.slice(0);
                            return Promise$1.all(initPromises).then(function() {
                                return dbInfo.db = dbContext.db, function(dbInfo) {
                                    return _getConnection(dbInfo, !1);
                                }(dbInfo);
                            }).then(function(db) {
                                return dbInfo.db = db, function(dbInfo, defaultVersion) {
                                    if (!dbInfo.db) return !0;
                                    var isNewStore = !dbInfo.db.objectStoreNames.contains(dbInfo.storeName), isDowngrade = dbInfo.version < dbInfo.db.version, isUpgrade = dbInfo.version > dbInfo.db.version;
                                    if (isDowngrade && (dbInfo.version !== defaultVersion && console.warn('The database "' + dbInfo.name + "\" can't be downgraded from version " + dbInfo.db.version + " to version " + dbInfo.version + "."), 
                                    dbInfo.version = dbInfo.db.version), isUpgrade || isNewStore) {
                                        if (isNewStore) {
                                            var incVersion = dbInfo.db.version + 1;
                                            incVersion > dbInfo.version && (dbInfo.version = incVersion);
                                        }
                                        return !0;
                                    }
                                    return !1;
                                }(dbInfo, self._defaultConfig.version) ? function(dbInfo) {
                                    return _getConnection(dbInfo, !0);
                                }(dbInfo) : db;
                            }).then(function(db) {
                                dbInfo.db = dbContext.db = db, self._dbInfo = dbInfo;
                                for (var k = 0; k < forages.length; k++) {
                                    var forage = forages[k];
                                    forage !== self && (forage._dbInfo.db = dbInfo.db, forage._dbInfo.version = dbInfo.version);
                                }
                            });
                        },
                        _support: function() {
                            try {
                                if (!idb) return !1;
                                var isSafari = "undefined" != typeof openDatabase && /(Safari|iPhone|iPad|iPod)/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent) && !/BlackBerry/.test(navigator.platform), hasFetch = "function" == typeof fetch && -1 !== fetch.toString().indexOf("[native code");
                                return (!isSafari || hasFetch) && "undefined" != typeof indexedDB && "undefined" != typeof IDBKeyRange;
                            } catch (e) {
                                return !1;
                            }
                        }(),
                        iterate: function(iterator, callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_ONLY, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).openCursor(), iterationNumber = 1;
                                            req.onsuccess = function() {
                                                var cursor = req.result;
                                                if (cursor) {
                                                    var value = cursor.value;
                                                    _isEncodedBlob(value) && (value = _decodeBlob(value));
                                                    var result = iterator(value, cursor.key, iterationNumber++);
                                                    void 0 !== result ? resolve(result) : cursor.continue();
                                                } else resolve();
                                            }, req.onerror = function() {
                                                reject(req.error);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        getItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_ONLY, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).get(key);
                                            req.onsuccess = function() {
                                                var value = req.result;
                                                void 0 === value && (value = null), _isEncodedBlob(value) && (value = _decodeBlob(value)), 
                                                resolve(value);
                                            }, req.onerror = function() {
                                                reject(req.error);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        setItem: function(key, value, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = new Promise$1(function(resolve, reject) {
                                var dbInfo;
                                self.ready().then(function() {
                                    return dbInfo = self._dbInfo, "[object Blob]" === toString.call(value) ? _checkBlobSupport(dbInfo.db).then(function(blobSupport) {
                                        return blobSupport ? value : (blob = value, new Promise$1(function(resolve, reject) {
                                            var reader = new FileReader();
                                            reader.onerror = reject, reader.onloadend = function(e) {
                                                var base64 = btoa(e.target.result || "");
                                                resolve({
                                                    __local_forage_encoded_blob: !0,
                                                    data: base64,
                                                    type: blob.type
                                                });
                                            }, reader.readAsBinaryString(blob);
                                        }));
                                        var blob;
                                    }) : value;
                                }).then(function(value) {
                                    createTransaction(self._dbInfo, READ_WRITE, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var store = transaction.objectStore(self._dbInfo.storeName);
                                            null === value && (value = void 0);
                                            var req = store.put(value, key);
                                            transaction.oncomplete = function() {
                                                void 0 === value && (value = null), resolve(value);
                                            }, transaction.onabort = transaction.onerror = function() {
                                                var err = req.error ? req.error : req.transaction.error;
                                                reject(err);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        removeItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_WRITE, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).delete(key);
                                            transaction.oncomplete = function() {
                                                resolve();
                                            }, transaction.onerror = function() {
                                                reject(req.error);
                                            }, transaction.onabort = function() {
                                                var err = req.error ? req.error : req.transaction.error;
                                                reject(err);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        clear: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_WRITE, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).clear();
                                            transaction.oncomplete = function() {
                                                resolve();
                                            }, transaction.onabort = transaction.onerror = function() {
                                                var err = req.error ? req.error : req.transaction.error;
                                                reject(err);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        length: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_ONLY, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).count();
                                            req.onsuccess = function() {
                                                resolve(req.result);
                                            }, req.onerror = function() {
                                                reject(req.error);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        key: function(n, callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                n < 0 ? resolve(null) : self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_ONLY, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var store = transaction.objectStore(self._dbInfo.storeName), advanced = !1, req = store.openCursor();
                                            req.onsuccess = function() {
                                                var cursor = req.result;
                                                cursor ? 0 === n ? resolve(cursor.key) : advanced ? resolve(cursor.key) : (advanced = !0, 
                                                cursor.advance(n)) : resolve(null);
                                            }, req.onerror = function() {
                                                reject(req.error);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        keys: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    createTransaction(self._dbInfo, READ_ONLY, function(err, transaction) {
                                        if (err) return reject(err);
                                        try {
                                            var req = transaction.objectStore(self._dbInfo.storeName).openCursor(), keys = [];
                                            req.onsuccess = function() {
                                                var cursor = req.result;
                                                cursor ? (keys.push(cursor.key), cursor.continue()) : resolve(keys);
                                            }, req.onerror = function() {
                                                reject(req.error);
                                            };
                                        } catch (e) {
                                            reject(e);
                                        }
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        }
                    };
                    var BASE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", BLOB_TYPE_PREFIX = "~~local_forage_type~", BLOB_TYPE_PREFIX_REGEX = /^~~local_forage_type~([^~]+)~/, SERIALIZED_MARKER = "__lfsc__:", SERIALIZED_MARKER_LENGTH = SERIALIZED_MARKER.length, TYPE_ARRAYBUFFER = "arbf", TYPE_BLOB = "blob", TYPE_INT8ARRAY = "si08", TYPE_UINT8ARRAY = "ui08", TYPE_UINT8CLAMPEDARRAY = "uic8", TYPE_INT16ARRAY = "si16", TYPE_INT32ARRAY = "si32", TYPE_UINT16ARRAY = "ur16", TYPE_UINT32ARRAY = "ui32", TYPE_FLOAT32ARRAY = "fl32", TYPE_FLOAT64ARRAY = "fl64", TYPE_SERIALIZED_MARKER_LENGTH = SERIALIZED_MARKER_LENGTH + TYPE_ARRAYBUFFER.length, toString$1 = Object.prototype.toString;
                    function stringToBuffer(serializedString) {
                        var i, encoded1, encoded2, encoded3, encoded4, bufferLength = .75 * serializedString.length, len = serializedString.length, p = 0;
                        "=" === serializedString[serializedString.length - 1] && (bufferLength--, "=" === serializedString[serializedString.length - 2] && bufferLength--);
                        var buffer = new ArrayBuffer(bufferLength), bytes = new Uint8Array(buffer);
                        for (i = 0; i < len; i += 4) encoded1 = BASE_CHARS.indexOf(serializedString[i]), 
                        encoded2 = BASE_CHARS.indexOf(serializedString[i + 1]), encoded3 = BASE_CHARS.indexOf(serializedString[i + 2]), 
                        encoded4 = BASE_CHARS.indexOf(serializedString[i + 3]), bytes[p++] = encoded1 << 2 | encoded2 >> 4, 
                        bytes[p++] = (15 & encoded2) << 4 | encoded3 >> 2, bytes[p++] = (3 & encoded3) << 6 | 63 & encoded4;
                        return buffer;
                    }
                    function bufferToString(buffer) {
                        var i, bytes = new Uint8Array(buffer), base64String = "";
                        for (i = 0; i < bytes.length; i += 3) base64String += BASE_CHARS[bytes[i] >> 2], 
                        base64String += BASE_CHARS[(3 & bytes[i]) << 4 | bytes[i + 1] >> 4], base64String += BASE_CHARS[(15 & bytes[i + 1]) << 2 | bytes[i + 2] >> 6], 
                        base64String += BASE_CHARS[63 & bytes[i + 2]];
                        return bytes.length % 3 == 2 ? base64String = base64String.substring(0, base64String.length - 1) + "=" : bytes.length % 3 == 1 && (base64String = base64String.substring(0, base64String.length - 2) + "=="), 
                        base64String;
                    }
                    var localforageSerializer = {
                        serialize: function(value, callback) {
                            var valueType = "";
                            if (value && (valueType = toString$1.call(value)), value && ("[object ArrayBuffer]" === valueType || value.buffer && "[object ArrayBuffer]" === toString$1.call(value.buffer))) {
                                var buffer, marker = SERIALIZED_MARKER;
                                value instanceof ArrayBuffer ? (buffer = value, marker += TYPE_ARRAYBUFFER) : (buffer = value.buffer, 
                                "[object Int8Array]" === valueType ? marker += TYPE_INT8ARRAY : "[object Uint8Array]" === valueType ? marker += TYPE_UINT8ARRAY : "[object Uint8ClampedArray]" === valueType ? marker += TYPE_UINT8CLAMPEDARRAY : "[object Int16Array]" === valueType ? marker += TYPE_INT16ARRAY : "[object Uint16Array]" === valueType ? marker += TYPE_UINT16ARRAY : "[object Int32Array]" === valueType ? marker += TYPE_INT32ARRAY : "[object Uint32Array]" === valueType ? marker += TYPE_UINT32ARRAY : "[object Float32Array]" === valueType ? marker += TYPE_FLOAT32ARRAY : "[object Float64Array]" === valueType ? marker += TYPE_FLOAT64ARRAY : callback(new Error("Failed to get type for BinaryArray"))), 
                                callback(marker + bufferToString(buffer));
                            } else if ("[object Blob]" === valueType) {
                                var fileReader = new FileReader();
                                fileReader.onload = function() {
                                    var str = BLOB_TYPE_PREFIX + value.type + "~" + bufferToString(this.result);
                                    callback(SERIALIZED_MARKER + TYPE_BLOB + str);
                                }, fileReader.readAsArrayBuffer(value);
                            } else try {
                                callback(JSON.stringify(value));
                            } catch (e) {
                                console.error("Couldn't convert value into a JSON string: ", value), callback(null, e);
                            }
                        },
                        deserialize: function(value) {
                            if (value.substring(0, SERIALIZED_MARKER_LENGTH) !== SERIALIZED_MARKER) return JSON.parse(value);
                            var blobType, serializedString = value.substring(TYPE_SERIALIZED_MARKER_LENGTH), type = value.substring(SERIALIZED_MARKER_LENGTH, TYPE_SERIALIZED_MARKER_LENGTH);
                            if (type === TYPE_BLOB && BLOB_TYPE_PREFIX_REGEX.test(serializedString)) {
                                var matcher = serializedString.match(BLOB_TYPE_PREFIX_REGEX);
                                blobType = matcher[1], serializedString = serializedString.substring(matcher[0].length);
                            }
                            var buffer = stringToBuffer(serializedString);
                            switch (type) {
                              case TYPE_ARRAYBUFFER:
                                return buffer;

                              case TYPE_BLOB:
                                return createBlob([ buffer ], {
                                    type: blobType
                                });

                              case TYPE_INT8ARRAY:
                                return new Int8Array(buffer);

                              case TYPE_UINT8ARRAY:
                                return new Uint8Array(buffer);

                              case TYPE_UINT8CLAMPEDARRAY:
                                return new Uint8ClampedArray(buffer);

                              case TYPE_INT16ARRAY:
                                return new Int16Array(buffer);

                              case TYPE_UINT16ARRAY:
                                return new Uint16Array(buffer);

                              case TYPE_INT32ARRAY:
                                return new Int32Array(buffer);

                              case TYPE_UINT32ARRAY:
                                return new Uint32Array(buffer);

                              case TYPE_FLOAT32ARRAY:
                                return new Float32Array(buffer);

                              case TYPE_FLOAT64ARRAY:
                                return new Float64Array(buffer);

                              default:
                                throw new Error("Unkown type: " + type);
                            }
                        },
                        stringToBuffer: stringToBuffer,
                        bufferToString: bufferToString
                    };
                    var webSQLStorage = {
                        _driver: "webSQLStorage",
                        _initStorage: function(options) {
                            var self = this, dbInfo = {
                                db: null
                            };
                            if (options) for (var i in options) dbInfo[i] = "string" != typeof options[i] ? options[i].toString() : options[i];
                            var dbInfoPromise = new Promise$1(function(resolve, reject) {
                                try {
                                    dbInfo.db = openDatabase(dbInfo.name, String(dbInfo.version), dbInfo.description, dbInfo.size);
                                } catch (e) {
                                    return reject(e);
                                }
                                dbInfo.db.transaction(function(t) {
                                    t.executeSql("CREATE TABLE IF NOT EXISTS " + dbInfo.storeName + " (id INTEGER PRIMARY KEY, key unique, value)", [], function() {
                                        self._dbInfo = dbInfo, resolve();
                                    }, function(t, error) {
                                        reject(error);
                                    });
                                });
                            });
                            return dbInfo.serializer = localforageSerializer, dbInfoPromise;
                        },
                        _support: "function" == typeof openDatabase,
                        iterate: function(iterator, callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("SELECT * FROM " + dbInfo.storeName, [], function(t, results) {
                                            for (var rows = results.rows, length = rows.length, i = 0; i < length; i++) {
                                                var item = rows.item(i), result = item.value;
                                                if (result && (result = dbInfo.serializer.deserialize(result)), void 0 !== (result = iterator(result, item.key, i + 1))) return void resolve(result);
                                            }
                                            resolve();
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        getItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("SELECT * FROM " + dbInfo.storeName + " WHERE key = ? LIMIT 1", [ key ], function(t, results) {
                                            var result = results.rows.length ? results.rows.item(0).value : null;
                                            result && (result = dbInfo.serializer.deserialize(result)), resolve(result);
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        setItem: function(key, value, callback) {
                            return function _setItem(key, value, callback, retriesLeft) {
                                var self = this;
                                key = normalizeKey(key);
                                var promise = new Promise$1(function(resolve, reject) {
                                    self.ready().then(function() {
                                        void 0 === value && (value = null);
                                        var originalValue = value, dbInfo = self._dbInfo;
                                        dbInfo.serializer.serialize(value, function(value, error) {
                                            error ? reject(error) : dbInfo.db.transaction(function(t) {
                                                t.executeSql("INSERT OR REPLACE INTO " + dbInfo.storeName + " (key, value) VALUES (?, ?)", [ key, value ], function() {
                                                    resolve(originalValue);
                                                }, function(t, error) {
                                                    reject(error);
                                                });
                                            }, function(sqlError) {
                                                if (sqlError.code === sqlError.QUOTA_ERR) {
                                                    if (retriesLeft > 0) return void resolve(_setItem.apply(self, [ key, originalValue, callback, retriesLeft - 1 ]));
                                                    reject(sqlError);
                                                }
                                            });
                                        });
                                    }).catch(reject);
                                });
                                return executeCallback(promise, callback), promise;
                            }.apply(this, [ key, value, callback, 1 ]);
                        },
                        removeItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("DELETE FROM " + dbInfo.storeName + " WHERE key = ?", [ key ], function() {
                                            resolve();
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        clear: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("DELETE FROM " + dbInfo.storeName, [], function() {
                                            resolve();
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        length: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("SELECT COUNT(key) as c FROM " + dbInfo.storeName, [], function(t, results) {
                                            var result = results.rows.item(0).c;
                                            resolve(result);
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        key: function(n, callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("SELECT key FROM " + dbInfo.storeName + " WHERE id = ? LIMIT 1", [ n + 1 ], function(t, results) {
                                            var result = results.rows.length ? results.rows.item(0).key : null;
                                            resolve(result);
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        keys: function(callback) {
                            var self = this, promise = new Promise$1(function(resolve, reject) {
                                self.ready().then(function() {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.db.transaction(function(t) {
                                        t.executeSql("SELECT key FROM " + dbInfo.storeName, [], function(t, results) {
                                            for (var keys = [], i = 0; i < results.rows.length; i++) keys.push(results.rows.item(i).key);
                                            resolve(keys);
                                        }, function(t, error) {
                                            reject(error);
                                        });
                                    });
                                }).catch(reject);
                            });
                            return executeCallback(promise, callback), promise;
                        }
                    };
                    function _isLocalStorageUsable() {
                        return !function() {
                            try {
                                return localStorage.setItem("_localforage_support_test", !0), localStorage.removeItem("_localforage_support_test"), 
                                !1;
                            } catch (e) {
                                return !0;
                            }
                        }() || localStorage.length > 0;
                    }
                    var localStorageWrapper = {
                        _driver: "localStorageWrapper",
                        _initStorage: function(options) {
                            var dbInfo = {};
                            if (options) for (var i in options) dbInfo[i] = options[i];
                            return dbInfo.keyPrefix = dbInfo.name + "/", dbInfo.storeName !== this._defaultConfig.storeName && (dbInfo.keyPrefix += dbInfo.storeName + "/"), 
                            _isLocalStorageUsable() ? (this._dbInfo = dbInfo, dbInfo.serializer = localforageSerializer, 
                            Promise$1.resolve()) : Promise$1.reject();
                        },
                        _support: function() {
                            try {
                                return "undefined" != typeof localStorage && "setItem" in localStorage && "function" == typeof localStorage.setItem;
                            } catch (e) {
                                return !1;
                            }
                        }(),
                        iterate: function(iterator, callback) {
                            var self = this, promise = self.ready().then(function() {
                                for (var dbInfo = self._dbInfo, keyPrefix = dbInfo.keyPrefix, keyPrefixLength = keyPrefix.length, length = localStorage.length, iterationNumber = 1, i = 0; i < length; i++) {
                                    var key = localStorage.key(i);
                                    if (0 === key.indexOf(keyPrefix)) {
                                        var value = localStorage.getItem(key);
                                        if (value && (value = dbInfo.serializer.deserialize(value)), void 0 !== (value = iterator(value, key.substring(keyPrefixLength), iterationNumber++))) return value;
                                    }
                                }
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        getItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = self.ready().then(function() {
                                var dbInfo = self._dbInfo, result = localStorage.getItem(dbInfo.keyPrefix + key);
                                return result && (result = dbInfo.serializer.deserialize(result)), result;
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        setItem: function(key, value, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = self.ready().then(function() {
                                void 0 === value && (value = null);
                                var originalValue = value;
                                return new Promise$1(function(resolve, reject) {
                                    var dbInfo = self._dbInfo;
                                    dbInfo.serializer.serialize(value, function(value, error) {
                                        if (error) reject(error); else try {
                                            localStorage.setItem(dbInfo.keyPrefix + key, value), resolve(originalValue);
                                        } catch (e) {
                                            "QuotaExceededError" !== e.name && "NS_ERROR_DOM_QUOTA_REACHED" !== e.name || reject(e), 
                                            reject(e);
                                        }
                                    });
                                });
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        removeItem: function(key, callback) {
                            var self = this;
                            key = normalizeKey(key);
                            var promise = self.ready().then(function() {
                                var dbInfo = self._dbInfo;
                                localStorage.removeItem(dbInfo.keyPrefix + key);
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        clear: function(callback) {
                            var self = this, promise = self.ready().then(function() {
                                for (var keyPrefix = self._dbInfo.keyPrefix, i = localStorage.length - 1; i >= 0; i--) {
                                    var key = localStorage.key(i);
                                    0 === key.indexOf(keyPrefix) && localStorage.removeItem(key);
                                }
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        length: function(callback) {
                            var promise = this.keys().then(function(keys) {
                                return keys.length;
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        key: function(n, callback) {
                            var self = this, promise = self.ready().then(function() {
                                var result, dbInfo = self._dbInfo;
                                try {
                                    result = localStorage.key(n);
                                } catch (error) {
                                    result = null;
                                }
                                return result && (result = result.substring(dbInfo.keyPrefix.length)), result;
                            });
                            return executeCallback(promise, callback), promise;
                        },
                        keys: function(callback) {
                            var self = this, promise = self.ready().then(function() {
                                for (var dbInfo = self._dbInfo, length = localStorage.length, keys = [], i = 0; i < length; i++) {
                                    var itemKey = localStorage.key(i);
                                    0 === itemKey.indexOf(dbInfo.keyPrefix) && keys.push(itemKey.substring(dbInfo.keyPrefix.length));
                                }
                                return keys;
                            });
                            return executeCallback(promise, callback), promise;
                        }
                    }, isArray = Array.isArray || function(arg) {
                        return "[object Array]" === Object.prototype.toString.call(arg);
                    }, DefinedDrivers = {}, DriverSupport = {}, DefaultDrivers = {
                        INDEXEDDB: asyncStorage,
                        WEBSQL: webSQLStorage,
                        LOCALSTORAGE: localStorageWrapper
                    }, DefaultDriverOrder = [ DefaultDrivers.INDEXEDDB._driver, DefaultDrivers.WEBSQL._driver, DefaultDrivers.LOCALSTORAGE._driver ], LibraryMethods = [ "clear", "getItem", "iterate", "key", "keys", "length", "removeItem", "setItem" ], DefaultConfig = {
                        description: "",
                        driver: DefaultDriverOrder.slice(),
                        name: "localforage",
                        size: 4980736,
                        storeName: "keyvaluepairs",
                        version: 1
                    };
                    function callWhenReady(localForageInstance, libraryMethod) {
                        localForageInstance[libraryMethod] = function() {
                            var _args = arguments;
                            return localForageInstance.ready().then(function() {
                                return localForageInstance[libraryMethod].apply(localForageInstance, _args);
                            });
                        };
                    }
                    function extend() {
                        for (var i = 1; i < arguments.length; i++) {
                            var arg = arguments[i];
                            if (arg) for (var _key in arg) arg.hasOwnProperty(_key) && (isArray(arg[_key]) ? arguments[0][_key] = arg[_key].slice() : arguments[0][_key] = arg[_key]);
                        }
                        return arguments[0];
                    }
                    var localforage_js = new (function() {
                        function LocalForage(options) {
                            for (var driverTypeKey in function(instance, Constructor) {
                                if (!(instance instanceof Constructor)) throw new TypeError("Cannot call a class as a function");
                            }(this, LocalForage), DefaultDrivers) if (DefaultDrivers.hasOwnProperty(driverTypeKey)) {
                                var driver = DefaultDrivers[driverTypeKey], driverName = driver._driver;
                                this[driverTypeKey] = driverName, DefinedDrivers[driverName] || this.defineDriver(driver);
                            }
                            this._defaultConfig = extend({}, DefaultConfig), this._config = extend({}, this._defaultConfig, options), 
                            this._driverSet = null, this._initDriver = null, this._ready = !1, this._dbInfo = null, 
                            this._wrapLibraryMethodsWithReady(), this.setDriver(this._config.driver).catch(function() {});
                        }
                        return LocalForage.prototype.config = function(options) {
                            if ("object" === (void 0 === options ? "undefined" : _typeof(options))) {
                                if (this._ready) return new Error("Can't call config() after localforage has been used.");
                                for (var i in options) {
                                    if ("storeName" === i && (options[i] = options[i].replace(/\W/g, "_")), "version" === i && "number" != typeof options[i]) return new Error("Database version must be a number.");
                                    this._config[i] = options[i];
                                }
                                return !("driver" in options && options.driver) || this.setDriver(this._config.driver);
                            }
                            return "string" == typeof options ? this._config[options] : this._config;
                        }, LocalForage.prototype.defineDriver = function(driverObject, callback, errorCallback) {
                            var promise = new Promise$1(function(resolve, reject) {
                                try {
                                    var driverName = driverObject._driver, complianceError = new Error("Custom driver not compliant; see https://mozilla.github.io/localForage/#definedriver");
                                    if (!driverObject._driver) return void reject(complianceError);
                                    for (var driverMethods = LibraryMethods.concat("_initStorage"), i = 0, len = driverMethods.length; i < len; i++) {
                                        var customDriverMethod = driverMethods[i];
                                        if (!customDriverMethod || !driverObject[customDriverMethod] || "function" != typeof driverObject[customDriverMethod]) return void reject(complianceError);
                                    }
                                    var setDriverSupport = function(support) {
                                        DefinedDrivers[driverName] && console.info("Redefining LocalForage driver: " + driverName), 
                                        DefinedDrivers[driverName] = driverObject, DriverSupport[driverName] = support, 
                                        resolve();
                                    };
                                    "_support" in driverObject ? driverObject._support && "function" == typeof driverObject._support ? driverObject._support().then(setDriverSupport, reject) : setDriverSupport(!!driverObject._support) : setDriverSupport(!0);
                                } catch (e) {
                                    reject(e);
                                }
                            });
                            return executeTwoCallbacks(promise, callback, errorCallback), promise;
                        }, LocalForage.prototype.driver = function() {
                            return this._driver || null;
                        }, LocalForage.prototype.getDriver = function(driverName, callback, errorCallback) {
                            var getDriverPromise = DefinedDrivers[driverName] ? Promise$1.resolve(DefinedDrivers[driverName]) : Promise$1.reject(new Error("Driver not found."));
                            return executeTwoCallbacks(getDriverPromise, callback, errorCallback), getDriverPromise;
                        }, LocalForage.prototype.getSerializer = function(callback) {
                            var serializerPromise = Promise$1.resolve(localforageSerializer);
                            return executeTwoCallbacks(serializerPromise, callback), serializerPromise;
                        }, LocalForage.prototype.ready = function(callback) {
                            var self = this, promise = self._driverSet.then(function() {
                                return null === self._ready && (self._ready = self._initDriver()), self._ready;
                            });
                            return executeTwoCallbacks(promise, callback, callback), promise;
                        }, LocalForage.prototype.setDriver = function(drivers, callback, errorCallback) {
                            var self = this;
                            isArray(drivers) || (drivers = [ drivers ]);
                            var supportedDrivers = this._getSupportedDrivers(drivers);
                            function setDriverToConfig() {
                                self._config.driver = self.driver();
                            }
                            function extendSelfWithDriver(driver) {
                                return self._extend(driver), setDriverToConfig(), self._ready = self._initStorage(self._config), 
                                self._ready;
                            }
                            var oldDriverSetDone = null !== this._driverSet ? this._driverSet.catch(function() {
                                return Promise$1.resolve();
                            }) : Promise$1.resolve();
                            return this._driverSet = oldDriverSetDone.then(function() {
                                var driverName = supportedDrivers[0];
                                return self._dbInfo = null, self._ready = null, self.getDriver(driverName).then(function(driver) {
                                    self._driver = driver._driver, setDriverToConfig(), self._wrapLibraryMethodsWithReady(), 
                                    self._initDriver = function(supportedDrivers) {
                                        return function() {
                                            var currentDriverIndex = 0;
                                            return function driverPromiseLoop() {
                                                for (;currentDriverIndex < supportedDrivers.length; ) {
                                                    var driverName = supportedDrivers[currentDriverIndex];
                                                    return currentDriverIndex++, self._dbInfo = null, self._ready = null, self.getDriver(driverName).then(extendSelfWithDriver).catch(driverPromiseLoop);
                                                }
                                                setDriverToConfig();
                                                var error = new Error("No available storage method found.");
                                                return self._driverSet = Promise$1.reject(error), self._driverSet;
                                            }();
                                        };
                                    }(supportedDrivers);
                                });
                            }).catch(function() {
                                setDriverToConfig();
                                var error = new Error("No available storage method found.");
                                return self._driverSet = Promise$1.reject(error), self._driverSet;
                            }), executeTwoCallbacks(this._driverSet, callback, errorCallback), this._driverSet;
                        }, LocalForage.prototype.supports = function(driverName) {
                            return !!DriverSupport[driverName];
                        }, LocalForage.prototype._extend = function(libraryMethodsAndProperties) {
                            extend(this, libraryMethodsAndProperties);
                        }, LocalForage.prototype._getSupportedDrivers = function(drivers) {
                            for (var supportedDrivers = [], i = 0, len = drivers.length; i < len; i++) {
                                var driverName = drivers[i];
                                this.supports(driverName) && supportedDrivers.push(driverName);
                            }
                            return supportedDrivers;
                        }, LocalForage.prototype._wrapLibraryMethodsWithReady = function() {
                            for (var i = 0, len = LibraryMethods.length; i < len; i++) callWhenReady(this, LibraryMethods[i]);
                        }, LocalForage.prototype.createInstance = function(options) {
                            return new LocalForage(options);
                        }, LocalForage;
                    }())();
                    module.exports = localforage_js;
                }, {
                    3: 3
                } ]
            }, {}, [ 4 ])(4);
        }, module.exports = f();
    }).call(exports, __webpack_require__(34));
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var events_1 = __webpack_require__(139);
    exports.Offline = function(onlineHandler, offlineHandler, win) {
        return void 0 === win && (win = window), events_1.listen(win, {
            online: onlineHandler,
            offline: offlineHandler
        }), {
            stop: function() {
                return events_1.unlisten(win, {
                    online: onlineHandler,
                    offline: offlineHandler
                });
            }
        };
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    }), exports.current = function(state) {
        return state.user;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Config = __webpack_require__(10), request_1 = __webpack_require__(205), experiment_1 = __webpack_require__(672), config_1 = __webpack_require__(11), util_1 = __webpack_require__(2), USE_SESSION_LIFE_TIME = 30 * util_1.MINUTE;
    exports.LOGIN_BY_COOKIE_CHANGE_TIMEOUT = 20 * util_1.SECOND, exports.MAX_COOKIE_HEADER_LENGTH = 7168, 
    exports.fetchUser = function(containerId) {
        var options = {
            method: "post",
            query: !0,
            headers: {
                "X-Client-Type": "extension-" + Config.getGlobal().bundleInfo.browser,
                "X-Client-Version": "" + Config.getGlobal().buildInfo.version
            },
            data: Object.assign({
                app: util_1.getBrowser() + "Ext"
            }, containerId ? {
                containerId: containerId
            } : {})
        };
        return request_1.fetch(config_1.URLS.userOrAnonymous, options);
    }, exports.isItTimeToRefresh = function(loginDate) {
        return !loginDate || Date.now() - new Date(loginDate).getTime() > USE_SESSION_LIFE_TIME;
    }, exports.fetchMimic = function(containerId) {
        var options = {
            data: containerId ? {
                containerId: containerId
            } : {},
            headers: {
                "X-Client-Type": "extension-" + Config.getGlobal().bundleInfo.browser,
                "X-Client-Version": "" + Config.getGlobal().buildInfo.version
            }
        };
        return request_1.fetch(config_1.URLS.dapiMimic, options);
    }, exports.fetchStats = function(containerId) {
        var options = {
            data: {
                containerId: containerId,
                regex: "STAT:.*"
            },
            headers: {
                "X-Client-Type": "extension-" + Config.getGlobal().bundleInfo.browser,
                "X-Client-Version": "" + Config.getGlobal().buildInfo.version
            }
        };
        return request_1.fetch(config_1.URLS.dapiProps, options);
    }, exports.prepareUser = function(data, dapiData, statsData, grauth) {
        void 0 === data && (data = {}), void 0 === dapiData && (dapiData = {}), void 0 === statsData && (statsData = {}), 
        grauth = grauth || "empty";
        var mimic = dapiData.groups || [], settings = dapiData.settings || {};
        data.token = data.grauth, data.premium = "Premium" === data.type, data.experiments = experiment_1.UserExperiments.create(mimic);
        var fixedErrors = parseInt(statsData["STAT:feedback_ACCEPT"], 10) || 0;
        return data.fixed_errors = isNaN(fixedErrors) ? 0 : fixedErrors, config_1.userFields.reduce(function(result, field) {
            var _a, value = data[field];
            return void 0 !== value && Object.assign(result, ((_a = {})[field] = value, _a)), 
            result;
        }, {
            mimic: mimic,
            settings: settings,
            grauth: grauth
        });
    }, exports.authRequestHelper = function(url, data) {
        return request_1.fetch(url, {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
                "X-Client-Type": "extension-" + Config.getGlobal().bundleInfo.browser,
                "X-Client-Version": "" + Config.getGlobal().buildInfo.version
            },
            method: "post"
        });
    }, exports.createCookieChannel = function(watchToken) {
        var channel = util_1.createChannel();
        return watchToken(channel.put), channel;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var tracking_1 = __webpack_require__(7), bg_1 = __webpack_require__(103);
    exports.update = function(api, shouldReloadTab) {
        return __awaiter(this, void 0, void 0, function() {
            var notification, tabs, tabsToReload, onClick, _this = this;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return notification = api.notification, [ 4, function(tabs, shouldReloadTab) {
                        return __awaiter(this, void 0, void 0, function() {
                            return __generator(this, function(_a) {
                                switch (_a.label) {
                                  case 0:
                                    return [ 4, tabs.getAllTabs() ];

                                  case 1:
                                    return [ 2, _a.sent().filter(function(_a) {
                                        var id = _a.id, url = _a.url;
                                        return url && shouldReloadTab(url) && (!id || id.toString() !== bg_1.SETTINGS_TAB_ID);
                                    }) ];
                                }
                            });
                        });
                    }(tabs = api.tabs, shouldReloadTab) ];

                  case 1:
                    if (!(tabsToReload = _a.sent()).length) return [ 2 ];
                    switch (notification.kind) {
                      case "web-extension":
                        onClick = function() {
                            return __awaiter(_this, void 0, void 0, function() {
                                return __generator(this, function(_a) {
                                    return "web-extension" !== tabs.kind ? [ 2 ] : (tracking_1.felog.reloadNotificationClick(), 
                                    tabsToReload.forEach(function(_a) {
                                        var id = _a.id;
                                        return tabs.reload(id);
                                    }), [ 2 ]);
                                });
                            });
                        }, notification.create({
                            title: "Grammarly needs to be reloaded",
                            message: "While you were working, we updated Grammarly. To take advantage of these improvements, please save the text you are working on, and click here.",
                            iconUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAIAAAAErfB6AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDE0IDc5LjE1Njc5NywgMjAxNC8wOC8yMC0wOTo1MzowMiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTQgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MTgzMjhCMkQ1NjBGMTFFNDg0NjBEMENBNkVFNzA3RDkiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MTgzMjhCMkU1NjBGMTFFNDg0NjBEMENBNkVFNzA3RDkiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxODMyOEIyQjU2MEYxMUU0ODQ2MEQwQ0E2RUU3MDdEOSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoxODMyOEIyQzU2MEYxMUU0ODQ2MEQwQ0E2RUU3MDdEOSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pg1zYWQAAA/kSURBVHja7J15dFNVHsfz0nRJ06ZN932FbtBSoK2AlM2hVhYZAetURWhZnBEQBIvjMIvjco6WEQVZBBmqIiCoqFSQw14KCHSl1G50pUuabiFJmzTdMr9DHY/CS0iT+5Yk93v4Q5P0vnd/n/fu/f3uvb97CY1Gw8EyX3GxCTBgLAwYCwPGwoCxMGAsDBgLA8aAsTBgLAwYCwPGwoCxMGAsDBgDxsKAsTBgLAwYCwPGwoCxMGAsDBgDxsKAsTBgLAwYCwPGwoCxMGAMGAsDxsKAsTBgLAwYCwPG0imeBda5d7C/uru1Ui5uUnY1q7paVFJpX4+sTykfUPUPDf76M2uulZDHd7KxF9kIfPgiX76Ln71LuNB7lIOXnZW1qVSWsJBddtp65T91VBVK6wu66up62oaMqDWXIIIFHhNdgieIgia7hXnYCTFgxlSlEJ9sKc5pK6+Qt1B0iQihz3SPyDk+sWGO3hgwTWpXy4815n3flF/X007bRYMF7gv84hb6x7vbCjFgqgSNcFbtxQuSskHNECM3YEVwZ3pGpYXMgAYcA0ap3PaKHVWnS+7eYcn9xDgHrAlLSnSPwICN1Y3OmvcrTrAH7X2YN0bMTXANxYANEcQ5meXZZ1pvsfw+Z3tFb4qcD1EWBqyvoIvNqs3Zefs0BLUmccMQOq8enZQWMh06aQz4IarplmQUHSqXN5vcnUcKfbeMfzbUwRMDJpeGoznccDWzLFs9NGCi3Yotl7cpan5q4BSCQ2DAv5NyQL255Ogp8U0z8PmTvce9E5Niz7PFgH/RHWXnS3n7oXE2m5AdGupd8ekB9q4YMKdIWr86P0va18MxL4lsBDvj0sZTOSRiAoDPS37eUHjAdDvdh3bJWycsmeU5xkIBn2wpfq348IBmkGO+4hFW78WmzvGJtTjAQDej+OCQBUxocgliS+xzVDBm74oOaJnh3R2yjOlqqCZUFqpsKYDBq4J+17xb5vsElYUqQ8XNHzBEROAzm6tXpUNQZag4VN+cASsH1BDvml9EpKeg4lB9MIJ5AtZwNJtLjprTaIYBguqDEcAUaFx0VtXtcMNVRkYirblW3nbOnnxnoTWfR3C5BLdvaEDRr+pQK8Squ6rBPprvB4wQ3xDybOCjZhUmwZO7KPcDerpegkNEOflOch011tk/xjnAhy/S8WNgXKUQF3TVFUrriqUN9CwGsuXyvkl8xfh5J7YABqs9fXkbDTOAgPOPfnGzPMd42jkZ8OeyfuXZ1tLjzQV5nbWoWlFtihT6fjV1nZHzx2wBvK/mwvsVJ6grH8w0z3fCkqCpY5z8ULn6n9bmfNuUR+mKg40Rc1eEzjR5wE3KrvmXtlBkKS5BJHuPWxeWHCBwQ144dNK7bp85eucaRe22nZV19rQMY9b6sALwywWfUbSuCvqwt2KeHk/xClbwHv5162vopKkofLZX9PaJS00Y8I3OmqXXdlPx4q4MnbV6dBJ4yPQEeAfqLkMv00eBk/jZpL8YvC6T+TiYiq7Xydp+T/yK9eFP0EN32C1/ITjx8JS1VCydNMZEDL/Bue0Vq27sQ1tmsMB93yOrdEc+v0rSK8vvqi25e6daIRGrpJ193T0DaqAl4Nm62ToCrdGOXrGiIHiBHHl2+hQo7etZk59ViHpIeW/CCsPW0DMM+Jkr29EuWAcn+ZOElSIbge6fAcjvGvNOiovLZHoFZjzCarLb6Cf9JiZ5RdtwHzI6BN7ihqIDFyRlaKO7I4++bGKA4TF/7uoOhAWOdfLPmvSig85XDcKbPdVns5sLf5sKrL9cbRyeD566NHga38pGx88GNINr8z+72IaS8cEpawzId2IS8NqCT8+2lqIqLVDgBl2gjncX2t7tVacO1V81fhYSMK+PeGKx/yO63+P063sQTv/9wWvsRxOXmQzgdrV85rm3UYWP4FV9k7jel6/VwbneWf36zS/FqrsIqxDnEvJu7J90XFTWr1yU+2GzqgvVWM2Fx/4+0txUxrzoY415qOiCT/RebKoOQ++pPrf8+l60dEHgnT11aes57csw4LGDENaWi2ZGB8wFRjOZMOn7pnxURS0PnTHdI5L0qyGNBl7cDyt/pGikSTHQuzb/073V57X9IMrJ95WIOQwajRnAVQoxqtz7IIH72rDHtdHNKD74HbonSdsQxweVJ98tO67tBxAfgw+M5FpgNDCdCQA+2VKMqnF+I3qRtrjljdKvUV3o4YNNdZe2lP+g7SZTAiYxZTpmAOe0lSMp53HvmEdcR5F+9Xld7ld3rtNZqf21F+GipF8hHN4aqekYANzWK0ey5w2XINaEJZF+VSpr/E/FD/RXLbM8+1pn9YOf13a3oboEmA4MyGrAP3VUISkn2Xsc6YKH/qHBv908Ytg4hvGObkbRQUW/6r6A+ICWN5sGAzIAGNU47ZKgRC2N86XbilamooMOteKFa7tv3W0c/t+absmKG3vR7uY0IgMysOgOybxpmKN3rCiQNG7ZU3Oew6igFU25sk1kI+ARVu1qObMGpBswtFd1PQg6pIX+8aSfQ2N4XwvJlKhb2g0GBDPquV8m3U10dXcrknQj0nzLAc3goforHHMXGBDMyNI+uFIuNr4Q8K38yRLjL0rKO/u6ORYg/c1IN+AmJYKR98luo0k//1FczLEM6W9GugEjmVqJdvYnbbgut1daCGD9zUg34BaV1PhCSNc2VynEcna4V6wyI92AjfctuQQRJHB/8PNSWSPHYqS/GekGLOtTGlmCq40jaTZHDbrhQPZLfzPSDVg+YGwrqi2nSIJ6Pp/N0t+MdAM2fojYnke+2q3LknLG9Tej+RyrQ38Wr0nIfADTvE0vBky3TOgsI3MGbHyykLZg18XGwXKw6W9GugELeXwjS2hXK0g/97UXWQ5g/c1IN2AnG3sjS+hSd5OugQ0WeFgOYP3NSDfgh6aFPVQajqaebIEE6QC1uUp/M9INWM+sTt26KSVJSAxx8DD+6TEV6W9Guld06Egw0V+lssYHV3QQHGKKW9iJliLqbh4uMctrzHjnQGsjslF23T4j61fSZka6ASNZIZzfVUv6eZJ3NHWAbbm8XfHp8AwZWc7ndbnGA9bfjHQ30eFCBEd03la03unpePDz6R5RjtZ8iu58eehM4+nSb0a6AY9y8OISCI6TId2VB16yhX7xFN15svc4toxdEASYkaWA7ayskcQzJ7Sk6CwLnkbRxivaJjnoFxhQ/2E7BoYqJ7oEG19IubyZdHmwF9/5mYDJVNx2iZQth1+OyIAMAEZ1sK62TK+Xwx53pWDYclvVKZbsYj0iAzIAeDIiV+WcpJR0xAP8rH9HL0Z+2w09HSlXth1vLmjtlSkGeu/7V9fTfqmtHL5lmwEZSF3xsBNGCH2MTzAc1Axllmfvikt/8KvHvMY+HzT1i/rLaO+8Sdn1WvFhHVHyzrg0qq0HpgMDsvoNvhfPRCIp54KkjDRdE/TXqCenuofTWal14ckzPaPYZjpmACM8IOit0mOk20NaEdztE5cicej0UWrglBdHPcZC0zEDOMzRO5hs6asBqu1u21Z5ivQrvpXNvoRV0wzaAXBkYyAhM/45diEtAZI7mM4EAIMW+MWhKiqrNudSe4W2sHt3/PL0kBkUHdZry+W9HZPyauQ81hqNMcAL/eNRraLScDQZRQfrtSRZcwkiI3LexwnLIURG7u8ceXTdIv8EeiwG5tKWNMtGwO62QoQuibxf9WLef3WkFkJD/cO0jFWjZiFZuiWyEbweteDrqet1jAmDy4126zUw10i3ueMwu+guLWQGwtLu9HSkX9ujYyxCwLN9JXzOmZl/A2/I4JEQP3uX1yLnn5u1+YXgRB0tkKRXtvLGJ2jnpw0zF5PnJk0QBcU4ByDcTrhKIV527eNPElbqiBTdbB3Xhz+xJizpcnvlmdZb1zqq9UnkCnXwfNQ9LMkrRh+3vFnVlX59L4F0oScYyrARQIYPxgJDo90QHBinXv1od3y6bm+TR1jN8IiCf/DfnWpFpULcqOxsVcmgqR9eQA9snKztffiiAIFrpNBXqPcsZKms8c95+6HM2V7RaA1l2B8yDDjRPQLtS8y5l1qZenXHm9GL5/qM1+f3rraOU2wdkVz6WGPem6XfDJ/t5aDfDvF6vr6JhgZ7zC983xgxF3mZygH1q0UHX7/5pWKgl55ayPqVG4u+2FxyhIqT24wxEfOAE1xD0bZmv+q7pvx5OZmUrtIaVnZz4dyLmRTtiwnGMfjIFQ5LUlc2Rc6nKPGkrVcOr/Liyx+eo+BwbRB4ailXtm0qPqT/5i8jOhAPzALGMeYOWXH6KMQeq0cnUXe03c+ypjX5WeArLQuZBp6w8Q9T/9Dg6daSz+tydXgP4t67pH/YqSUzg1RgFiOXKVrc4ZQQDSd7jxtu93QfrEGK50ZnzVnJLWiNH7ofCETJJ6ZvCvz9eXrHmwt0TDjeJ7M6nJJD7/GywwBiRYHjRUEQ44Y4eATYuzk/kA8CPlqzsqu+p71SLr55t6FIWj+iAxYhVNuTsMLr/1sSwMMBDYmefp+5HS87rEMNV94q/ZbBG4DYxp5nY03wlIPqngG18efUQXcAEY67rXD4BGL9O+B/jH3K3A6IHnZANhR+wcgh4KwSdCJbJzyPZAaMXQngUKV3YlKMb5dMWlB9MAKq+U3WZfjb82x3xadbThrZfYKKQ/XBCKgKZOMWDgH2rjvj0lAdN2RCgipDxQPI9lk1K8AgcG63TljCI6wshy5UFqqM/Cxr9m7CMstzzHuxqUgSmdgvqCZUlnQTbLMFzLm3gnBL7HNm/x5DBaGaCFeasjdMItV5yc8bCg/QNgBCf78LLTMV767JAAYVSetX52dJzW6zQvCZwatC3u+aHmDOvYOdX8rbX9MtMad4FyIitD6zCQPm3JvG31xy1DzGuZK9x70Tk4Iw3jUHwJx7Y5mHG65mlmWbbpcMne6mqPmpgVMoWotv2oCHBQ11RtEhGuYWkStS6Ltl/LN0jsWaJGDOvfnjrNqcnbdPj2j+jkHZWVmvHp2UFjKd5l1xTRXwsJqUXZnl2aQbsrBKs72iN0XOR3jIrKUAHtaNzpr3K06gXXuLSjHOARsj5hqzag4D/kW57RU7qk6zBzOgXROWlEh98qqlAB5WobQ+q/biBUkZ6Y60NAi62JmeUWkhMyZQOXxhuYCH1a6WH2vM+74pH+3BvboVLHBf4Be30D/egBxADNhAVSnEJ1uKc9rKkRwqT6oIoc90j8g5PrEjzb3HgFGqrVf+U0cVNOAFXXV1PW3GHHHLJYhggcdEl2BohCe7hY1ozxsMmA5B6Fzd3VopF0OU1azqalFJpX09sj6lfED12/OIrLlWQh7fycZeZCPw4Yt8+S4Q54QLvUc5eJnQASCWCNiihM8awoCxMGAsDBgLA8bCgLEwYCwMGAPGwoCxMGAsDBiLav1PgAEASePGMkSWuH0AAAAASUVORK5CYII=",
                            buttons: [ {
                                title: "Reload",
                                iconUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA3NpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8wMy8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDowZDJiMWMzMi1mODMzLTQxOTgtOGVlMy05YWY1OGVmOGUzNzEiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RjFBODMzNzYxQkREMTFFNDk0ODFGNTFFRDg1MkEzMjUiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MkY1RjA5NjYxQkREMTFFNDk0ODFGNTFFRDg1MkEzMjUiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChNYWNpbnRvc2gpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6N2FmMWVkMGUtZjZkZC00YmYwLWE2MjctNTBkMjA4MjRiZDViIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjBkMmIxYzMyLWY4MzMtNDE5OC04ZWUzLTlhZjU4ZWY4ZTM3MSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PuUD9ZcAAAM8SURBVHjatJbbS1RRFIePOjqG99LSLFMzoazMFLsHQQVFl8fee+qhP6cX3+sxiG6QFV0MNCjNjAyx1MoumpmXsRnz0m/Bd2A3TNocpw0fw5lz9v7tddlr7bSWlhYvwNgqzosMcVl0JrtAyAs2FkSeKBQ7xKT4Kqb+t/CcqBD1olpsEDdFdyqF00Q+FtpvWDSLWrEeMsUqPPBRjIifbDCwcBiROrFLrBU1Yp3zzWZxju/axCMxsJTr/yacLopwZw0WWix3i5IE3+eBbSYiXovhIK42KxvESaw0i9aIHC9FI5TguRDLToszWG1jXnwQ4yKb/7N5N01Wd8KomE1GOFc0irPioCh33r0Q98Rz3H/B2ZTF84ZojUuuZYXToEocEydEJe/MymeiQ9wVXaJJHCeT7f01jlNXsq5Ow23VxLaM/79gyXUxJD7x/y/eRcVV8RArk45xLgm0X+wkuSax0iy5EzdvTNyngpm134MmVz5VyEQLREz0inbiFz++sZlFNuitRLiBs5qJG5+KB+J9gnlRYht4pDvntoSiYeOH6BP9WJ/y4VucRSnM4tlK3TvO7EqGVbNNeNRfd9B+feEMpxj4xWImBYaZ6EVCaOOVuCR6QnFdKNXDCtBRToxHVbzixng+rtKEUlSXQ3GeG/FLqS88S62NObGxKraaMCQ7MkjUSidvYpTTqCscQ9gvBHaWt1DJwgGEw9TzWtbyWHvEN86P8QRNwJp9MbttZofWed4kKWzN44jYw1pWYnu4Gk26FtvDS15OsOM6SmhVAIttzl5uo2HW7EFjyrU4QsFop/Ef4OztE5+pyUNUtAgWuCOTZCzlCJ1ibj4x7WbtPj/GvvAivn9LI6/kCJRyIShjYhvfjMYJF/L9IQSbmOtxBepkXgytP4TnaQit9NnDYpvYCBXcKPv5LsLcHFxbg3CjcwW2u9dj1hxAI+ENJEIzT8e9BbjOIwSlxGjaubqGaKt5jpW+pdanb7FmZKmrzxy99gm7m6NdVpGd5csk1TgMENfbhGjmX2+ZUY7XGHGtJ0O308WKnROxQH8epRb3IjpI64wmc71dQHSMLjVDHhRR08NOU4kiPExMO2DJC8JvAQYA0OLb9zl5D+gAAAAASUVORK5CYII="
                            } ],
                            onButtonClicked: onClick
                        });
                        break;

                      case "safari":
                        notification.create(function(reloadTabs) {
                            return {
                                title: "Grammarly needs to be reloaded",
                                message: "While you were working, we updated Grammarly. To take advantage of these improvements, please save the text you are working on, and click here.",
                                onClicked: reloadTabs
                            };
                        }());
                        break;

                      default:
                        throw new Error("Unsupported notification type");
                    }
                    return tracking_1.felog.reloadNotificationShow(), [ 2 ];
                }
            });
        });
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    }, __values = this && this.__values || function(o) {
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
    });
    var redux_saga_1 = __webpack_require__(148), omit = __webpack_require__(1157), effects_1 = __webpack_require__(99), actions_1 = __webpack_require__(98), selectors = __webpack_require__(670), log = __webpack_require__(1).Logger.create("universal.bg.state.connection.sagas"), ConnectionSagas = function() {
        function ConnectionSagas(_prefs, _emitTabs, _telemetry, _isIncognito, _getNextPingDate) {
            this._prefs = _prefs, this._emitTabs = _emitTabs, this._telemetry = _telemetry, 
            this._isIncognito = _isIncognito, this._getNextPingDate = _getNextPingDate;
        }
        return ConnectionSagas.prototype.start = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 5, __values(redux_saga_1.takeLatest(actions_1.t.UPDATE_CONNECTION, this.checkOnline.bind(this))) ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, ConnectionSagas.prototype.checkOnline = function() {
            var currentConnection, currentOnline, connectionErrors_1, newOnline, error_1;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return _a.trys.push([ 0, 7, , 8 ]), [ 4, effects_1.select(selectors.current) ];

                  case 1:
                    return currentConnection = _a.sent(), currentOnline = currentConnection.online, 
                    connectionErrors_1 = omit(currentConnection, "online", "authDegradation", "cookiesDisabled"), 
                    currentConnection.cookiesDisabled ? [ 4, effects_1.fork([ this, this.monitorCookiesDisable ]) ] : [ 3, 3 ];

                  case 2:
                    _a.sent(), _a.label = 3;

                  case 3:
                    return newOnline = Object.keys(connectionErrors_1).map(function(key) {
                        return connectionErrors_1[key];
                    }).every(function(on) {
                        return !on;
                    }), currentOnline === newOnline ? [ 2 ] : [ 4, effects_1.put(actions_1.onlineConnection(newOnline)) ];

                  case 4:
                    return _a.sent(), newOnline ? (log.trace("ONLINE SERVICE| reseting capi connections after offline"), 
                    [ 4, effects_1.call(this._emitTabs, "reset") ]) : [ 3, 6 ];

                  case 5:
                    _a.sent(), _a.label = 6;

                  case 6:
                    return [ 3, 8 ];

                  case 7:
                    return error_1 = _a.sent(), redux_saga_1.isCancelError(error_1) ? [ 2 ] : [ 3, 8 ];

                  case 8:
                    return [ 2 ];
                }
            });
        }, ConnectionSagas.prototype.monitorIsIncognito = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._isIncognito) ];

                  case 1:
                    return _a.sent() ? [ 4, effects_1.call([ this, this.callDaily ], this._telemetry.incognitoInit) ] : [ 3, 3 ];

                  case 2:
                    _a.sent(), _a.label = 3;

                  case 3:
                    return [ 2 ];
                }
            });
        }, ConnectionSagas.prototype.monitorCookiesDisable = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call([ this, this.callDaily ], this._telemetry.disabledCookiesInit) ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, ConnectionSagas.prototype.callDaily = function(fn, type, name) {
            var pingDate, nextDate;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.get, name) ];

                  case 1:
                    return !(pingDate = _a.sent()) || pingDate < Date.now() ? [ 4, effects_1.call(fn, type, name) ] : [ 3, 5 ];

                  case 2:
                    return _a.sent(), [ 4, effects_1.call(this._getNextPingDate) ];

                  case 3:
                    return nextDate = _a.sent(), [ 4, effects_1.call(this._prefs.set, name, nextDate) ];

                  case 4:
                    _a.sent(), _a.label = 5;

                  case 5:
                    return [ 2 ];
                }
            });
        }, ConnectionSagas;
    }();
    exports.ConnectionSagas = ConnectionSagas;
}, function(module, exports, __webpack_require__) {
    var arrayMap = __webpack_require__(85), baseClone = __webpack_require__(358), baseUnset = __webpack_require__(443), castPath = __webpack_require__(83), copyObject = __webpack_require__(37), customOmitClone = __webpack_require__(1158), flatRest = __webpack_require__(1159), getAllKeysIn = __webpack_require__(359), omit = flatRest(function(object, paths) {
        var result = {};
        if (null == object) return result;
        var isDeep = !1;
        paths = arrayMap(paths, function(path) {
            return path = castPath(path, object), isDeep || (isDeep = path.length > 1), path;
        }), copyObject(object, getAllKeysIn(object), result), isDeep && (result = baseClone(result, 7, customOmitClone));
        for (var length = paths.length; length--; ) baseUnset(result, paths[length]);
        return result;
    });
    module.exports = omit;
}, function(module, exports, __webpack_require__) {
    var isPlainObject = __webpack_require__(177);
    module.exports = function(value) {
        return isPlainObject(value) ? void 0 : value;
    };
}, function(module, exports, __webpack_require__) {
    var flatten = __webpack_require__(357), overRest = __webpack_require__(196), setToString = __webpack_require__(198);
    module.exports = function(func) {
        return setToString(overRest(func, void 0, flatten), func + "");
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
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
    });
    var redux_saga_1 = __webpack_require__(148), effects_1 = __webpack_require__(99), tracking = __webpack_require__(7), stdlib_1 = __webpack_require__(3), util_1 = __webpack_require__(2), tracking_1 = __webpack_require__(216), helpers_1 = __webpack_require__(1161), actions = __webpack_require__(89), selectors = __webpack_require__(671), newsVersion = __webpack_require__(10).getGlobal().appConfig.newsVersion, SettingsSagas = function() {
        function SettingsSagas(_prefs, _dapi, _reconnectAllSockets, _emitFocusedTab) {
            this._prefs = _prefs, this._dapi = _dapi, this._reconnectAllSockets = _reconnectAllSockets, 
            this._emitFocusedTab = _emitFocusedTab;
        }
        return SettingsSagas.prototype.start = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, [ redux_saga_1.takeEvery(actions.DAPI_ACTIONS, this.saveToDapi.bind(this)), redux_saga_1.takeEvery(actions.CACHED_ACTIONS, this.cacheSettings.bind(this)), redux_saga_1.takeLatest(actions.t.SAVE_ANONYMOUS_PROPERTIES, this.saveAnonymousDapiProps.bind(this)), redux_saga_1.takeLatest(actions.t.DISABLE_ON_TAB, this.disableOnTab.bind(this)), redux_saga_1.takeLatest(actions.t.SAVE_EMAIL_CONNECTEDNESS_DATA, this.saveEmailConnectednessData.bind(this)) ] ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.initializeDapiProps = function() {
            var _a, _b, _i, prop;
            return __generator(this, function(_c) {
                switch (_c.label) {
                  case 0:
                    for (_b in _a = [], helpers_1.dapiPropsMap) _a.push(_b);
                    _i = 0, _c.label = 1;

                  case 1:
                    return _i < _a.length ? (prop = _a[_i], [ 4, effects_1.call([ this, this.initializeDapiProp ], helpers_1.dapiPropsMap[prop]) ]) : [ 3, 4 ];

                  case 2:
                    _c.sent(), _c.label = 3;

                  case 3:
                    return _i++, [ 3, 1 ];

                  case 4:
                    return [ 2 ];
                }
            });
        }, SettingsSagas.prototype.initializeDapiProp = function(prop, cacheReset) {
            var key, cache, value, newCache, _a, _b;
            return void 0 === cacheReset && (cacheReset = !1), __generator(this, function(_c) {
                switch (_c.label) {
                  case 0:
                    if (void 0 === prop) throw new Error("Incorrect DAPI property name");
                    return [ 4, effects_1.call([ this, this.getDapiPropsPrefsKey ]) ];

                  case 1:
                    return key = _c.sent(), [ 4, effects_1.call(this._prefs.get, key) ];

                  case 2:
                    return (cache = _c.sent()) && cache[prop] && !cacheReset ? [ 4, effects_1.put(actions.setDapiProp(prop, cache[prop])) ] : [ 3, 4 ];

                  case 3:
                    return _c.sent(), [ 3, 11 ];

                  case 4:
                    return _c.trys.push([ 4, 10, , 11 ]), [ 4, effects_1.call(tracking.felog.initializePropFromDapi, prop) ];

                  case 5:
                    return _c.sent(), [ 4, effects_1.call(this._dapi.common[prop]) ];

                  case 6:
                    return null === (value = _c.sent()) ? [ 3, 9 ] : [ 4, effects_1.put(actions.setDapiProp(prop, value)) ];

                  case 7:
                    return _c.sent(), newCache = Object.assign({}, cache, ((_a = {})[prop] = value, 
                    _a)), [ 4, effects_1.call(this._prefs.set, (_b = {}, _b[key] = newCache, _b)) ];

                  case 8:
                    _c.sent(), _c.label = 9;

                  case 9:
                    return [ 3, 11 ];

                  case 10:
                    return _c.sent(), [ 3, 11 ];

                  case 11:
                    return [ 2 ];
                }
            });
        }, SettingsSagas.prototype.resetStrongDialectFromDapi = function() {
            var strongDialect;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return strongDialect = helpers_1.dapiPropsMap[actions.t.CHANGE_STRONG_DIALECT], 
                    [ 4, effects_1.call([ this, this.initializeDapiProp ], strongDialect, !0) ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.saveToDapi = function(_a) {
            var propName, dapiPropsKey, cache, newCache, strongDialect, _b, _c, type = _a.type, data = _a.data;
            return __generator(this, function(_d) {
                switch (_d.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors.getDapiProp, type) ];

                  case 1:
                    return _d.sent() === data ? [ 2 ] : (propName = helpers_1.dapiPropsMap[type], [ 4, effects_1.call([ this, this.getDapiPropsPrefsKey ]) ]);

                  case 2:
                    dapiPropsKey = _d.sent(), _d.label = 3;

                  case 3:
                    return _d.trys.push([ 3, 5, , 6 ]), [ 4, effects_1.call(helpers_1.dapiPropsSetter[propName], this._dapi, data) ];

                  case 4:
                    return _d.sent(), [ 3, 6 ];

                  case 5:
                    return _d.sent(), [ 3, 6 ];

                  case 6:
                    return [ 4, effects_1.call(this._prefs.get, dapiPropsKey) ];

                  case 7:
                    return cache = _d.sent(), newCache = Object.assign({}, cache, ((_b = {})[propName] = data, 
                    _b)), [ 4, effects_1.call(this._prefs.set, (_c = {}, _c[dapiPropsKey] = newCache, 
                    _c)) ];

                  case 8:
                    return _d.sent(), [ 4, effects_1.put(actions.setDapiProp(propName, data)) ];

                  case 9:
                    return _d.sent(), [ 4, effects_1.call(tracking_1.fire, "set-dapi-prop", propName, data) ];

                  case 10:
                    return _d.sent(), strongDialect = helpers_1.dapiPropsMap[actions.t.CHANGE_STRONG_DIALECT], 
                    propName !== strongDialect ? [ 3, 12 ] : [ 4, effects_1.call(this._reconnectAllSockets, data) ];

                  case 11:
                    _d.sent(), _d.label = 12;

                  case 12:
                    return [ 2 ];
                }
            });
        }, SettingsSagas.prototype.setInitialSettings = function() {
            var data;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call([ this, this.getSettings ]) ];

                  case 1:
                    return data = _a.sent(), [ 4, effects_1.put(actions.initialSettings(data)) ];

                  case 2:
                    return _a.sent(), [ 4, effects_1.call([ this, this.setShowNews ]) ];

                  case 3:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.cacheSettings = function() {
            var extensionSettings;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors.current) ];

                  case 1:
                    return extensionSettings = _a.sent(), [ 4, effects_1.call(this._prefs.set, {
                        extensionSettings: extensionSettings
                    }) ];

                  case 2:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.getDapiPropsPrefsKey = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors.getUserId) ];

                  case 1:
                    return [ 2, "dapiProps_" + _a.sent() ];
                }
            });
        }, SettingsSagas.prototype.setShowNews = function() {
            var common, previousNewsVersion, showNews;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors.current) ];

                  case 1:
                    return common = _a.sent().common, previousNewsVersion = common && Number.isInteger(common.seenNewsVersion) && parseInt(common.seenNewsVersion, 10), 
                    showNews = newsVersion !== previousNewsVersion && newsVersion > 0, [ 4, effects_1.put(actions.showNews(showNews)) ];

                  case 2:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.getSettings = function() {
            var settings, old, extensionSettings;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.get, "extensionSettings") ];

                  case 1:
                    return (settings = _a.sent()) ? [ 2, settings ] : [ 4, effects_1.call(this._prefs.get, helpers_1.oldSettingsFields) ];

                  case 2:
                    return old = _a.sent(), [ 4, effects_1.call(helpers_1.migrateSettings, old) ];

                  case 3:
                    return extensionSettings = _a.sent(), [ 4, effects_1.call(this._prefs.set, {
                        extensionSettings: extensionSettings
                    }) ];

                  case 4:
                    return _a.sent(), [ 2, extensionSettings ];
                }
            });
        }, SettingsSagas.prototype.saveAnonymousDapiProps = function(_a) {
            var props = _a.props;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.set, helpers_1.anonymousDapiPropsKey, props) ];

                  case 1:
                    return _b.sent(), [ 4, effects_1.select(selectors.getUserAnonymous) ];

                  case 2:
                    return !1 !== _b.sent() ? [ 3, 4 ] : [ 4, effects_1.call([ this, this.setAnonymousPropsToDapi ]) ];

                  case 3:
                    _b.sent(), _b.label = 4;

                  case 4:
                    return [ 2 ];
                }
            });
        }, SettingsSagas.prototype.setAnonymousPropsToDapi = function() {
            var props, _a, _b, _i, key;
            return __generator(this, function(_c) {
                switch (_c.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.get, helpers_1.anonymousDapiPropsKey) ];

                  case 1:
                    if (null == (props = _c.sent())) return [ 3, 10 ];
                    for (_b in _a = [], props) _a.push(_b);
                    _i = 0, _c.label = 2;

                  case 2:
                    if (!(_i < _a.length)) return [ 3, 7 ];
                    key = _a[_i], _c.label = 3;

                  case 3:
                    return _c.trys.push([ 3, 5, , 6 ]), [ 4, effects_1.call(helpers_1.dapiPropsSetter[key], this._dapi, props[key]) ];

                  case 4:
                    return _c.sent(), [ 3, 6 ];

                  case 5:
                    return _c.sent(), [ 3, 6 ];

                  case 6:
                    return _i++, [ 3, 2 ];

                  case 7:
                    return [ 4, effects_1.call(this._prefs.remove, helpers_1.anonymousDapiPropsKey) ];

                  case 8:
                    return _c.sent(), [ 4, effects_1.call([ this, this.resetStrongDialectFromDapi ]) ];

                  case 9:
                    _c.sent(), _c.label = 10;

                  case 10:
                    return [ 2 ];
                }
            });
        }, SettingsSagas.prototype.disableOnTab = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(this._emitFocusedTab, "disable-on-tab") ];

                  case 1:
                    return _a.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.saveEmailConnectednessData = function(_a) {
            var savedEmailConnectednessData, connectednessPropsData, sender, recipiants, timestamp, timezoneOffset, emailType, _b, hashedS, hashedR, emailConnectednessData = _a.emailConnectednessData;
            return __generator(this, function(_c) {
                switch (_c.label) {
                  case 0:
                    return [ 4, effects_1.call(this._prefs.get, helpers_1.emailConnectednessDataPropsKey) ];

                  case 1:
                    return savedEmailConnectednessData = _c.sent(), connectednessPropsData = null !== savedEmailConnectednessData ? savedEmailConnectednessData : [], 
                    sender = emailConnectednessData.sender, recipiants = emailConnectednessData.recipiants, 
                    timestamp = emailConnectednessData.timestamp, timezoneOffset = emailConnectednessData.timezoneOffset, 
                    sender ? [ 4, effects_1.call(helpers_1.getEmailType, sender) ] : [ 3, 3 ];

                  case 2:
                    return _b = _c.sent(), [ 3, 4 ];

                  case 3:
                    _b = "personal", _c.label = 4;

                  case 4:
                    return emailType = _b, hashedS = util_1.normalizedHashCode(sender, 1e9), hashedR = recipiants.map(function(x) {
                        return util_1.normalizedHashCode(x, 1e9);
                    }), connectednessPropsData.push({
                        hashedS: hashedS,
                        hashedR: hashedR,
                        timestamp: timestamp,
                        timezoneOffset: timezoneOffset,
                        emailType: emailType
                    }), [ 4, effects_1.call(this._prefs.set, helpers_1.emailConnectednessDataPropsKey, connectednessPropsData) ];

                  case 5:
                    return _c.sent(), [ 2 ];
                }
            });
        }, SettingsSagas.prototype.processEmailConnectednessData = function() {
            var nextSyncDate, futureSyncDate, emailConnectednessData, totalCount, _a, personalEmailConnectednessData, businessEmailConnectednessData, firstTimestamp, userId, hashedUserId, personalCount, businessCount, histogramByRecipients, personalHistogramByRecipients, businesshistogramByRecipients, histogramByRecipientsCount, personalHistogramByRecipientsCount, businesshistogramByRecipientsCount;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors.getUserExperiments) ];

                  case 1:
                    return _b.sent().connectednessData ? [ 4, effects_1.call(this._prefs.get, helpers_1.emailConnectednessDataNextSyncDate) ] : [ 2 ];

                  case 2:
                    return null === (nextSyncDate = _b.sent()) || Date.now() > parseInt(nextSyncDate, 10) ? (futureSyncDate = Date.now() + stdlib_1.Ms.week, 
                    [ 4, effects_1.call(this._prefs.set, helpers_1.emailConnectednessDataNextSyncDate, futureSyncDate) ]) : [ 3, 8 ];

                  case 3:
                    return _b.sent(), [ 4, effects_1.call(this._prefs.get, helpers_1.emailConnectednessDataPropsKey) ];

                  case 4:
                    return null !== (emailConnectednessData = _b.sent()) && emailConnectednessData.length > 0 ? (totalCount = emailConnectednessData.length, 
                    _a = __read(emailConnectednessData.reduce(function(x, item) {
                        return "presonal" === item.emailType ? x[0].push(item) : x[1].push(item), x;
                    }, [ [], [] ]), 2), personalEmailConnectednessData = _a[0], businessEmailConnectednessData = _a[1], 
                    firstTimestamp = emailConnectednessData[0].timestamp, [ 4, effects_1.select(selectors.getUserId) ]) : [ 3, 8 ];

                  case 5:
                    return userId = _b.sent(), hashedUserId = util_1.normalizedHashCode(userId, 1e9), 
                    personalCount = personalEmailConnectednessData.length, businessCount = businessEmailConnectednessData.length, 
                    histogramByRecipients = helpers_1.getHistogramByRecipients(emailConnectednessData), 
                    personalHistogramByRecipients = helpers_1.getHistogramByRecipients(personalEmailConnectednessData), 
                    businesshistogramByRecipients = helpers_1.getHistogramByRecipients(businessEmailConnectednessData), 
                    histogramByRecipientsCount = helpers_1.getHistogramByRecipientsCount(emailConnectednessData), 
                    personalHistogramByRecipientsCount = helpers_1.getHistogramByRecipientsCount(personalEmailConnectednessData), 
                    businesshistogramByRecipientsCount = helpers_1.getHistogramByRecipientsCount(businessEmailConnectednessData), 
                    [ 4, effects_1.call([ tracking_1.gnar, tracking_1.gnar.connectednessDataEmail ], businessCount, businesshistogramByRecipientsCount, businesshistogramByRecipients, hashedUserId, histogramByRecipientsCount, histogramByRecipients, personalCount, personalHistogramByRecipientsCount, personalHistogramByRecipients, firstTimestamp, totalCount) ];

                  case 6:
                    return _b.sent(), [ 4, effects_1.call(this._prefs.set, helpers_1.emailConnectednessDataPropsKey, []) ];

                  case 7:
                    _b.sent(), _b.label = 8;

                  case 8:
                    return [ 2 ];
                }
            });
        }, SettingsSagas;
    }();
    exports.SettingsSagas = SettingsSagas;
}, function(module, exports, __webpack_require__) {
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
    var actions_1 = __webpack_require__(89), logger_1 = __webpack_require__(1), newsVersion = __webpack_require__(10).getGlobal().appConfig.newsVersion, log = logger_1.Logger.create("universal.bg.state.settings");
    exports.anonymousDapiPropsKey = "anonymousDapiProps", exports.oldSettingsFields = [ "enabled_db", "enabledDefs", "disabledFields", "seenNewsVersion" ], 
    exports.emailConnectednessDataPropsKey = "connectednessProps", exports.emailConnectednessDataNextSyncDate = "connectednessDataNextSyncDate";
    var _a, personalEmailDomains = [ "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com", "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk" ];
    exports.dapiPropsMap = ((_a = {})[actions_1.t.CHANGE_WEAK_DIALECT] = "dialectWeak", 
    _a[actions_1.t.CHANGE_STRONG_DIALECT] = "dialectStrong", _a), exports.dapiPropsSetter = {
        dialectWeak: function(dapi, dialect) {
            return dapi.common.setDialectWeak.call(dapi, dialect);
        },
        dialectStrong: function(dapi, dialect) {
            return dapi.common.setDialectStrong.call(dapi, dialect);
        },
        writingType: function(dapi, writingType) {
            return dapi.common.setWrittingType.call(dapi, writingType);
        },
        primaryLanguage: function(dapi, primaryLanguage) {
            return dapi.common.setPrimaryLanguage.call(dapi, primaryLanguage);
        },
        grammarSkills: function(dapi, grammarSkills) {
            return dapi.common.setGrammarSkills.call(dapi, grammarSkills);
        }
    }, exports.getEmailType = function(email) {
        var _a = __read(email.split("@").map(function(x) {
            return x.toLowerCase();
        }), 2), domain = (_a[0], _a[1]);
        return !0 === personalEmailDomains.includes(domain) ? "presonal" : "business";
    }, exports.getHistogramByRecipients = function(emailConnectednessData) {
        var recipiantsDict = emailConnectednessData.reduce(function(x, item) {
            return item.hashedR.forEach(function(r) {
                x[r] = x[r] ? x[r] + 1 : 1;
            }), x;
        }, {}), countByRecipient = Object.keys(recipiantsDict).reduce(function(x, key) {
            var val = recipiantsDict[key];
            return x[val] = x[val] ? x[val] + 1 : 1, x;
        }, {});
        return Object.keys(countByRecipient).reduce(function(x, k) {
            return x.push({
                key: parseInt(k, 10),
                value: countByRecipient[k]
            }), x;
        }, []);
    }, exports.getHistogramByRecipientsCount = function(emailConnectednessData) {
        var recipiantsCount = emailConnectednessData.reduce(function(x, item) {
            var count = item.hashedR.length;
            return x[count] = x[count] ? x[count] + 1 : 1, x;
        }, {});
        return Object.keys(recipiantsCount).reduce(function(x, k) {
            return x.push({
                key: parseInt(k, 10),
                value: recipiantsCount[k]
            }), x;
        }, []);
    }, exports.migrateSettings = function(_a) {
        var enabled_db = _a.enabled_db, enabledDefs = _a.enabledDefs, disabledFields = _a.disabledFields, seenNewsVersion = _a.seenNewsVersion, previousSettings = {};
        try {
            var parsedPrevSettings = JSON.parse(enabled_db);
            parsedPrevSettings && (delete parsedPrevSettings.lastChange, previousSettings = parsedPrevSettings);
        } catch (e) {
            log.error("error in parse enabled_db", e);
        }
        if (previousSettings.common = {
            enabledDefs: Boolean(enabledDefs),
            seenNewsVersion: seenNewsVersion || newsVersion
        }, !disabledFields) return previousSettings;
        var fields = Object.keys(disabledFields);
        return fields.length ? fields.filter(function(parts) {
            return disabledFields[parts];
        }).reduce(function(result, parts) {
            var _a, sepPos = parts.indexOf(":"), domain = parts.substr(0, sepPos), field = parts.substr(sepPos + 1), domainData = result[domain] || {
                enabled: !0
            };
            return domainData.disabledFields = Object.assign({}, domainData.disabledFields || {}, ((_a = {})[field] = !0, 
            _a)), result[domain] = domainData, result;
        }, previousSettings) : previousSettings;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var effects_1 = __webpack_require__(99), helpers_1 = __webpack_require__(1163), location_1 = __webpack_require__(16), tracking_1 = __webpack_require__(216), actions = __webpack_require__(201), selectors_1 = __webpack_require__(1164), TabsSagas = function() {
        function TabsSagas(_connectionSagas, _emitTo, _emitFocusedTab, _api, _pageConfig) {
            this._connectionSagas = _connectionSagas, this._emitTo = _emitTo, this._emitFocusedTab = _emitFocusedTab, 
            this._api = _api, this._pageConfig = _pageConfig;
        }
        return TabsSagas.prototype.start = function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.fork([ this, this.listenActiveTabChange ]) ];

                  case 1:
                    return _a.sent(), [ 4, effects_1.select(selectors_1.getActiveTab) ];

                  case 2:
                    return _a.sent() ? [ 3, 4 ] : [ 4, effects_1.take(actions.t.SET_ACTIVE_TAB) ];

                  case 3:
                    _a.sent(), _a.label = 4;

                  case 4:
                    return [ 4, effects_1.fork([ this, this.listenNewTabsConnections ]) ];

                  case 5:
                    return _a.sent(), [ 2 ];
                }
            });
        }, TabsSagas.prototype.listenNewTabsConnections = function() {
            var channel, _a, tab, url, state, csState;
            return __generator(this, function(_b) {
                switch (_b.label) {
                  case 0:
                    return [ 4, effects_1.call(helpers_1.createNewTabsChannel) ];

                  case 1:
                    channel = _b.sent(), _b.label = 2;

                  case 2:
                    return [ 4, effects_1.call(channel.take) ];

                  case 3:
                    return _a = _b.sent(), tab = _a.tab, url = _a.url, [ 4, effects_1.call(this._pageConfig.invalidateMemoized) ];

                  case 4:
                    return _b.sent(), [ 4, effects_1.select(selectors_1.stateByUrl, this._pageConfig, url) ];

                  case 5:
                    return (state = _b.sent()).connection.cookiesDisabled || !1 === navigator.cookieEnabled ? [ 4, effects_1.fork([ this._connectionSagas, this._connectionSagas.monitorCookiesDisable ]) ] : [ 3, 7 ];

                  case 6:
                    _b.sent(), _b.label = 7;

                  case 7:
                    return "popup" !== tab ? [ 3, 9 ] : [ 4, effects_1.call(this._emitTo, "popup", "state", state) ];

                  case 8:
                    return _b.sent(), [ 3, 12 ];

                  case 9:
                    return csState = selectors_1.stateForTab(state), [ 4, effects_1.call(tracking_1.fire, "tab-connected", state.user, state.config, state.connection, state.settings.enabled, csState.page.domain, csState.page.grammarlyEditor) ];

                  case 10:
                    return _b.sent(), [ 4, effects_1.call(this._emitTo, tab, "state", csState) ];

                  case 11:
                    _b.sent(), _b.label = 12;

                  case 12:
                    return [ 3, 2 ];

                  case 13:
                    return [ 2 ];
                }
            });
        }, TabsSagas.prototype.sendStateToTabs = function() {
            var state, activeTab, tabState;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.select(selectors_1.stateByActiveTab, this._pageConfig) ];

                  case 1:
                    return state = _a.sent(), [ 4, effects_1.select(selectors_1.getActiveTab) ];

                  case 2:
                    return activeTab = _a.sent(), window.__disableSendStateToTabs ? [ 2 ] : [ 4, effects_1.call([ this, this.renderBadge ], state) ];

                  case 3:
                    return _a.sent(), [ 4, effects_1.call(this._emitTo, "popup", "state", state) ];

                  case 4:
                    return _a.sent(), window.__popupState = state, tabState = selectors_1.stateForTab(state), 
                    activeTab && activeTab.id ? [ 4, effects_1.call(this._emitTo, activeTab.id, "state", tabState) ] : [ 3, 6 ];

                  case 5:
                    _a.sent(), _a.label = 6;

                  case 6:
                    return [ 4, effects_1.call(this._emitFocusedTab, "state", tabState) ];

                  case 7:
                    return _a.sent(), [ 2 ];
                }
            });
        }, TabsSagas.prototype.listenActiveTabChange = function() {
            var channel, tab, oldTab, domain;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, effects_1.call(helpers_1.createActiveTabsChannel, this._api) ];

                  case 1:
                    channel = _a.sent(), _a.label = 2;

                  case 2:
                    return [ 4, effects_1.call(channel.take) ];

                  case 3:
                    return tab = _a.sent(), [ 4, effects_1.select(selectors_1.getActiveTab) ];

                  case 4:
                    return oldTab = _a.sent(), domain = location_1.domainFromUrl(tab.url), oldTab && oldTab.id === tab.id && oldTab.url === tab.url ? [ 3, 7 ] : [ 4, effects_1.put(actions.setActiveTab(tab)) ];

                  case 5:
                    return _a.sent(), [ 4, effects_1.call(helpers_1.setUninstallURL, domain) ];

                  case 6:
                    _a.sent(), _a.label = 7;

                  case 7:
                    return [ 3, 2 ];

                  case 8:
                    return [ 2 ];
                }
            });
        }, TabsSagas.prototype.renderBadge = function(state) {
            var activeTab, user, config, settings, isGdocsExperiment, gdocsIsActiveTab, text;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return activeTab = state.activeTab, user = state.user, config = state.config, settings = state.settings, 
                    isGdocsExperiment = user.experiments && user.experiments.googleDocsBeta, gdocsIsActiveTab = activeTab && /^http(s?)\:\/\/docs\.google\.com\/document/.test(activeTab.url), 
                    isGdocsExperiment && gdocsIsActiveTab ? [ 4, effects_1.call(helpers_1.setBadgeText, this._api, "BETA", helpers_1.BETA_BADGE_COLOR) ] : [ 3, 2 ];

                  case 1:
                    return _a.sent(), [ 3, 9 ];

                  case 2:
                    return user.anonymous || config.grammarlyEditor || config.dontShowDisabledBadge ? [ 4, effects_1.call(helpers_1.setBadgeText, this._api, "") ] : [ 3, 4 ];

                  case 3:
                    return _a.sent(), [ 3, 9 ];

                  case 4:
                    return config.enabled || config.servicePage ? [ 3, 6 ] : [ 4, effects_1.call(helpers_1.setBadgeIcon, this._api, "bang") ];

                  case 5:
                    return _a.sent(), [ 3, 9 ];

                  case 6:
                    return [ 4, effects_1.call(helpers_1.getBadgeText, {
                        user: user,
                        settings: settings
                    }) ];

                  case 7:
                    return text = _a.sent(), [ 4, effects_1.call(helpers_1.setBadgeText, this._api, text) ];

                  case 8:
                    _a.sent(), _a.label = 9;

                  case 9:
                    return [ 2 ];
                }
            });
        }, TabsSagas;
    }();
    exports.TabsSagas = TabsSagas;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var Config = __webpack_require__(10), url_1 = __webpack_require__(90), message = __webpack_require__(15), util_1 = __webpack_require__(2), log = __webpack_require__(1).Logger.create("universal.bg.state.tabs"), newsVersion = Config.getGlobal().appConfig.newsVersion;
    exports.createNewTabsChannel = function() {
        var channel = util_1.createChannel();
        return message.on("tab-connected", function(_a) {
            var tab = _a.tab, url = _a.url;
            return channel.put({
                tab: tab,
                url: url
            });
        }), channel;
    }, exports.createActiveTabsChannel = function(api) {
        var channel = util_1.createChannel({
            buffered: !1
        });
        return api.tabs.onActiveTabChange(function(_a) {
            var url = _a.url, favIconUrl = _a.favIconUrl, windowId = _a.windowId, id = _a.id;
            return channel.put({
                url: url,
                favIconUrl: favIconUrl,
                windowId: windowId,
                id: id
            });
        }, function(err) {
            return log.error("runtime error by changing active tab", err);
        }), channel;
    }, exports.DEFAULT_BADGE_COLOR = "#e75146", exports.BETA_BADGE_COLOR = "#555A70", 
    exports.setBadgeIcon = function(api, name) {
        util_1.isSafari() || api.button.setBadge(""), api.button.setIconByName(name);
    }, exports.setBadgeText = function(_a, text, color) {
        var button = _a.button;
        switch (void 0 === color && (color = exports.DEFAULT_BADGE_COLOR), button.kind) {
          case "web-extension":
            button.setBadgeBackgroundColor(color), button.setIconByName("");
            break;

          case "fallback":
            break;

          default:
            throw new Error("Unsupported browser button action");
        }
        button.setBadge(text);
    }, exports.getBadgeText = function(_a) {
        _a.user;
        var _c = _a.settings, seenNewsVersion = _c.seenNewsVersion, enabled = _c.enabled;
        return newsVersion > 0 && seenNewsVersion !== newsVersion ? "NEW" : enabled ? "" : "off";
    }, exports.setUninstallURL = function(domain) {
        if (util_1.isChrome() || util_1.isFF()) {
            var url = url_1.getUninstallURL(domain);
            window.chrome.runtime.setUninstallURL && window.chrome.runtime.setUninstallURL(url);
        }
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var location_1 = __webpack_require__(16);
    function stateByUrl(state, pageConfig, url) {
        var domain = location_1.domainFromUrl(url), page = pageConfig.get(domain, url), settings = getTabSettings(state.settings, domain);
        return Object.assign({}, state, {
            config: Object.assign({}, page, {
                domain: domain
            })
        }, {
            settings: settings,
            activeTab: state.tabs && state.tabs.active
        });
    }
    function getTabSettings(settings, domain) {
        var domainSettings = settings[domain], enabled = !domainSettings || void 0 === domainSettings.enabled || domainSettings.enabled;
        return Object.assign({}, settings.common, domainSettings, {
            enabled: enabled
        });
    }
    exports.stateByUrl = stateByUrl, exports.stateByActiveTab = function(state, pageConfig) {
        return stateByUrl(state, pageConfig, state.tabs && state.tabs.active && state.tabs.active.url);
    }, exports.getTabSettings = getTabSettings, exports.stateForTab = function(_a) {
        var user = _a.user, connection = _a.connection, config = _a.config, settings = _a.settings;
        return {
            user: user,
            connection: connection,
            page: Object.assign({}, settings, config, {
                enabled: settings.enabled && config.enabled
            })
        };
    }, exports.getActiveTab = function(_a) {
        return _a.tabs.active;
    }, exports.getAll = function(state) {
        return state;
    }, exports.getUserGroups = function(state) {
        return state.user.groups;
    }, exports.getExperiments = function(state) {
        return state.user.experiments;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var tracking_1 = __webpack_require__(7), location_1 = __webpack_require__(16), util_1 = __webpack_require__(2), log = __webpack_require__(1).Logger.create("lib.bg.chrome"), UPDATE_TIMER = 20, chrome = window.chrome, updateStarted = !1;
    function requestUpdateCheck() {
        chrome.runtime.requestUpdateCheck && chrome.runtime.requestUpdateCheck(function(status) {
            return "update_available" === status ? log.info("update pending...") : "no_update" === status ? log.info("no update found") : "throttled" === status ? log.info("Oops, I'm asking too frequently - I need to back off.") : void 0;
        }), setTimeout(requestUpdateCheck, 72e5);
    }
    function execJS(id, file, opts) {
        return void 0 === opts && (opts = {}), id ? new Promise(function(resolve, reject) {
            return chrome.tabs.executeScript(id, Object.assign({
                file: file
            }, opts), function() {
                return util_1.chromeBgError() ? reject(util_1.chromeBgError()) : resolve();
            });
        }) : Promise.reject(util_1.chromeBgError());
    }
    function isNotCSLoaded(tab) {
        return __awaiter(this, void 0, void 0, function() {
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, new Promise(function(resolve) {
                        return tab.id && chrome.tabs.executeScript(tab.id, {
                            code: "document.body.dataset.grCSLoaded"
                        }, function(res) {
                            return resolve(res && res.pop());
                        });
                    }) ];

                  case 1:
                    return [ 2, !_a.sent() && tab || void 0 ];
                }
            });
        });
    }
    function filteredTabs(api, pageConfig, onlyOneInstance, domain) {
        return __awaiter(this, void 0, void 0, function() {
            var tabs, allTabs, current, filterFn, t;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return [ 4, (tabs = api.tabs).getAllTabs() ];

                  case 1:
                    return allTabs = _a.sent(), [ 4, tabs.getActiveTabUrl() ];

                  case 2:
                    return current = _a.sent(), filterFn = domain ? function(tab) {
                        return tab.url && tab.url.includes(domain);
                    } : function(_a) {
                        var url = _a.url;
                        if (url && 0 === url.indexOf("http")) return !!url.includes("grammarly") || pageConfig.get(location_1.domainFromUrl(url)).enabled;
                    }, t = allTabs.filter(filterFn), [ 4, Promise.all(t.map(onlyOneInstance ? isNotCSLoaded : function(tab) {
                        return Promise.resolve(tab);
                    })) ];

                  case 3:
                    return [ 2, _a.sent().filter(function(tab) {
                        return !!tab;
                    }).sort(function(_a) {
                        return _a.url === current ? -1 : 1;
                    }) ];
                }
            });
        });
    }
    exports.setupForcedUpdate = function() {
        !util_1.isChrome() && !util_1.isFF() || updateStarted || (chrome.runtime.onUpdateAvailable && chrome.runtime.onUpdateAvailable.addListener(function(details) {
            log.info("Detected the next extension version " + details.version), tracking_1.felog.chromeForcedToUpdate(details.version), 
            updateStarted = !0;
            var willUpdateInMinutes = util_1.getRandomIntInclusive(1, UPDATE_TIMER);
            log.info("Going to update in minutes: " + willUpdateInMinutes), setTimeout(chrome.runtime.reload, 60 * willUpdateInMinutes * 1e3);
        }), requestUpdateCheck());
    }, exports.loadContentScripts = function(api, pageConfig, domain) {
        return __awaiter(this, void 0, void 0, function() {
            var manifest, cs, source, jsSource, cssSource, tabs, errorHandle, startTime, endTime;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    return (util_1.isChrome() || util_1.isFF()) && (manifest = chrome.runtime.getManifest()) && (cs = manifest.content_scripts) && (source = cs.pop()) ? (jsSource = source.js, 
                    cssSource = source.css, jsSource && cssSource ? [ 4, filteredTabs(api, pageConfig, !0, domain) ] : [ 2 ]) : [ 2 ];

                  case 1:
                    return (tabs = _a.sent()).length ? (log.info("Load content scripts to", tabs), errorHandle = function(error, type) {
                        tracking_1.felog.chromeContentScriptLoadError(error && error.message, type), log.error("cs " + type + " loaded with error: " + error.message);
                    }, startTime = performance.now(), [ 4, Promise.all(tabs.map(function(_a) {
                        var id = _a.id;
                        return Promise.all([ jsSource.reduce(function(loader, js) {
                            return loader.then(function() {
                                return execJS(id, js, {
                                    runAt: "document_idle"
                                });
                            });
                        }, Promise.resolve()).then(function() {
                            return log.info("scripts loaded");
                        }).catch(function(e) {
                            return errorHandle(e, "js");
                        }), cssSource.reduce(function(loader, css) {
                            return loader.then(function() {
                                return function(id, file, opts) {
                                    return void 0 === opts && (opts = {}), id ? new Promise(function(resolve, reject) {
                                        return chrome.tabs.insertCSS(id, Object.assign({
                                            file: file
                                        }, opts), function() {
                                            return util_1.chromeBgError() ? reject(util_1.chromeBgError()) : resolve();
                                        });
                                    }) : Promise.reject(util_1.chromeBgError());
                                }(id, css, {
                                    runAt: "document_idle"
                                });
                            });
                        }, Promise.resolve()).then(function() {
                            return log.info("css loaded");
                        }).catch(function(e) {
                            return errorHandle(e, "css");
                        }) ]);
                    })) ]) : [ 2 ];

                  case 2:
                    return _a.sent(), endTime = performance.now(), log.trace("Content scripts load time: " + (endTime - startTime) + " ms"), 
                    [ 2 ];
                }
            });
        });
    }, exports.loadProxy = function(api, pageConfig) {
        return __awaiter(this, void 0, void 0, function() {
            var tabs, e_1, message;
            return __generator(this, function(_a) {
                switch (_a.label) {
                  case 0:
                    if (!util_1.isChrome()) return [ 2 ];
                    _a.label = 1;

                  case 1:
                    return _a.trys.push([ 1, 4, , 5 ]), [ 4, filteredTabs(api, pageConfig) ];

                  case 2:
                    return tabs = _a.sent(), [ 4, Promise.all(tabs.map(function(_a) {
                        return execJS(_a.id, "src/js/Grammarly-proxy.js");
                    })) ];

                  case 3:
                    return _a.sent(), log.info("proxy loaded on", tabs.map(function(tab) {
                        return tab.url;
                    })), [ 3, 5 ];

                  case 4:
                    return e_1 = _a.sent(), message = e_1 && e_1.message || e_1, log.error("proxy loaded with error: ", message), 
                    [ 3, 5 ];

                  case 5:
                    return [ 2 ];
                }
            });
        });
    }, exports.filteredTabs = filteredTabs;
}, function(module, exports, __webpack_require__) {
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
    var util_1 = __webpack_require__(2), defaults_1 = __webpack_require__(109), location_1 = __webpack_require__(16), config_loader_1 = __webpack_require__(1167), intersection = __webpack_require__(1170), PageConfigImpl = function(_super) {
        function PageConfigImpl(prefs, _userStateOrNull) {
            var _this = _super.call(this, prefs) || this;
            return _this._userStateOrNull = _userStateOrNull, _this._invalidate = function() {
                return _this.load();
            }, _this.invalidateMemoized = util_1.memoize(_this._invalidate, void 0, 1e4), _this.getByPage = function(pages, url) {
                if (void 0 === url && (url = location_1.getUrl()), pages) {
                    var findUrl = Object.keys(pages).find(function(page) {
                        return new RegExp(page).test(url);
                    });
                    return findUrl ? pages[findUrl] : void 0;
                }
            }, _this;
        }
        return __extends(PageConfigImpl, _super), PageConfigImpl.prototype._transformConfig = function(pageConfig, _domain) {
            var userState = this._userStateOrNull();
            return !(userState && userState.mimic && pageConfig && pageConfig.enabledForGroups && intersection(pageConfig.enabledForGroups, userState.mimic).length) || pageConfig.disabledBrowsers && pageConfig.disabledBrowsers.includes(util_1.getBrowser()) || (pageConfig.enabled = !0), 
            pageConfig;
        }, PageConfigImpl.prototype.get = function(domain, url) {
            var rawConfig = this.config.pageConfig[domain] || this.config.subdomains.find(function(conf) {
                return new RegExp("\\." + util_1.escapeRegExp(conf.domain) + "$").test(domain);
            }) || this.config.partials.find(function(conf) {
                return domain.includes(conf.domain);
            }), config = this._transformConfig(rawConfig, domain);
            if (config && !1 === config.enabled) return config;
            var newConfig = this.getByPage(config && config.pages, url) || config || {};
            return newConfig.enabled = !1 !== newConfig.enabled, newConfig;
        }, PageConfigImpl.prototype.toReload = function(url) {
            return 0 === url.indexOf("http") && defaults_1.SITES_TO_RELOAD.some(function(domain) {
                return url.includes(domain);
            });
        }, PageConfigImpl;
    }(config_loader_1.ConfigLoader);
    exports.PageConfigImpl = PageConfigImpl;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var localforage_1 = __webpack_require__(461), request_1 = __webpack_require__(205), config_1 = __webpack_require__(11), tracking_1 = __webpack_require__(7), meta_1 = __webpack_require__(1168), utils_1 = __webpack_require__(673), decorator_1 = __webpack_require__(1169), profiler_1 = __webpack_require__(462), log = __webpack_require__(1).Logger.create("lib.page-config.config-loader"), ConfigLoader = function() {
        function ConfigLoader(_prefs) {
            this._prefs = _prefs;
        }
        return ConfigLoader.prototype.init = function() {
            return __awaiter(this, void 0, void 0, function() {
                var config, _a;
                return __generator(this, function(_b) {
                    switch (_b.label) {
                      case 0:
                        return profiler_1.Profiler.start("pageConfig_init"), [ 4, this.isSkipConfig() ];

                      case 1:
                        return _b.sent() ? (log.warn("Config: use default config in DEBUG mode (skipConfig=true)"), 
                        [ 3, 4 ]) : [ 3, 2 ];

                      case 2:
                        return [ 4, this.loadFromStorage() ];

                      case 3:
                        config = _b.sent(), _b.label = 4;

                      case 4:
                        return this.config = config || {}, _a = this, [ 4, new meta_1.Meta().load() ];

                      case 5:
                        return _a.meta = _b.sent(), profiler_1.Profiler.stop("pageConfig_init"), [ 2, this ];
                    }
                });
            });
        }, ConfigLoader.prototype.isSkipConfig = function() {
            return __awaiter(this, void 0, void 0, function() {
                var _a;
                return __generator(this, function(_b) {
                    switch (_b.label) {
                      case 0:
                        return (_a = !1) ? [ 4, this._prefs.get("skipConfig") ] : [ 3, 2 ];

                      case 1:
                        _a = _b.sent(), _b.label = 2;

                      case 2:
                        return [ 2, _a ];
                    }
                });
            });
        }, Object.defineProperty(ConfigLoader.prototype, "config", {
            get: function() {
                return this._config;
            },
            set: function(config) {
                config = config || {}, this._config = decorator_1.decorateConfig(config);
            },
            enumerable: !0,
            configurable: !0
        }), ConfigLoader.prototype.load = function() {
            return __awaiter(this, void 0, void 0, function() {
                var _a, date, interval, minutesToUpdate;
                return __generator(this, function(_b) {
                    return _a = this.meta.config, date = _a.date, interval = _a.interval, date + interval > Date.now() ? (minutesToUpdate = (date + interval - Date.now()) / 1e3 / 60, 
                    log.info("Config: next update in " + minutesToUpdate.toFixed(2) + " m"), [ 2 ]) : (log.info("Config: going to update config from CDN..."), 
                    [ 2, this.updateFromCDN() ]);
                });
            });
        }, ConfigLoader.prototype.updateFromCDN = function() {
            return __awaiter(this, void 0, void 0, function() {
                var config, error_1, msg;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return _a.trys.push([ 0, 2, , 3 ]), [ 4, request_1.fetch(config_1.URLS.pageConfigUrl, {
                            timeout: 6e4
                        }) ];

                      case 1:
                        if (config = _a.sent(), !utils_1.isValid(config)) throw new Error("Config malformed");
                        return this.config = config, this.save(config), [ 3, 3 ];

                      case 2:
                        return error_1 = _a.sent(), tracking_1.felog.pageConfigCDNError(error_1.message), 
                        msg = "Config: can't get valid config - " + error_1.message, log.warn(msg), this.saveOnError(msg), 
                        [ 3, 3 ];

                      case 3:
                        return [ 2 ];
                    }
                });
            });
        }, ConfigLoader.prototype.loadFromStorage = function() {
            return __awaiter(this, void 0, void 0, function() {
                var rawConfig, error_2;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return _a.trys.push([ 0, 2, , 3 ]), [ 4, localforage_1.localforage.getItem("config") ];

                      case 1:
                        if (!(rawConfig = _a.sent())) throw new Error("Config missed");
                        if (!utils_1.isValid(rawConfig)) throw new Error("Config malformed");
                        return log.info("Config: loaded from local storage successfully"), [ 2, rawConfig ];

                      case 2:
                        return "Config missed" === (error_2 = _a.sent()).message || tracking_1.felog.pageConfigLocalStorageError(error_2.message, error_2.name), 
                        log.warn("Config: cannot get valid config from storage: " + error_2), [ 2, void 0 ];

                      case 3:
                        return [ 2 ];
                    }
                });
            });
        }, ConfigLoader.prototype.save = function(config) {
            var interval = config.interval, protocolVersion = config.protocolVersion, version = config.version;
            localforage_1.localforage.setItem("config", config), this.fireVersionUpdate(version, this.meta.config.version), 
            this.meta.set({
                date: this.getCurrentTimestamp(),
                status: "success",
                interval: interval,
                protocolVersion: protocolVersion,
                version: version
            }), log.info("Config: new config saved to local storage successfully: " + config.version, config);
        }, ConfigLoader.prototype.saveOnError = function(info) {
            var _a = this.meta.config, interval = _a.interval, protocolVersion = _a.protocolVersion, version = _a.version;
            this.meta.set({
                date: this.getCurrentTimestamp(),
                status: "failed",
                interval: interval,
                protocolVersion: protocolVersion,
                version: version,
                info: info
            });
        }, ConfigLoader.prototype.fireVersionUpdate = function(newVersion, oldVersion) {
            newVersion && oldVersion !== newVersion && tracking_1.felog.pageConfigUpdated(oldVersion, newVersion);
        }, ConfigLoader.prototype.getCurrentTimestamp = function() {
            return Date.now();
        }, ConfigLoader;
    }();
    exports.ConfigLoader = ConfigLoader;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var localforage_1 = __webpack_require__(461), utils_1 = __webpack_require__(673), Meta = function() {
        function Meta() {}
        return Meta.prototype.load = function() {
            return __awaiter(this, void 0, void 0, function() {
                var meta;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return [ 4, localforage_1.localforage.getItem("lastConfigUpdate") ];

                      case 1:
                        return meta = _a.sent(), this.set(meta), [ 2, this ];
                    }
                });
            });
        }, Meta.prototype.set = function(meta) {
            var _a = meta || {}, protocolVersion = _a.protocolVersion, version = _a.version, status = _a.status, info = _a.info, date = _a.date, interval = _a.interval;
            return this._meta = {
                date: Number(date) || 0,
                interval: utils_1.getInterval(Number(interval)),
                protocolVersion: protocolVersion,
                version: version,
                status: status,
                info: info
            }, localforage_1.localforage.setItem("lastConfigUpdate", this._meta);
        }, Object.defineProperty(Meta.prototype, "config", {
            get: function() {
                return this._meta;
            },
            enumerable: !0,
            configurable: !0
        }), Meta;
    }();
    exports.Meta = Meta;
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var config_1 = __webpack_require__(11), defaults_1 = __webpack_require__(109), util_1 = __webpack_require__(2), merge = __webpack_require__(172), log = __webpack_require__(1).Logger.create("lib.page-config.decorator");
    function deepCopyWithDefault(config) {
        var newConfig = merge({
            pageConfig: {}
        }, config);
        return newConfig.pageConfig || (newConfig.pageConfig = {}), newConfig;
    }
    exports.deepCopyWithDefault = deepCopyWithDefault;
    var RawConfigDecorator = function() {
        function RawConfigDecorator() {}
        return RawConfigDecorator.decorate = function(config) {
            return config = config || {}, config = this.filterByVersion(config), config = this.withDefault(config), 
            config = this.parseBooleans(config), config = this.parseBrowserValues(config), config = this.filterInvalidPageRegexp(config), 
            config = this.collectSubdomains(config), config = this.collectPartials(config);
        }, RawConfigDecorator.withDefault = function(config) {
            config = deepCopyWithDefault(config);
            var defaultConfig = defaults_1.PAGE_CONFIG && defaults_1.PAGE_CONFIG.pageConfig || {};
            defaults_1.OVERRIDE_PAGE_CONFIG;
            return config.pageConfig = merge({}, defaultConfig, config.pageConfig), config;
        }, RawConfigDecorator.filterByVersion = function(config, version) {
            void 0 === version && (version = config_1.getVersion());
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            return config.pageConfig = Object.keys(pageConfig || {}).filter(function(key) {
                var ruleVersion = pageConfig[key].version;
                return !ruleVersion || "*" === ruleVersion || 1 !== util_1.versionComparator(version, ruleVersion);
            }).reduce(function(hsh, key) {
                return Object.assign({}, hsh, ((_a = {})[key] = config.pageConfig[key], _a));
                var _a;
            }, {}), config;
        }, RawConfigDecorator.parseBooleans = function(config) {
            function isTruly(value) {
                return !(!1 === value || "false" === value);
            }
            function isExistsOrFalse(value) {
                return !!value && isTruly(value);
            }
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            return Object.keys(pageConfig || {}).forEach(function(key) {
                pageConfig[key] || (pageConfig[key] = {});
                var rule = pageConfig[key];
                rule.enabled = isTruly(rule.enabled), rule.matchInclusions = isExistsOrFalse(rule.matchInclusions), 
                rule.matchSubdomains = isExistsOrFalse(rule.matchSubdomains), rule.pages && Object.keys(rule.pages).forEach(function(key) {
                    rule.pages[key].enabled = isTruly(rule.pages[key].enabled);
                });
            }), config;
        }, RawConfigDecorator.parseBrowserValues = function(config, browser) {
            void 0 === browser && (browser = util_1.getBrowser());
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            return Object.keys(pageConfig || {}).map(function(key) {
                var disabled = pageConfig[key] && pageConfig[key].disabledBrowsers;
                disabled && disabled.includes(browser) && (pageConfig[key].enabled = !1);
            }), config;
        }, RawConfigDecorator.filterInvalidPageRegexp = function(config) {
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            return Object.keys(pageConfig || {}).forEach(function(key) {
                var config = pageConfig[key];
                config.pages && (config.pages = Object.keys(config.pages).filter(function(key) {
                    try {
                        return new RegExp(key);
                    } catch (e) {
                        return !1;
                    }
                }).reduce(function(hsh, key) {
                    return Object.assign({}, hsh, ((_a = {})[key] = config.pages[key], _a));
                    var _a;
                }, {}));
            }), config;
        }, RawConfigDecorator.collectSubdomains = function(config) {
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            config.subdomains = [];
            try {
                config.subdomains = Object.keys(pageConfig || {}).filter(function(domain) {
                    return pageConfig[domain].matchSubdomains;
                }).map(function(domain) {
                    return Object.assign({
                        domain: domain
                    }, pageConfig[domain]);
                });
            } catch (err) {
                log.warn("Cannot collect subdomains from config");
            }
            return config;
        }, RawConfigDecorator.collectPartials = function(config) {
            var pageConfig = (config = deepCopyWithDefault(config)).pageConfig;
            config.partials = [];
            try {
                config.partials = Object.keys(pageConfig || {}).filter(function(domain) {
                    return pageConfig[domain].matchInclusions;
                }).map(function(domain) {
                    return Object.assign({
                        domain: domain
                    }, pageConfig[domain]);
                });
            } catch (err) {
                log.warn("Cannot collect partials from config");
            }
            return config;
        }, RawConfigDecorator;
    }();
    exports.RawConfigDecorator = RawConfigDecorator, exports.decorateConfig = function(config) {
        return RawConfigDecorator.decorate(config);
    };
}, function(module, exports, __webpack_require__) {
    var arrayMap = __webpack_require__(85), baseIntersection = __webpack_require__(1171), baseRest = __webpack_require__(94), castArrayLikeObject = __webpack_require__(1172), intersection = baseRest(function(arrays) {
        var mapped = arrayMap(arrays, castArrayLikeObject);
        return mapped.length && mapped[0] === arrays[0] ? baseIntersection(mapped) : [];
    });
    module.exports = intersection;
}, function(module, exports, __webpack_require__) {
    var SetCache = __webpack_require__(126), arrayIncludes = __webpack_require__(364), arrayIncludesWith = __webpack_require__(365), arrayMap = __webpack_require__(85), baseUnary = __webpack_require__(79), cacheHas = __webpack_require__(127), nativeMin = Math.min;
    module.exports = function(arrays, iteratee, comparator) {
        for (var includes = comparator ? arrayIncludesWith : arrayIncludes, length = arrays[0].length, othLength = arrays.length, othIndex = othLength, caches = Array(othLength), maxLength = 1 / 0, result = []; othIndex--; ) {
            var array = arrays[othIndex];
            othIndex && iteratee && (array = arrayMap(array, baseUnary(iteratee))), maxLength = nativeMin(array.length, maxLength), 
            caches[othIndex] = !comparator && (iteratee || length >= 120 && array.length >= 120) ? new SetCache(othIndex && array) : void 0;
        }
        array = arrays[0];
        var index = -1, seen = caches[0];
        outer: for (;++index < length && result.length < maxLength; ) {
            var value = array[index], computed = iteratee ? iteratee(value) : value;
            if (value = comparator || 0 !== value ? value : 0, !(seen ? cacheHas(seen, computed) : includes(result, computed, comparator))) {
                for (othIndex = othLength; --othIndex; ) {
                    var cache = caches[othIndex];
                    if (!(cache ? cacheHas(cache, computed) : includes(arrays[othIndex], computed, comparator))) continue outer;
                }
                seen && seen.push(computed), result.push(value);
            }
        }
        return result;
    };
}, function(module, exports, __webpack_require__) {
    var isArrayLikeObject = __webpack_require__(111);
    module.exports = function(value) {
        return isArrayLikeObject(value) ? value : [];
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var config_1 = __webpack_require__(11), tracking_1 = __webpack_require__(7), log = __webpack_require__(1).Logger.create("lib.bg.dapi"), dialects = [ "british", "american", "australian", "canadian" ], writingTypes = [ "work", "school", "otherProjects" ], primaryLanguages = [ "english", "notEnglish" ], grammarSkills = [ "beginner", "intermediate", "advanced" ], checkPropValue = function(arr, val) {
        return null != val && arr.includes(val) ? val : null;
    };
    function parseDialect(val) {
        return checkPropValue(dialects, val);
    }
    function parseWritingType(val) {
        return checkPropValue(writingTypes, val);
    }
    function parsePrimaryLanguage(val) {
        return checkPropValue(primaryLanguages, val);
    }
    function parseGrammarSkills(val) {
        return checkPropValue(grammarSkills, val);
    }
    exports.parseDialect = parseDialect, exports.parseWritingType = parseWritingType, 
    exports.parsePrimaryLanguage = parsePrimaryLanguage, exports.parseGrammarSkills = parseGrammarSkills;
    var Property = function() {
        function Property(_key, _parser, _fetch) {
            this._key = _key, this._parser = _parser, this._fetch = _fetch;
        }
        return Property.prototype.get = function() {
            return __awaiter(this, void 0, void 0, function() {
                var url, res, e_1;
                return __generator(this, function(_a) {
                    switch (_a.label) {
                      case 0:
                        return _a.trys.push([ 0, 2, , 3 ]), url = config_1.URLS.dapiProps + "/" + this._key, 
                        [ 4, this._fetch(url, {
                            isText: !0
                        }) ];

                      case 1:
                        return [ 2, (res = _a.sent()) ? this._parser(res) : null ];

                      case 2:
                        throw e_1 = _a.sent(), log.error("Error by getting prop " + this._key + " from dapi", e_1), 
                        tracking_1.felog.getDapiPropError(this._key, e_1 && e_1.body), e_1;

                      case 3:
                        return [ 2 ];
                    }
                });
            });
        }, Property.prototype.set = function(value) {
            return __awaiter(this, void 0, void 0, function() {
                var url, e_2, _a;
                return __generator(this, function(_b) {
                    switch (_b.label) {
                      case 0:
                        return _b.trys.push([ 0, 2, , 3 ]), url = "" + config_1.URLS.dapiProps, [ 4, this._fetch(url, {
                            method: "post",
                            isText: !0,
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify((_a = {}, _a[this._key] = value, _a))
                        }) ];

                      case 1:
                        return [ 2, _b.sent() ];

                      case 2:
                        throw e_2 = _b.sent(), log.error("Error by setting prop " + this._key + " to dapi", e_2), 
                        tracking_1.felog.setDapiPropError(this._key, e_2 && e_2.body), e_2;

                      case 3:
                        return [ 2 ];
                    }
                });
            });
        }, Property;
    }();
    exports.Property = Property;
    var CommonImpl = function() {
        return function(fetch) {
            var _this = this;
            this.dialectStrong = function() {
                return _this._dialectStrong.get();
            }, this.dialectWeak = function() {
                return _this._dialectWeak.get();
            }, this.writingType = function() {
                return _this._writingType.get();
            }, this.primaryLanguage = function() {
                return _this._primaryLanguage.get();
            }, this.grammarSkills = function() {
                return _this._grammarSkills.get();
            }, this.setDialectWeak = function(val) {
                return _this._dialectWeak.set(val);
            }, this.setDialectStrong = function(val) {
                return _this._dialectStrong.set(val);
            }, this.setWrittingType = function(val) {
                return _this._writingType.set(val);
            }, this.setPrimaryLanguage = function(val) {
                return _this._primaryLanguage.set(val);
            }, this.setGrammarSkills = function(val) {
                return _this._grammarSkills.set(val);
            }, this._dialectStrong = new Property("dialectStrong", parseDialect, fetch), this._dialectWeak = new Property("dialectWeak", parseDialect, fetch), 
            this._writingType = new Property("writingType", parseWritingType, fetch), this._primaryLanguage = new Property("primaryLanguage", parsePrimaryLanguage, fetch), 
            this._grammarSkills = new Property("grammarSkills", parseGrammarSkills, fetch);
        };
    }(), DapiImpl = function() {
        return function(fetch) {
            this.common = new CommonImpl(fetch);
        };
    }();
    exports.DapiImpl = DapiImpl;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __assign = this && this.__assign || Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
        return t;
    }, __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
        return new (P || (P = Promise))(function(resolve, reject) {
            function fulfilled(value) {
                try {
                    step(generator.next(value));
                } catch (e) {
                    reject(e);
                }
            }
            function rejected(value) {
                try {
                    step(generator.throw(value));
                } catch (e) {
                    reject(e);
                }
            }
            function step(result) {
                result.done ? resolve(result.value) : new P(function(resolve) {
                    resolve(result.value);
                }).then(fulfilled, rejected);
            }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }, __generator = this && this.__generator || function(thisArg, body) {
        var f, y, t, g, _ = {
            label: 0,
            sent: function() {
                if (1 & t[0]) throw t[1];
                return t[1];
            },
            trys: [],
            ops: []
        };
        return g = {
            next: verb(0),
            throw: verb(1),
            return: verb(2)
        }, "function" == typeof Symbol && (g[Symbol.iterator] = function() {
            return this;
        }), g;
        function verb(n) {
            return function(v) {
                return function(op) {
                    if (f) throw new TypeError("Generator is already executing.");
                    for (;_; ) try {
                        if (f = 1, y && (t = y[2 & op[0] ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
                        switch (y = 0, t && (op = [ 0, t.value ]), op[0]) {
                          case 0:
                          case 1:
                            t = op;
                            break;

                          case 4:
                            return _.label++, {
                                value: op[1],
                                done: !1
                            };

                          case 5:
                            _.label++, y = op[1], op = [ 0 ];
                            continue;

                          case 7:
                            op = _.ops.pop(), _.trys.pop();
                            continue;

                          default:
                            if (!(t = (t = _.trys).length > 0 && t[t.length - 1]) && (6 === op[0] || 2 === op[0])) {
                                _ = 0;
                                continue;
                            }
                            if (3 === op[0] && (!t || op[1] > t[0] && op[1] < t[3])) {
                                _.label = op[1];
                                break;
                            }
                            if (6 === op[0] && _.label < t[1]) {
                                _.label = t[1], t = op;
                                break;
                            }
                            if (t && _.label < t[2]) {
                                _.label = t[2], _.ops.push(op);
                                break;
                            }
                            t[2] && _.ops.pop(), _.trys.pop();
                            continue;
                        }
                        op = body.call(thisArg, _);
                    } catch (e) {
                        op = [ 6, e ], y = 0;
                    } finally {
                        f = t = 0;
                    }
                    if (5 & op[0]) throw op[1];
                    return {
                        value: op[0] ? op[1] : void 0,
                        done: !0
                    };
                }([ n, v ]);
            };
        }
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var stdlib_1 = __webpack_require__(3), websocket = __webpack_require__(371), util_1 = __webpack_require__(2), config_1 = __webpack_require__(11), socket_1 = __webpack_require__(363), fake_1 = __webpack_require__(1175);
    exports.FakeCapi = fake_1.FakeCapi;
    var socket_2 = __webpack_require__(1176), log = __webpack_require__(1).Logger.create("universal.bg.socket"), BackgroundSocketManager = function() {
        return function(_telemetry, _getConnectionState, _updateConnectionState, _refreshUser, _getTokenCookie, _message, _fakeCapi) {
            var _this = this;
            this._telemetry = _telemetry, this._getConnectionState = _getConnectionState, this._updateConnectionState = _updateConnectionState, 
            this._refreshUser = _refreshUser, this._getTokenCookie = _getTokenCookie, this._message = _message, 
            this._fakeCapi = _fakeCapi, this._sockets = {}, this._releaseTimeout = 5e3, this._maxReconnectTime = 12e4, 
            this._log = [], this.reconnectAll = function(dialect) {
                _this._dialect = dialect, Object.keys(_this._sockets).forEach(function(id) {
                    return _this._sockets[id].reconnect();
                });
            }, this.getLog = function() {
                var result = _this._log.slice(0);
                return _this._log = [], result;
            }, this._setMessageType = function(_a) {
                var id = _a.id, iframeMode = _a.iframeMode;
                log.trace("IFRAME MODE " + id, _this._sockets);
                var socket = _this._sockets[id];
                socket && socket.setMessageType(iframeMode ? socket_1.MessageTypes.serverIframe : socket_1.MessageTypes.server);
            }, this._onBackgroundSocketEmit = function(message, messageType, sender) {
                var event = message.event, socketId = message.socketId, msg = message.msg;
                if (log.trace("from ws " + event + " " + socketId, {
                    msg: msg,
                    messageType: messageType
                }), msg && msg.error && "not_authorized" === msg.error) return _this._tryToFixSession();
                var releaseTimer = setTimeout(function() {
                    var socket = _this._sockets[socketId];
                    socket && (socket.release(), socket.overrideEmitToNoOp(), delete _this._sockets[socketId]);
                }, _this._releaseTimeout);
                _this._message.emitTo(sender, messageType, __assign({}, message, {
                    id: util_1.guid()
                }), function(msg) {
                    return msg && clearTimeout(releaseTimer);
                });
            }, this._onContentScriptSocketMessage = function(data, _, sender) {
                if (data && !_this._getConnectionState().authToCapiDegradation) {
                    var socketId = data.socketId, method = data.method, isClose = "close" === method, socket = _this._sockets[socketId];
                    if (socket || !isClose) {
                        switch (socket || (socket = new socket_2.BackgroundSocket(data, sender, _this._onBackgroundSocketEmit, _this._fakeCapi), 
                        _this._sockets[socketId] = socket), data.arg && "start" === data.arg.action && _this._dialect && (data.arg.dialect = _this._dialect), 
                        method) {
                          case "connect":
                            _this._refreshUser(!0, "onSessionStart").then(function() {
                                return socket.connect(data.arg);
                            });
                            break;

                          case "send":
                            socket.send(data.arg);
                            break;

                          case "reconnect":
                            socket.reconnect();
                            break;

                          case "release":
                            socket.release();
                            break;

                          case "close":
                            socket.close();
                            break;

                          case "wsPlay":
                            socket.wsPlay();
                            break;

                          case "wsPause":
                            socket.wsPause();
                            break;

                          default:
                            log.error("Unknown method", method);
                        }
                        isClose && (socket.close(), socket.overrideEmitToNoOp(), delete _this._sockets[socketId]);
                    }
                }
            }, this._tryToFixSession = function() {
                var _a = _this._getConnectionState(), authToCapiDegradation = _a.authToCapiDegradation, authDegradation = _a.authDegradation, cookiesDisabled = _a.cookiesDisabled;
                if (authToCapiDegradation) return _this._telemetry.capiNotAuthorizedLoop(!!authDegradation, !!cookiesDisabled), 
                void log.error("User not authorized... Recovery fail =(");
                cookiesDisabled && (_this._telemetry.socketDisabledCookie(), log.error("User disabled cookies... =(")), 
                log.warn("User not authorized... Try to recover"), _this._updateConnectionState({
                    authToCapiDegradation: !0
                }), _this._connectionFixer();
            }, this._connectionFixer = function() {
                return __awaiter(_this, void 0, void 0, function() {
                    var count, _this = this;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return Object.keys(this._sockets).forEach(function(id) {
                                return _this._sockets[id].release();
                            }), [ 4, new Promise(function(resolve) {
                                return _this._tryToConnect(resolve);
                            }) ];

                          case 1:
                            return count = _a.sent(), this._updateConnectionState({
                                authToCapiDegradation: !1
                            }), Object.keys(this._sockets).forEach(function(id) {
                                return _this._sockets[id].reconnect();
                            }), this._telemetry.socketBgRestored(count), [ 2 ];
                        }
                    });
                });
            }, this._tryToConnect = function(resolve, timeToReconnect, count) {
                return void 0 === timeToReconnect && (timeToReconnect = 1e4), void 0 === count && (count = 1), 
                __awaiter(_this, void 0, void 0, function() {
                    var ws, browser, clientName, start, close, _this = this;
                    return __generator(this, function(_a) {
                        switch (_a.label) {
                          case 0:
                            return log.warn("Fixer inited, will try to connect in " + timeToReconnect / 1e3 + "s., count:" + count), 
                            [ 4, util_1.delay(timeToReconnect) ];

                          case 1:
                            return _a.sent(), [ 4, this._refreshUser(!1, "recover_after_capi_error") ];

                          case 2:
                            return _a.sent(), ws = websocket({
                                url: config_1.URLS.capi
                            }), browser = util_1.getBrowser(), clientName = "chrome" === browser ? "extension_chrome" : "firefox" === browser ? "extension_firefox" : "safari" === browser ? "extension_safari" : "edge" === browser ? "extension_edge" : stdlib_1.try_(function() {
                                return stdlib_1.assertNever(browser);
                            }, function(_) {
                                return "extension";
                            }), start = {
                                docid: util_1.guid(),
                                client: clientName,
                                protocolVersion: "1.0",
                                action: "start",
                                id: 0
                            }, close = function() {
                                ws && (ws.close(), ws.release(), ws.emit = util_1._f), ws = null;
                            }, ws && (ws.emit = function(event, msg) {
                                return void 0 === msg && (msg = {}), "connect" === event ? ws && ws.send(start) : msg.action && "start" === msg.action ? (close(), 
                                log.warn("yay, we fixed capi connection!"), resolve(count)) : void ((msg.error || "error" === event) && (close(), 
                                count % 10 == 0 && _this._logFailedReconnect({
                                    count: count,
                                    error: msg.error
                                }), log.warn("still on error( " + event, msg), _this._tryToConnect(resolve, Math.min(_this._maxReconnectTime, 2 * timeToReconnect), count + 1)));
                            }), ws && ws.connect(), [ 2 ];
                        }
                    });
                });
            }, this._logFailedReconnect = function(_a) {
                var count = _a.count, error = _a.error;
                return __awaiter(_this, void 0, void 0, function() {
                    var token;
                    return __generator(this, function(_b) {
                        switch (_b.label) {
                          case 0:
                            token = "exception", _b.label = 1;

                          case 1:
                            return _b.trys.push([ 1, 3, , 4 ]), [ 4, this._getTokenCookie() ];

                          case 2:
                            return token = _b.sent(), [ 3, 4 ];

                          case 3:
                            return _b.sent(), [ 3, 4 ];

                          case 4:
                            return log.warn("log failed reconnect " + count, error), this._telemetry.socketBgReconnectFail(token || "", count), 
                            [ 2 ];
                        }
                    });
                });
            }, _message.on(socket_1.MessageTypes.iframeMode, this._setMessageType), _message.on(socket_1.MessageTypes.client, this._onContentScriptSocketMessage);
        };
    }();
    exports.BackgroundSocketManager = BackgroundSocketManager;
}, function(module, exports, __webpack_require__) {
    "use strict";
    var __assign = this && this.__assign || Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) for (var p in s = arguments[i]) Object.prototype.hasOwnProperty.call(s, p) && (t[p] = s[p]);
        return t;
    };
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var emitter = __webpack_require__(18), util_1 = __webpack_require__(2), debounce = __webpack_require__(53), FakeCapi = function() {
        return function() {
            var _this = this;
            this._fakeWebsocketData = [], this._isAutorun = !1, this._latestRevision = 0, this.isOn = function() {
                return _this._fakeWebsocketData && _this._fakeWebsocketData.length > 0;
            }, this.getSocket = function() {
                return _this._socket;
            }, this.run = function() {
                if (_this._fakeWebsocketData.length > 0) {
                    var obj = _this._fakeWebsocketData.shift();
                    obj.rev = _this._latestRevision, "synonyms" === obj.action ? _this._socket.emit("message", obj) : _this._socket.emit(obj.event, obj), 
                    setTimeout(_this.run, 0);
                } else _this._latestRevision = 0, _this._isAutorun = !1;
            }, this.setData = function(data) {
                _this._fakeWebsocketData = data.value, _this._isAutorun = data.autorun, _this._debouncedRunFakeCapi.cancel();
            }, this._fakeWebsocket = function() {
                var ws = __assign({}, emitter({}), {
                    send: function(message) {
                        "start" === message.action && ws.emit("start", {
                            event: "message",
                            action: "start"
                        }), "submit_ot" === message.action && (_this._latestRevision = message.rev, _this._isAutorun && _this._debouncedRunFakeCapi());
                    },
                    close: util_1._f,
                    connect: function() {
                        ws.emit("connect", {
                            event: "connect"
                        });
                    },
                    reconnect: function() {
                        return ws.connect();
                    },
                    isConnected: util_1._F,
                    release: util_1._f,
                    toString: function() {
                        return "Fake socket";
                    },
                    wsPlay: util_1._f,
                    wsPause: util_1._f
                });
                return ws;
            }, this._socket = this._fakeWebsocket(), this._debouncedRunFakeCapi = debounce(this.run, 3e3);
        };
    }();
    exports.FakeCapi = FakeCapi;
}, function(module, exports, __webpack_require__) {
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
    var websocket = __webpack_require__(371), logger_1 = __webpack_require__(1), emitter_1 = __webpack_require__(372), log = logger_1.Logger.create("universal.bg.socket"), BackgroundSocket = function(_super) {
        function BackgroundSocket(config, _sender, _onInternalSocketEmit, _fakeCapi) {
            var _this = _super.call(this) || this;
            return _this._sender = _sender, _this._onInternalSocketEmit = _onInternalSocketEmit, 
            _this._fakeCapi = _fakeCapi, _this._messageType = "socket-server", _this._closedByMe = !1, 
            _this.connect = function(force) {
                return _this._internalSocket.connect(force);
            }, _this.send = function(data) {
                return _this._internalSocket.send(data);
            }, _this.close = function() {
                return _this._internalSocket.close();
            }, _this.wsPlay = function() {
                return _this._internalSocket.wsPlay();
            }, _this.wsPause = function() {
                return _this._internalSocket.wsPause();
            }, _this.isConnected = function() {
                return _this._internalSocket.isConnected();
            }, _this.socketId = "0", _this.reconnect = function() {
                _this._reconnectInProgress || (_this._reconnectInProgress = !0, _this._reconnectFn().then(function() {
                    return _this._reconnectInProgress = !1;
                }));
            }, _this.release = function() {
                log.trace("CLOSE SOCKET"), _this._internalSocket.close(), _this._internalSocket.release();
            }, _this.overrideEmitToNoOp = function() {
                return _this._internalSocket.emit = function() {};
            }, _this.setMessageType = function(type) {
                log.trace("USE EXT SOCKET", type), _this._messageType = type;
            }, _this._getEnhancedSocket = function(config) {
                var socket = _this._fakeCapi.isOn() ? _this._fakeCapi.getSocket() : websocket(config), originalEmit = socket.emit;
                return Object.assign(socket, {
                    emit: function(event, msg) {
                        originalEmit(event, msg), _this._emit(event, msg);
                    },
                    reconnect: _this.reconnect,
                    toString: function() {
                        return "[object BackgroundSocket]";
                    }
                });
            }, _this._emit = function(event, msg) {
                "disconnect" === event && _this._closedByMe ? _this._closedByMe = !1 : _this._onInternalSocketEmit({
                    event: event,
                    socketId: _this._socketId,
                    msg: msg
                }, _this._messageType, _this._sender);
            }, _this._reconnectFn = function() {
                var finish = function() {}, promise = new Promise(function(resolve) {
                    return finish = resolve;
                });
                return _this._internalSocket.one("connect", finish), _this._internalSocket.isConnected() ? (_this._internalSocket.one("disconnect", function() {
                    return setTimeout(function() {
                        return _this._internalSocket.connect(!0);
                    }, 0);
                }), _this._closedByMe = !0, _this._internalSocket.close()) : _this._internalSocket.connect(!0), 
                promise;
            }, _this._internalSocket = _this._getEnhancedSocket(config), _this._socketId = config.socketId, 
            _this;
        }
        return __extends(BackgroundSocket, _super), BackgroundSocket;
    }(emitter_1.Emitter);
    exports.BackgroundSocket = BackgroundSocket;
}, function(module, exports, __webpack_require__) {
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
    });
    var message = __webpack_require__(15), METHODS = [ "log", "info", "warn", "error", "time", "timeEnd", "debug" ], w = window, savedConsole = console;
    exports.startSendingBgLogsToActiveTab = function() {
        var newConsole = {};
        METHODS.forEach(function(method) {
            newConsole[method] = function() {
                for (var args = [], _i = 0; _i < arguments.length; _i++) args[_i] = arguments[_i];
                if ("toFocussed not allowed for popup when it open like regular tab" !== args[0]) try {
                    message.emitFocusedTab("bg-log", {
                        method: method,
                        args: args
                    });
                } catch (e) {}
                savedConsole[method].apply(savedConsole, __spread(args));
            };
        }), w.console = newConsole;
    };
}, function(module, exports, __webpack_require__) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: !0
    });
    var GnarSpec = function() {
        function GnarSpec(gnar) {
            this.gnar = gnar;
        }
        return GnarSpec.prototype.checkingToggleClick = function(placement, siteCategory, state) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/checking-toggle-click",
                object: "toggle",
                objectId: "checking",
                placement: placement,
                siteCategory: siteCategory,
                state: state
            });
        }, GnarSpec.prototype.connectednessDataEmail = function(businessCount, businessHistogramByRCount, businessHistogramByRecipients, hashedUserId, histogramByRCount, histogramByRecipients, personalCount, personalHistogramByRCount, personalHistogramByRecipients, startDateTime, totalCount) {
            return this.gnar.track({
                eventName: "chromeExt/connectednessData-email",
                object: "email",
                objectId: "connectednessData",
                businessCount: businessCount,
                businessHistogramByRCount: businessHistogramByRCount,
                businessHistogramByRecipients: businessHistogramByRecipients,
                hashedUserId: hashedUserId,
                histogramByRCount: histogramByRCount,
                histogramByRecipients: histogramByRecipients,
                personalCount: personalCount,
                personalHistogramByRCount: personalHistogramByRCount,
                personalHistogramByRecipients: personalHistogramByRecipients,
                startDateTime: startDateTime,
                totalCount: totalCount
            }, {
                lite: !0,
                sendInstance: !1,
                sendBrowser: !1,
                sendUser: !1
            });
        }, GnarSpec.prototype.definitionPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/definition-popup-show",
                object: "popup",
                objectId: "definition"
            });
        }, GnarSpec.prototype.definitionToggleClick = function(state) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/definition-toggle-click",
                object: "toggle",
                objectId: "definition",
                state: state
            });
        }, GnarSpec.prototype.disableButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/disable-button-click",
                object: "button",
                objectId: "disable",
                placement: placement
            });
        }, GnarSpec.prototype.disableReminderDoNotShowAgainButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/disableReminderDoNotShowAgain-button-click",
                object: "button",
                objectId: "disableReminderDoNotShowAgain",
                placement: placement
            });
        }, GnarSpec.prototype.disableReminderNotificationShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/disableReminder-notification-show",
                object: "notification",
                objectId: "disableReminder"
            });
        }, GnarSpec.prototype.disableUntilNextVisitButtonClick = function(placement, siteCategory) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/disableUntilNextVisit-button-click",
                object: "button",
                objectId: "disableUntilNextVisit",
                placement: placement,
                siteCategory: siteCategory
            });
        }, GnarSpec.prototype.documentGenreButtonClick = function(documentGenre, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/documentGenre-button-click",
                object: "button",
                objectId: "documentGenre",
                documentGenre: documentGenre,
                placement: placement
            });
        }, GnarSpec.prototype.editorInit = function(docId, mode) {
            return this.gnar.track({
                action: "init",
                eventName: "chromeExt/editor-init",
                object: "editor",
                docId: docId,
                mode: mode
            });
        }, GnarSpec.prototype.emailSummarizationAcceptButtonClick = function(docId, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/emailSummarizationAccept-button-click",
                object: "button",
                objectId: "emailSummarizationAccept",
                docId: docId,
                placement: placement
            });
        }, GnarSpec.prototype.emailSummarizationBadgeShow = function(docId) {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/emailSummarization-badge-show",
                object: "badge",
                objectId: "emailSummarization",
                docId: docId
            });
        }, GnarSpec.prototype.emailSummarizationDisableButtonClick = function(docId, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/emailSummarizationDisable-button-click",
                object: "button",
                objectId: "emailSummarizationDisable",
                docId: docId,
                placement: placement
            });
        }, GnarSpec.prototype.emailSummarizationExpandButtonClick = function(docId, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/emailSummarizationExpand-button-click",
                object: "button",
                objectId: "emailSummarizationExpand",
                docId: docId,
                placement: placement
            });
        }, GnarSpec.prototype.emailSummarizationIgnoreButtonClick = function(docId, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/emailSummarizationIgnore-button-click",
                object: "button",
                objectId: "emailSummarizationIgnore",
                docId: docId,
                placement: placement
            });
        }, GnarSpec.prototype.emailSummarizationPopupShow = function(docId) {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/emailSummarization-popup-show",
                object: "popup",
                objectId: "emailSummarization",
                docId: docId
            });
        }, GnarSpec.prototype.facebookSignInButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/facebookSignIn-button-click",
                object: "button",
                objectId: "facebookSignIn",
                placement: placement
            });
        }, GnarSpec.prototype.facebookSignUpButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/facebookSignUp-button-click",
                object: "button",
                objectId: "facebookSignUp",
                placement: placement
            });
        }, GnarSpec.prototype.feedbackPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/feedback-popup-show",
                object: "popup",
                objectId: "feedback",
                placement: "gdocs"
            });
        }, GnarSpec.prototype.feedbackSentButtonClick = function(feedback, placement, score) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/feedbackSent-button-click",
                object: "button",
                objectId: "feedbackSent",
                feedback: feedback,
                placement: placement,
                score: score
            });
        }, GnarSpec.prototype.gButtonClick = function(docId, numberOfAdvancedAlerts, numberOfCriticalAlerts, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/g-button-click",
                object: "button",
                objectId: "g",
                docId: docId,
                numberOfAdvancedAlerts: numberOfAdvancedAlerts,
                numberOfCriticalAlerts: numberOfCriticalAlerts,
                placement: placement
            });
        }, GnarSpec.prototype.gdocsEditorInit = function(docId, mode) {
            return this.gnar.track({
                action: "init",
                eventName: "chromeExt/gdocs/editor-init",
                feature: "gdocs",
                object: "editor",
                docId: docId,
                mode: mode
            });
        }, GnarSpec.prototype.gdocsLargeDocumentButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/gdocs/largeDocument-button-click",
                feature: "gdocs",
                object: "button",
                objectId: "largeDocument",
                placement: placement
            });
        }, GnarSpec.prototype.gdocsLargeDocumentPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/gdocs/largeDocument-popup-show",
                feature: "gdocs",
                object: "popup",
                objectId: "largeDocument"
            });
        }, GnarSpec.prototype.gdocsOfflinePageReloadButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/gdocs/offlinePageReload-button-click",
                feature: "gdocs",
                object: "button",
                objectId: "offlinePageReload",
                placement: placement
            });
        }, GnarSpec.prototype.gdocsOfflinePopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/gdocs/offline-popup-show",
                feature: "gdocs",
                object: "popup",
                objectId: "offline"
            });
        }, GnarSpec.prototype.gdocsOpenEditorButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/gdocs/openEditor-button-click",
                feature: "gdocs",
                object: "button",
                objectId: "openEditor",
                placement: placement
            });
        }, GnarSpec.prototype.gdocsOptInPopupCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/gdocs/optInPopupClose-button-click",
                feature: "gdocs",
                object: "button",
                objectId: "optInPopupClose",
                placement: placement
            });
        }, GnarSpec.prototype.gdocsOptInPopupEnableButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/gdocs/optInPopupEnable-button-click",
                feature: "gdocs",
                object: "button",
                objectId: "optInPopupEnable",
                placement: placement
            });
        }, GnarSpec.prototype.gdocsOptInPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/gdocs/optIn-popup-show",
                feature: "gdocs",
                object: "popup",
                objectId: "optIn"
            });
        }, GnarSpec.prototype.getPremiumButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/getPremium-button-click",
                object: "button",
                objectId: "getPremium",
                placement: placement
            });
        }, GnarSpec.prototype.googleSignInButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/googleSignIn-button-click",
                object: "button",
                objectId: "googleSignIn",
                placement: placement
            });
        }, GnarSpec.prototype.googleSignUpButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/googleSignUp-button-click",
                object: "button",
                objectId: "googleSignUp",
                placement: placement
            });
        }, GnarSpec.prototype.install = function(installSource) {
            return this.gnar.track({
                action: "install",
                eventName: "chromeExt/install",
                installSource: installSource
            });
        }, GnarSpec.prototype.languageSettingUpdate = function(language, languageSource, isLikeCapi) {
            return this.gnar.track({
                action: "update",
                eventName: "chromeExt/language-setting-update",
                object: "setting",
                objectId: "language",
                language: language,
                languageSource: languageSource,
                isLikeCapi: isLikeCapi
            });
        }, GnarSpec.prototype.largeDocumentButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/largeDocument-button-click",
                object: "button",
                objectId: "largeDocument",
                placement: placement
            });
        }, GnarSpec.prototype.largeDocumentPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/largeDocument-popup-show",
                object: "popup",
                objectId: "largeDocument"
            });
        }, GnarSpec.prototype.loginReminderBadgeShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/loginReminder-badge-show",
                object: "badge",
                objectId: "loginReminder"
            });
        }, GnarSpec.prototype.loginReminderCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/loginReminderClose-button-click",
                object: "button",
                objectId: "loginReminderClose",
                placement: placement
            });
        }, GnarSpec.prototype.loginReminderDoNotShowThisAgainButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/loginReminderDoNotShowThisAgain-button-click",
                object: "button",
                objectId: "loginReminderDoNotShowThisAgain",
                placement: placement
            });
        }, GnarSpec.prototype.loginReminderPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/loginReminder-popup-show",
                object: "popup",
                objectId: "loginReminder"
            });
        }, GnarSpec.prototype.myGrammarlyButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/myGrammarly-button-click",
                object: "button",
                objectId: "myGrammarly",
                placement: placement
            });
        }, GnarSpec.prototype.newBadgeButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/newBadge-button-click",
                object: "button",
                objectId: "newBadge",
                placement: placement
            });
        }, GnarSpec.prototype.newDocumentButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/newDocument-button-click",
                object: "button",
                objectId: "newDocument",
                placement: placement
            });
        }, GnarSpec.prototype.offlinePageReloadButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/offlinePageReload-button-click",
                object: "button",
                objectId: "offlinePageReload",
                placement: placement
            });
        }, GnarSpec.prototype.offlinePopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/offline-popup-show",
                object: "popup",
                objectId: "offline"
            });
        }, GnarSpec.prototype.onboardingOverlayCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/overlayClose-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "overlayClose",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingOverlayLetsWriteButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/overlayLetsWrite-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "overlayLetsWrite",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingOverlayNextButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/overlayNext-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "overlayNext",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingOverlayPersonalizeButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/overlayPersonalize-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "overlayPersonalize",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingOverlaySaveButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/overlaySave-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "overlaySave",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingOverlayShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/onboarding/overlay-show",
                feature: "onboarding",
                object: "overlay"
            });
        }, GnarSpec.prototype.onboardingPopupCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/onboarding/popupClose-button-click",
                feature: "onboarding",
                object: "button",
                objectId: "popupClose",
                placement: placement
            });
        }, GnarSpec.prototype.onboardingPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/onboarding/popup-show",
                feature: "onboarding",
                object: "popup"
            });
        }, GnarSpec.prototype.openEditorButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/openEditor-button-click",
                object: "button",
                objectId: "openEditor",
                placement: placement
            });
        }, GnarSpec.prototype.optInPopupCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/optInPopupClose-button-click",
                object: "button",
                objectId: "optInPopupClose",
                placement: placement
            });
        }, GnarSpec.prototype.optInPopupEnableButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/optInPopupEnable-button-click",
                object: "button",
                objectId: "optInPopupEnable",
                placement: placement
            });
        }, GnarSpec.prototype.optInPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/optIn-popup-show",
                object: "popup",
                objectId: "optIn"
            });
        }, GnarSpec.prototype.overlayCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/overlayClose-button-click",
                object: "button",
                objectId: "overlayClose",
                placement: placement
            });
        }, GnarSpec.prototype.overlayLetsWriteButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/overlayLetsWrite-button-click",
                object: "button",
                objectId: "overlayLetsWrite",
                placement: placement
            });
        }, GnarSpec.prototype.overlayNextButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/overlayNext-button-click",
                object: "button",
                objectId: "overlayNext",
                placement: placement
            });
        }, GnarSpec.prototype.overlayPersonalizeButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/overlayPersonalize-button-click",
                object: "button",
                objectId: "overlayPersonalize",
                placement: placement
            });
        }, GnarSpec.prototype.overlaySaveButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/overlaySave-button-click",
                object: "button",
                objectId: "overlaySave",
                placement: placement
            });
        }, GnarSpec.prototype.overlayShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/overlay-show",
                object: "overlay"
            });
        }, GnarSpec.prototype.popupCloseButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/popupClose-button-click",
                object: "button",
                objectId: "popupClose",
                placement: placement
            });
        }, GnarSpec.prototype.popupEditorDocumentGenreButtonClick = function(documentGenre, placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/popupEditor/documentGenre-button-click",
                feature: "popupEditor",
                object: "button",
                objectId: "documentGenre",
                documentGenre: documentGenre,
                placement: placement
            });
        }, GnarSpec.prototype.popupEditorSettingToggleClick = function(settingName, state) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/popupEditor/setting-toggle-click",
                feature: "popupEditor",
                object: "toggle",
                objectId: "setting",
                settingName: settingName,
                state: state
            });
        }, GnarSpec.prototype.popupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/popup-show",
                object: "popup"
            });
        }, GnarSpec.prototype.settingToggleClick = function(settingName, state) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/setting-toggle-click",
                object: "toggle",
                objectId: "setting",
                settingName: settingName,
                state: state
            });
        }, GnarSpec.prototype.signInButtonClick = function() {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/signIn-button-click",
                object: "button",
                objectId: "signIn",
                placement: "settingsToolbar"
            });
        }, GnarSpec.prototype.signInFormFail = function(placement, fieldErrors, formErrorMessage) {
            return this.gnar.track({
                action: "fail",
                eventName: "chromeExt/signIn-form-fail",
                object: "form",
                objectId: "signIn",
                placement: placement,
                fieldErrors: fieldErrors,
                formErrorMessage: formErrorMessage
            });
        }, GnarSpec.prototype.signInFormSuccess = function(placement) {
            return this.gnar.track({
                action: "success",
                eventName: "chromeExt/signIn-form-success",
                object: "form",
                objectId: "signIn",
                placement: placement
            });
        }, GnarSpec.prototype.signInOverlayShow = function(placement) {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/signIn-overlay-show",
                object: "overlay",
                objectId: "signIn",
                placement: placement
            });
        }, GnarSpec.prototype.signUpButtonClick = function() {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/signUp-button-click",
                object: "button",
                objectId: "signUp",
                placement: "settingsToolbar"
            });
        }, GnarSpec.prototype.signUpFormFail = function(placement, fieldErrors, formErrorMessage) {
            return this.gnar.track({
                action: "fail",
                eventName: "chromeExt/signUp-form-fail",
                object: "form",
                objectId: "signUp",
                placement: placement,
                fieldErrors: fieldErrors,
                formErrorMessage: formErrorMessage
            });
        }, GnarSpec.prototype.signUpFormSuccess = function(placement) {
            return this.gnar.track({
                action: "success",
                eventName: "chromeExt/signUp-form-success",
                object: "form",
                objectId: "signUp",
                placement: placement
            });
        }, GnarSpec.prototype.signUpOverlayShow = function(placement) {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/signUp-overlay-show",
                object: "overlay",
                objectId: "signUp",
                placement: placement
            });
        }, GnarSpec.prototype.synonymAcceptButtonClick = function(placement) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/synonymAccept-button-click",
                object: "button",
                objectId: "synonymAccept",
                placement: placement
            });
        }, GnarSpec.prototype.synonymsPopupShow = function() {
            return this.gnar.track({
                action: "show",
                eventName: "chromeExt/synonyms-popup-show",
                object: "popup",
                objectId: "synonyms"
            });
        }, GnarSpec.prototype.toolbarButtonClick = function(placement, type) {
            return this.gnar.track({
                action: "click",
                eventName: "chromeExt/toolbar-button-click",
                object: "button",
                objectId: "toolbar",
                placement: placement,
                type: type
            });
        }, GnarSpec.prototype.update = function(oldVersion) {
            return this.gnar.track({
                action: "update",
                eventName: "chromeExt/update",
                oldVersion: oldVersion
            });
        }, GnarSpec;
    }();
    exports.GnarSpec = GnarSpec;
} ]);