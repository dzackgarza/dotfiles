(function(){

var url = "http://us.mg1.mail.yahoo.com/ws/mail/v1/formrpc?m=ListFolders&appid=YahooMailRC";
///url = "http://us.mg1.mail.yahoo.com/ws/mail/v1/formrpc?m=ListFolders&appid=YahooMailRC&wssid=sdYPN0LDuwO";

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function updateUnreadCount(unread) {
  set_indicator("yahoo-mail", unread);
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
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    var xml = this.responseXML;
    if (this.status == 200) {
      var unread = 0;
      var folders = xml.getElementsByTagName("folder");
      for (var i = folders.length; i--;) {
        var f = folders[i];
        if (f.getAttribute("isSystem") === "false" || 
            f.firstChild.getAttribute("name") === "Inbox") {
          unread += parseInt(f.getAttribute("unread"), 10);
        }
      }
      updateUnreadCount(unread);
    } 
    else if (this.status == 500) {
      var code = xml.getElementsByTagName("code")[0].textContent;
      if (code == "Client.ClientRedirect.SessionIdReissue") {
        url = xml.getElementsByTagName("url")[0].textContent;
        getMailFolderCount();
      } 
      else if (code == "Client.ExpiredCredentials") {
        console.log("Please log in to Yahoo Mail!");
      }
    }
  };
  req.send(null);
}

//window.addEventListener("DOMContentLoaded", check, false);
check();

})();






(function(){

stored.yahoo_mail || (stored.yahoo_mail = "[]");

var o = {"reqs":[{"handler":"cfg.maple_dali.handler.refresh","data":{"maple":{"module":"p_30345624_a2a","ba":{"_txnid":0,"_mode":"json","_id":"p_30345624_a2a","_container":0,"_action":"show","_subAction":"mail_preview"}}},"txId":1}],"props":{"dali":{"crumb":"wFwaBE6PmUz","yuid":"","loggedIn":"1","mLogin":1}}}

var url = "http://uk.yahoo.com/js?&__r=1346520219993&post=" + encodeURIComponent(JSON.stringify(o));

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

var MAX_YAHOO_MAIL = 20;


function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function check() {
  getMails();
  scheduleRequest();
}

function getData(item, key) {
  return item.getElementsByClassName(key)[0].textContent;
}

var el = document.createElement('div');

function processMails(html) {

  el.innerHTML = html;
  var items = el.getElementsByClassName('email');

  if (!items.length) return;

  var since_id = stored.yahoo_mail_since_id;
  var new_items = [];
  var notifications = [];

  //var link = "http://us.mg40.mail.yahoo.com/neo/launch";

  for (var i = 0; i < items.length; i++) {

    var item = items[i];
    var status_el = item.getElementsByClassName('status')[0];
    var link_el = item.getElementsByTagName("a")[0];
    var link = link_el.href;
    var id = /\?mid=[^&]+/.exec(link_el.rel)[0].replace('?mid=', '');
    var spans = item.getElementsByClassName('subject')[0].getElementsByTagName('span');
    var from = spans[0].textContent.replace('From: ', '');
    var subject = spans[1].textContent.replace('Subject: ', '');
    var status = (/unread/i.test(status_el.textContent) || /unread/i.test(status_el.className)) 
                 ? 'unread' : 'read';

    if (id == since_id) break;
    if (status != 'unread') continue;  // skip read items

    new_items.push({
      id: id,
      link: link,
      subject: subject,
      from: from
    });
    notifications.push(['yahoo-mail', "<a href='"+link+"' target='_blank'>" + from + "</a> " + subject, ""]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  var link_el = items[0].getElementsByTagName("a")[0];
  var link = link_el.href;
  var id = /\?mid=[^&]+/.exec(link_el.rel)[0].replace('?mid=', '');
  stored.yahoo_mail_since_id = id;

  var old_items = JSON.parse(stored.yahoo_mail);
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_YAHOO_MAIL);

  setTimeout(function() {
    stored.yahoo_mail = JSON.stringify(new_items);
  }, 1000);

}

function getMails() { 
  var req = new XMLHttpRequest();
  req.open("POST", url, true);
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      var res = JSON.parse(this.responseText);
      if (res.resps[0].status == 200) {
       processMails(res.resps[0].data.html);
      }
    } 
  };
  req.send(null);///null for GET
}

check();

})();