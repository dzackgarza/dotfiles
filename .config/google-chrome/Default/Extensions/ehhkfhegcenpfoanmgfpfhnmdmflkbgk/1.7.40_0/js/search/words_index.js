
// SELECT words.word, urls.url FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND urls_for_word.url_id = 50

// SELECT words.word, urls.url, urls.frecency FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND words.word LIKE 'lo%' ORDER BY frecency DESC LIMIT 100


//"SELECT type, url, title, frecency, typedVisitIds, tag FROM urls LIMIT 100"


var q = 'SELECT rowid, * FROM urls WHERE type = 1';

// "https://market_place.ad-techus.com/h2/set.do"
// .split(/[^a-z0-9]+/i) 
// .split(/\b[^a-z0-9-]+/i)  -> leaves alone - and _
// .split(/\b/i)
var allWordsCount = 0;
var allWords = [];
var allWordsMap = {};

var wordFrequencies = {};

var removedWords = {};

//window.addEventListener('DOMContentLoaded', indexWordsFromUrls);

function indexWordsFromUrls(onSucess, onError) {

	openDb();

	logger.options.elapsed = true;
	logger.start();

	var start = +new Date;

	//console.profile();

	var wordUrlPairs = []; // for bulk insert

	window.db.transaction(function (tx) {
	///(function (tx) { // readTransaction
			tx.executeSql(q, [], function (tx, results) {

				logger.log('Initialized transaction');

				initWordTables(tx);

				//console.profile();
				//console.log(results);
				var rows = results.rows;

				for (var i = 0; i < results.rows.length; i++) {
						var row = results.rows[i];
						if (!row) continue;
						if (row.frecency < 60) continue;		

						// url: /webhp remove
						// google: .hu/search?q=
						// google: .hu/url (?sa=) url= sig2=
						if (row.url.indexOf('/webhp') != -1) continue;
						if (row.url.indexOf('/search?q=') != -1) continue;

						// filter
						// TODO: only register words for URLs above a certain frecency (no one timers)
						// TODO: ignore hash after # 
						// TODO: ignore all numbers? (may leave short ones like 1972)
						// TODO: leave out http, https, www, com, co, 2 letter words
						// TODO: 2 numbers out of 3 chars
						// TODO: 2 character shorties from domain?

						var url = simplifyURL(decodeURLSafe(row.url));
						var words = tokenize(url).concat(tokenize(row.title));

						for (var w = 0; w < words.length; w++) {
							var word = words[w];
							if (isWithinLimits(word, 3, 25) && !isNumeric(word) && 
								 !isGibberish(word) && !isProbablyEncoded(word)) {
								word = word.toLowerCase();
								wordFrequencies[word] || (wordFrequencies[word] = 0);
								wordFrequencies[word] += 1;
								if (!allWordsMap[word]) {
									allWords.push(word);
									allWordsMap[word] = ++allWordsCount;
								}

								//tx.executeSql('INSERT INTO urls_for_word (word_id, url_id) VALUES (?, ?)', [allWordsMap[word], row.rowid]); 
								wordUrlPairs.push([allWordsMap[word], row.rowid]);
							}
							/*if (isWithinLimits(word, 3, 25) && !isNumeric(word) && isGibberish(word)) {
								removedWords[word] || (removedWords[word] = 0);
								removedWords[word] += 1;
							}*/
						}
				}

				bulkInsert(tx, 'urls_for_word', 'word_id, url_id', wordUrlPairs.length, function (i) {
					return wordUrlPairs[i]; 
				});


				// here simple insert is faster
				for (var w = 0; w < allWords.length; w++)
					tx.executeSql('INSERT INTO words (word) VALUES (?)', [allWords[w]]); 
				//bulkInsert(tx, 'words', 'word', allWords.length, function (w) { 
				//	return [allWords[w]]; 
				//});

				initWordTablesIndexes(tx);

				logger.log('Built up transaction');


				//console.profileEnd();

				/*
				console.log(allWords.length);
				console.log(allWords);
				console.log(allWordsMap);
				*/

				/*
				var removedWordsList = [];
				for (var word in removedWords) {
					removedWordsList.push([word, removedWords[word]]);
				}
				removedWordsList.sort(function (a, b) { return b[1] - a[1] });
				removedWordsList = removedWordsList.map(function (a) { return a[0] });
				console.log(removedWordsList);
				console.log(removedWordsList.length);
				*/

				/*
				var wordFrequenciesList = [];
				for (var word in wordFrequencies) {
					wordFrequenciesList.push([word, wordFrequencies[word]]);
				}
				wordFrequenciesList.sort(function (a, b) { return b[1] - a[1] });
				wordFrequenciesList = wordFrequenciesList.map(function (a) { return a[0] });
				console.log(wordFrequenciesList);
				*/
			});
		}, 
		function (e) {
			//e&&console.log('ERROR ' + e.code + ': ' + e.message);
			errorHandlerDatabase(t, getLineInfo());
			onError && onError();
		},
		function (e) {
			console.profileEnd();
			var elapsed = (+new Date - start);
			logger.log('Executed transaction');
			console.log('elapsed: ' + elapsed);
			console.log('SUCCESS');
			ga('send', 'event', 'search', 'index', 'words', allWords.length);
			ga('send', 'event', 'search', 'index', 'word_url_pairs', wordUrlPairs.length);
			ga('send', 'event', 'timing-search-index', 'words', '', elapsed);
			//ga('send', 'timing', 'search-index', 'words', elapsed);
			onSucess && onSucess();
		}
	);
}


