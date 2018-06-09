
//window.DEBUG = true;

window.addEventListener('DOMContentLoaded', openDb);
window.addEventListener('load', openDb);

// Number of recent visits to sample when calculating frecency scores for URLs.
localStorage.FB_option_recentvisits = 99999; // 20 || 99999
localStorage.FB_option_frecency_unvisitedbookmark = 1;

// FB_index_base_time; FB_index_is_building; FB_index_ready;

//if (navigator.hardwareConcurrency) 
var kCalculateBatchSize  =  10; //  10
var kCalculateBatchDelay = 100; // 100
var kFrecencyCutoff = 100;

if (window.DEV) kCalculateBatchSize = 1000*1000;

//
// Init
//

localStorage.FB_index_is_building = "false";

// if we don't have an index, let's build one
if (localStorage.FB_index_ready != "true") {
	startIndexing();
}

function startIndexing() {
	if (!chrome.history) return;
	if (!isDocumentReady()) {
		window.addEventListener('DOMContentLoaded', startIndexing);
		return;
	} else if (!openDb()) {
		setTimeout(startIndexing, 5*1000);
		return;
	}
	window.addEventListener('error', errorWhileIndexing);
	localStorage.FB_index_is_building = "true";
	localStorage.FB_index_ready = "false";
	localStorage.FB_index_base_time = "";
	chrome.runtime.sendMessage({ action: "search-indexing-start" });
	index();
}

function finishIndexing() {
	localStorage.FB_index_is_building = "false";
	localStorage.FB_index_ready = "true";
	localStorage.FB_index_base_time = +new Date;
	localStorage.FB_index_first_run_complete = "true"; // even if it wasn't the first
	window.removeEventListener('error', errorWhileIndexing);
	chrome.runtime.sendMessage({ action: "search-indexing-complete" });
}

function errorWhileIndexing() {
	localStorage.FB_index_is_building = "false";
	localStorage.FB_index_ready = "false";
	localStorage.FB_index_base_time = "";
	chrome.runtime.sendMessage({ action: "search-indexing-error" });
}

chrome.permissions.onAdded.addListener(function (details) { 
	if (details.permissions.indexOf('history') != -1) {
		setTimeout(function () {
			window.location.reload(); // chrome.history will only be available on the next run
		}, 1000); // need a little delay to register response
	}
});


//
// Index (private)
//

function index() {

	if (!chrome.history) return;
	if (!openDb()) return;

	//console.profile();
	logger.options.elapsed = true;
	logger.start();
	var startTime = +new Date;

	var urls = [];
	var tags = [];
	var toInsert = {tags:[], searchEngines:[], historyItems:[], bookmarks:[], frecencyScores:[], totalUrls:0};
	var unvisitedBookmarkScore = localStorage.FB_option_frecency_unvisitedbookmark;

	// Get history
	logStep("Fetching history items");

	chrome.history.search({text:"", startTime:0, maxResults:100*1000}, function (historyItems) {
		var filteredHistory = [];
		var now = +new Date;
		var days30 = 30*24*60*60*1000;
		var ignoreRe = /^(data:|javascript:)/i;
		for (var h = 0; h < historyItems.length; h++) {
			var item = historyItems[h];
			if ( (item.visitCount > 1 || now - item.lastVisitTime < days30) && 
					 !ignoreRe.test(item.url)) {
				urls.push(item.url);
				filteredHistory.push(item);
			}
		}
		toInsert.historyItems = filteredHistory;
		// Get bookmarks
		logStep("Fetching bookmarks");

		//chrome.bookmarks.getTree(
		run(function (nodes) {
			/*
			var indexBookmarks = function (nodes) {
					for (var n = 0; n < nodes.length; n++) {
						toInsert.bookmarks.push(nodes[n]);
						if (nodes[n].url) {
							urls.push(nodes[n].url);
						}
						if (nodes[n].children) {
							indexBookmarks(nodes[n].children);
						}
					}
			};
			indexBookmarks(nodes);
			*/

			// Frecency scores
			toInsert.totalUrls = urls.length;

			var urlsNum = numberWithCommas(toInsert.totalUrls);
			logStep("Calculating frecency scores for " + urlsNum + " different URLs...");
			//console.profile();///

			var frecencyScoresCalculated = 0;
			var titles = {}
			var typedVisitIds = [];
			window.db.transaction(function (tx) {
				createDatabaseTable_urls(tx, true);
				tx.executeSql('SELECT url, title, typed_visits FROM urls WHERE type = 1', [], function (tx, places) {
					if (places.rows.length) {
						for (var x = 0; x < places.rows.length; x++) {
							var place = places.rows.item(x);
							titles[place.url] = place.title;
							typedVisitIds[place.url] = place.typed_visits;
						}
					}
				});
			}, function txError(err) {
				errorWhileIndexing();
				errorHandlerDatabase(err, getLineInfo());
			}, function txSuccess() {

				if (urls.length) {
					calculateScoresBatch();
				} else {
					calculationsFinished();
				}

				calculateScoresBatch.index = 0;
				calculateScoresBatch.batchEndIndex = 0;

				function calculateScoresBatch() {
					var i = calculateScoresBatch.index;
					var end = Math.min(i + kCalculateBatchSize, urls.length);
					for ( ; i < end; i++) {
						calculateScores(urls[i]); // calculateScoresAndFinish
					}
					calculateScoresBatch.index = i;
					calculateScoresBatch.batchEndIndex = end;
				}

				calculateScoresBatch();

				function calculateScores(url) {
					chrome.history.getVisits({ url:url }, function (visits) {

						frecencyScoresCalculated++;

						if (frecencyScoresCalculated == calculateScoresBatch.batchEndIndex) {
							setTimeout(calculateScoresBatch, kCalculateBatchDelay);
						}
						
						toInsert.frecencyScores[url] = calculateFrecency(visits, typedVisitIds[url]||'');
						// stop here if we still have work to do 
						if (toInsert.totalUrls == frecencyScoresCalculated) 
							calculationsFinished();
					});
				}

				function calculateScoresSimple(url, visits) {
					toInsert.frecencyScores[url] = calculateFrecency(visits, typedVisitIds[url]||'');
				}

				function calculationsFinished() {
					// Insert everything into database if all is ready
					window.db.transaction(function (tx) {
						//console.profileEnd();///
						// Create tables and some indixes
						logger.log("Creating database tables");
						createDatabaseTables(tx);
						// insert history items
						var historyNum = numberWithCommas(toInsert.historyItems.length);
						logStep("Adding " + historyNum + " history items to Database...");
						ga('send', 'event', 'search', 'index', 'history', toInsert.historyItems.length);
						insertHistoryToDatabase(tx, toInsert, typedVisitIds, titles);
						// insert bookmarks
						/*var bookmarksNum = numberWithCommas(toInsert.bookmarks.length);
						logStep("Adding " + bookmarksNum + " bookmarks to Database...");
						insertBookmarksToDatabase(tx, toInsert, typedVisitIds, unvisitedBookmarkScore);*/
						// lazy indexes
						createDatabaseIndexes_urls(tx);
						// some cleanup
						// tx.executeSql('DELETE FROM urls WHERE url LIKE "data:%" OR url LIKE "javascript:%"');
						// all done
						logStep("Saving");
					}, function txError(err) { 
						console.log(err);
						errorWhileIndexing();
						errorHandlerDatabase(err, getLineInfo());
					}, function txSuccess() {
						console.profileEnd();
						var secs = Math.round((+new Date-startTime)/1000);
						logStep("Indexing complete! Took " + secs + " seconds.");	
						//ga('send', 'timing', 'search-index', 'history', (+new Date-startTime));
						ga('send', 'event', 'timing-search-index', 'history', '', (+new Date-startTime));
						indexWordsFromUrls(function () {
							finishIndexing();
						}, errorWhileIndexing);
					});
				}
			});
		});
	});
}

