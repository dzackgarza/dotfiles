(function () { 


window.addEventListener('DOMContentLoaded', openDb);
window.addEventListener('load', openDb);

// SELECT words.word, urls.url FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND urls_for_word.url_id = 50

// SELECT words.word, urls.url, urls.frecency FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND words.word LIKE 'lo%' ORDER BY frecency DESC LIMIT 100

// relies on window.currentSearchTerm being updated
window.getHistoryBookmarksSuggestions = getHistoryBookmarksSuggestions;
function getHistoryBookmarksSuggestions(term, callback) {

  //if (term != window.currentSearchTerm) return;
  //console.log(term);
  var tokens = tokenize(term);
  if (!tokens.length) {
    callback && callback([]);
    return;
  }

  var protocols = ['http', 'https'];
  var subdomains = ['', 'www'];
  var params = [];

  if (term.length > 3) {
    params.push('%' + term + '%');
  } else {
    protocols.forEach(function (protocol) {
      if (term.indexOf('ww') == 0) {
        params.push(protocol + '://' + term + '%');
      } else {
        subdomains.forEach(function (subdomain) {
          subdomain = subdomain ? subdomain + '.' : '';
          params.push(protocol + '://' + subdomain + term + '%');
        });
      }
    });
  }
  //console.log(params.join(', '));

  //var likes = repeat('words.word LIKE ?', tokens.length).join(' OR ');
  //params = tokens.map(function (t) { return t + '%' });

  var likes = repeat('word BETWEEN ? AND ? || X\'FFFF\'', tokens.length).join(' OR ');
  q = 'SELECT url_id, urls.url, urls.title, urls.frecency FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND (' + likes + ') AND frecency > 100 GROUP BY urls.rowid ORDER BY frecency DESC LIMIT 100';
  params = tokens.concat(tokens).sort();

  if (term == 'ww' || term.indexOf('www') == 0) {
    q = 'SELECT urls.rowid as url_id, urls.url, urls.title, urls.frecency FROM urls WHERE url LIKE ? ORDER BY frecency DESC LIMIT 100';
    params = ['%://' + term + '%'];
  } 

  // AND type = 1   -- SLOOW

  //var q = "SELECT  * FROM urls LIMIT 10";

  var pstart = +new Date;

  window.db.readTransaction(function (tx) {

      if (term != window.currentSearchTerm) return;

      tx.executeSql(q, params, function(tx, results) {

        if (term != window.currentSearchTerm) return;

        //console.log(+new Date - pstart);
        
        /*
        var equasion = /^[0-9+\-*\/.,%!() ]+$/.test(term);
        var containsDot = term.indexOf('.') != -1;
        var containsUrlLike = /[\/.\-_&]/.test(term);
        var containsPunctiation = /[?!,]/.test(term);
        */

        var start = +new Date;

        var rows = [];
        for (var i = 0; i < results.rows.length; i++) {
          var row = results.rows[i];

          var link = createLinkFromURL(row.url);
          var host = link.hostname;
          var path = link.pathname;
          var search = link.search;
          var wasHostBonusGiven = false;
          var tld = link.hostname.split('.').pop();

          // don't care zone
          if (link.protocol.indexOf('http') != 0) continue;

          // from here we care
          rows.push(row);

          //continue;
    
          // no bonus zone
          if (term == 'ww' || term == 'www') continue;

          // bonuses
          if (host.indexOf(term) == 0 || host.replace('www.', '').indexOf(term) == 0) {
            row.frecency += 300*1000; // 500*1000 top frecency dependent?
            wasHostBonusGiven = true;
          } 

          //var shortness = Math.max(100-row.url.length, 0);
          //row.frecency += ~~((shortness/100) * 200*1000);
          //row.frecency -= row.url.length * 1000;

          for (var t = 0; t < tokens.length; t++) {

            if (tokens[t] == tld) continue; // matching in TLD doesn't mean much

            var hostIndex = host.indexOf(tokens[t]);
            var pathIndex = path.indexOf(tokens[t]);
            var searchIndex = search.indexOf(tokens[t]);

            var titleIndex = row.title ? row.title.indexOf(tokens[t]) : -1;

            if (!wasHostBonusGiven) {
              if (hostIndex == 0) { // subdomain start with
                row.frecency += 30*1000 * tokens[t].length; // 100*1000
              } else if (hostIndex != -1) { // somewhere else in the domain
                row.frecency += 20*1000 * tokens[t].length; // 5*1000
              }
            }

            if (pathIndex != -1) {
              // min: matches at the end, max: matches at the beginning
              var pathLengthDelta = (path.length - tokens[t].length);
              var pathMultiplier = (pathLengthDelta - pathIndex) / pathLengthDelta;
              pathMultiplier *= pathMultiplier;
              row.frecency += Math.round(20*1000 * pathMultiplier * tokens[t].length);
            }

            if (titleIndex != -1) {
              // min: matches at the end, max: matches at the beginning
              var titleLengthDelta = (row.title.length - tokens[t].length);
              var titleMultiplier = (titleLengthDelta - titleIndex) / titleLengthDelta;
              titleMultiplier *= titleMultiplier;
              row.frecency += Math.round(20*1000 * titleMultiplier * tokens[t].length);
            }

            if (searchIndex != -1) {
              // min: matches at the end, max: matches at the beginning
              var searchLengthDelta = (search.length - tokens[t].length);
              var searchMultiplier = (searchLengthDelta - searchIndex) / searchLengthDelta;
              row.frecency += Math.round(1000 * searchMultiplier * tokens[t].length);
            }
          }
        }

        rows.sort(function (a, b) {
          return b.frecency - a.frecency;
        });

        // enough of your kind already, dear sir
        //var domainExactRe = new RegExp('^' + term + '(\.[^/]+)?\/'); // except TLD
        //if (!domainExactRe.test(protocolless(row.url))) {
          var rowsForDomain = {};
          var filtered = rows.filter(function (row) {
            var domain = createLinkFromURL(row.url).hostname;
            var matchingRows = rowsForDomain[domain];
            if (matchingRows)
              if (matchingRows.length >= 2)
                return false;
              else if (matchingRows[0] && 
                      protocolless(row.url) == protocolless(matchingRows[0]))
                return false;
              else
                matchingRows.push(row.url);
            else
              rowsForDomain[domain] = [row.url];
            return true;
          });
          if (filtered.length > 20)
            rows = filtered;
        //}


        //rows = rows.slice(0, 20);
        ///console.log('sort: ' + (+new Date - start));

        callback && callback(rows);


        // order 


        
        //[].forEach.call(results.rows, function (row) {
        //  console.log(row.url);
        //})
        //window.frecencyThreshold = results.rows.item(0).frecency;
      });

    }, 
    function (e) {
      errorHandlerDatabase(e, getLineInfo());
      // no such table | database closed
      if (e.code == 5 || e.code == 0) { 
        // ... let the backround script know
      } 
      //e&&console.log(e)
    },
    function () {}
  );
}

})();


