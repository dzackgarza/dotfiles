//console.profile();
//setTimeout(function ( ){ console.profileEnd(); }, 10000)
var g_update_time = Math.max(+new Date, 1490038398000);
var homeTabId;
var return_to_home_hook;
var apps;
var stored = localStorage;
var ordered = [];
var isMac =  /mac/i.test(navigator.userAgent);

var custom_apps = {};
try {  // id -> bool (enabled state)
  if (stored.custom_apps) custom_apps = JSON.parse(stored.custom_apps);
} catch (e) {
  logError(new Error("ERROR: stored custom_apps has invalid JSON: "));
  console.log('ERROR: stored custom_apps has invalid JSON: ' + stored.custom_apps);
  // throw new Error('...');
}

var user_apps = {};
try {  // id -> bool (enabled state)
  if (stored.user_apps) user_apps = JSON.parse(stored.user_apps);
} catch (e) {
  logError(new Error('ERROR: stored user_apps has invalid JSON: '));
  console.log('ERROR: stored user_apps has invalid JSON: ' + stored.user_apps);
  // throw new Error('...');
}

if (null == stored.user_app_id_inc) stored.user_app_id_inc = 0;
if (null == stored.user_app_ids) stored.user_app_ids = '';

function save_options() {
  try {
    stored.settings = JSON.stringify(settings);
  } catch(e) {
    /// TODO: log error
    // throw new Error('...');
  } 
}

// stored.user_app_ids list of user app IDs
// stored.user_app_id_inc auto increment index
// stored.user_app_<ID> => { ... }

localStorage.install_time || (localStorage.install_time = g_update_time);

function return_to_home() {

  if (!return_to_home_hook) {
     chrome.tabs.update(homeTabId, {active: true});
     return;
  }
  chrome.tabs.captureVisibleTab(null, {
    //format: "jpeg"
    //,quality: 100
  }, function(dataUrl) {
    /*
    console.log(dataUrl.length);
    var img = document.createElement("img");
    img.src = dataUrl;
    document.body.appendChild(img);
    */
    return_to_home_hook(dataUrl, function(){
      chrome.tabs.update(homeTabId, {active: true});
    });
  });
}

chrome.extension.onRequest.addListener(
  function(request, sender, sendResponse) {
    if (request.name == "get-home-tab-id") {
      sendResponse(homeTabId);
    } else if (request.name == "return-to-home") {
      return_to_home();
    }
  });


// INSTALL & ENABLE

function remove_custom_app() {

}

chrome.management.onInstalled.addListener(function(app) {
  ///stored.icons_order += "," + app.id;

  if (!app.isApp) return;

  apps[app.id] = app;

  // all views should update the UI
  chrome.extension.sendMessage({ name: "add_new_app", id: app.id });

  // active view should scroll to show the newly installed app
  chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {name: "go_last_page"})
  });
});

chrome.management.onEnabled.addListener(function(app) {
  if (app.isApp)
    stored.icons_order += "," + app.id;
});


// UNINSTALL & DISABLE
function removeAppFromIcons(id) {
  var ordered = stored.icons_order.split(',');
  for (var i = 0; i < ordered.length; i++)
    if (ordered[i] == id)
      ordered.splice(i, 1);
  stored.icons_order = ordered.join(',');
  if (id.indexOf('user_app') == 0)
    remove_user_app(id);
}

function onUninstalled(id) {
  removeAppFromIcons(id);
  if (custom_apps[id]) {
    apps[id].enabled = false;
    custom_apps[id] = false;
    stored.custom_apps = JSON.stringify(custom_apps);
  }
}

function onDisabled(id) {
  removeAppFromIcons(id);
  apps[id].enabled = false;
}

// callded in main.js because of custom apps
///chrome.management.onUninstalled.addListener(onUninstalled);

chrome.management.onDisabled.addListener(function(app) {
  if (app.isApp) onDisabled(app.id);
});