function logStep(message) {
	logger.log(message);
	window.indexStatus = message;
	chrome.runtime.sendMessage(null, {
		message: "currentStatus",
		status: message, 
		step: window.currentStep
	});
	window.currentStep++;
}


//
// SQL Tables
//

function createDatabaseTables(tx) {

	createDatabaseTable_urls(tx);

	tx.executeSql('CREATE TABLE IF NOT EXISTS errors (id INTEGER PRIMARY KEY, date NUMERIC, version TEXT, url TEXT, file TEXT, line NUMERIC, message TEXT, count NUMERIC)');

	tx.executeSql('CREATE TABLE IF NOT EXISTS inputurls (input TEXT, url TEXT)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS inputurls__input ON inputurls (input)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS inputurls__url ON inputurls (url)');

	tx.executeSql('CREATE TABLE IF NOT EXISTS searchqueries (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS searchqueries__query ON searchqueries (query)');
	// "manual" meaning the thumb a user-defined, not a top frecency scored one
	tx.executeSql('CREATE TABLE IF NOT EXISTS thumbs (url TEXT UNIQUE ON CONFLICT REPLACE, data BLOB, date INTEGER, title TEXT, frecency NUMERIC DEFAULT -1, manual NUMERIC DEFAULT 0)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS thumbs__url ON thumbs (url)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS thumbs__frecency ON thumbs (frecency)');
}

// IMPORTANT: all changes to fields should be made to "INSERT OR REPLACE" queries too!!
function createDatabaseTable_urls(tx, keepOld) {
	if (!keepOld) tx.executeSql('DROP TABLE IF EXISTS urls');
	tx.executeSql('CREATE TABLE IF NOT EXISTS urls (url TEXT, type INTEGER, title TEXT, frecency INTEGER DEFAULT -1, bookmark_id INTEGER DEFAULT NULL, bookmark_parent_id INTEGER DEFAULT NULL,typed_visits TEXT DEFAULT "", frecency_is_dirty BOOLEAN DEFAULT 0, queued_for_deletion BOOLEAN DEFAULT 0)'); // type1 = history item, type2 = bookmark
	// [create all INDEX after INSERT for performance]
}

function createDatabaseIndexes_urls(tx) {
	// INDEX for urls (after all INSERT for performance)
	//tx.executeSql('CREATE INDEX IF NOT EXISTS urls__url ON urls (url)');
	//tx.executeSql('CREATE INDEX IF NOT EXISTS urls__type ON urls (type)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls__title ON urls (title)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls__frecency ON urls (frecency DESC)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls__bookmark_id ON urls(bookmark_id)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls__bookmark_parent_id ON urls (bookmark_parent_id)');
	tx.executeSql('CREATE UNIQUE INDEX IF NOT EXISTS urls__url_type ON urls (url, type)'); // UNIQUE
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls__frecency_dirty ON urls (frecency_is_dirty)'); 
}

//
// Tabs
//

// When a tab changes its URL, or finishes loading the page...
/*
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
	//!processUpdatedTab(tabId, tab);
	//!toggleContextMenu && tabId && toggleContextMenu(tabId);
	// Update title in database

	if (localStorage.FB_index_ready != 'true') return;
	if (changeInfo.status && changeInfo.status == "complete") {
		openDb() && window.db.transaction(function (tx) {
			tx.executeSql('UPDATE urls SET title = ? WHERE url = ? AND type = 1', [tab.title, tab.url]);
			tx.executeSql('UPDATE thumbs SET title = ? WHERE url = ?', [tab.title, tab.url]);
		}, function (err) {
			errorHandlerDatabase(err, getLineInfo());
		});
	}
});
*/


//
// Frecency
//

// Generate a frecency score number for a URL.
// Scoring derived from https://developer.mozilla.org/en/The_Places_frecency_algorithm
function calculateFrecency(visitItems, typedVisitIds) {

	// Determine which bonus score to give
	var transitionBonuses = {
		link          : 100,  // FF: 120
		typed         : 2000, // FF: 200
		auto_bookmark : 75,   // FF: 140
		reload        : 0,
		start_page    : 0,
		form_submit   : 0,
		keyword       : 0,
		generated     : 0
	};

	var fCutoff1 = 4;
	var fCutoff2 = 14;
	var fCutoff3 = 31;
	var fCutoff4 = 90;
	var fWeight1 = 100;
	var fWeight2 = 70;
	var fWeight3 = 50;
	var fWeight4 = 30;
	var fWeight5 = 10;
	var fMaxSampleSize = localStorage.FB_option_recentvisits || 10;

	var fauxbarTypedVisitIds = [];
	if (typedVisitIds && typedVisitIds.length) {
		typedVisitIds = typedVisitIds.split(',');
		for (var t = 0; t < typedVisitIds.length; t++) {
			if (typedVisitIds[t]) {
				fauxbarTypedVisitIds[typedVisitIds[t]] = true;
			}
		}
	}

	// order is messed up sometimes for some reason
	visitItems.sort(function (a, b) {
		return a.visitTime - b.visitTime;
	});

	var singleVisitPoints = 0, summedVisitPoints = 0;

	// For each sampled recent visits to this URL...
	//var sampledVisits = visitItems.slice(-fSampleSize);
	var previousSampleVisitTime = Number.MAX_VALUE;
	var sampledVisits = 0;

	for (var i = visitItems.length; i--;) {

		if (sampledVisits >= fMaxSampleSize) 
			break; // done collecting the samples

		var vi = visitItems[i];
		var deltaSinceLastVisit = previousSampleVisitTime - vi.visitTime;
		previousSampleVisitTime = vi.visitTime;

		// sometimes a link transition comes after a typed
		if (deltaSinceLastVisit < 5*1000) { 
			//console.log('dropped. ' + deltaSinceLastVisit);
			/*
			console.log('dropped. ' + (~~deltaSinceLastVisit) +
									': ' + vi.transition + ' -> ' + visitItems[i+1].transition);
			*/
			//continue; 
		}

		if (fauxbarTypedVisitIds[vi.visitId]) {
			vi.transition = "typed";
		}

		var bonus = transitionBonuses[vi.transition] || 0;
		var bucketWeight;

		// Determine the weight of the score, based on the age of the visit
		var days = (+new Date - vi.visitTime) / 24 / 60 / 60 / 1000;
		if (days < fCutoff1) {
			bucketWeight = fWeight1;
		} else if (days < fCutoff2) {
			bucketWeight = fWeight2;
		} else if (days < fCutoff3) {
			bucketWeight = fWeight3;
		} else if (days < fCutoff4) {
			bucketWeight = fWeight4;
		} else {
			bucketWeight = fWeight5;
		}

		//var lambda = Math.LN2 / 30;
		//var bucketWeight = Math.pow(Math.E, (-lambda * days)) * 100;

		// Calculate the points
		singleVisitPoints = (bonus / 100) * bucketWeight;
		summedVisitPoints = summedVisitPoints + singleVisitPoints;

		sampledVisits += 1;
	}

	// Calculate and return the frecency score for the URL
	return Math.ceil(visitItems.length * summedVisitPoints / sampledVisits);
}