// accented chars too
// hÁnyáß übül
// a-z0-9\u00E0-\u00FC (more upvotes)
// àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ
function tokenize(url) {
	return url.match(/[%a-z0-9\u00E0-\u00FC]+/gi) || []; // {3,20}
}

function decodeURLSafe(url) {
	try {
		return decodeURIComponent(url); // decodeURI
	} catch(e) { 
		return unescape(url); 
	}
}

function simplifyURL(url) { 
	url = url.replace(/^https?:\/\//, '')
	url = url.replace(/^www\./, '');
	url = url.replace('.com/', '/'); // org too?
	return url;
}

function isWithinLimits(str, min, max) {
	return str.length >= min && str.length <= max;
}
	
function isNumeric(str) {
	return /^\d+$/.test(str);
}
		
// gsdgRtd3DgY || gsd4xy3gr21
function isGibberish(str) {
	return (!/^[a-z]+$/i.test(str) &&
				 (hasSuspiciousUpperCases(str) || hasTooManyNumbers(str)));
}

function isProbablyEncoded(str) {
	return str.indexOf('%') != -1;
}

function hasSuspiciousUpperCases(str) {
	var tail = str.slice(1);
	return tail.toLowerCase() !== tail;
}

function hasTooManyNumbers(str) {
	return str.replace(/[^\d]/g, '').length > 2;
}

function isGibberish2() {}

function initWordTables(tx) {
	// INTEGER PRIMARY KEY
	tx.executeSql('DROP TABLE IF EXISTS words');
	tx.executeSql('DROP TABLE IF EXISTS urls_for_word');
	tx.executeSql('CREATE TABLE IF NOT EXISTS words (word TEXT)');
	tx.executeSql('CREATE TABLE IF NOT EXISTS urls_for_word (word_id INTEGER, url_id INTEGER)'); 

}

function initWordTablesIndexes(tx) {
	// words
	tx.executeSql('CREATE INDEX IF NOT EXISTS words__word ON words (word)'); // COLLATE NOCASE
	// urls_for_word
	//tx.executeSql('CREATE INDEX IF NOT EXISTS ufw_word_index ON urls_for_word (word_id)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls_for_word__url_id ON urls_for_word (url_id)');
	tx.executeSql('CREATE INDEX IF NOT EXISTS urls_for_word__compound ON urls_for_word (word_id, url_id)');
}


//////////////////////////////////////////

// for large arrays only
function pushToArray(a, b) {
	for (var i = 0; i < b.length; i++)
		a.push(b[i]);
	return a;
}


// only does one pass of decoding, 
// drops multiple decoded params
function tokenizeURL_long(url) {
	var tokens = [];
	var tokenizerRe = /[%a-z0-9\u00E0-\u00FC]+/gi;
	var firstPass = url.match(tokenizerRe);
	for (var i = 0; i < firstPass.length; i++) {
		var token = firstPass[i];
		if (token.indexOf('%') == -1) {
			tokens.push(token);
			continue;
		} 
		var decodedPart   = decodeURLPart(token);
		var decodedTokens = decodedPart.match(tokenizerRe);
		if (!decodedTokens) continue;
		for (var j = 0; j < decodedTokens.length; j++) {
			if (decodedTokens[j].indexOf('%') == -1) {
				tokens.push(decodedTokens[j]);
			} 
		}
	}
	return tokens;
}

function decodeURLPart(part) {
	try {
		return decodeURIComponent(part);
	} catch (e) { 
		return unescape(part);
	}
}

function decodeURL_long(url) {
	var parts = url.split(/:\/\/(.+)?/);
	var protocol = parts[0];
	parts = parts[1].split(/\?(.+)?/)
	url = protocol + '://' + decodeURLPart(parts[0]);
	var search = parts[1];
	if (search) {
		parts = search.split('&');
		for (var i = 0; i < parts.length; i++) {
			parts[i] = decodeURLPart(parts[i]);
		}
		url += '?' + parts.join('&');
	}
	return url;
}
