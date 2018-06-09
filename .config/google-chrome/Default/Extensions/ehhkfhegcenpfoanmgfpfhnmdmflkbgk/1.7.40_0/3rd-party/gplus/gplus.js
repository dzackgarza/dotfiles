(function(){

var url = "https://plus.google.com/u/0/_/n/guc";

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function updateUnreadCount(unread) {
  set_indicator("gplus", unread);
}

function check() {
  getNotificationCount();
  scheduleRequest();
}

function getNotificationCount() { 
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      var unread = JSON.parse(this.responseText.substr(4).replace(/,+/g, ','))[0][1];
      updateUnreadCount(unread);
    } 
  };
  req.send(null);
}

//window.addEventListener("DOMContentLoaded", check, false);
check();

})();