//
// History
//

window.typedUrls = [];

function insertHistoryToDatabase(tx, toInsert, typedVisitIds, titles) {
	var fields = 'type, url, title, frecency, typed_visits';
	bulkInsert(tx, 'urls', fields,  toInsert.historyItems.length, function (i) {
		var hI = toInsert.historyItems[i];
		return [1, hI.url, titles[hI.url]||hI.title, toInsert.frecencyScores[hI.url], typedVisitIds[hI.url]||''];
	});
	/*for (var h = 0; h < toInsert.historyItems.length; h++) {
		var hI = toInsert.historyItems[h];
		tx.executeSql(
			'INSERT INTO urls (type, url, title, frecency, typed_visits) VALUES (?, ?, ?, ?, ?)',
			[1, hI.url, titles[hI.url]||hI.title, toInsert.frecencyScores[hI.url], typedVisitIds[hI.url]||'']
		);
	}*/
}

// When Chrome adds a page visit to its history index, update urls index with this information.
// note: Chrome adds a "visit" as soon as the page starts loading. But this happens before the <title> tag is read, and so visits sometimes aren't recorded with a title in Chrome's history the first time they're loaded.
var kBackgroundPageLaunchTime = +new Date;

if (chrome.history) chrome.history.onVisited.addListener(onHistoryVisited);
function onHistoryVisited(historyItem) {

	/// LAUNCH if (+new Date - kBackgroundPageLaunchTime < 10*1000) return;

	if (localStorage.FB_index_is_building == 'true') return;

	var url = historyItem.url, title = historyItem.title;

	// We don't want to keep our extension page visits
	if (url.indexOf(chrome.extension.getURL("")) == 0) {
		chrome.history.deleteUrl({ url: url });
		return;
	}

	// DEV: While browsing, inspec background.html console to view visit objects.
	// Useful for determining what visit transition types Chrome uses.
	/*chrome.history.getVisits({url:historyItem.url}, function (visits) {
		var item = visits.pop();
		item.url = historyItem.url;
		console.log(item);
	});*/

	// TODO: use .referringVisitId (redirects, etc)

	if (localStorage.FB_index_ready != 'true') 
		return;
	else if (url.substr(0, 5) == 'data:') 
		return;
	if (!openDb())
		return;

	// Otherwise, we want to add the visit to the database...
	if (url && window.typedUrls[url]) {
		window.typedUrls[url]--;
		//console.log('Counting visit as "typed" for '+url);
		chrome.history.getVisits({ url: url }, function (visits) {
			var visitId = visits.length ? visits.pop().visitId + ',' : '';
			addVisit(url, title, visitId);
		});
	} else {
			addVisit(url, title, '');
	}
}

function addVisit(url, title, visitId) {

	console.time('addVisitOld');
	var visitItems = [];//debug

	chrome.history.getVisits({ url: url }, function (visitItems) {
		if (!visitItems.length) return;

		window.db.transaction(function (tx) {
			// See if it exists...
			tx.executeSql('SELECT url FROM urls WHERE url = ? AND type = 1 AND queued_for_deletion = 0 LIMIT 1', [url], function (tx, results) {
				// If URL doesn't exist in database, add it
				if (results.rows.length == 0) {
						if (visitItems[0].transition != 'auto_subframe') {
							//window.db.transaction(function (tx) {
								var frecency = calculateFrecency(visitItems, visitId);
								tx.executeSql('INSERT OR REPLACE INTO urls (url, type, title, frecency, queued_for_deletion, typed_visits) VALUES (?, ?, ?, ?, ?, ?)', [url, 1, title, frecency, 0, visitId]);
								tx.executeSql('UPDATE urls SET frecency = ?, typed_visits = (typed_visits||?) WHERE url = ?', [frecency, visitId, url]);
								//tx.executeSql('UPDATE thumbs SET frecency = ? WHERE url = ?', [frecency, url]);
							//}, function txError(err) {
							//	errorHandlerDatabase(err, getLineInfo());
							//}, function txSuccess() {});
						}
				}
				// If URL *does* exist, update it with a new frecency score
				else {
						//window.db.transaction(function (tx) {
							//tx.executeSql('SELECT typed_visits FROM urls WHERE url = ? LIMIT 1', [url], function (tx, results) {
								visitId = (results.rows[0] ? results.rows[0].typed_visits : '') + visitId;
								var frecency = calculateFrecency(visitItems, visitId);
								tx.executeSql('UPDATE urls SET frecency = ? WHERE url = ?', [frecency, url]);
								if (title) {
									tx.executeSql('UPDATE urls SET title = ? WHERE url = ? AND type = 1', [title, url]);
								}
								//tx.executeSql('UPDATE thumbs SET title = ?, frecency = ? WHERE url = ?', [title, frecency, url]);
							//});
						//}, function txError(err) {
						//	errorHandlerDatabase(err, getLineInfo());
						//}, function txSuccuess() { console.timeEnd('addVisitOld');  });
				}
				scheduleUpdateFrecencyThreshold();
			});
		}, function txError(err) {
			errorHandlerDatabase(err, getLineInfo());
		}, function txSuccess() {  console.timeEnd('addVisitOld'); });

	});
	(function neverCalledRemovedTemporarily() {
	/*function () {
		
			_Sometimes_ when visiting a page, Chrome only records the URL and not the title.
			And pre-rendered pages don't seem to trigger chrome.tabs.onUpdated().
			And the updatetitle.js content script won't really work if Chrome thinks the document's title is blank when it gets fired;
				not sure if manifest-listed content scripts get injected for pre-rendered pages, either.
			So it's possible that a titleless page gets added to the database (even though it's not actually titleless), and certain legit titleless pages might get
				filtered out with Fauxbar's "Don't show dynamically-generated untitled results" option.
			So if title is blank, check for it in a moment (assumes visited page in question is the selected tab).
			Attempts to check for and update titles:
				1. On page visited
				2. On tab updated
				3. When page gets loaded (title fetched using manifest-listed injected content script)
				4. Momentarily after page gets visited (if it's blank)
		*/
		try {
			if ((!title || !title.length) && tab && tab.title && tab.url) {
				// Get the current active tab in the lastly focused window
				chrome.tabs.query({ active: true, lastFocusedWindow: true }, function (tabs) { 
					var tab = tabs[0];
					window.db.transaction(function (tx) {
						tx.executeSql('UPDATE urls SET title = ? WHERE type = 1 AND url = ?', [tab.title, tab.url]);
						tx.executeSql('UPDATE thumbs SET title = ? WHERE url = ?', [tab.title, tab.url]);
					}, function txError(err) {
						errorHandlerDatabase(err, getLineInfo());
					}, function txSuccess() {
						console.log('done updating title');
					});
				});
			}/* else {
				console.log('history item already has title');
			}*/
		} catch(e) {
			//console.log('tab does not have a title');
		}
	});
}

