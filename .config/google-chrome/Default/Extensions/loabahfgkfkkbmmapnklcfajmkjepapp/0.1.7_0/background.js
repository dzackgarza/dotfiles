var buttonExtension = (function(module) {
    module.grabText = 'PomoDone it!';
    module.namespace = 'pomodone';
    module.options = {
        apiKey: '',
        blackList: '',
        openIn: 'web',
        blockerIsActive: false
    };

    module.realTime = {
        timer: null,
        card: null
    };

    module.primus = Primus.connect('wss://ws.pomodoneapp.com/primus', {
        reconnect: {
            retries: 50,
            factor: 1.5
        }
    });

    module.reconnect = function () {
        module.options.apiKey && module.primus.write({
            action: 'join',
            room: module.options.apiKey,
            type: 'ext'
        });
    };

    module.primus.on('disconnection', module.timerIsStopped);

    module.primus.on('open', function open() {
        chrome.storage && chrome.storage.sync.get({
            options: module.options
        }, function(data) {
            module.options = data.options;

            module.reconnect();

            module.startEvents();
        });
    });

    if (chrome.storage) {
        chrome.storage.onChanged.addListener(function (optionsDiff) {
            var options = optionsDiff.options.newValue;

            if (options) {
                module.options = options;

                module.reconnect();
            }
        });
    }

    module.primus.on('data', function (event) {
        switch (event.action) {
            case 'open':
                var id = event.data.id;

                if (id && module.options.openIn == 'web') {
                    chrome.tabs.query({
                        url: '*://app.pomodoneapp.com/*'
                    }, function (tabs) {
                        // console.info('tabs', tabs);

                        if (tabs.length) {
                            var tab = tabs[0];
                            var pathArray = tab.url.split('/');
                            var protocol = pathArray[0];

                            chrome.tabs.update(tab.id, {
                                url: protocol + '//app.pomodoneapp.com/#/card/' + id,
                                active: true
                            });
                        } else {
                            chrome.tabs.create({
                                url: 'https://app.pomodoneapp.com/#/card/' + id
                            });
                        }
                    });
                }
            break;

            case 'status':
                if (event.timers.length) {
                    module.timerIsStarted(event.timers[0].timer, event.timers[0].card);
                }
            break;

            case 'timerStart':
                module.timerIsStarted(event.timer, event.card);
            break;

            case 'timerStop':
                module.timerIsStopped(event.timer, event.card);
            break;
        }
    });

    module.timerIsStarted = function (timer, card) {
        module.realTime.timer = timer;
        module.realTime.card = card;

        if (module.options.blockerIsActive) {
            chrome.browserAction.setIcon({
                path: 'icon-gray.png'
            });

            module.searchDomainsForBlock();
        }
    };

    module.timerIsStopped = function () {
        module.realTime.timer = null;
        module.realTime.card = null;

        chrome.browserAction.setIcon({
            path: 'icon.png'
        });

        if (module.options.blockerIsActive) {
            chrome.tabs.query({
                windowType: 'normal',
                url: ['http://*/*', 'https://*/*']
            }, function (tabs) {
                tabs.forEach(function (tab) {
                    chrome.tabs.sendMessage(tab.id, {
                        action: 'unblock'
                    });
                });
            });
        }
    };

    module.addItem = function (url, title) {
        if (module.options.apiKey) {
            module.primus.write({
                to: 'pomodone',
                action: 'add',
                room: module.options.apiKey,
                data: {
                    url: url,
                    title: title
                }
            });

            if (module.options.openIn == 'app') {
                chrome.tabs.executeScript({
                    code: 'var iframe=document.createElement("iframe");iframe.style.display="none";iframe.src="pomodone://app";document.body.appendChild(iframe);'
                });
            }
        } else {
            module.openOptions();
        }
    };

    module.verifyDomainBlacklistInTab = function (url, tabId) {
        var blackList = module.options.blackList.split('\n');
        var i;
        var domain;

        if (url && module.realTime.timer && module.options.blockerIsActive) {
            for (i in blackList) {
                domain = blackList[i];

                if (domain && url.includes(domain)) {
                    chrome.tabs.sendMessage(tabId, {
                        action: 'block'
                    });
                }
            }
        }
    };

    module.createContextMenu = function () {
        if (!chrome.contextMenus) {
            return;
        }

        chrome.contextMenus.create({
            'title': module.grabText,
            'contexts': ['selection'],
            'onclick': function (info, tab) {
                module.addItem(tab.url, info.selectionText);
            }
        });

        chrome.contextMenus.create({
            'title': module.grabText,
            'contexts': ['page'],
            'onclick': function (info, tab) {
                module.addItem(tab.url, tab.title);
            }
        });
    };

    module.createContextMenu();

    chrome.browserAction.onClicked.addListener(function (tab) {
        module.addItem(tab.url, tab.title);
    });

    module.openOptions = function () {
        chrome.tabs.create({
            url: chrome.extension.getURL('/options.html')
        });
    };

    module.searchDomainsForBlock = function () {
        chrome.tabs.query({
            windowType: 'normal',
            url: ['http://*/*', 'https://*/*']
        }, function (tabs) {
            tabs.forEach(function (tab) {
                module.verifyDomainBlacklistInTab(tab.url, tab.id);
            });
        });
    };

    module.startEvents = function () {
        chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
            var apiKey = module.options.apiKey;

            if (!apiKey) {
                module.openOptions();
            }

            if (request.to = module.namespace) {
                request.room = apiKey;

                switch (request.action) {
                    case 'add':
                        module.primus.write(request);

                        break;

                    case 'getStatus':
                        if (module.realTime.timer) {
                            sendResponse(module.realTime);
                        }

                        break;
                }
            }
        });

        chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
            module.verifyDomainBlacklistInTab(tab.url, tabId);
        });

        module.searchDomainsForBlock();

        chrome.tabs.query({
            windowType: 'normal',
            url: ['http://*/*', 'https://*/*']
        }, function (tabs) {
            tabs.forEach(function (tab) {
                chrome.tabs.executeScript(tab.id, {
                    file: 'inject.js'
                });

            });
        });
    };

    return module;
}(buttonExtension || {}));
