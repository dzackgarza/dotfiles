
var logger = {
	options: { elapsed: false },
	last: null,
	start: function () {
		console.log('Log session started');
		this.last = +new Date;
	},
	log: function (text) {
		var now = +new Date;
		var elapsed = numberWithCommas(now-this.last);
		var postfix = this.options.elapsed ? '(' + elapsed + ' ms)' : '';
		postfix && console.log(postfix);
		console.log(text); // + ' ' + postfix
		this.last = now;
	}
}

//
// Initialize/create the database
function openDb(force) {
	// Hopefully prevent issue #47 from happening... 
	// don't try to load the database if the page isn't ready
	if (!isDocumentReady()) {
		if (Math.random() < 0.01 && window.ga) {
			ga('send', 'event', 'debug', 'openDb called before domReady', (new Error()).stack);
		}	
		console.error('openDb called before domReady');
		return false;
	}
	if (!window.db) {
		var db = openDatabase('home', '1.0', 'Home - New Tab Page data', 100 * 1024 * 1024);
		window.db = db;
		/*
		db._transactionNative = db.transaction;
		db._readTransactionNative = db.readTransaction;
		function forcedErrorHandler(t) { 
			errorHandlerDatabase(t, getLineInfo()); 
		}
		db.transaction = function (tx, onError, onSuccess) {
			db._transactionNative(tx, function (tx) {
				forcedErrorHandler(tx);
				onError && onError(tx);
			}, onSuccess);
		}
		db.readTransaction = function (tx, onError, onSuccess) {
			db._readTransactionNative(tx, function (tx) {
				forcedErrorHandler(tx);
				onError && onError(tx);
			}, onSuccess);
		}
		*/
	}

	if (window.db) {
		return true;
	}
	else {
		console.error("Database error: Unable to create or open SQLite database.");
		return false;
	}
}

function isDocumentReady() {
	return /interactive|complete/i.test(document.readyState);
}


// errorHandler catches errors when SQL statements don't work.
// transaction contains the SQL error code and message
// lineInfo contains contains the line number and filename for where the error came from
function errorHandlerDatabase(transaction, lineInfo) {
	if (window.goingToUrl) return;
	if (transaction.code || transaction.message) {
		var code = '';

		if (transaction.code == 0) {
			sendReloadEvent('db-error', function () {
				location.reload();
			});
			return;
		}

		// we have to reindex (reload background page?)
		if (transaction.code == 5 && 
				transaction.message.indexOf('no such table') != -1) {
			localStorage.FB_index_base_time = '';
			localStorage.FB_index_ready = 'false';
			chrome.runtime.getBackgroundPage(function (bg) { bg.startIndexing(); })
		}

		switch (transaction.code) {
			case 0:
				code = "unknown";
			break;
			case 1:
				code = "database";
				break;
			case 2:
				code = "version";
				break;
			case 3:
				code = '"too large"';
				break;
			case 4:
				code = "quota";
				break;
			case 5:
				code = "syntax";
				break;
			case 6:
				code = "constraint";
				break;
			case 7:
				code = "timeout";
				break;
			default: // case 0:
				break;
		}
		var errorMsg = 'SQL '+code+' error: "'+transaction.message+'"';
		logError(errorMsg, lineInfo.file, lineInfo.line);
	} else {
		logError('Generic SQL error (no transaction)', lineInfo.file, lineInfo.line);
	}
}

function numberWithCommas(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
function repeat(v, n) { for (var a = [], i = 0; i < n; i++) a.push(v); return arr;	}