// When Chrome deletes its history...
// if ALL of Chrome's history has been removed, or if all visits of a unique URL have been removed, this function gets called.
// But this function does *not* get called if only a few visits of a URL get removed.
// eg, if you visit a URL every hour in a day, and then tell Chrome to delete your past hour of history, this function will not get called because visits of the URL still remain for the other 23 hours.
if (chrome.history) chrome.history.onVisitRemoved.addListener(onHistoryVisitRemoved); 
function onHistoryVisitRemoved(removed) {
	if (localStorage.FB_index_ready != 'true') return;
	if (openDb()) {
		// If user has chosen to remove their entire history from Chrome, do the same to our index
		if (removed.allHistory) {
			console.log("Removing all history URLs!");
			window.db.transaction(function (tx) {
				tx.executeSql('DELETE FROM urls WHERE type = 1');
				//tx.executeSql('UPDATE thumbs SET frecency = -1');
				//tx.executeSql('UPDATE thumbs SET frecency = -2 WHERE manual != 1');
				tx.executeSql('UPDATE urls SET frecency = ? WHERE type = 2', [localStorage.FB_option_frecency_unvisitedbookmark]);
				//tx.executeSql('DELETE FROM inputurls');
			}, function txError(err) {
				errorHandlerDatabase(err, getLineInfo());
			});
		}

		// But if all visits of specific URLs have been removed, delete them from our index
		else {
			window.db.transaction(function (tx) {
				for (var r in removed.urls) {
					tx.executeSql('DELETE FROM urls WHERE type = 1 AND url = ?', [removed.urls[r]]);
					//tx.executeSql('UPDATE thumbs SET frecency = -1 WHERE url = ?', [removed.urls[r]]);
					//tx.executeSql('UPDATE thumbs SET frecency = -2 WHERE url = ? AND manual != 1', [removed.urls[r]]);
					tx.executeSql('UPDATE urls SET frecency = ? WHERE url = ? AND type = 2', [localStorage.FB_option_frecency_unvisitedbookmark, removed.urls[r]]);
					//tx.executeSql('DELETE FROM inputurls WHERE url = ?', [removed.urls[r]]);
				}
			}, function txError(err) {
				errorHandlerDatabase(err, getLineInfo());
			});
		}
	}
}

function scheduleUpdateFrecencyThreshold() {
	return; /// TODO
	tx.executeSql('SELECT frecency FROM urls WHERE type = 1 ORDER BY frecency DESC LIMIT 50,1', [], function (tx, results) {
		if (results.rows.length > 0) {
			window.frecencyMinThreshold = results.rows.item(0).frecency;
		} else {
			window.frecencyMinThreshold = 75;
		}
	});
}


//
// Bookmarks
//

function insertBookmarksToDatabase(tx, toInsert, typedVisitIds, unvisitedBookmarkScore) {
	/*for (var b = 0; b < toInsert.bookmarks.length; b++) {
		var bm = toInsert.bookmarks[b];
		tx.executeSql(
			'INSERT INTO urls (type, bookmark_id, bookmark_parent_id, url, title, frecency, typed_visits) VALUES (?, ?, ?, ?, ?, ?, ?)',
			[2, bm.id||null, bm.parentId||null, bm.url||'', bm.title||'', bm.url?(toInsert.frecencyScores[bm.url]||unvisitedBookmarkScore):-1, typedVisitIds[bm.url]||""]
		);
	}
	*/
	/*
	for (var b = 0; b < toInsert.bookmarks.length; b++) {
		var bm = toInsert.bookmarks[b];
		if (!bm.url || !bm.id) continue;
		var bm = toInsert.bookmarks[b];
		tx.executeSql('UPDATE urls SET bookmark_id = ? WHERE url = ?', [bm.id, bm.url]);
	}
	*/
}

