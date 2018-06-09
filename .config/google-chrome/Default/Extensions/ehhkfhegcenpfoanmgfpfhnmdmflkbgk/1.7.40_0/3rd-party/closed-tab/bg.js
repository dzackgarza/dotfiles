
var SU_settings = {numLimit: 20};
localStorage["SU_closedTabIdInc"] = localStorage["SU_closedTabIdInc"] || 0;

// Replace HTML tags < >
function quote(s) {
  var s1=s;
  s1 = s1.replace(new RegExp("<", "g"), "&lt;");
  s1 = s1.replace(new RegExp(">", "g"), "&gt;");
  return s1;
}

function addNewTab(tabId, changeInfo, tab) {  
	//if (!isTabRecordable(tab)) return;
  localStorage["SU_openTab:" + tabId] = JSON.stringify({
  	index: tab.index,
  	url: tab.url,
  	title: tab.title || null,
  	incognito: tab.incognito
  });
  storeOpenTabId(tabId);
}

function onRemoved(tabId, info)  {
	forgetOpenTabId(tabId);
	var tab;
	var tabJSON = localStorage["SU_openTab:" + tabId];
	delete localStorage["SU_openTab:" + tabId];

	if (!tabJSON) {
		//console.log('WARN: tab doesn\'t exist: ' + tabId)
		return;
	}

	try {
		tab = JSON.parse(tabJSON);
	} catch (e) {
		logError(new Error('ERROR: stored tab has invalid JSON'));
		console.log('ERROR: stored tab has invalid JSON: ' + tabId)
		return;
	}

  // Should we record this tab?
  if (!isTabRecordable(tab)) return;

  // save this
  var closedTabId = localStorage["SU_closedTabIdInc"]++;
  localStorage["SU_closedTab:" + closedTabId] = tabJSON;

  // shift out the one after cutoff point
  var deleteId = closedTabId - SU_settings.numLimit;
  delete localStorage["SU_closedTab:" + deleteId];
}

function isTabRecordable(tab) {
	return tab.url && /^(http:|https:|ftp:|file:)/i.test(tab.url);
}

chrome.tabs.onUpdated.addListener(addNewTab);

chrome.tabs.onRemoved.addListener(onRemoved);

// needed to register instant/prerendered pages
chrome.webNavigation.onTabReplaced.addListener(function (details) {
	// register new tab data
	chrome.tabs.get(details.tabId, function (tab) {
		addNewTab(details.tabId, null, tab);
		delete localStorage["SU_openTab:" + details.replacedTabId];
		forgetOpenTabId(details.replacedTabId);
	});
});


// This persistent data structure is supposed 
// to help remember tab ids for crash recovery
var openTabIds;
try {
	openTabIds = JSON.parse(localStorage.openTabIds || "{}");
} catch (e) {
	openTabIds = {};
	logError(new Error('ERROR: stored openTabIds has invalid JSON'));
}

function storeOpenTabId(tabId) {
	openTabIds[tabId] = 1;
	localStorage.SU_openTabIds = JSON.stringify(openTabIds);
}
function forgetOpenTabId(tabId) {
	delete openTabIds[tabId];
	localStorage.SU_openTabIds = JSON.stringify(openTabIds);
}

// Crash recovery
// Add all tabs to the ClosedTabs list from localStorage 
// that were open before crash (but currently are not)
Object.keys(openTabIds).forEach(onRemoved);
 
// Add already opened tabs on start
chrome.tabs.query({}, function (tabs) {
	for (var i = tabs.length; i--;) {
		addNewTab(tabs[i].id, null, tabs[i]);
	}
});


/// TEMPORARY CODE
/// clean up tablist remainder of old crashes and replaced tabs
/*
var isWithinLimitedTimeframe = +new Date < 1432992008513 + (30 * 24 * 60 * 60 * 1000);
if (localStorage.tablist_cleanup_done2 != 'true' && isWithinLimitedTimeframe) {
  localStorage.tablist_cleanup_done2 = 'true';
	var id = 0;
	setTimeout(function remove_cruft() {
		var max = id + 100;
		for ( ; id < max; id++) {
			delete localStorage['TabList-' + id];
			delete localStorage['ClosedTab-' + id];
		}
		if (id < 100*1000) setTimeout(remove_cruft, 1);
	}, 1);
}
*/



/*
function addNewHistoryEntry(tabId, url) {
	if (!localStorage["HistoryBackward-"+tabId])
		localStorage["HistoryBackward-"+tabId] = url;
	else 
		localStorage["HistoryBackward-"+tabId] += "%%" + url;
	// new url, drop old forward history
	localStorage["HistoryForward-"+tabId] = "";
}

function registerHistoryNavigation(tabId, url) { /// TODO MAKE SURE THEY EXISTS
	var backward = (localStorage["HistoryBackward-"+tabId]||'').split("%%");
	var forward  = (localStorage["HistoryForward-"+tabId]||'').split("%%");
	// backwards array last url is the curent one
	if (url == backward.slice(-2, -1)) {
		// remove us from back history
		// add old url to forward history
		forward.unshift(backward.pop());
	} else if (url == forward[0]) {
		// remove us from forward list
		// add old url to back history
		backward.push(forward.shift())
	}

	// limit history to 10 entries
	backward = backward.slice(-10);
	forward = forward.slice(0, 10);

	localStorage["HistoryBackward-"+tabId] = backward.join('%%');
	localStorage["HistoryForward-"+tabId]  = forward.join('%%');
}

function isHistoryButtonUsed(details) {
	return details.transitionQualifiers.indexOf('forward_back') > -1;
}
*/