var settings = default_settings;
try {  // default.js
  if (stored.settings) settings = JSON.parse(stored.settings);
  settings.notifications = settings.notifications || {};
} catch (e) {
  logError(new Error('ERROR: stored settings has invalid JSON: '));
  console.log('ERROR: stored settings has invalid JSON: ' + stored.settings);
  // throw new Error('...');
}

/* temporary fix for old settings */

if (settings.fetch_interval < 5) {
  settings.fetch_interval = 5;
  save_options();
}

if ("undefined" != typeof settings.showClear) {
  settings = default_settings;
}

try { 
  stored.settings = JSON.stringify(settings); 
} catch (e) {
  //throw new Error('problem with stringify settings');
}


var FETCH_INTERVAL = settings.fetch_interval ? settings.fetch_interval*MINUTES : 5*MINUTES;
var ITEM_SEPARATOR = "\\c";
var FIELD_SEPARATOR = "\\a";
var MAX_NOTIFICATIONS = 10; // shown / stored

var ICONS = {
  'tweet':      'icons/twitter.png',/// TODO remove later
  'twitter':    'icons/twitter.png',
  'mail':       'icons/mail.png',
  'gmail':      'icons/gmail.png',
  'yahoo-mail': 'icons/yahoo-mail.png',
  'hotmail':    'icons/hotmail.png',
  'news':       'icons/news.png',
  'facebook':   'icons/facebook.png'
};

var indicators = {
  'pjkljhegncpnkpknbcohdijeoejaedia': 'gmail',
  'pjjhlfkghdhmijklfnahfkpgmhcmfgcm': 'greader',
  'dlppkpafhbajpcmmoheippocdidnckmm': 'gplus',
  'yahoo-mail': 'yahoo-mail',
  'hotmail':    'hotmail',
  'facebook':   'facebook'
};

stored.notifications || (stored.notifications = "");


function set_indicator(id, count) {
  // broadcast indicator change
  chrome.extension.sendMessage({
    name: "set_indicator",
    args: [id, count],
    type: "rpc",
  });
  // store indicator change
  var key = "indicator-" + id;
  stored[key] = count;
}

function is_notification_enabled(i) {
  return ("undefined" == typeof settings.notifications[i] || settings.notifications[i]);
}

function create_notification(icon, title, body) {

  if (!icon || !title) return;

  if (icon == 'gmail'      && !is_notification_enabled('pjkljhegncpnkpknbcohdijeoejaedia')) return;
  if (icon == 'news'       && !is_notification_enabled('pjjhlfkghdhmijklfnahfkpgmhcmfgcm')) return;
  if (icon == 'yahoo-mail' && !is_notification_enabled('yahoo-mail')) return;
  if (icon == 'hotmail'    && !is_notification_enabled('hotmail')) return;
  if (icon == 'facebook'   && !is_notification_enabled('facebook')) return;
  if (icon == 'twitter'    && !is_notification_enabled('twitter')) return;

  // broadcast new notification
  chrome.extension.sendMessage({
    name: "create_notification",
    args: [icon, title, body],
    type: "rpc",
  });

  /*
  if (icon == 'tweet' && +new Date - last_sound > 1000)  {
    last_sound = +new Date;
    byId('twittersound', bg.document).currentTime = 0;
    byId('twittersound', bg.document).play();
  }
  */

  icon = ICONS[icon] || icon;
  var new_item = icon + FIELD_SEPARATOR + title + FIELD_SEPARATOR + body;

  // fetch stored notifications and refresh list
  var notifications = stored.notifications ? stored.notifications.split(ITEM_SEPARATOR) : [];
  notifications.unshift(new_item);
  if (notifications.length > MAX_NOTIFICATIONS) {
    notifications.pop();
  }

  // update storage
  stored.notifications = notifications.join(ITEM_SEPARATOR);
}

function play_notification_sound(type) {
}