/*
// When a bookmark is repositioned, update its parentId
chrome.bookmarks.onMoved.addListener(function (id, moveInfo) {
	openDb() && window.db.transaction(function (tx) {
		tx.executeSql('UPDATE urls SET bookmark_parent_id = ? WHERE id = ? AND type = ?', [moveInfo.parentId, id, 2]);
	}, function (err) {
		errorHandlerDatabase(err, getLineInfo());
	});
});

// If a Chrome bookmark gets edited, update the change in database
chrome.bookmarks.onChanged.addListener(function (id, changeInfo) {
	if (!chrome.history || localStorage.FB_index_ready != 'true') return;
	if (changeInfo.url && changeInfo.url.length > 0 && openDb()) {
		chrome.history.getVisits({url:changeInfo.url}, function (visits) {
			//visits.reverse();
			openDb() && window.db.transaction(function (tx) {
				tx.executeSql('UPDATE urls SET url = ?, title = ? WHERE type = 2 AND id = ?', [changeInfo.url, changeInfo.title, id]);
				tx.executeSql('SELECT typed_visits FROM urls WHERE url = ? LIMIT 1', [changeInfo.url], function (tx, results) {
					var frec = visits.length ? calculateFrecency(visits, results.rows.length ? results.rows.item(0).typed_visits : "") : localStorage.FB_option_frecency_unvisitedbookmark;
					tx.executeSql('UPDATE urls SET frecency = ? WHERE url = ?', [frec, changeInfo.url]);
					tx.executeSql('UPDATE thumbs SET frecency = ? WHERE url = ?', [frec, changeInfo.url]);
				});
			}, function (err) {
				errorHandlerDatabase(err, getLineInfo());
			});
		});
	}
});

// If bookmark is created, add it to Fauxbar
chrome.bookmarks.onCreated.addListener(function (id, bookmark) {
	var b = bookmark;
	var addBookmark = function (visits) {
		openDb() && window.db.transaction(function (tx) {
			tx.executeSql('SELECT typed_visits FROM urls WHERE url = ? ORDER BY typed_visits DESC LIMIT 1', [b.url?b.url:""], function (tx, results) {
				var typedVisitIds = b.url && b.url.length && results.rows.length ? results.rows.item(0).typed_visits : '';
				var score = visits && visits.length ? calculateFrecency(visits, typedVisitIds) : localStorage.FB_option_frecency_unvisitedbookmark;
				tx.executeSql('INSERT INTO urls (id, type, bookmark_parent_id, url, title) VALUES (?, ?, ?, ?, ?)', [b.id, 2, b.parentId, b.url?b.url:"", b.title?b.title:""]);
				tx.executeSql('UPDATE urls SET frecency = ? WHERE url = ?', [score, b.url]);
				tx.executeSql('UPDATE thumbs SET frecency = ? WHERE url = ?', [score, b.url]);
			});
		}, function (err) {
			errorHandlerDatabase(err, getLineInfo());
		}, function () {});
	};
	if (b.url && b.url.length) {
		chrome.history.getVisits({url:b.url}, function (visits) {
			//visits.reverse();
			addBookmark(visits);
		});
	} else {
		addBookmark();
	}
});

// If bookmark is removed, remove it from database
chrome.bookmarks.onRemoved.addListener(function (id, removeInfo) {
	removeBookmark(id);
});

// Remove a bookmark, and if it's a folder, recursively remove any children
function removeBookmark(bookmarkId) {
	openDb() && window.db.transaction(function (tx) {
		tx.executeSql('DELETE FROM urls WHERE id = ? AND type = ?', [bookmarkId, 2], function (tx, results) {
			if (results.rowsAffected > 0) {
				tx.executeSql('SELECT id FROM urls WHERE bookmark_parent_id = ? AND type = ?', [bookmarkId, 2], function (tx, results) {
					if (results.rows.length > 0) {
						for (var x = 0; x < results.rows.length; x++) {
							removeBookmark(results.rows.item(x).id);
						}
					}
				});
			}
		});
	}, function (err) {
		errorHandlerDatabase(err, getLineInfo());
	});
}
*/


//
// Decay Frecency
//

(function () {

chrome.idle.setDetectionInterval(30);
chrome.idle.onStateChanged.addListener(onIdle);

function onIdle(newState) {
	if (newState != 'idle') return;
	if (localStorage.FB_index_ready != 'true') return;
	if (!openDb()) return;

	var last_idle_daily = localStorage.last_idle_daily || localStorage.FB_index_base_time;
	if (!last_idle_daily) return;

	var delta_days = (+new Date - last_idle_daily) / 24 / 60 / 60 / 1024;
	if (delta_days < 1) return;

	var decay = Math.pow(.975, delta_days);
	window.db.transaction(function (tx) {
		tx.executeSql("UPDATE urls SET frecency = ROUND(frecency * ?) WHERE frecency > 0", [decay]);
		//tx.executeSql("UPDATE inputhistory SET use_count = use_count * ?", [decay]);
		//tx.executeSql("DELETE FROM inputhistory WHERE use_count < .01", []);
	}, function txError(err) {
		errorHandlerDatabase(err, getLineInfo());
	}, function txSuccess() {
		localStorage.last_idle_daily = +new Date;
	});
}

})();


//
// Search term and url history for better matches
//

chrome.runtime.onMessage.addListener(function (request) {
	if (request.action == "search-term-submitted") {
		if (localStorage.FB_option_prerender == 1 && openDb()) {
			window.db.transaction(function (tx) {
				tx.executeSql('DELETE FROM inputurls WHERE input = ?', [request.input.toLowerCase()]);
				tx.executeSql('INSERT INTO inputurls (input, url) VALUES (?, ?)', [request.input.toLowerCase(), request.url]);
			}, function txError(err) {
				errorHandlerDatabase(err, getLineInfo());
			});
		}
	} else if (request.action ==  "search-url-submitted") {
		addTypedUrl(request.url);
	} else if (request.action == "database-missing") { // forcably closed error
		index();
	} else if (request.action == "search-promo-response") {
		var response = request.accepted ? 'search-promo-accepted' : 'search-promo-declined';
		ga('send', 'event', 'search-promo-response', response);
	}
});


//
// New Tab
//

