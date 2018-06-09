(function(){

// https://col002.mail.live.com/mail/mail.fpp?cnmn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox.GetInboxData&ptid=0&a=SDRDHE28S3sO%2fUjx0hBlNA%3d%3d&au=12972223128560157161
// http://jsbin.com/ehusiv/latest/edit
var url = "https://dub122.mail.live.com/default.aspx?rru=Inbox"; // col002

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds
var inboxOnly = false; 
var MAX_HOTMAIL = 20;

stored.hotmail || (stored.hotmail = "[]");


function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function updateUnreadCount(unread) {
  set_indicator("hotmail", unread);
}

function check() {
  getMailFolderCount();
  scheduleRequest();
}

function getMailFolderCount() { 
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
  req.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
  //req.overrideMimeType('text/xml');
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    var text = this.responseText;
    if (text && this.status == 200) {
      var unread = getCountFromText(text);
      updateUnreadCount(unread);
      getMailsFromText(text);
    }
  };
  req.send(null);
}

// from X-notifier
// https://chrome.google.com/webstore/detail/apebebenniibdlpbookhgelaghfnaonp
function getCountFromText(aData){
  var fnd=aData.match(/<ul.+?class="List FolderList.+?>([\s\S]+?)<\/ul>/g);
  var count = 0;
  if (fnd){
    fnd=fnd.toString();
    var re=/<li.+?\s+id="(.+?([^-]+?))"\s+nm="(.+?)"\s+count="(\d+)"/g;
    var o;
    while ((o = re.exec(fnd)) != null){
      if(o[2]=="000000000005"||o[2]=="000000000004"
        ||o[2]=="000000000003"||o[2]=="000000000002")continue;
      var n=parseInt(o[4]);
      if (inboxOnly) {
        if (o[2]=="000000000001") {
          count = n;
        }
      }
      else  {
        count += n;
      }
    }
  }
  return count;
}


function getMailsFromText(aData) {
  var fnd = aData.match(/<table\s+class="Narrow\s+InboxTable"[^>]+>([\s\S]+?)<\/table>/g);
  if (!fnd) return;

  var since_id = stored.hotmail_since_id;
  var new_items = [];
  var notifications = [];

  fnd=fnd.toString();
  var re=/<tr\s+class="ia_hc[^"]+"\s+id="(.+?([^-]+?))"[^>]+>([\s\S]+?)<\/tr>/g;
  var o, first_id, is_first = true;
  while ((o = re.exec(fnd)) != null){
    o = o[0];
    var id = o.match(/id="([^"]+)"/)[1];

    if (is_first) {
      is_first = false;
      first_id = id;
    }

    if (id == since_id) break;
    if (o.indexOf("mlUnrd") == -1) continue; // skip read items

    var match = o.match(/<span\s+email="([\s\S]+?)">([\s\S]+?)<\/span>/);
    var email = match[1];
    var name = match[2];
    var date = +new Date(o.match(/mdt="([^"]+)"/)[1]); // o.match(/<div\s+class=DtB><a>([\s\S]+?)<\/a>/)[1]; //
    var subject = o.match(/<a\s+href=#\s+class="TextSemiBold">([\s\S]+?)<\/a>/)[1];
    var link = "https://col002.mail.live.com/default.aspx?fid=1&mid=" + id;

    new_items.push({
      email: email,
      name: name,
      date: date,
      subject: subject
    });
    notifications.push(['hotmail', "<a href='"+link+"' target='_blank'>" + name + "</a> " + subject, ""]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  stored.hotmail_since_id = first_id;

  var old_items = JSON.parse(stored.hotmail);
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_HOTMAIL);

  setTimeout(function() {
    stored.hotmail = JSON.stringify(new_items);
  }, 1000);
  
}

//window.addEventListener("DOMContentLoaded", check, false);
check();

})();