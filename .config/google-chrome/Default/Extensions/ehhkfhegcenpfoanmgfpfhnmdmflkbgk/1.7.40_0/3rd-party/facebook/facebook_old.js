// This file is packaged with the extension then re-fetched from the
// server for updates. Bitter experience has taught us that we can't depend on
// the server resource loading correctly.

/**
 * Copyright 2004-present Facebook. All Rights Reserved.
 *
 * Provides functions to get and display notifications in a desktop window.
 * Currently only Chrome supports the "web notifications" spec. Its
 * implementation is called webkitNotifications.
 *
 * Typically webkitNotifications is accessed from two distinct contexts:
 * 1) from a document on the host site
 * 2) from a Chrome extension that has permission to request data from the
 *    host site.
 *
 * This module supports both use cases. Some functions are Chrome-extension
 * only. A future refactoring may resolve to put them in a subclass, but
 * chances are higher we will eliminate support for 1) entirely.
 *
 * This module intentionally has no @requires dependencies so that it can
 * work in the extension context with a single <script> tag. The extension
 * may also load it as a haste resource via rscrx.php. Contact gdingle for
 * details.
 *
 * Web Notifications:
 *   http://dev.w3.org/2006/webapi/WebNotifications/publish/
 *   Chrome implementation: http://www.fburl.com/?key=1717695
 *
 * @provides desktop-notifications
 */