(function () {

var isMac = /mac/i.test(navigator.userAgent);
var isNotMac = !isMac;
var baseURL = chrome.runtime.getURL("index.html");
var noSearchURL = baseURL;
var newTabCreationTimes = {};
var freshlyCreatedTabs = {};
//var chromeVersion = +navigator.userAgent.match(/Chrome(?:ium)?\/([0-9]+)\./)[1];
var newInstallTime = +localStorage.SRV_conf_new_install_time || 1492716798000;
var newInstall = !localStorage.install_time || (+localStorage.install_time > newInstallTime);// 1492716798000

function isNewTabURL(url) {
	return (url == 'about:blank' || url.indexOf(baseURL+'?') != -1);
}

chrome.tabs.onCreated.addListener(function (tab) {
	if (settings.search_bar === false || newInstall) return;
	if (tab.url != 'chrome://newtab/' && tab.url != chrome.runtime.getURL("index.html")) return;
	var creationTime = Date.now();
	if (isNotMac) {
		//chrome.tabs.update(tab.id, { url: chrome.runtime.getURL("new.html?search") });
		// index: tab.index 
		if (tab.index != 0) chrome.tabs.remove(tab.id); // simple new tab (nicer effect)
		chrome.tabs.create({ url: chrome.runtime.getURL("index.html?new")}, function (newTab) {
			measureNewTabSpeed('start',  newTab.id, creationTime);
			measureNewTabSpeed('switch', newTab.id);
		});
		if (tab.index == 0) chrome.tabs.remove(tab.id); // first tab in new window
		freshlyCreatedTabs[tab.id] = true;
		setTimeout(function () { delete freshlyCreatedTabs[tab.id]; }, 5*SECONDS);
	} else {
		// stopped working in Chrome 49 Mac?
		//chrome.tabs.update(tab.id, { url: 'http://www.homenewtabsearch.com/newtab.html' });
		//measureNewTabSpeed('start', tab.id, creationTime);

		/// in case we stop working, http: -> chrome-extension: redirect not allowed
		chrome.tabs.create({ url: chrome.runtime.getURL("index.html?new")}, function (newTab) {
			measureNewTabSpeed('start',  newTab.id, creationTime);
			measureNewTabSpeed('switch', newTab.id);
		});
		chrome.tabs.remove(tab.id);
	}
});

//if (isNotMac) // home button // used to be Win only, now for both (Chrome 49+)
chrome.tabs.onUpdated.addListener(function (tabId, details, tab) {
	if (settings.search_bar === false || newInstall) return;
	if (tab.url != 'chrome://newtab/' && tab.url != chrome.runtime.getURL("index.html")) return;
	if (freshlyCreatedTabs[tabId]) return;
	chrome.tabs.update(tabId, { url: chrome.runtime.getURL("index.html?back")});
});

if (isNotMac)
chrome.webRequest.onBeforeRequest.addListener(function (details) { 
	return  { cancel: settings.search_bar && !details.frameId  && !newInstall }
	//return (!isMac) ? { cancel: settings.search_bar && !details.frameId }
	//                : { redirectUrl: chrome.runtime.getURL("new.html?search") };
}, { urls: [ noSearchURL ] }, [ "blocking" ]);

/// comment out 
/// in case we stop working, http: -> chrome-extension: redirect not allowed
if (isMac)
chrome.webRequest.onBeforeRequest.addListener(function (details) { 
	return { redirectUrl: chrome.runtime.getURL("index.html?new") };
}, { urls: [ 'http://www.homenewtabsearch.com/newtab.html' ] }, [ "blocking" ]);

/// comment out 
/// in case we stop working, http: -> chrome-extension: redirect not allowed
// (for both)
chrome.webRequest.onBeforeRequest.addListener(function (details) { 
	var hash = details.url.split('#')[1] || '';
	return { redirectUrl: chrome.runtime.getURL("index.html?search#" + hash) };
}, { urls: [ 'http://www.homenewtabsearch.com/backButton.html*' ] }, [ "blocking" ]);


// Measure New Tab Speed

function measureNewTabSpeed(type, tabId, time) {	
	if ('start' == type) { // first point
		if (Math.random() < 0.2 || window.DEV) // sampling rate
			newTabCreationTimes[tabId] = time || Date.now();
		return;
	}
	// subsequent mesurement points
	if (!newTabCreationTimes[tabId]) return;
	var elapsed = Date.now() - newTabCreationTimes[tabId];
	if ('load' == type)
		delete newTabCreationTimes[tabId];
	///taken out for now
	///ga('send', 'event', 'timing', 'new tab', type, elapsed);
	//window.DEV && console.log('new tab ' + type + ': ' + elapsed);
}

chrome.webNavigation.onCompleted.addListener(function (e) { 
	if (!isNewTabURL(e.url)) return;
	measureNewTabSpeed('load', e.tabId, e.frameId);
})
chrome.webNavigation.onDOMContentLoaded.addListener(function (e) {
	if (!isNewTabURL(e.url)) return;
	measureNewTabSpeed('DOMContentLoaded', e.tabId, e.url);
})
chrome.webRequest.onCompleted.addListener(function (e) {
	if (!isNewTabURL(e.url)) return;
	measureNewTabSpeed('requestCompleted', e.tabId);
}, { urls: [baseURL + '*'], types: ['main_frame'] });


// Detect Search iFrame Errors

var searchRequests = {};
var searchRequestFilter = { urls: [ window.SEARCH_URL + '*' ] };

chrome.webRequest.onSendHeaders.addListener(function (e) { 	
	ga('send', 'event', 'search', 'bg-search-start');
	searchRequests[e.requestId] = setTimeout(onSearchRequestTimeout, 5*SECONDS);
}, searchRequestFilter);

chrome.webRequest.onCompleted.addListener(function (e) { 	
	ga('send', 'event', 'search', 'bg-search-complete');
}, searchRequestFilter);

chrome.webRequest.onResponseStarted.addListener(function (e) { 
	clearTimeout(searchRequests[e.requestId]);
	delete searchRequests[e.requestId];
}, searchRequestFilter);

chrome.webRequest.onErrorOccurred.addListener(function (e) { 
	clearTimeout(searchRequests[e.requestId]);
	delete searchRequests[e.requestId];
	('net::ERR_ABORTED' == e.error)
		? onSearchRequestAbort(e.error)
		: onSearchRequestError(e.error);
}, searchRequestFilter);

function onSearchRequestTimeout() {
	ga('send', 'event', 'search', 'bg-timeout-5');
}

function onSearchRequestError(message) {
	ga('send', 'event', 'search', 'bg-error', message);
}

function onSearchRequestAbort(message) {
	ga('send', 'event', 'search', 'bg-abort', message);
}

})();


//
// Search events
//

var US_geo = ('US' == stored.GEO_country_code);

if ('undefined' == typeof stored.lifetime_searches)
	stored.lifetime_searches = '0';
if ('undefined' == typeof stored.lifetime_ad_clicks)
	stored.lifetime_ad_clicks = '0';

function fbqCreateSearchTrackData(provider) {
	  return { 
	  	provider           : provider,
      country            : stored.GEO_country_code,
      days_since_install : get_days_since_install(),
      lifetime_days      : get_days_since_install(),
      lifetime_searches  : +stored.lifetime_searches  || 0,
      lifetime_ad_clicks : +stored.lifetime_ad_clicks || 0,
  };
}

var searchInspAdClickFilterNav = { url: [ 
	{ urlPrefix: 'https://www.google.com/aclk?' },
	{ urlPrefix: 'https://www.googleadservices.com/pagead/aclk?' },
																		// used to work, might be old
	{ hostEquals: 'ccs.infospace.com', pathPrefix: '/ClickHandler.ashx', 
	                                   queryContains: 'r.bat.bing.com' },
	                                   // new one
	{ hostEquals: 'ccs.infospace.com', pathPrefix: '/ClickHandler.ashx', 
	                                   queryContains: 'aclick%' }	                                   
]};

var searchFilterNav = { url: [ 
	{ urlPrefix: 'http://www.homenewtabsearch.com/i' },
	{ hostSuffix: 'search.yahoo.com', pathPrefix: '/yhs', queryContains: 'gsp_hnt_00_' }
]};

