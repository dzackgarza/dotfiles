(function(){

// https://col002.mail.live.com/mail/mail.fpp?cnmn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox.GetInboxData&ptid=0&a=SDRDHE28S3sO%2fUjx0hBlNA%3d%3d&au=12972223128560157161
// old col002 subdomain doesn't work
// dub122.mail.live.com works, but may stop working at some point
// http://jsbin.com/ehusiv/latest/edit
var url = "https://mail.live.com/default.aspx?rru=Inbox"; // ?fid=flinbox, older: ?rru=Inbox

var pollInterval = FETCH_INTERVAL || 1 * MINUTES;
var inboxOnly = false; 
var MAX_HOTMAIL = 20;

stored.hotmail || (stored.hotmail = "[]");

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
  isNotificationsEnabled() ? getMailFolderCount() : updateUnreadCount("");
}

function delayNextFetchByBackoff() {
  fetchDelay = Math.min(2 * fetchDelay, MAX_BACKOFF_DELAY);
  scheduleRequest();
  console.log("Hotmail: delaying next fetch (probably logged out)", fetchDelay);
}

function resetFetchDelayToNormal() {
  if (fetchDelay == pollInterval) return;
  fetchDelay = pollInterval;
  scheduleRequest();
  console.log("Hotmail: resuming normal fetching (probably logged in)", fetchDelay);
}

function updateUnreadCount(unread) {
  set_indicator("hotmail", unread);
}

function isNotificationsEnabled() {
  return is_notification_enabled('hotmail');
}

function getMailFolderCount() { 
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
  xhr.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
  //xhr.overrideMimeType('text/xml');
  xhr.onerror = function() {
    console.log("an error occurred");
  };
  xhr.onload = function() {
    var text = this.responseText;
    if (isLoggedOutResponse(xhr)) {
      return delayNextFetchByBackoff();
    }
    if (text && this.status == 200) {
      var unread = getCountFromText(text);
      updateUnreadCount(unread);
      getMailsFromText(text);
      resetFetchDelayToNormal();
    }
  };
  xhr.send(null);
}

function getCountFromText(aData){
  // Note: only works for inbox count for now
  var countMatch = /class="count">([^<]+)</g.exec(aData);
  var count = countMatch ? "" + parseInt(countMatch[1], 10) : "";
  return count;
}

var $ = function (sel, ctx) { return (ctx||document).querySelectorAll(sel); }

function getMailsFromText(aData) {
  var fnd = aData.match(/class="[^"]*InboxTableBody[^>]+>([\s\S]+?)<\/ul>/g);
  if (!fnd) return;

  var first_id, is_first = true;
  var since_id = stored.hotmail_since_id;
  var new_items = [];
  var notifications = [];

  fnd.forEach(function (inboxHtml) {

    var dummy = document.createElement('div');
    inboxHtml = inboxHtml.replace(/<img[^>]+>/g, ''); 
    dummy.innerHTML = "<ul " + inboxHtml;

    var rows = dummy.getElementsByTagName('li');

    if (!rows.length) return;

    
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var id = row.id;

      if (is_first) {
        is_first = false;
        first_id = id;
      }

      if (id == since_id) break;
      if (!row.classList.contains("mlUnrd")) continue; // skip read items

      var email_el = $('span[email]', row)[0];
      var name = email_el.textContent.trim();
      var email = email_el.getAttribute('email');
      var subject = $('a.t_estc.t_elnk', row)[0].textContent.trim(); //a.TextSemiBold
      var link = "https://mail.live.com/?fid=1&tid=" + id; // old: mid=

      new_items.push({
        email: email,
        name: name,
        //date: date,
        subject: subject
      });
      notifications.push(['hotmail', "<a href='"+link+"' target='_blank'>" + name + "</a> " + subject, ""]);
    }
  });

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  stored.hotmail_since_id = first_id;

  var old_items = [];
  try {
    old_items = JSON.parse(stored.hotmail);
  } catch (e) {
    logError(new Error("ERROR: stored hotmail has invalid JSON: "));
    console.log('ERROR: stored hotmail has invalid JSON: ' + stored.hotmail);
    //  throw new Error('ERROR: stored hotmail has invalid JSON: ' + stored.hotmail);
  }
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_HOTMAIL);

  setTimeout(function() {
    stored.hotmail = JSON.stringify(new_items);
  }, 1000);
}

function isLoggedOutResponse(xhr) {
  return xhr.responseURL.indexOf('login.live.com') != -1;
}

})();