(function(){

var chrome;

DesktopNotifications = {

  DEFAULT_FADEOUT_DELAY: 10000,
  CLOSE_ON_CLICK_DELAY: 300,
  // 250 is a good delay for a human-visible flash
  COUNTER_BLINK_DELAY: 250,

  // Collection of notifications currently on screen
  notifications: [],
  _timer: null,

  // The following values are supposed to be in window.webkitNotifications,
  // but they're not defined as of Chrome 9/Chromium 75753.
  PERMISSION_ALLOWED: 0,
  PERMISSION_NOT_ALLOWED: 1,
  PERMISSION_DENIED: 2,

  // These may be overridden by clients
  getEndpoint: '/desktop_notifications/get.php',
  countsEndpoint: '/desktop_notifications/counts.php',
  domain: 'www.facebook.com',
  protocol: 'https://',

  // polling instance
  _interval: null,

  // These are used to short circuit data fetching on the server.
  // See flib/notifications/prepare/prepare.php
  _latest_notif: 0,
  _latest_read_notif: 0,

  // Unread counts, used for badge and fetching new HTML
  _num_unread_notif: 0,
  _num_unseen_inbox: 0,

  // We may obtain a CSRF token from the server to suppress click-jacking
  // protection on requests to HTML pages.
  fb_dtsg: '',

  /**
   * Start polling for notifications. New notifications are displayed
   * immediately. This should called from clients off of facebook.com. On the
   * main site we have presence to do our polling for us.
   */
  start: function(refresh_time) {
    var self = DesktopNotifications;
    // Don't refresh faster than fade out
    if (refresh_time < self.DEFAULT_FADEOUT_DELAY) {
      refresh_time = self.DEFAULT_FADEOUT_DELAY;
    }

    self.stop();
    self.showActiveIcon();
    // fetch the current counts immediately
    self.fetchServerInfo(self.handleServerInfo, self.showInactiveIcon);


    function check() {
      self.fetchServerInfo(
        function(serverInfo) {
          self.handleServerInfo(serverInfo);
          // set back to active in case of previous error
          self.showActiveIcon();
        },
        self.showInactiveIcon);
    }

    self._interval = setInterval(check, refresh_time);
    check();
  },

  /**
   * Get the best popup type to show. See WebDesktopNotificationsBaseController
   */
  getPopupType: function() {
    var self = DesktopNotifications;

    var type = 'notifications';
    if (self._num_unseen_inbox && !self._num_unread_notif) {
      type = 'inbox';
    }
    return type;
  },

  /**
   * Stop polling.
   */
  stop: function() {
    clearInterval(DesktopNotifications._interval);
    DesktopNotifications.showInactiveIcon();
  },

  /**
   * Updates icon in Chrome extension to normal blue icon
   */
  showActiveIcon: function() {
    if (chrome && chrome.browserAction) {
      chrome.browserAction.setIcon({path: '/images/icon19.png'});
    }
  },

  /**
   * Updates icon in Chrome extension to gray icon and clears badge.
   */
  showInactiveIcon: function() {
    if (chrome && chrome.browserAction) {
      chrome.browserAction.setBadgeText({text: ''});
      chrome.browserAction.setIcon({path: '/images/icon-loggedout.png'});
    }
  },

  /**
   * Fetches metadata from the server on the current state of the user's
   * notifications and inbox.
   */
  fetchServerInfo: function(callback, errback, no_cache) {
    callback = callback || function(d) { console.log(d); };
    errback = errback || function(u, e) { console.error(u, e); };
    var self = DesktopNotifications;
    var uri = self.protocol + self.domain + self.countsEndpoint +
      '?latest=' + self._latest_notif +
      '&latest_read=' + self._latest_read_notif;
    if (no_cache) {
      uri += '&no_cache=1';
    }
    self._fetch(
      uri,
      function(json) {
        callback(JSON.parse(json));
      },
      errback
    );
  },

  _fetch: function(uri, callback, errback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", uri, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        try {
          if (xhr.status == 200) {
            return callback(xhr.responseText);
          } else {
            throw 'Status ' + xhr.status + ': ' + xhr.responseText;
          }
        } catch (e) {
          errback(e, uri);
        }
      }
    };
    xhr.send(null);
  },

  /**
   * Decides whether to fetch any items for display depending on data from
   * server on unread counts.
   */
  handleServerInfo: function(serverInfo) {
    var self = DesktopNotifications;
    // update CSRF token
    self.fb_dtsg = serverInfo.fb_dtsg;

    self._handleNotifInfo(serverInfo.notifications);
    self._handleInboxInfo(serverInfo.inbox);
    self.updateUnreadCounter();
  },

  _handleNotifInfo: function(notifInfo) {
    var self = DesktopNotifications;
    // The server will return a lone no_change flag if latest and latest_read
    // match its current values.
    if (!notifInfo || notifInfo.no_change) {
      return;
    }
    if (self._num_unread_notif !== notifInfo.num_unread) {
      if (self._latest_notif < notifInfo.latest) {
        self._latest_notif = notifInfo.latest;
        self._latest_read_notif = notifInfo.latest_read;
        // see WebDesktopNotificationsBaseController::TYPE_NOTIFICATIONS
        self.addNotificationByType('notifications');
      }
      self._num_unread_notif = notifInfo.num_unread;
      //self.updateUnreadCounter();
    }
  },

  _handleInboxInfo: function(inboxInfo) {
    var self = DesktopNotifications;
    if (!inboxInfo) {
      return;
    }
    /*
    if (inboxInfo.seen_time != self._inbox_seen_time) {
      self.addNotificationByType('inbox');
      self._inbox_seen_time = inboxInfo.seen_time;
      self._num_unseen_inbox = inboxInfo.unseen;
    }
    */

    if (inboxInfo.unseen !== self._num_unseen_inbox) {
      if (inboxInfo.unseen > self._num_unseen_inbox) {
        // see WebDesktopNotificationsBaseController::TYPE_INBOX
        self.addNotificationByType('inbox');
      }
      self._num_unseen_inbox = inboxInfo.unseen;
      //self.updateUnreadCounter();
    }

  },

  /**
   * Updates "badge" in Chrome extension toolbar icon.
   * See http://code.google.com/chrome/extensions/browserAction.html#badge
   */
  updateUnreadCounter: function() {
    var self = DesktopNotifications;
    set_indicator('facebook', self.getUnreadCount());
    if (chrome && chrome.browserAction) {
      // first set the counter to empty
      chrome.browserAction.setBadgeText({text: ''});
      // wait, then set it to new value
      setTimeout(function() {
          // don't show a zero
          var num = (self.getUnreadCount() || '') + '';
          chrome.browserAction.setBadgeText({text: num});
        },
        self.COUNTER_BLINK_DELAY,
        false // quickling eats timeouts otherwise
        );
    }
  },

  getUnreadCount: function() {
    var self = DesktopNotifications;
    return self._num_unread_notif + self._num_unseen_inbox;
  },

  addNotificationByType: function(type) {
    var self = DesktopNotifications;
    var uri = self.protocol + self.domain + self.getEndpoint +
      '?type=' + (type || '');
    var notification = {}
    ///  window.webkitNotifications.createHTMLNotification(uri);

    if (type == 'inbox')
      self._fetch(uri, processFacebook, function(u, e) { console.error(u, e) });

    // In case the user has multiple windows or tabs open, replace
    // any existing windows for this alert with this one.
    notification.replaceId = 'com.facebook.alert.' + type;

    ///self.showNotification(notification, self.DEFAULT_FADEOUT_DELAY);
  },

  /**
   * Adds a new notification to the queue.
   * After an expiration period, it is closed.
   */
  addNotification: function(alert_id, delay) {
    var self = DesktopNotifications;
    if (!window.webkitNotifications) {
      return;
    }

    if (typeof delay == 'undefined') {
      delay = self.DEFAULT_FADEOUT_DELAY;
    }
    var uri = self.protocol + self.domain + self.getEndpoint +
      '?alert_id=' + (alert_id || '') +
      '&latest=' + self._latest_notif +
      '&latest_read=' + self._latest_read_notif;
    var notification =
      window.webkitNotifications.createHTMLNotification(uri);

    // In case the user has multiple windows or tabs open, replace
    // any existing windows for this alert with this one.
    notification.replaceId = 'com.facebook.alert.' + alert_id;

    self.showNotification(notification, delay);
  },

  showNotification: function(notification, delay) {
    return; /// disabled for now
    notification.show();
    notification.onclick = function(e) {
      // Oddly, defer(0) still cancels the notification before the
      // click passes through.  Give it a little time before we
      // close the window.
      setTimeout(function() {
          e.srcElement.cancel();
        },
        DesktopNotifications.CLOSE_ON_CLICK_DELAY,
        false // quickling eats timeouts otherwise
        );
    };
    DesktopNotifications.notifications.push(notification);
    DesktopNotifications.restartTimer(delay);
  },

  expireNotifications: function() {
    DesktopNotifications.notifications.forEach(function(n) { n.cancel(); });
    DesktopNotifications.notifications = [];
    DesktopNotifications._timer = null;
  },

  restartTimer: function(extraTime) {
    if (DesktopNotifications._timer) {
      clearTimeout(DesktopNotifications._timer);
    }
    DesktopNotifications._timer = setTimeout(function() {
      DesktopNotifications.expireNotifications();
    }, extraTime);
  }
};