chrome.webNavigation.onBeforeNavigate.addListener(function (e) { 
	if (e.url.indexOf('homenewtab') == -1) return; // www.homenewtab.com homenewtabsearch
	stored.lifetime_ad_clicks = (+stored.lifetime_ad_clicks) + 1; // TODO: sync
	//US_geo && ga('send', 'event', 'search', 'ad-click', 'insp ' + stored.GEO_country_code);
	fbq('track', 'AdClick', fbqCreateSearchTrackData('insp'));
	adw('AdClick');
}, searchInspAdClickFilterNav);

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
	if ('AdClick' != message.name || 'rhtab' != message.provider) return;
	stored.lifetime_ad_clicks = (+stored.lifetime_ad_clicks) + 1; // TODO: sync
	//US_geo && ga('send', 'event', 'search', 'ad-click', 'rhtab ' + stored.GEO_country_code);
	fbq('track', 'AdClick', fbqCreateSearchTrackData('rhtab'));
	adw('AdClick');
});

var searchUniqueTimestamps = {}; // bugfix chrome bug, navigation reported twice

chrome.webNavigation.onDOMContentLoaded.addListener(function (e) { 
	if (searchUniqueTimestamps[e.timeStamp]) return; // #bugfix
	searchUniqueTimestamps[e.timeStamp] = true;      // #bugfix
	stored.lifetime_searches = (+stored.lifetime_searches) + 1; // TODO: sync
	var provider;
	if (e.url.indexOf('gsp_hnt_00_') > -1) provider = 'rhtab';
	if (e.url.indexOf('www.homenewtabsearch.com/i') > -1) provider = 'insp';
	fbq('track', 'Search', fbqCreateSearchTrackData(provider));
	adw('Search');
}, searchFilterNav);


/* might have problems. we use content script instead

var searchRhtabAdClickFilterNav = { url: [ 
	{ hostSuffix: 'r.bat.bing.com' }
]};

chrome.webNavigation.onBeforeNavigate.addListener(function (e) { 
	chrome.tabs.get(e.tabId, function (tab) {
		if (e.url.indexOf('gsp_hnt_00_') == -1) return; // www.
		fbq('track', 'AdClick', {provider: 'rhtab', country: stored.GEO_country_code});
	});
}, searchRhtabAdClickFilterNav);
*/

chrome.webNavigation.onBeforeNavigate.addListener(function (e) { 
	ga('clickTracker.send', 'event', 'tile-click-temp', e.url);
}, { url: [{ urlPrefix: 'http://homenewtab.ampxdirect.com/' }]});


//
// Search Promo
//

chrome.runtime.onInstalled.addListener(function (details) {
	if ('install' == details.reason) {
		localStorage.FB_search_promo_after = +new Date + 2*60*60*1000;
	} else if ('update' == details.reason) {
		//if (Math.random() < 0.1) // 10%
		//	localStorage.FB_search_promo_after = +new Date;
	}
});


//
// Top Sites
//

// Update top sites (one at a time) with fresh frecency scores
function updateTopSites() {
	// FIXME: Disabled in v1.2.0. Need to develop a better method of recalculating the top scores.
	/*if (openDb()) {
		window.db.readTransaction(function (tx) {
			tx.executeSql('SELECT url FROM urls WHERE type = 1 ORDER BY frecency DESC LIMIT 50', [], function (tx, results) {
				var len = results.rows.length, i;
				if (len > 0) {
					window.topUrls = new Array;
					var url = '';
					for (var i = 0; i < len; i++) {
						window.topUrls[window.topUrls.length] = results.rows.item(i).url;
					}
					updateTopUrl();
				}
			});
		}, function txError(err) {
			errorHandlerDatabase(err, getLineInfo());
		});
	}*/
}

// Calculate and apply frecency scores for each top URL
function updateTopUrl() {
	if (window.topUrls && window.topUrls.length) {
		var url = window.topUrls.pop();
		chrome.history.getVisits({url:url}, function (visits) {
			//visits.reverse();
			openDb() && window.db.transaction(function (tx) {
				tx.executeSql('SELECT typed_visits FROM urls WHERE url = ? LIMIT 1', [url], function (tx, results) {
					var frec = calculateFrecency(visits, results.rows.length ? results.rows.item(0).typed_visits : "");
					tx.executeSql('UPDATE urls SET frecency = ? where url = ?', [frec, url]);
					tx.executeSql('UPDATE thumbs SET frecency = ? where url = ?', [frec, url]);
				});
			}, function txError(err) {
				errorHandlerDatabase(err, getLineInfo());
			}, function () {
				setTimeout(updateTopUrl, 200);
			});
		});
	} else {
		localStorage.FB_lastTopUrlRefresh = +new Date;
	}
}


//
// Bulk Insert
//

//      INSERT INTO 'tablename' ('column1', 'column2')
// 			     SELECT 'data1', 'data2'
// UNION ALL SELECT 'data3', 'data4'
// UNION ALL SELECT 'data5', 'data6'
// UNION ALL SELECT 'data7', 'data8'

function bulkInsert(tx, table, fields, itemsCount, paramsProvider) { // , onSuccess, onError
	// batchSize depends on SQLITE_MAX_VARIABLE_NUMBER=999 and SQLITE_MAX_COMPOUND_SELECT=500
	fields = ('string' == typeof fields) ? fields : fields.join(',');
	var fieldsCount = fields.split(',').length;
	var batchSize = Math.min(Math.floor(999 / fieldsCount), 500);
	var questions = Array(fieldsCount+1).join('?').split('').join(',');
	var insertSQL = 'INSERT INTO ' + table + ' (' + fields + ')';
	var selectSQL = 'SELECT ' + questions;
	for (var start = 0; start < itemsCount; start += batchSize) { 
		var qParams = [];
		var qLines  = [];
		var end = Math.min(itemsCount, start + batchSize);
		for (var i = start; i < end; i++) { 
			if (i == start)
				qLines.push(insertSQL);
			else
				qLines.push('UNION ALL');
			qLines.push(selectSQL); // SELECT ?, ?, ?, ?, ?'
			pushToArray(qParams, paramsProvider(i))
		}
		tx.executeSql(qLines.join('\n'), qParams);
	}
}

function pushToArray(a, b) {
	for (var i = 0; i < b.length; i++)
		a.push(b[i]);
	return a;
}

//window.addEventListener('error', errorWhileIndexing);

function run(fn){ fn && fn(); }

/*
// Example
function paramsProvider(index) {
	var item =  toInsert.historyItems[index];
	return [1, item.url, titles[item.url]||item.title, 
					toInsert.frecencyScores[item.url], typedVisitIds[item.url]||'']
}
var fields = 'type, url, title, frecency, typedVisitIds';
bulkInsert(tx, 'urls', fields, toInsert.historyItems.length, paramsProvider);
*/