function build_apps_list(chrome_apps_arr) {
  ///bench('build start');///

  // save default custom apps' states upon first launch
  if ("undefined" == typeof custom_apps["webstore"]) {
    custom_apps = {"contacts":true,"webstore":true,"yahoo-mail":true,"hotmail":true,"facebook":true,"twitter":true,"ebay":true,"booking":true,"aliexpress":true}; // ,"amazon":true
    stored.custom_apps = JSON.stringify(custom_apps);
  }

  // existing users (but only ones that are new additions to test group 3)
  if ("undefined" == typeof custom_apps["ebay"] && 'true' == stored.testing_tiles_active) {
    custom_apps.ebay = true;
    custom_apps.booking = true;
    custom_apps.aliexpress = true;
    stored.custom_apps = JSON.stringify(custom_apps);
  }

  if ("undefined" == typeof custom_apps["ebay"]) {
    custom_apps.ebay = true;
    stored.custom_apps = JSON.stringify(custom_apps);
  }

  //if (custom_apps.booking && localStorage.GEO_country_code == 'US') {
  //  custom_apps.booking = false;
  //  stored.custom_apps = JSON.stringify(custom_apps);
  //}
  

  // youtube: blpcfgokakmgnkcojhhkbfbldkacnbeo
  //custom_apps.amazon = true;

  var sys_apps_arr = []; 

  if (chrome_apps_arr) {

    // if you want to change any of the links don't forget to purhe html cache

    if (custom_apps["contacts"])
    sys_apps_arr.unshift({
      name: "Contacts",
      id:   "contacts",
      icons: [{size: 128, url: "icons/app/contacts-128.png"}],
      appLaunchUrl: "https://www.google.com/contacts/#contacts",
      isApp:   true,
      enabled: custom_apps["contacts"]
    });

    if (custom_apps["aliexpress"])
    sys_apps_arr.unshift({
      name: "AliExpress",
      id:   "aliexpress",
      icons: [{size: 128, url: "icons/app/aliexpress-128.png"}],
      appLaunchUrl: "https://s.click.aliexpress.com/e/yNnuBeeQf",
      isApp:   true,
      enabled: custom_apps["aliexpress"]
    });

    if (custom_apps["booking"])
    sys_apps_arr.unshift({
      name: "Booking.com",
      id:   "booking",
      icons: [{size: 128, url: "icons/app/booking-128.png"}],
      appLaunchUrl: "https://www.booking.com/index.html?aid=1195117",
      isApp:   true,
      enabled: custom_apps["booking"]
    });

    if (custom_apps["ebay"])
    sys_apps_arr.unshift({
      name: "Ebay",
      id:   "ebay",
      icons: [{size: 128, url: "icons/app/ebay-128.png","borderRadius":16}],
      appLaunchUrl: "http://www.ebay.com/",
      isApp:   true,
      enabled: custom_apps["ebay"]
    });

    if (custom_apps["webstore"])
    sys_apps_arr.unshift({
      name: "Store",
      id:   "webstore",
      icons: [{size: 128, url: "chrome://extension-icon/ahfgeienlihckogmohjhadlkjgocpleb/128/0"}],
      appLaunchUrl: "https://chrome.google.com/webstore/category/popular",
      isApp:   true,
      enabled: custom_apps["webstore"]
    });

    if (custom_apps["yahoo-mail"])
    sys_apps_arr.push({
      name: "Yahoo! Mail",
      id:   "yahoo-mail",
      icons: [{size: 128, url: "icons/app/yahoo-mail-128.png"}],
      appLaunchUrl: "http://us.mg40.mail.yahoo.com/neo/launch?.rand=" + (+new Date),
      isApp:   true,
      enabled: custom_apps["yahoo-mail"]
    });

    if (custom_apps["hotmail"])
    sys_apps_arr.push({
      name: "Hotmail",
      id:   "hotmail",
      icons: [{size: 128, url: "icons/app/hotmail-128.png"}],
      appLaunchUrl: "http://mail.live.com/default.aspx?rru=inbox", /// http vs https
      optionsUrl: "https://mail.live.com/P.mvc#!/mail/options.aspx",
      isApp:   true,
      enabled: custom_apps["hotmail"]
    });

    if (custom_apps["facebook"])
    sys_apps_arr.push({
      name: "Facebook",
      id:   "facebook",
      icons: [{size: 128, url: "icons/app/facebook-128.png"}],
      appLaunchUrl: "https://www.facebook.com/",
      optionsUrl: "https://www.facebook.com/settings",
      isApp:   true,
      enabled: custom_apps["facebook"]
    });

    if (custom_apps["twitter"])
    sys_apps_arr.push({
      name: "Twitter",
      id:   "twitter",
      icons: [{size: 128, url: "icons/app/twitter-128.png"}],
      appLaunchUrl: "https://twitter.com/",
      optionsUrl: "https://twitter.com/settings/account",
      isApp:   true,
      enabled: custom_apps["twitter"]
    });

    // if blpcfgokakmgnkcojhhkbfbldkacnbeo is not installed
    if (custom_apps["youtube"])
    sys_apps_arr.push({
      name: "YouTube",
      id:   "youtube",
      icons: [{size: 128, url: "icons/app/youtube-128.png"}],
      appLaunchUrl: "https://www.youtube.com/",
      optionsUrl: "https://www.youtube.com/account",
      isApp:   true,
      enabled: custom_apps["youtube"]
    });
  }

  function add_amazon_user_app() {
    return add_user_app(
      'Amazon', 
      'https://www.amazon.com/', 
      [{size: 128, url: "icons/app/amazon-128.png", "borderRadius":16}]
    );
  }



  var in_ordered = {};

  // stored list of apps in custom order
  ///
  /*for (var i = 0; i < ordered.length; i++) {
    for (var j = 0; j < ordered[i].length; j++) {
      in_ordered[ordered[i][j]] = true;
    }
  }*/
  for (var j = 0; j < ordered.length; j++) {
    in_ordered[ordered[j]] = true;
  }

  apps = {};

  // check for missing system apps (recently added)
  for (var i = sys_apps_arr.length; i--;) {
    var app = sys_apps_arr[i];
    if (!app.isApp) continue;
    apps[app.id] = app;
    if (!in_ordered[app.id] && app.enabled)
      ordered.unshift(app.id);
  }

  // check for missing chrome apps (recently added)
  for (var i = 0; i < chrome_apps_arr.length; i++) {
    var app = chrome_apps_arr[i];
    if (!app.isApp) continue;
    apps[app.id] = app;
    if (!in_ordered[app.id] && app.enabled)
      ///push_to_empty_index(ordered, app.id);
      ordered.push(app.id);
  }

  // check for missing user apps (after purge)
  var user_app_ids = stored.user_app_ids.split(',');
  for (var j = 0; j < user_app_ids.length; j++) {
    var id = user_app_ids[j];
    if (!id) continue;
    if (!stored[id]) continue;
    if (in_ordered[id]) continue;
    ordered.push(id);
  }

  // user apps data
  for (var j = 0; j < ordered.length; j++) {
    var id = ordered[j];
    if (id.indexOf('user_app') != 0) 
      continue;
    if (!stored[id]) 
      continue;
    try { 
      apps[id] = JSON.parse(stored[id]);
      on_user_app_init(apps[id]);
    } catch(e) {
      logError(new Error('ERROR: stored app has invalid JSON: ' + id));
    }
  }

  // add amazon if not exists
  /*
  try { 
    if (!stored.AMZN_app_added) {
      var amazonIDs = ordered.filter(function (id) {
        if (id.indexOf('user_app') != 0) return false;
        if (is_amazon_url(apps[id].appLaunchUrl)) return id;
      });
      if (!amazonIDs.length) {
        var newAmazonID = add_amazon_user_app().id;
        if (ordered[0] == 'webstore')
          ordered.splice(1, 0, newAmazonID);
        else
          ordered.unshift(newAmazonID);
      }
      stored.AMZN_app_added = 'true';
    }
  } catch(e) {
    logError(e);
  }
  */

  stored.icons_order = ordered.join(',')///JSON.stringify(ordered);
}


