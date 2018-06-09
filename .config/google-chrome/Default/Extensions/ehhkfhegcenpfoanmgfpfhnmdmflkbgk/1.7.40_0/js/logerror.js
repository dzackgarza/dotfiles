
/////////////////////////////////////////////////////////////////////////
//window.ga || (window.ga = function() {});
/*var gaException = window.ga || (function (send, exception, data) {
	if (send == 'send' && exception == 'exception') {
		chrome.runtime.sendMessage({ name: 'new-tab-exception', data: data });
	}
	// 'exDescription': msg + ' | ' + file + ':' + line,
});*/
var gaException = function (message, file, line, stack) {
	var extra = (file + ':' + line + '\n' + (stack||'')).trim();
	if (window.ga) // background page
		ga('send', 'event', 'JS Error', message, extra);
	else // extension pages
		chrome.runtime.sendMessage({ 
			name    : 'new-tab-exception', 
			message : message,
			file    : file,
			line    : line,
			stack   : stack
		});
}

// Do a bit of stack tracing and return filename, line # and column #
function getLineInfo(error) {
	error = error || new Error();
	var lines = error.stack.split("\n");
	//console.log(lines[0] + ': ' + lines.slice(2).join('\n').trim());
	var line = lines[lines.length-1];
	var file = line.split(chrome.extension.getURL(""), 2);
	file = file[1];
	var bits = file.split(":");
	return {file:bits[0], line:bits[1], col:bits[2]};
}

// Add an error to the database, to keep track of them
// ('message', 'file', line)
// ({Error})
// ({ErrorEvent}|'message', file, line, col, {Error})
function logError(arg0, file, line, col, error) {

 var msg;

	// called by window.onerror
	if (arg0 instanceof ErrorEvent) {
		msg   = arg0.message;
		error = arg0.error || error;
		file  = arg0.filename;
		line  = arg0.lineno;
	}
	// called by us with new Error
	else if (arg0 instanceof Error) {
		msg   = arg0.message;
		error = arg0;
		// why not using Error.fileName, Error.lineNumber?
		var lineInfo = getLineInfo(error);
		file = file || lineInfo.file; // second arg can be used for custom GA event label
		line = lineInfo.line;
	}
	// else arg0 was a string
	else {
		msg = arg0;
	}

	var url = document.URL;
	var base = chrome.extension.getURL("");
	if (file.substring(0, base.length) == base)
		file = file.substring(base.length);
	if (url.substring(0, base.length) == base)
		url = url.substring(base.length);

	// otherwise somebody else called us (like database error handler)
	if (!(arg0 instanceof ErrorEvent)) {
		console.error(msg +'\n'+file+', line '+line);
		//console.log(msg+'\n'+file+', line '+line);
	}

	var stack = error ? error.stack : '';

	gaException(msg, file, line, stack);

	var version = window.APP_VERSION; // localStorage.FB_db_current_version;
	if (!localStorage.unreadErrors) {
		localStorage.unreadErrors = 0;
	}
	localStorage.unreadErrors++;
	localStorage.latestError = JSON.stringify({version:version, file:file, line:line, msg:msg, date:+new Date, count:1, url:url});

	// I think this happens *after* a runtime.reload, but only *sometimes*
	// Basically we "try again" with a simple page reload (hopefully without errors)
	if (file == 'background.html' && line == 1 && /Unexpected (end|token)/i.test(msg)) {
		sendReloadEvent('exception', function () {
			location.reload();
		});
	}

	// currently tied to FB database
	if (localStorage.FB_index_ready != 'true') return; 
	if (!openDb(true)) return;

	window.db.transaction(function (tx) {
		var today = +new Date;
		tx.executeSql('SELECT * FROM errors ORDER BY id DESC LIMIT 1', [], function(tx, results){
			var action = 'insert';
			if (results.rows.length == 1) {
				var item = results.rows.item(0);
				if (item.version == version && item.file == file && item.line == line && item.message == msg && item.date == today && item.url == url) {
					action = 'update';
				}
			}
			if (action == 'insert') {
				tx.executeSql('INSERT INTO errors (version, file, line, message, date, count, url) VALUES (?, ?, ?, ?, ?, ?, ?)', [version, file, line, msg, today, 1, url]);
			} else {
				tx.executeSql('UPDATE errors SET count = count+1 WHERE id = ?', [item.id]);
			}
		});
	}, function (t) {

		// Prevent recursion if the database operation fails
		window.removeEventListener('error', logError);
		setTimeout(function(){
			window.addEventListener('error', logError);
		}, 1000);
		console.log('Such Meta, error handler encountered an error:\n"'+t.message+'"');
	}, function () {
		delete localStorage.latestError;
	});
}
window.addEventListener('error', logError);

window.addEventListener('DOMContentLoaded', function () {
	if (localStorage.latestError && localStorage.latestError.length) {

		var e;
		try {
		  e = JSON.parse(localStorage.latestError);
		} catch (e) {
		  console.log('ERROR: stored latestError has invalid JSON: ' + stored.hotmail);
		  /// TODO: log error, kinda meta :)
		  return;
		}

		if (openDb()) {
			window.db.transaction(function(tx){
				tx.executeSql('CREATE TABLE IF NOT EXISTS errors (id INTEGER PRIMARY KEY, date NUMERIC, version TEXT, url TEXT, file TEXT, line NUMERIC, message TEXT, count NUMERIC)');
				tx.executeSql('INSERT INTO errors (date, version, url, file, line, message, count) VALUES (?, ?, ?, ?, ?, ?, ?)', [e.date, e.version, e.url, e.file, e.line, e.msg, e.count]);
			}, function(t){
				errorHandlerDatabase(t, getLineInfo());
			}, function () {
				delete localStorage.latestError;
			});
		}
	}
})

function sendReloadEvent(reason, callback) {
	ga('send', 'event', {
	  category    : reason,
	  action      : 'reload',
	  label       : 'reload',
	  hitCallback : createHitCallback(callback)
	});
}

function createHitCallback(fn) {
	var done = false;
	function callbackIfNotDone() { !done && fn && fn(); done = true; }
	function callbackNextTick()  { setTimeout(callbackIfNotDone, 2000); } // 1
	setTimeout(callbackIfNotDone, 5000); // 2000
	return callbackNextTick;
}