//
// Common?
//

function repeat(value, n) {
  return Array(n+1).join('*').split('').map(function(){ return value });
}

function tokenize(term) {
  var tokens = term.split(/[^a-z0-9\u00E0-\u00FC]+/i);
  return tokens.filter(function (t) { return !!t; });
}

var linkDummy = document.createElement('a');
function createLinkFromURL(url) {
  linkDummy.href = url;
  return linkDummy;
}

function protocolless(url) {
  return url.replace(/^[^:]+:\/\//i, '');
}

function httpless(url) {
  return url.replace(/^http:\/\//i, '');
}

function dashlessending(url) {
  return url.replace(/\/$/i, '');
}

function topleveldomainless(url) {
  return url.replace(/\.[^.]+$/i, '');
}

function simplifyURL(url) { 
  url = url.replace(/^https?:\/\//, '')
  url = url.replace(/^www\./, '');
  //url = url.replace('.com/', '/'); // org too?
  return url;
}


// https://dxr.mozilla.org/mozilla-central/source/toolkit/components/places/nsPlacesAutoComplete.js#481


/*
var likes = repeat('word BETWEEN ? AND ? || X\'FFFF\'', tokens.length).join(' OR ');
q = 'SELECT words.word, urls.url, urls.frecency ' +
    'FROM words ' +
    'LEFT JOIN urls_for_word ON (words.rowid = urls_for_word.word_id) ' +
    'LEFT JOIN urls ON (urls.rowid = urls_for_word.url_id ) ' +
    'WHERE (' + likes + ') ' +
    'GROUP BY urls.rowid ' + 
    'ORDER BY frecency DESC ' + 
    'LIMIT 100 ';
    // AND frecency > 100
params = tokens.concat(tokens).sort();
*/

/*
// Strip prefixes from the URI that we don't care about for searching.
function stripPrefix(aURIString)
{
  let uri = aURIString;

  if (uri.indexOf("http://") == 0) {
    uri = uri.slice(7);
  }
  else if (uri.indexOf("https://") == 0) {
    uri = uri.slice(8);
  }
  else if (uri.indexOf("ftp://") == 0) {
    uri = uri.slice(6);
  }

  if (uri.indexOf("www.") == 0) {
    uri = uri.slice(4);
  }
  return uri;
}
*/

// BETWEEN 'h' AND 'h' || X'FFFF'

/*
function baseQuery(conditions = "") {
  let query = `SELECT h.url, h.title, f.url, ${kBookTagSQLFragment},
                      h.visit_count, h.typed, h.id, :query_type,
                      t.open_count
               FROM moz_places h
               LEFT JOIN moz_favicons f ON f.id = h.favicon_id
               LEFT JOIN moz_openpages_temp t ON t.url = h.url
               WHERE h.frecency <> 0
                 AND AUTOCOMPLETE_MATCH(:searchString, h.url,
                                        IFNULL(btitle, h.title), tags,
                                        h.visit_count, h.typed,
                                        bookmarked, t.open_count,
                                        :matchBehavior, :searchBehavior)
               ${conditions}
               ORDER BY h.frecency DESC, h.id DESC
               LIMIT :maxResults`;
  return query;
}

XPCOMUtils.defineLazyGetter(this, "_adaptiveQuery", function() {
  return this._db.createAsyncStatement(
   // do not warn (bug 487789) 
    `SELECT h.url, h.title, f.url, ${kBookTagSQLFragment},
            h.visit_count, h.typed, h.id, :query_type, 
            t.open_count
     FROM (
     SELECT ROUND(
         MAX(use_count) * (1 + (input = :search_string)), 1
       ) AS rank, place_id
       FROM moz_inputhistory
       WHERE input BETWEEN :search_string AND :search_string || X'FFFF'
       GROUP BY place_id
     ) AS i
     JOIN moz_places h ON h.id = i.place_id
     LEFT JOIN moz_favicons f ON f.id = h.favicon_id
     LEFT JOIN moz_openpages_temp t ON t.url = h.url
     WHERE AUTOCOMPLETE_MATCH(NULL, h.url,
                              IFNULL(btitle, h.title), tags,
                              h.visit_count, h.typed, bookmarked,
                              t.open_count,
                              :matchBehavior, :searchBehavior)
     ORDER BY rank DESC, h.frecency DESC`
  );
});
*/

/*
EXPLAIN QUERY PLAN
SELECT url_id, urls.url, urls.frecency FROM words, urls_for_word, urls WHERE words.rowid = urls_for_word.word_id AND urls.rowid = urls_for_word.url_id AND words.word LIKE 'fac%' GROUP BY urls.rowid ORDER BY frecency DESC LIMIT 100

EXPLAIN QUERY PLAN 
SELECT url_id, url, frecency FROM
(SELECT url_id, urls.url, urls.frecency 
FROM words, urls_for_word, urls 
WHERE words.rowid = urls_for_word.word_id 
AND urls.rowid = urls_for_word.url_id 
AND words.word BETWEEN 'fac' AND 'fac' || X'FFFF') m
ORDER BY frecency DESC 
LIMIT 100

EXPLAIN QUERY PLAN 
SELECT words.word, urls.url, urls.frecency FROM words 
LEFT JOIN urls_for_word ON (words.rowid = urls_for_word.word_id)
LEFT JOIN urls ON (urls.rowid = urls_for_word.url_id )
WHERE word BETWEEN 'fac' AND 'fac' || X'FFFF' 
GROUP BY urls.rowid
ORDER BY frecency DESC
LIMIT 100

EXPLAIN QUERY PLAN 
SELECT * FROM words 
WHERE word BETWEEN 'fac' AND 'fac' || X'FFFF' 
LIMIT 100

EXPLAIN QUERY PLAN 
SELECT * FROM words 
WHERE word >= 'fac' AND word < 'fad'  
LIMIT 100
*/