if (stored.icons_order) {
  ordered = stored.icons_order.split(',');//JSON.parse(stored.icons_order);
}


chrome.management.getAll(function(array) {
    build_apps_list(array);
    include_3rd_party_services();
});


var custom_gmail, custom_facebook;

function on_user_app_init(app) {
  var url = app.appLaunchUrl;
  if (url.indexOf('facebook.com') > -1)
    custom_facebook = app.id;
  else (url.indexOf('gmail.com') > -1 || 
        url.indexOf('google.com/mail') > -1 ||
        url.indexOf('mail.google.com') > -1) 
    custom_gmail = app.id;
}


function add_user_app(name, url, icons) {
  var id = 'user_app_' + stored.user_app_id_inc++;
  stored.icons_order += "," + id;
  apps[id] = {
      name: name,
      id: id,
      icons: icons,
      appLaunchUrl: url,
      isApp: true,
      enabled: true
  };
  stored[id] = JSON.stringify(apps[id]);
  stored.user_app_ids += id + ',';
  chrome.runtime.sendMessage({name: 'add_new_app', id:id});
  // active view should scroll to show the newly installed app
  chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {name: "go_last_page"})
  });
  return apps[id];
}

function edit_user_app(id, name, url, icons) {
  apps[id] = {
      name: name,
      id: id,
      icons: icons,
      appLaunchUrl: url,
      isApp: true,
      enabled: true
  };
  stored[id] = JSON.stringify(apps[id]);
  chrome.runtime.sendMessage({name: 'edit_app', id:id});
}

