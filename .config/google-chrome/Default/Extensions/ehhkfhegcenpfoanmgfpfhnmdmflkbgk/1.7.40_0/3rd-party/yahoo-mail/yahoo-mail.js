(function(){

// public url without crumb, for testing only
//https://query.yahooapis.com/v1/public/yql?q=select%20messageInfo.mid%2C%20messageInfo.from%2C%20messageInfo.subject%2C%20messageInfo.receivedDate%20from%20ymail.messages%20where%20messageInfo.flags.isRead%3D0%20limit%2020&format=json&callback=
var mailsUrl = "https://ucs.query.yahoo.com/v1/console/yql?&q=select%20folder.folderInfo%2C%20messageInfo.mid%2C%20messageInfo.from%2C%20messageInfo.subject%2C%20messageInfo.receivedDate%2C%20sourceFolderInfo%20from%20ymail.messages%20where%20messageInfo.flags.isRead%3D0%20limit%2020&format=json";
//var foldersUrl = "https://ucs.query.yahoo.com/v1/console/yql?&q=select%20folder%20from%20ymail.folders&format=json"; -- requires higher permission?
var foldersUrl = "https://ucs.query.yahoo.com/v1/console/yql?&q=select%20folder%20from%20ymail.messages&format=json";
var crumbUrl = "https://ucs.query.yahoo.com/v1/test/getcrumb";

stored.yahoo_mail || (stored.yahoo_mail = "[]");

var pollInterval = FETCH_INTERVAL || 5 * 60 * 1000;

pollInterval = Math.max(pollInterval, 5 * 60 * 1000);

var MAX_YAHOO_MAIL = 20;

var fetchTimer;
var fetchDelay = pollInterval;
var MAX_BACKOFF_DELAY = 1 * HOURS;

// init background fetching
check();

function scheduleRequest() {
  clearTimeout(fetchTimer);
  fetchTimer = window.setTimeout(check, fetchDelay);
}

function check() {
  scheduleRequest();
  if (!navigator.onLine) return;
  isNotificationsEnabled() ? getMails() : updateUnreadCount("");
}

function delayNextFetchByBackoff() {
  fetchDelay = Math.min(2 * fetchDelay, MAX_BACKOFF_DELAY);
  scheduleRequest();
  console.log("Yahoo Mail: delaying next fetch (probably logged out)", fetchDelay);
}

function resetFetchDelayToNormal() {
  if (fetchDelay == pollInterval) return;
  fetchDelay = pollInterval;
  scheduleRequest();
  console.log("Yahoo Mail: resuming normal fetching (probably logged in)", fetchDelay);
}

function updateUnreadCount(unread) {
  set_indicator("yahoo-mail", unread);
}

function isNotificationsEnabled() {
  return is_notification_enabled('yahoo-mail');
}

function processFolders(responseText, crumb) {
  var response;
  try {
    response = JSON.parse(responseText); 
  } catch (e) {
    logError(new Error("ERROR: Yahoo Mail processFolders JSON: " + e));
    return;
  }
  try {
    var results = response.query.results;
    if (!results) // could be simply that there's no unread to see?
      return;     //logError(new Error("ERROR: Yahoo Mail processFolders results null: "));

    var folders = results.result.folder; 
    /*
    var unread = folders.reduce(function(acc, folder) {
      if ('Inbox' == folder.folderInfo.fid || !folder.folderInfo.isSystem)
        return acc + folder.folderInfo.unread;
      else 
        return acc;
    });
    */
    updateUnreadCount(folders.unread);
  } catch (e) {
    return logError(new Error("ERROR: Yahoo Mail processFolders other error: "));
  }
}

/*
"messageInfo": {
    "from": {
     "name": "peter",
     "email": "peter@gmail.com"
    },
    "subject": "subject",
    "receivedDate": "1432815323",
    "mid": "<MESSAGE_ID>"
   }
},
*/

function processMails(response, crumb) {
  try {
    response = JSON.parse(response); 
  } catch (e) {
    logError(new Error('ERROR: Yahoo Mail processMails JSON: ' + e));
    return;
  }

  if (!response.query.results) return;

  //updateUnreadCount(response.query.count);
  var results = response.query.results.result;
  var notifications = [];
  var since_id = stored.yahoo_mail_since_id;

  // with one item it wouldn't be an array, go figure YQL
  if (results.length == null) results = [results];

  // going backwards intentionally for notifications to appear in order
  for (var i = 0; i < results.length; i++) {
    var m = results[i].messageInfo;

    if (m.mid == since_id) break;

    var link = "https://mrd.mail.yahoo.com/msg" + 
               "?mid=" + m.mid + 
               "&fid=Inbox"
               //"&.crumb=" + crumb + 
               //"&src=hp";
    notifications.push([
      "yahoo-mail", 
      "<a href='" + link + "' target='_blank'>" + m.from.name + "</a> " + m.subject, 
      ""
    ]);
  }

  for (var i = notifications.length; i--;) {
    create_notification.apply(null, notifications[i]);
  }

  if (results[0]) {
    stored.yahoo_mail_since_id = results[0].messageInfo.mid;
  }
}

var XHR_STATUS_UNAUTHORIZED = 401;

function getMails() { 
  get(crumbUrl, function (crumb) {
    // get mails -> for notifications
    get(mailsUrl + "&crumb=" + crumb, function (response) {
      processMails(response, crumb);
    }, function (xhr) {
      console.log("error retrievieng emails");
    });
    // get folders -> for unread count
    get(foldersUrl + "&crumb=" + crumb, function (response) {
      processFolders(response, crumb);
      resetFetchDelayToNormal();
    }, function (xhr) {
      console.log("error retrievieng folders");
      if (XHR_STATUS_UNAUTHORIZED == xhr.status)
        delayNextFetchByBackoff();
    });
  }, function (xhr) {
    console.log("error getting crumb");
  });
}

function get(url, onSuccess, onError) { 
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.onerror = function() {
    onError && onError(this);
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      onSuccess(this.responseText);
    } else {
      onError && onError(this);
    }
  };
  req.send(null);
}


})();