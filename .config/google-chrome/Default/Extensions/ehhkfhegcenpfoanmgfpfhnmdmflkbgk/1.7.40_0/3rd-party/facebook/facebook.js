var MAX_FACEBOOK = 20;

(function () {

var pollInterval = FETCH_INTERVAL || 3 * 60 * 1000;

var response;

function fetchUnseenCount() {
  var url = "https://www.facebook.com/home.php";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState != 4) 
      return;
    if (xhr.status != 200)
      return console.error('Facebook error:' , xhr.status);
    // <span ... id="mercurymessagesCountValue">1</span> 
    response = xhr.responseText;
    var fnd = /id="mercurymessagesCountValue">([^<]+)<\/span>/g.exec(response);
    if (!fnd || !fnd[1] || isNaN(fnd[1])) return;
    var unseen_count = fnd[1];
    updateUnreadCount(unseen_count);
  }
  xhr.send(null);
}

function updateUnreadCount(unread) {
  set_indicator("facebook", unread);
}

function isNotificationsEnabled() {
  return is_notification_enabled('facebook');
}

function check() {
  scheduleRequest();
  if (!navigator.onLine) 
    return;
  if (isNotificationsEnabled()) {
    fetchUnseenCount();
    facebookFetchUnseenMessages();
  } else {
    updateUnreadCount("");
  }
}

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

// initial check
setTimeout(check, 1000);

})();


(function () {

// We record __a, __dyn, fb_dtsg parameters in order to be able to send
// authorized requests to Facebook's servers and get the unread messages 
// so they can be displayed as notifications to the user.
chrome.webRequest.onBeforeRequest.addListener(function (details) { 
  processFacebookRequest(details);
}, { urls: [ 'https://www.facebook.com/*' ], 
    types: ["xmlhttprequest"] 
}, ["requestBody"] );

function processFacebookRequest(details) {
  var url = details.url;
  var data = (details.requestBody||{}).formData;
  if (!url.indexOf('__dyn=')) {
    processURL(url);
  }
  if (data) {
    processData(data);
  }
}

function processURL() {
  var fnd = /__dyn=([^&]+)&/g.exec(url);
  if (!fnd || !fnd[1]) return;
  stored['facebook_$__dyn'] = fnd[1];
}

function processData(data) {
  if (typeof data != 'object') return;
  if (data.__dyn)   stored['facebook_$__dyn']   = data.__dyn;
  if (data.__a)     stored['facebook_$__a']     = data.__a;
  if (data.fb_dtsg) stored['facebook_$fb_dtsg'] = data.fb_dtsg; 
  //__user, __rev?
}

})();

(function () {

var pollInterval = FETCH_INTERVAL || 3 * 60 * 1000;

window.addEventListener('message', function (m) {
  //console.log(m.data);
  var message = m.data;
  if (!message) return;
  if (message.indexOf && message.indexOf('oauth2callback') != -1) return;
  if (message.action != 'unseen_messages' && !message.data) return;

  processUnseenMessages(message.data); // unseen threads really :)
});


var fbFrame = document.createElement('iframe');
fbFrame.name = "fbFrame";
fbFrame.src = 'https://www.facebook.com/ajax/mercury/threadlist_info.php' +
               '?__pc=EXP1%3ADEFAULT&dpr=3';
document.body.appendChild(fbFrame);

/*
window.addEventListener('message',function(e){
  console.log("message received: " + JSON.stringify(e.data));
  console.log("message received: ", e);
});
*/


function facebookFetchUnseenMessages() {
  fbFrame.contentWindow.postMessage({
    action : 'fetch_facebook_unseen_messages',
    data   : {
      __dyn   : stored['facebook_$__dyn'],
      __a     : stored['facebook_$__a'],
      fb_dtsg : stored['facebook_$fb_dtsg'],
    }
  }, '*');
}

window.facebookFetchUnseenMessages = facebookFetchUnseenMessages;

function processUnseenMessages(messages) {

  var since_id = stored.facebook_messages_since_id;
  var new_items = [];
  var notifications = [];

  messages.forEach(function (message) {

    if (message.timestamp <= since_id) return;

    var link = 'https://www.facebook.com/messages/t/' + message.thread_fbid;

    new_items.push({
      id: message.timestamp, // id.808113364270858&source=unspecified-1334254140
      link: link,
      author: message.sender_short_name, // sender_name (full name)
      timestamp: message.timestamp
    });
    notifications.push(['facebook', "<a href='"+link+"' target='_blank'>" + 
                              message.sender_short_name + "</a> " , message.snippet]);
  });



  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  var timestamps = messages.map(function (message) {
    return message.timestamp;
  });
  timestamps.sort(function (a, b) { return b-a });

  if (timestamps[0])
    stored.facebook_messages_since_id = timestamps[0];

  if ('undefined' == typeof stored.facebook_messages)
    stored.facebook_messages = '[]';

  var old_items = jsonSafeParse(stored.facebook_messages, [],
                                'stored facebook_messages');

  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_FACEBOOK);

  setTimeout(function() {
    stored.facebook_messages = JSON.stringify(new_items);
  }, 1000);
}

})();

/*
home.php

"bootload_args":{"message_counts":[{"unread_count":2,"unseen_count":1,"seen_timestamp":1457976473716,"last_action_id":null,"folder":"inbox"},{"unread_count":0,"unseen_count":0,"seen_timestamp":0,"last_action_id":null,
*/