function remove_user_app(id) {
  var user_app_ids = stored.user_app_ids.split(',');
  for (var i = 0; i < user_app_ids.length; i++)
    if (user_app_ids[i] == id)
      user_app_ids.splice(i, 1);
  stored.user_app_ids = user_app_ids.join(',');
  delete stored[id];
  apps[id].icons.forEach(function (icon) {
    remove_file(extract_filename(icon.url));
  });
}


function save_new_background(url, callback) {
  imageURLToBlob(url, function (blob) {
    save_file_blob('/background.jpg', blob, callback);
    var protocol = 'filesystem:chrome-extension://';
    var url = protocol + window.APP_ID + '/persistent/background.jpg';
    settings.background_image = url;
    save_options();
  });
}

function include_3rd_party_services() {

    include_js("3rd-party/closed-tab/bg.js");

    // TODO: check settings.notifications['facebook'] etc.

    // optional services

    if (apps['pjkljhegncpnkpknbcohdijeoejaedia'] &&
        apps['pjkljhegncpnkpknbcohdijeoejaedia'].enabled ||
        custom_gmail) {
      include_js("3rd-party/gmail/gmail.js");
    }

    //if (apps['dlppkpafhbajpcmmoheippocdidnckmm'] &&
    //    apps['dlppkpafhbajpcmmoheippocdidnckmm'].enabled) {
    //  include_js("3rd-party/gplus/gplus.js");
    //}

    if (apps['yahoo-mail'].enabled) {
      include_js("3rd-party/yahoo-mail/yahoo-mail.js");
    }

    if (apps['facebook'].enabled || custom_facebook) {
      include_js("3rd-party/facebook/facebook.js");
    }

    if (apps['hotmail'].enabled) {
      include_js("3rd-party/hotmail/hotmail.js");
    }

    //if (apps['ejjicmeblgpmajnghnpcppodonldlgfn'] &&
    //    apps['ejjicmeblgpmajnghnpcppodonldlgfn'].enabled) {
    // onload=GCAL_checkAuth
      window.GCAL_LOADED = function() {
        include_js("3rd-party/gcalendar/gcalendar.js", function () {
          window.GCAL_checkAuth();
        });
      };
      include_js("https://apis.google.com/js/client.js?onload=GCAL_LOADED");
    //}  
}

// temporary force update
var hotmail_html = stored.app_html_hotmail
if (hotmail_html && hotmail_html.indexOf('col002') > -1) {
  delete stored.app_html_hotmail;
}

if (chrome.runtime.setUninstallURL && !window.DEV) 
  chrome.runtime.setUninstallURL("http://www.homenewtab.com/farewell.html");

