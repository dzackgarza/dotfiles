// Copyright 2009 Google Inc. All Rights Reserved.

(function() {

stored.greader_timestampUsec || (stored.greader_timestampUsec = '0');
var feed_url = "http://www.google.com/reader/api/0/stream/contents/?n=20&refresh=true";
var feed_id;

//
// closure.js
//

var e=this;function f(b,c,a){b=b.split(".");a=a||e;!(b[0]in a)&&a.execScript&&a.execScript("var "+b[0]);for(var d;b.length&&(d=b.shift());)if(!b.length&&c!==undefined)a[d]=c;else a=a[d]?a[d]:(a[d]={})}Math.floor(Math.random()*2147483648).toString(36);f("goog.bind",function(b,c){var a=c||e;if(arguments.length>2){var d=Array.prototype.slice.call(arguments,2);return function(){var g=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(g,d);return b.apply(a,g)}}else return function(){return b.apply(a,arguments)}},undefined);f("goog.inherits",function(b,c){function a(){}a.prototype=c.prototype;b.a=c.prototype;b.prototype=new a},undefined);

//
// util.js
//

/**
 * A wrapper method for document.getElementById.
 */
function $(id) {
  return document.getElementById(id);
}

/**
 * Regular expression to check whether or not a tab is opened to Reader.
 */
var READER_URL_RE_ = /https?\:\/\/www.google.com\/reader\/view\//;


/**
 * Reader homepage URL
 */
var READER_URL = 'https://www.google.com/reader/view/';

/**
 * Regular expression to extract the unread count out of a Reader tab title.
 */
var TITLE_UNREAD_COUNT_RE = /\s+\((\d+)(\+?)\)$/;

/**
 * Time in milliseconds that we wait for an unread count request to complete.
 */
var REQUEST_TIMEOUT_MS_ = 30 * 1000; // 30 seconds

/**
 * Unread count request URL (expected to return JSON)
 */
var REQUEST_URL_ =
    'http://www.google.com/reader/api/0/unread-count' +
    '?output=json&client=chromenotifier&refresh=true';

/**
 * Regular expression to match the user's reading list.
 */
var READING_LIST_RE_ =
    new RegExp('user/[\\d]+/state/com\\.google/reading-list');


//
// main.js
//

var REFRESH_INTERVAL_KEY = "REFRESH_INTERVAL_KEY";

function getRefreshInterval() {
  return FETCH_INTERVAL || parseInt(localStorage[REFRESH_INTERVAL_KEY] || '300000', 10);
}

var requestTimeout;
var lastCountText = 'start';

function updateUnreadCount(count, isMax) {
  var countText = '';
  if (count > 0) {
    countText = count + '';
    if (isMax) {
      countText += '+';
    }
  }

  if (countText == lastCountText) {
    return;
  }

  lastCountText = countText;

  set_indicator("greader", countText);
}


function startRequest(opt_noSchedule) {

  if (requestTimeout) {
    window.clearTimeout(requestTimeout);
  }
  requestTimeout = null;

  getUnreadCount(
    function(count, isMax) {
      updateUnreadCount(count, isMax);
      if (!opt_noSchedule) {
        scheduleRequest();
      }
    },
    function(opt_isSignedOut) {
      if (!opt_noSchedule) {
        scheduleRequest(opt_isSignedOut);
      }
    }
  );
}

function getUnreadCount(onSuccess, onError) {
  var xhr = new XMLHttpRequest();
  var abortTimerId = window.setTimeout(function() {
    xhr.abort();
    onError();
  }, REQUEST_TIMEOUT_MS_);

  function handleSuccess(jsonText) {
    window.clearTimeout(abortTimerId);
    var json;

    try {
      json = JSON.parse(jsonText); //  eval('(' + jsonText + ')');
    } catch (e) {
      console.log('JSON parse exception: ' + e);
      handleError();
      return;
    }

    /// newestItemTimestampUsec

    // Find the reading list unread count
    for (var i = 0, stream; stream = json.unreadcounts[i]; i++) {
      if (READING_LIST_RE_.test(stream.id)) {
        onSuccess(stream.count, stream.count >= json.max);

        // fresh news should be fetched to the notification center
        if (stream.newestItemTimestampUsec > stored.greader_timestampUsec) {
          if (!feed_id) {
            feed_id = stream.id.replace('reading-list', 'read');
            feed_url += "&xt=" + encodeURIComponent(feed_id); 
          }
          getGReaderNews(); // timestamp is updated when the feed is loaded
        }
        
        return;
      }
    }

    // Fallthrough: we couldn't find the reading list unread count, assume it's
    // 0 (items with a 0 unread count are not output)
    onSuccess(0, false);
  }

  function handleError(opt_isSignedOut) {
    window.clearTimeout(abortTimerId);
    onError(opt_isSignedOut);
  }

  try {
    ///console.log('request..');
    xhr.onreadystatechange = function() {
      ///console.log('readystate: ' + xhr.readyState);
      if (xhr.readyState == 4) {
        if (xhr.status >= 400) {
          console.log(
              'Error response code: ' + xhr.status + '/' + xhr.statusText);
          handleError(xhr.status == 401);
        } else if (xhr.responseText) {
          ///console.log('responseText: ' + xhr.responseText.substring(0, 200) +
          ///            '...');
          handleSuccess(xhr.responseText);
        } else {
          console.log('No responseText!');
          handleError();
        }
      }
    }

    xhr.onerror = function(error) {
      console.log('error');
      console.log(error);
      handleError();
    }

    xhr.open('GET', REQUEST_URL_, true);
    xhr.send(null);
  } catch (e) {
    console.log('XHR exception: ' + e);
    handleError();
  }
}

function scheduleRequest(opt_isSignedOut) {
  if (requestTimeout) {
    window.clearInterval(requestTimeout);
  }

  var interval = getRefreshInterval();
  // Refresh more often while the user is signed out, so that we can pick up
  // the unread count faster
  //if (opt_isSignedOut) {
  //  interval *= .1;
  //}
  ///console.log('scheduling request in ' + interval + 'ms');
  requestTimeout = window.setTimeout(startRequest, interval);
}

function getReaderTab(callback) {
  chrome.tabs.getAllInWindow(undefined, function(tabs) {
    for (var i = 0, tab; tab = tabs[i]; i++) {
      if (tab.url && READER_URL_RE_.test(tab.url)) {
        callback(tab);
        return;
      }
    }

    callback(null);
  });
}

/////////////////////////////////////////////////////////////////////////////////////

(function() {

stored.greader || (stored.greader = "[]");

var MAX_GREADER = 20;
//var feed_id;


//var url = "http://www.google.com/reader/api/0/stream/contents/?n=20&refresh=true";

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function check() {
  getGReaderNews();
  scheduleRequest();
}

function processNews(items) {

  if (!items.length) return;

  var since_id = stored.greader_since_id;
  var new_items = [];
  var notifications = [];

  for (var i = 0; i < items.length; i++) {
    if (items[i].id == since_id) break;
    var item = items[i];
    new_items.push({
      id: item.id,
      title: item.title,
      published: item.published,
      link: item.alternate[0].href,
      //content: item.content ? item.content.content : (items.summary ? items.summary.content : ""),
      origin: item.origin.title
    });
    notifications.push(['news', "<a href='"+item.alternate[0].href+"' target='_blank'>" + item.origin.title + "</a>", item.title]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  stored.greader_since_id = items[0].id;
  stored.greader_timestampUsec = items[0].timestampUsec;

  var old_items = JSON.parse(stored.greader);
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_GREADER);

  setTimeout(function() {
    stored.greader = JSON.stringify(new_items);
  }, 1000);


}

function getGReaderNews() { 
  var req = new XMLHttpRequest();
  req.open("GET", feed_url, true);
  //req.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
  //req.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      var json = JSON.parse(this.responseText);
      if (!feed_id) {
        feed_id = json.id.replace('reading-list', 'read');
        feed_url += "&xt=" + encodeURIComponent(feed_id); 
      }
      processNews(json.items);
    } 
  };
  req.send(null);
}

window.getGReaderNews = getGReaderNews;

check();

})();


//
// greader.js
//

// Kick off auto-refreshing
startRequest();

// Also monitor tabs for a Reader tab, and use its unread count if
// possible (can't use chrome.tabs.onUpdated since it doesn't fire for
// title changes)
window.setInterval(function() {
  getReaderTab(function(tab) {
    if (tab && tab.title) {
      var match = TITLE_UNREAD_COUNT_RE.exec(tab.title);
      if (match && match[1]) {
        updateUnreadCount(parseInt(match[1], 10), match[2] == '+');
      } else {
        // For handling the case if the count in reader tab goes to 0
        // which will remove the count from the extension.
        updateUnreadCount(null, false);
      }
      scheduleRequest();
    }
  });
}, 2000);


})();