!function(e){var n;e.getUnavailablePreferences=(n=e.getUnavailablePreferences,function(){var e=n();return e.enablenewlogin=!g_shownewloginoption,e.hidecontextspan=void 0===chrome.contextMenus,e});var t=function(e){return e?{windowID:e.windowId,tabURL:e.url,tabID:e.id}:null};e.initialize=function(){chrome.runtime.onConnect.addListener(function(n){if(0===n.name.indexOf("requestPort")){var o=e.initializeRequestFramework({sendContentScript:function(e){n.postMessage(e)},tabDetails:t(n.sender&&n.sender.tab),frameIdentity:n.sender&&n.sender.frameId?n.sender.tab.id+"-"+n.sender.frameId:null});n.onMessage.addListener(o.requestHandler),n.onDisconnect.addListener(function(){o.disconnectHandler()})}})},e.getUILanguage=function(){return chrome.i18n.getUILanguage()},e.openPopoverDialog=function(n){e.openTabDialog.apply(e,arguments)},e.refreshGroupNames=function(){},e.closePopovers=function(){chrome.extension.getViews({type:"popup"}).forEach(function(e){e.close()})},e.getFavicon=function(){if(g_ischrome&&(g_isedge||g_isfirefoxwebext))return function(e){e.callback&&e.callback(null)};var e=null,n=function(e,n){var t=document.createElement("img");t.src=e,t.addEventListener("load",function(){var e=function(e){var n="";try{var t=document.createElement("canvas");t.height=e.clientHeight,t.width=e.clientWidth,t.getContext("2d").drawImage(e,0,0),n=t.toDataURL()}catch(e){}return n}(t);document.body.removeChild(t),n(e)}),t.addEventListener("error",function(){n(""),document.body.removeChild(t)}),document.body.appendChild(t)};return document.addEventListener("DOMContentLoaded",function(){n("chrome://favicon/",function(n){e=n})}),function(t){t.url&&t.callback&&n("chrome://favicon/"+t.url,function(n){t.callback(n===e?"":n)})}}(),function(){var n=function(e,n){LPTabs.get({tabID:e.id,callback:function(t){if(n.inject){var o=0,r=[].concat(n.inject.files),a=function(){++o===r.length&&(t.extendTop({context:n.inject.context}),n.inject.allFrames&&t.extendFrames({context:n.inject.context}),n.loadHandler&&n.loadHandler(t))};r.forEach(function(t){chrome.tabs.executeScript(e.id,{file:t,allFrames:n.inject.allFrames},a)})}else n.loadHandler&&n.loadHandler(t);if(n.closeHandler){var i=function(e){var n=chrome.extension.getViews({type:"tab",windowId:e.windowID});if(1===n.length)return n[0];for(var t=0,o=n.length;t<o;++t){var r=n[t];if(r.tabID===e.tabID)return r}return null}(t.tabDetails);i&&i.addEventListener("beforeunload",function(){n.closeHandler(i)})}}})};function o(e){chrome.tabs.executeScript(e,{file:"modaloverlay/removeModalOverlay.js"},function(){chrome.runtime.lastError&&(console.log("Error removing modal overlay"),"Cannot access a chrome:// URL"===chrome.runtime.lastError.message?console.log("Extensions cannot affect internal chrome:// URLs"):console.log(chrome.runtime.lastError.message))})}e.getCurrentTab=function(e){chrome.tabs.query({active:!0,currentWindow:!0},function(n){1===n.length?LPTabs.get({tabID:n[0].id,callback:e}):e(null)})},e.getCurrentTabDetails=function(e){chrome.tabs.query({active:!0,currentWindow:!0},function(n){e(t(n[0]))})},e.openDialogWindow=function(e){var t=e.features||{};t.url=e.url,t.type=chrome.windows.CreateType.POPUP,chrome.windows.create(t,function(t){n(t.tabs[0],e)})},e.openTab=function(e){chrome.tabs.create({url:e.url,active:!e.inactive},function(t){n(t,e)})},e.openWindow=function(e){chrome.windows.create({url:e.url},function(t){n(t.tabs[0],e)})},e.openSame=function(e){chrome.tabs.update(null,{url:e.url},function(t){n(t,e)})},e.navigateTab=function(n){chrome.tabs.update(n.tabId,{url:n.url,active:!0},function(t){var o=e.onTabUpdated(function(e){e.tabDetails.tabID===t.id&&(o(),"function"==typeof n.loadHandler&&n.loadHandler(e))})})},e.activateTab=function(e){chrome.windows.update(e.windowID,{focused:!0}),chrome.tabs.update(e.tabID,{active:!0})},e.closeTab=function(e){chrome.tabs.remove(e.tabID)},e.onTabUpdated=function(e){if("function"==typeof e){var n=function(n,t){"complete"===t.status&&LPTabs.get({tabID:n,callback:e})};chrome.tabs.onUpdated.addListener(n)}return function(){chrome.tabs.onUpdated.removeListener(n)}},e.onTabActivated=function(e){if("function"==typeof e){var n=function(n){LPTabs.get({tabID:n.tabId,callback:e})};chrome.tabs.onActivated.addListener(n)}return function(){chrome.tabs.onActivated.removeListener(n)}},e.onTabClosed=function(e){if("function"==typeof e){var n=function(n){e(n)};chrome.tabs.onRemoved.addListener(n)}return function(){chrome.tabs.onRemoved.removeListener(n)}},e.onTransition=function(e){if("function"==typeof e){var n=function(n){e(n)};chrome.webNavigation.onCommitted.addListener(n)}return function(){chrome.webNavigation.onCommitted.removeListener(n)}},e.onAuthRequired=function(e){if(chrome.webRequest.onAuthRequired){if("function"==typeof e){var n=function(n){return e(n,n.tabId)};chrome.webRequest.onAuthRequired.addListener(n,{urls:["<all_urls>"]},["blocking"])}return function(){chrome.webRequest.onAuthRequired.removeListener(n)}}return function(){}},e.showModalOverlay=function(n){e.getCurrentTabDetails(function(e){chrome.tabs.executeScript(e.tabID,{file:"modaloverlay/showModalOverlay.js"},function(){chrome.runtime.lastError&&(console.log("Error showing modal overlay"),"Cannot access a chrome:// URL"===chrome.runtime.lastError.message?console.log("Extensions cannot affect internal chrome:// URLs"):console.log(chrome.runtime.lastError.message)),"function"==typeof n&&n(e.tabID)})})},e.removeModalOverlay=function(e){e?o(e):chrome.tabs.getAllInWindow(null,function(e){for(var n=0;n<e.length;n++)o(e[n].id)})},e.hideYoureAlmostDoneMarketingOverlay=function(e){chrome.tabs.executeScript(e,{file:"modaloverlay/hideYoureAlmostDoneMarketingOverlay.js"},function(){chrome.runtime.lastError&&(console.log("Error hiding marketing overlay"),"Cannot access a chrome:// URL"===chrome.runtime.lastError.message?console.log("Extensions cannot affect internal chrome:// URLs"):console.log(chrome.runtime.lastError.message))})}}()}(LPPlatform);
//# sourceMappingURL=sourcemaps/platformBackgroundOverride.js.map