chrome.extension.onMessage.addListener(
  function(message, sender, sendResponse) {
    //if (window.DEV) return;
    if (message.name == "ga" && message.arguments) {
      ga.apply(window, message.arguments);
    } else if (message.name == "ga_cb" && message.arguments) {
      ga.apply(window, message.arguments);
      if ('function' == typeof sendResponse)
        sendResponse();
    } else if (message.name == "fbq" && message.arguments) {
      fbq.apply(window, message.arguments);
    } else if (message.name == "fbq_cb" && message.arguments) {
      fbq.apply(window, message.arguments);
      if ('function' == typeof sendResponse)
        sendResponse();
    } else if (message.name == "adw" && message.arguments) {
      adw.apply(window, message.arguments);
    } else if (message.name == "pageview") {
      ga('set',  'dimension1', settings.search_bar);
      ga('set',  'dimension2', settings.search_bar ? settings.search_fullscreen : -1); 
      ga('set',  'dimension4', isMac ? stored.SS_discrete_mouse_wheel == 'true' : -1); 
      ga('set',  'dimension5', localStorage.GEO_country_code); 
      ga('send', 'pageview', { page: message.page || 'main.html' });
    } else if (message.name == "search-event") {
      ga('send', 'event', 'search', 'click');
    } else if (message.name == "search-timeout") {
      ga('send', 'event', 'search', 'timeout');
    } else if (message.name == "search-slow") {
      ga('send', 'event', 'search', 'slow');
    }  else if (message.name == "search-event-url") {
      ga('send', 'event', 'search', 'url', message.url);
    } else if (message.name == "search-event-url-suggested") {
      ga('send', 'event', 'search', 'url-suggested', message.url);
    } else if (message.name == "new-tab-exception") {
      gaException(message.message, message.file, message.line, message.stack);
    }
  });

chrome.runtime.onInstalled.addListener(function (details) {
  //if (window.DEV) return;
  if ('install' == details.reason) {
    ga('send', 'pageview', { page: 'install.html' });
    ga('send', 'event', 'install', 'install');
    fbq('track', 'Install');
    adw('Install');
    localStorage.install_time = g_update_time;
    checkInstallConversion();
    show_thank_you_page();
  } else if ('update' == details.reason) {
    var version = chrome.runtime.getManifest().version;
    ga('send', 'event', 'update', 'update', version);
  }
});

function show_thank_you_page() {
  chrome.tabs.create({
    url: chrome.extension.getURL('thank_you.html'), 
    active: true
  });
}

// check for connection errors
function testConnectionToSearch() {
  if (!navigator.onLine) return;
  if (Math.random() > 0.01) return; // 20% chance
  var img = new Image();
  var start = Date.now();
  var searchErrorTimeout;
  searchErrorTimeout = setTimeout(function () {
    ga('send', 'event', 'test-connection', 'failed', '');
  }, 5*SECONDS);
  img.onerror = function () {
    ga('send', 'event', 'test-connection', 'failed', '');
    clearTimeout(searchErrorTimeout);
  };
  img.onload = function () {
    ga('send', 'event', 'test-connection', 'passed', '', Date.now()-start);
    clearTimeout(searchErrorTimeout);
  };
  img.src = window.SEARCH_ORIGIN + '/blank.gif';
}

window.DEV ? testConnectionToSearch()
           : setTimeout(testConnectionToSearch, 10*SECONDS);

function checkInstallConversion() {
  if (!chrome.cookies) return;
  var url = "https://chrome.google.com/webstore/"; // detail/ehhkfhegcenpfoanmgfpfhnmdmflkbgk
  //"73091649.1441531513.921.486.utmcsr=sscr|utmccn=sscr-cmp|utmcmd=(not%20set)"
  var map = {'utmcsr': 'source', 'utmccn': 'name', 'utmcmd': 'medium'}; // campaign
  chrome.cookies.get({ url: url, name: "__utmz" }, function (cookie) { 
    if (!cookie) return;
    cookie = cookie.value;
    cookie = cookie.slice(cookie.indexOf('utm'));
    var campaign = {};
    var parts = cookie.split('|');
    parts.forEach(function (part) {
      var key   = part.split('=')[0];
      var value = part.split('=')[1];
      campaign[map[key]] = decodeURIComponent(value);
    });
    ga('send', 'event', 'conversion', 'install', campaign.source);
    ga('set', 'campaignName',   campaign.name   || '(direct)');
    ga('set', 'campaigSource',  campaign.source || '(direct)');
    ga('set', 'campaignMedium', campaign.medium || 'organic');
  });
}