stored.facebook_messages || (stored.facebook_messages = "[]");

var MAX_FACEBOOK = 20;
var el = document.createElement('div');

function processFacebook(html) {

  var fnd = html.match(/<ul\s+class="jewelItemList.+?>([\s\S]+?)<\/ul>/g);

  if (!fnd) return;

  el.innerHTML = fnd.toString();
  var items = el.getElementsByTagName('li');

  if (!items.length) return;

  var since_id = stored.facebook_messages_since_id;
  var new_items = [];
  var notifications = [];


  for (var i = 0; i < items.length; i++) {

    var item = items[i];
    if (!item.getElementsByTagName("a")[0]) continue;
    var link = item.getElementsByTagName("a")[0].href;
    link = "https://www.facebook.com" + link.slice(link.indexOf("/messages"));
    var author = item.getElementsByClassName('author')[0].textContent.replace(/\(\d+\) ?/, "");
    var snippet = item.getElementsByClassName('snippet')[0].textContent;
    var timestamp = item.getElementsByClassName('timestamp')[0].getAttribute('data-utime');
    var id = /tid=[^%]+/.exec(link)[0].replace('tid=', '') + "-" + timestamp;

    if (id == since_id) break;

    new_items.push({
      id: id,
      link: link,
      author: author,
      timestamp: timestamp
    });
    notifications.push(['facebook', "<a href='"+link+"' target='_blank'>" + author + "</a> " , snippet]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  var link = items[0].getElementsByTagName("a")[0].href;
  var timestamp = items[0].getElementsByClassName('timestamp')[0].getAttribute('data-utime');
  var id = /tid=[^%]+/.exec(link)[0].replace('tid=', '') + "-" + timestamp;
  stored.facebook_messages_since_id = id;


  var old_items = [];
  try {
    old_items = JSON.parse(stored.facebook_messages);
  } catch (e) {
    console.log('ERROR: stored facebook_messages has invalid JSON: ' + stored.facebook_messages);
    /// TODO: log error
  }

  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_FACEBOOK);

  setTimeout(function() {
    stored.facebook_messages = JSON.stringify(new_items);
  }, 1000);

}


DesktopNotifications.start(FETCH_INTERVAL || 30 * 1000);

})();



/*
(function(){


stored.facebook_messages || (stored.facebook_messages = "[]");


var url = "https://www.facebook.com/desktop_notifications/popup.php";
var params = "type[inbox]=Inbox&fb_dtsg=AQC1Nukr";

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

var MAX_FACEBOOK = 20;

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function check() {
  getFacebook();
  scheduleRequest();
}

var el = document.createElement('div');

function processFacebook(html) {

  var fnd = html.match(/<ul\s+class="jewelItemList.+?>([\s\S]+?)<\/ul>/g);

  if (!fnd) return;

  el.innerHTML = fnd.toString();
  var items = el.getElementsByTagName('li');

  if (!items.length) return;

  var since_id = stored.facebook_messages_since_id;
  var new_items = [];
  var notifications = [];


  for (var i = 0; i < items.length; i++) {

    var item = items[i];
    if (!item.getElementsByTagName("a")[0]) continue;
    var link = item.getElementsByTagName("a")[0].href;
    var id = /tid=[^%]+/.exec(link)[0].replace('tid=', '');
    var author = item.getElementsByClassName('author')[0].textContent;
    var snippet = item.getElementsByClassName('snippet')[0].textContent;
    var timestamp = item.getElementsByClassName('timestamp')[0].getAttribute('data-utime');

    if (id == since_id) break;

    new_items.push({
      id: id,
      link: link,
      author: author,
      timestamp: timestamp
    });
    notifications.push(['facebook', "<a href='"+link+"' target='_blank'>" + author + "</a> " + snippet, ""]);
  }

  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  var link = items[0].getElementsByTagName("a")[0].href;
  var id = /tid=[^%]+/.exec(link)[0].replace('tid=', '');
  stored.facebook_messages_since_id = id;

  var old_items = JSON.parse(stored.facebook_messages);
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_FACEBOOK);

  setTimeout(function() {
    stored.facebook_messages = JSON.stringify(new_items);
  }, 1000);

}

function getFacebook() { 
  var req = new XMLHttpRequest();
  req.open("POST", url, true);
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    if (this.status == 200) {
      processFacebook(this.responseText);
    } 
  };
  req.send(params);///null for GET
}

check();


})();
*/