/*
(function(){

stored.yahoo_mail || (stored.yahoo_mail = "[]");


// &callback=cbfunc
//var url = "http://query.yahooapis.com/v1/public/yql?q=select%20messageInfo%20from%20ymail.messages%20where%20numInfo%20%3D%20'10'&format=json";
var url = "http://query.yahooapis.com/v1/public/yql?q=select%20messageInfo%20from%20ymail.messages%20where%20numInfo%20%3D%20'10'&format=json";
url = "http://developer.yahoo.com/yql/console/proxy.php";

var params = "q=select * from ymail.messages where numInfo = '10'&" +
             "format=json&crumb:B6TIJYV3woG";

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

var MAX_YAHOO_MAIL = 20;


function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function check() {
  getMails();
  scheduleRequest();
}

function processMails(items) {

  if (!items.length) return;

  var since_id = stored.yahoo_mail_since_id;
  var new_items = [];
  var notifications = [];

  var link = "http://us.mg40.mail.yahoo.com/neo/launch";

  for (var i = 0; i < items.length; i++) {
    if (items[i].mid == since_id) break;
    var item = items[i];
    new_items.push({
      id: item.mid,
      date: item.receivedDate,
      subject: item.subject,
      from: item.from.name
    });
    notifications.push(['yahoo-mail', "<a href='"+link+"' target='_blank'>" + item.from.name + "</a> " + item.subject, ""]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  stored.yahoo_mail_since_id = items[0].mid;

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
  req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  //req.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
  //req.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      processMails(JSON.parse(this.responseText).query.results.result.messageInfo);
    } 
  };
  req.send(params);///null for GET
}

setTimeout(check, 30*1000);

})();
*/