window.is_notification_enabled = is_notification_enabled;


chrome.runtime.onInstalled.addListener(function (details) {
  if ('install' == details.reason)
    stored.TEST_search_fullscreen = true;
});

if (/mac/i.test(navigator.userAgent)) {
  chrome.webNavigation.onCompleted.addListener(function(details) {
    if (!/^https?:\/\/www\.google\./.test(details.url)) return;
    chrome.tabs.executeScript(details.tabId, { file: "/js/temp/sscr_detect.js" });
  });
  chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.to != 'bg') return;
    if (msg.name == "SS_discreteMouseWheel") {
      stored.SS_discrete_mouse_wheel = true;
    }
  });
}

(function () {

function ajax(url, onSuccess, onError) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function () {
    if (200 == xhr.status)
      onSuccess && onSuccess(xhr);
    else 
      onError && onError(xhr);
  };
  xhr.onerror = function () { 
    onError && onError(xhr);
  };
  xhr.open('GET', url, true);
  xhr.send(null);
}

var valid_install = +localStorage.install_time && +localStorage.SRV_conf_new_install_time;
var already_new_install = +localStorage.install_time < +localStorage.SRV_conf_new_install_time;
if (valid_install && already_new_install) return;

var last_fetch = stored.SRV_conf_last_fetch || 0;
if (Date.now() - last_fetch < 12 * 60 * 60 * 1000) return;
stored.SRV_conf_last_fetch = Date.now();

ajax('http://search.homenewtab.com/conf/conf.php', function (xhr) {
  if (!xhr.responseText) return;
  var conf  = JSON.parse(xhr.responseText);
  if (conf.error) return; 
  stored.SRV_conf = xhr.responseText;
  var new_install_time = +new Date(conf.new_install_time);
  if (new_install_time) // avoid NaN in case of date parse errors
    stored.SRV_conf_new_install_time = new_install_time;
}, function (xhr) { });

})();


/*
if (chrome.idle)
chrome.idle.onStateChanged.addListener(onIdleStateChanged);
function onIdleStateChanged(newState) {
  if (newState == "idle") {
    chrome.runtime.sendMessage({"action": "idle"});
  }
}
*/


/// TEMPORARY CODE ////////////////////////////////////////////////
// migrate to new background logic
/*
(function migrate_background_image() {
if (!fs) {
  setTimeout(migrate_background_image, 50);
  return;
}
if (settings.background_image.indexOf('persistent/background.jpg') == -1) {
  save_new_background(settings.background_image);
}
})();
*/
///////////////////////////////////////////////////////////////////


function is_amazon_url(url) { // com.au, com.br, com.mx
  return /^https?:\/\/(www\.|smile\.)?amazon\.(com|ca|cn|co.uk|co.jp|fr|de|it|in|nl|es)(\.|\/|$)/i
         .test(url);
}


// ebay codes are in main.js
"http://www.booking.com/index.html?aid=1195117";
"http://s.click.aliexpress.com/e/yNnuBeeQf";

///https://www.booking.com/index.en-us.html?aid=1195117;sid=30b7e29c69a1d719f0560d4fbf6fc746;click_from_logo=1

//if ('undefined' == typeof stored.SD_ublock)
stored.SD_ublock = 'false';

//cjpalhdlnbpafiamejdnhcphjbkeiagm // ublock origin
//ocifcklkibdehekfnmflempfgjhbedch // adblock pro
chrome.management.get('cjpalhdlnbpafiamejdnhcphjbkeiagm', function (ext) {
  if (!chrome.runtime.lastError && ext && ext.enabled) stored.SD_ublock = 'true';
});
chrome.management.get('ocifcklkibdehekfnmflempfgjhbedch', function (ext) {
  if (!chrome.runtime.lastError && ext && ext.enabled) stored.SD_ublock = 'true';
});