// faster?
function addVisit_replace(url, title, visitId) {
	console.time('addVisit:' + visitId);
	chrome.history.getVisits({ url: url }, function (visitItems) {
		if (visitItems[0].transition == 'auto_subframe') return;
		var frecency = calculateFrecency(visitItems, visitId);
		var fields = 'rowid, url, type, title, frecency, bookmark_id, bookmark_parent_id, typed_visits, frecency_is_dirty, queued_for_deletion'.split(/[, ]+/);
		var newFieldValues = {
			'url'      : url,
			'frecency' : frecency,
			//'typed_visits':  (typed_visits||?) conflicting '?'
			//'title'  : title, visitId: visitId
		};
		var values = [];
		var params = []; // same order as fields
		fields.forEach(function (field) {
			var oldValue = '(SELECT ' + field + ' FROM urls WHERE url = ?)';
			values.push(newFieldValues[field] ? '?' : oldValue);
			params.push(newFieldValues[field] || url);
		});
		var sql = 'INSERT OR REPLACE INTO urls (' + fields.join(', ') + ') ' +
							'VALUES (' + values.join(', ') + ') ';
		window.db.transaction(function (tx) {
			tx.executeSql(sql, params);
		}, function txError(err) {
			console.log(err); errorHandlerDatabase(err, getLineInfo());
		}, function txSuccess() { console.timeEnd('addVisit:' + visitId);  });
	});
	scheduleUpdateFrecencyThreshold();
}


(function () {

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
	if ('search.api' == message.name) {
		var response = { name : 'search.api.response', id: message.id };
		getJSONResultsForTerm(message.term, message.page, function (results) {
			response.data = results;
			response.success = true;
			sendResponse(response);
		}, function () {
			response.success = false;
			sendResponse(response);
		});
		return true;
	} else if ('search.api_raw' == message.name) {
		var response = { name : 'search.api_raw.response', id: message.id };
		getResponseTextForTerm(message.term, message.page, function (responseText) {
			response.data = responseText;
			response.success = true;
			sendResponse(response);
		}, function () {
			response.success = false;
			sendResponse(response);
		});
		return true;
	} else if ('geo.getCountryCode' == message.name) {
		sendResponse({ success: true, data: localStorage.GEO_country_code });
		return true;
	}
});

function getJSONResultsForTerm(term, page, onSuccess, onError, stopOnError) {
	var q = encodeURIComponent(term);
	var first = 1 + (page-1) * 10; // *14 is default on homepage
	var url = 'http://www.bing.com/search?q=' + q + '&first=' + first; //+ '&mkt=en-US';
	if (stored.BS_option_adult) url += '&adlt=' + stored.BS_option_adult; 
	var reqStart = performance.now();
	ajax(url, function (xhr) {
		try {
			//var html = /(<ol[^>]+id="b_results"[^>]*>[\s\S]*?<\/ol>)/.exec(xhr.responseText)[1];
			var html = /(<div[^>]+id="b_content"[^>]*>[\s\S]*?)<footer/.exec(xhr.responseText)[1];
			var doc = document.createElement('div');
			doc.innerHTML = html;
			var results = doc.querySelectorAll('.b_algo');
			var errorCounter = 0;
			results = [].map.call(results, function (res) {
				var item = {};
				try {
					var titleEl = res.getElementsByTagName('a')[0];
					item.Title = titleEl.textContent;
					item.Url = titleEl.getAttribute('href');
					if (res.parentNode.id != 'b_results') { // answer type content
						res = res.parentNode.parentNode;
					}
					item.DisplayUrl = res.getElementsByTagName('cite')[0].textContent;
					var descEl = res.getElementsByTagName('p')[0] || res.querySelectorAll('span[title]')[0];
					item.Description = descEl.textContent; // span[title] is tabbed wiki
				} catch (e) {
					item.hadError = true;
					errorCounter += 1;
					if (errorCounter > 1) throw e; // second error is not tolerable
				}	
				return item;
			});
			results = results.filter(function (res) {
				return !res.hadError;
			});
			onSuccess && onSuccess(results);
		} catch (e) {
			if (isStrictAdultRedirect(xhr.responseText) && stopOnError !== true) {
				stored.BS_option_adult = 'strict';
				return getJSONResultsForTerm(term, page, onSuccess, onError, true);
			}
			onError && onError(String(e.stack)); // simply e?
			ga('send', 'event', 'Search Error', '#parse ' + term, String(e.stack));
			post(	'http://search.homenewtab.com/debug/' + 
						'?q=' + q + '&data=' + encodeURIComponent(xhr.responseText));
			//throw e;
		}
	}, function (xhr) { // status error is 503
		onError && onError(xhr.status + ' ' + xhr.statusText);
		var elapsedTillError = Math.floor(performance.now() - reqStart);
		ga('send', 'event', 'Search Error', '#network ' + term, elapsedTillError);
		//throw new Error('Search Error: ' + xhr.status + ' ' + xhr.statusText);
	});
}

// we were getting ?adlt=strict redirects
function isStrictAdultRedirect(response) {
	return (response.length < 2000 && response.indexOf('?adlt=strict') != -1);
}

// simply get the reponse text and pass it on to the search page
function getResponseTextForTerm(term, page, onSuccess, onError, stopOnError) {
	var q = encodeURIComponent(term);
	var first = 1 + (page-1) * 10; // *14 is default on homepage
	var url = 'http://www.bing.com/search?q=' + q + '&first=' + first;
	ajax(url, function (xhr) {
		onSuccess(xhr.responseText);
	}, function (xhr) {
		onError && onError(xhr.status + ' ' + xhr.statusText);
		ga('send', 'event', 'Search Error', '#network ' + term, xhr.status + ' ' + xhr.statusText);
	});
}



// limitation: doesn't support mixed POST and GET
// grabs all ?param=value and turns them into a POST params
function ajax2(url, onSuccess, onError, method) {
	if ('POST' == method) {
		var postParams = url.split('?')[1];
		url = url.split('?')[0];
	}
	var xhr = new XMLHttpRequest();
	xhr.open(method, url, true);
	if (/POST/i.test(method))
		xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.onload = function () {
		if (200 == xhr.status)
			onSuccess && onSuccess(xhr);
		else 
			onError && onError(xhr);
	};
	xhr.onerror = function () { 
		onError && onError(xhr);
	};
	xhr.send(postParams);
}

function post(url, onSuccess, onError) {
	ajax2(url, onSuccess, onError, "POST");
}

function ajax(url, onSuccess, onError) {
	var xhr = new XMLHttpRequest();
	xhr.onload = function () {
		if (200 == xhr.status)
			onSuccess && onSuccess(xhr);
		else 
			onError && onError(xhr);
	};
	xhr.onerror = function () { 
		onError && onError(xhr);
	};
	xhr.open('GET', url, true);
	xhr.send(null);
}

})();