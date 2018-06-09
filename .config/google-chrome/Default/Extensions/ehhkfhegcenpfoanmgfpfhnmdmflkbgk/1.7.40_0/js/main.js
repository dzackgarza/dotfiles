
// Copyright (c) 2015 Balázs Galambosi (galambalazs@yahoo.co.uk)

function byId(id, base) { return (base||document).getElementById(id); }
function bySelector(sel, base) { return (base||document).querySelector(sel); }
function bySelectorAll(sel, base) { return (base||document).querySelectorAll(sel); }
function bench(text) { console.log( (text||"") + ": " + (+new Date - start) ); }

var stored = localStorage;
//var settings = stored.settings ? JSON.parse(stored.settings) : default_settings;
var html = document.documentElement;
window.requestAnimationFrame = window.requestAnimationFrame || 
                               window.webkitRequestAnimationFrame;

var bg = chrome.extension.getBackgroundPage();
var apps;
var ordered = [];
var tabs = {};
var tabs_history = {};
var recently_closed_tabs = new Array(10);
var page = byId("page");
var ITEM_SEPARATOR = "\\c";
var FIELD_SEPARATOR = "\\a";
var start = +new Date;
var last_sound = +new Date;
var MAX_NOTIFICATIONS = 10; // shown / stored
var MAX_NOTIFICATIONS_SHOWN = 10; // shown / stored
var MIDDLE_BUTTON = 1;
var RIGHT_BUTTON  = 2;


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


window.$ = function (sel, ctx) { return (ctx||document).querySelectorAll(sel); }
NodeList.prototype.__proto__ = Array.prototype;

Node.prototype.on = window.on = function (name, fn, capture) {
  this.addEventListener(name, fn, capture)
};
Node.prototype.off = window.off = function (name, fn, capture) {
 this.removeEventListener(name, fn, capture)
};
Node.prototype.remove = function () {
 this.parentNode && this.parentNode.removeChild(this);
};
  
NodeList.prototype.on = 
NodeList.prototype.addEventListener = function (name, fn, capture) {
  this.forEach(function (elem, i) {
    elem.on(name, fn, capture)
  });
};
NodeList.prototype.off = 
NodeList.prototype.removeEventListener = function (name, fn, capture) {
  this.forEach(function (elem, i) {
    elem.off(name, fn, capture)
  });
};


function bindNextTick(fn, thisArg, args) {
  return function () { setTimeout(fn, 1) }; 
}

function easing(pos){ return (-Math.cos(pos*Math.PI)/2) + 0.5; }

function rec() {
  launch_app_animation(rec)
}
//rec();

function launch_app_animation(callback) {
  setTimeout(callback,1); return; ///

  var el = $('.open-app')[0];
  var overlay = $('.open-app-overlay')[0];

  //el.style.cssText += "; top:0; right:0; bottom:0; left:0;";
  el.style.display = "block";
  overlay.style.display = "block";

  var start = +new Date;
  var duration = 3000//300;

  function step(timestamp) {
    timestamp || (timestamp = +new Date);
    var pos  = (timestamp - start) / (duration) + 0.1;
    var pos2 = (timestamp - start) / (duration*0.5) + 0.05;
    var pos3 = (timestamp - start) / (duration);
    pos  = pos  < 1 ? pos  : 1;
    pos2 = pos2 < 1 ? pos2 : 1;
    pos2 = pos3 < 1 ? pos3 : 1;
    var percentage = (50 - easing(pos) * 50) + "%";
    el.style.top    = percentage
    el.style.right  = percentage;
    el.style.bottom = percentage;
    el.style.left   = percentage;
    el.style.opacity = easing(pos2);
    overlay.style.opacity = easing(pos3);
    if (pos < 1) {
      requestAnimationFrame(step);
    }
    else setTimeout(callback,1);
  }
  requestAnimationFrame(step);
}

function get_domain(url) {
  return url.split("/")[2];
}

function hide_overlays() {
  var overlay_foreground = $('.open-app')[0];
  var overlay_background = $('.open-app-overlay')[0];
  overlay_foreground.style.display = "none";
  overlay_background.style.display = "none";
}

function select_tab(id) {
  chrome.tabs.update(id, {active: true});
}

function launch_app(el, new_tab) {

  var url   = turn_tags_in_url(el.dataset.url);
  var app   = apps[el.id];
  var newTabId = app.tabId;

  // we have a running tab for the app
  if (newTabId) {
    launch_app_animation(function(){
      select_tab(newTabId);
      hide_overlays();
    });
    return;
  }

  function create_tab(url) {
    chrome.tabs.create({
      url: url,
      active: false
    }, function(tab) {
      newTabId = tab.id;
    });
  }

  // different ways to open the app
  logAppLaunchURLForApp(app, function () {
    if (!url)
      chrome.management.launchApp(app.id);
    else if (new_tab)
      create_tab(url);
    else 
      chrome.tabs.update({url: url});
  });

  /*
  launch_app_animation(function(){
    app.tabId = newTabId;
    app.domain = get_domain(url);
    tabs[newTabId] = app;

    //create_tab();

    select_tab(newTabId);
    hide_overlays();
  });
  */
}


chrome.extension.onMessage.addListener(function(message) {
  if (message.type == 'rpc' && 'function' == typeof window[message.name])
    window[message.name].apply(window, message.args);
});

function set_indicator(id, count) {
  var key = "indicator-" + id;
  var el = byId(key);
  if (!el) 
    return setTimeout(function () { set_indicator(id, count) }, 1000);
  el.innerHTML = count;
  if (+count)
    el.style.display = "block";
  else
    el.style.display = "none";
  stored[key] = count;
  cache_set_app_html(el.parentNode);
}

function generate_indicator(name) {
  var count = +stored["indicator-"+name];
  var style = count ? "display:block" : "";
  return '<div class="indicator" id="indicator-'+name+'" style="'+style+'">'+ count +'</div>';
}

function create_notification(icon, title, body) {

  /*
  if (icon == 'tweet' && +new Date - last_sound > 1000)  {
    last_sound = +new Date;
    byId('twittersound', bg.document).currentTime = 0;
    byId('twittersound', bg.document).play();
  }
  */

  icon = ICONS[icon] || icon;

  // update UI
  var container = byId('notifications');
  var items = $('.box-text', container);
  var item = document.createElement('div');
  item.className = 'box-text';
  item.style.opacity = 0;
  item.innerHTML = '<img src="'+ icon +'" class="ticker-icon" /><div class="bd"><strong>'+ title +'</strong> '+ body + '</div>';
  container.insertBefore(item, container.firstChild);
  if (items.length > MAX_NOTIFICATIONS_SHOWN) {
    container.removeChild(container.lastChild);
  }

  // notification animation

  // start at zero height
  var height = item.offsetHeight;
  item.style.webkitTransition = "none";
  item.style.height = 0;
  //item.style.webkitTransform = "rotateX(90deg)";

  // open up and fade in
  setTimeout(function(){
    item.style.webkitTransition = "";
    item.style.height = height + "px";
    item.style.opacity = 1;
    //item.style.webkitTransform = "";
  }, 10);

  // reset auto height after animation finished
  item.on("webkitTransitionEnd", function transitionEnd(e) {
    if (e.propertyName == "height") {
      item.off("webkitTransitionEnd", transitionEnd);
      item.style.webkitTransition = "none";
      item.style.height = "";
    }
  });
}

function play_notification_sound(type) {
}

function show_recent_notifications() {
  var container = byId('notifications');
  var notifications = stored.notifications.split(ITEM_SEPARATOR);
  var max = Math.min(notifications.length, MAX_NOTIFICATIONS_SHOWN);
  var html = "";
  if (!notifications[0]) return;
  for (var i = 0; i < max; i++) {
    var parts = notifications[i].split(FIELD_SEPARATOR);
    html += '<div class="box-text"><img src="'+ parts[0] +'" class="ticker-icon" /><div class="bd"><strong>'+ parts[1]  +'</strong> '+ parts[2]  + '</div></div>';
  }
  container.innerHTML = html;
}

function clickable_links() {}

function save_ordered() {
  stored.icons_order = ordered.join(',');
}

function load_ordered() {
  if (stored.icons_order)
    return stored.icons_order.split(',');
}

//var shadow = '<img class="sb-shadow sb-el" alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADMAAAAzCAYAAAA6oTAqAAABzElEQVR42u3a3Y6DIBCG4f6IUpEF3b3/a10OTD7DaKYMtc5uNXnPNuk+AdIKXCqe627t/FwVtBvittK9ohuNR8kR/D/eSOOAchSPaFJmUfvCzKKGQ0kg9wzRvjGgUqUgOiKAtKnugFqA6AhVQ/SDtiHmUAgyWyBmVAjEKoiC6OjQUckWu1VUCxAZHYIh60QVhq4fHpONykNPGB0Gs7pWHtraXjv8FOsVYuzWVOOmWK8uYAyLyaaYUwZxmGoCjMJ4DF38+jFYNx+IGbQlwVjlGCvFeC2dmAzzpaUT858xQUsnJsNELUkxnXJMV4MZFVSNccowjsGQ9xm1GPnLGV6bQ2pSUMBrMzClewBeCcZL9gCwO4OpFlLfBxYwxZiNQIKh68an4kGQOH++e2bfjJ9q+I0WU9ObEFMq4jcZN8Xw8FMNoJAaF6iflwXEmArz53lmihWfAvQroAhUqnYUgIgrkJ47BSg6n8lGyGcoVPjdgQhiwIiUnc9c2CNAgPolCrDqfIboAWGOAgvPNM0KCjA0CHJzAFCE4c40RSCgZhhwtVkAZoQUwt8DAIrAaJYPf78OAAIBgmpvaCCzQw1ibmh80N0Z/beazvtmf/Em4C+GnVIq6T5d5wAAAABJRU5ErkJggg==" style="position: absolute;height: 160px;width: 160px;left: -15px;top: -10px;z-index: -1;">';
// height: 204px; width: 204px; left: -31px; top: -17px;
var blankSrc = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';

function get_app_html(app) {
  if (app.name.indexOf("Google ") > -1)
    app.name = app.name.replace('Google ', '');
  if (app.name == "Store")
    app.name = "Install apps";
  var name = app.name.length <  14 ? app.name : app.name.slice(0,12) + '.';
  var icon = (app.icons||[]).filter(function(icon){ return icon.size == 128; })[0];
  if (app.id == 'ejjicmeblgpmajnghnpcppodonldlgfn') {
    icon = get_calendar_icon() ;
  } else if (icon) {
    var style = icon.borderRadius ? 'style="border-radius:' + icon.borderRadius + 'px"' : '';
    var className = icon.borderRadius ? 'class="bordered"' : '';
    className = icon.borderRadius > 60 ? 'class="bordered circle"' : className;
    icon = '<img src="'+ icon.url +'" '+ className +' '+ style +'>';
  } else {
    icon = '<img src="'+ blankSrc +'">';
  }
  return '<div class="test-item" id="'+ app.id +'" data-url="'+ app.appLaunchUrl +'">' +
            (indicators[app.id] ? generate_indicator(indicators[app.id]) : '') +
            '<div class="test-item-launcher">' +
              icon +
            '<\/div>' +
            '<div class="test-item-text">' + name + '<\/div>' +
         '<\/div>';
}

function get_apps_page_html() {
  if (!ordered) return;

  var fragments = [];
  // build html (ignoring disabled apps)
  ///
  //for (var i = 0; i < ordered.length; i++) {
  //  var page_items = ordered[i];
  var page_items = ordered;
    for (var j = 0; j < page_items.length; j++) {
      var id  = page_items[j];
      var app = apps[id];
      // if the app got deleted (e.g.: Google removed it from the store)
      // we should ignore it
      if (!app) {
        //delete ordered[id]; 
        continue;
      }
      if (app.id == "pfpeapihoiogbcmdmnibeplnikfnhoge") {
        continue; ///original hotmail
      }
      var html = cache_get_app_html(app);
      if (!html) {
        html = get_app_html(app);
        cache_set_app_html(app, html);
      }
      fragments.push(html);
    }
  //}

  return fragments.join('');
}

function cache_set_app_html(app, html) {
  var id = (typeof app == 'string') ? app : app.id;
  html || (html = get_app_html(apps[id]));
  stored['app_html_' + id] = html;
}

function cache_get_app_html(app) {
  ///get_app_html(app);
  /// cachin turned off currently

  /// no caching for webstore (temporary)
  if (app.name == 'Store')
    return get_app_html(app);

  // no caching for live Calendar icon
  if (app.id == 'ejjicmeblgpmajnghnpcppodonldlgfn')
    return get_app_html(app);
  // everything else is fine
  var id = (typeof app == 'string') ? app : app.id;
  return stored['app_html_' + app.id];

}

function apps_init() {

  // GA error: getBackgroundPage is not a function 
  ///if ('function' == typeof chrome.extension.getBackgroundPage)
  ///above fix temporarily removed
    bg = chrome.extension.getBackgroundPage();

  // when launching the browser, wait for the bg page to be ready
  if (!bg || !bg.apps) {
    setTimeout(apps_init, 10);
    return;
  }

  apps = bg.apps;
  ordered = load_ordered();

  build_apps_pages();
}


function push_to_empty_index(array2d, item) {
  for (var i = 0; i < array2d.length; i++) {
    if (array2d[i].length < 20) {
      array2d[i].push(item);
      return;
    }
  }
  // new page, first item
  array2d[i] = [item];
}

function build_apps_pages() {
  var apps_page = byId('apps-pages-list');
  apps_page.innerHTML = get_apps_page_html();
  requestAnimationFrame(function () {
    if (window.draggable_init)
      window.draggable_init();
    else
      window.draggable_should_init_async = true; 
  });
}

function purge_html_cache() {
  delete stored.icons_order;
  if (!ordered) return;
  for (var i = 0; i < ordered.length; i++)
    delete stored['app_html_' + ordered[i]];
  chrome.extension.getBackgroundPage().location.reload();
  location.reload();
}

function dom_ready() {
  ///bench('ready');///
  refresh_date_loop();
  refresh_event_start();
  if (!settings.focus_mode) {
    apps_init();
    show_recent_notifications();
    //new ApplicationPanel(byId('apps-wrapper'));
  }
}

var months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

var days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];

function refresh_date() {
  var date = new Date;
  var minutes = prefix_with_zero(date.getMinutes());
  var hours = date.getHours();
  if (settings.time_format == '12') {
    hours = ((hours + 11) % 12 + 1);
  }
  if (!settings.focus_mode) {
    hours = prefix_with_zero(hours);
  }
  // date.toLocaleDateString().slice(0, -6);
  byId("date").innerHTML = days[date.getDay()] + ', ' + 
                           months[date.getMonth()] + ' ' + 
                           date.getDate();
  byId("time").innerHTML = hours + ":" + minutes;
  return date;
}

function refresh_date_loop() {
  var date = refresh_date();
  setTimeout(refresh_date_loop, (60 - date.getSeconds()) * SECONDS);
}

function prefix_with_zero(num) {
  return num < 10 ? '0' + num : ''+num;
}

function format_time(date) {
  var hours = date.getHours();
  var mins = date.getMinutes();
  var ampm = (hours < 12) ? 'AM' : 'PM';
  hours = ((hours + 11) % 12 + 1);
  return hours + ':' +  prefix_with_zero(mins) + ' ' + ampm;
}

// it assumes a date in the future (google calendar)
function format_day(date) {
  var today = new Date;
  if (today.toDateString() == date.toDateString()) {
    return 'Today';
  } 

  var tomorrow = new Date;
  tomorrow.setDate(tomorrow.getDate()+1);
  if (tomorrow.toDateString() == date.toDateString()) {
    return 'Tomorrow';
  } 

  var end_of_week = new Date()
  var day = today.getDay();
  end_of_week.setDate( 7 + today.getDate() - day + (day == 0 ? -6 : 1)  );
  end_of_week.setHours(0)
  end_of_week.setMinutes(0);
  if (+date < +end_of_week) {
    return days[date.getDay()];
  }

  var end_of_next_week = new Date(end_of_week)
  end_of_next_week.setDate( end_of_week.getDate() + 7 );
  if (+date < +end_of_next_week) {
    return 'Next ' + days[date.getDay()];
  }
}

function refresh_event_start() {
  // listen to all new events
  chrome.extension.onMessage.addListener(function(message){
     if (message.name == 'upcoming-event') {
        refresh_event(message.data)
     }
  });
  // fetch current calendar events
  chrome.extension.sendMessage("get-calendar-events", refresh_event);
}

function refresh_event(events) {

  if ('string' == typeof events && events == 'forbidden') {
    byId('upcoming-event').innerHTML = "Click To Enable<br>Calendar Events";
    byId('upcoming-event').classList.add('forbidden');
    return;
  }

  // calendar notifications turned off
  if (settings.notifications['ejjicmeblgpmajnghnpcppodonldlgfn'] === false) {
    byId('upcoming-event').innerHTML = "";
    return;
  }

  // no events found (or url is down)
  if (!events || !events.length) {  
    byId('upcoming-event').innerHTML = "";
    return;
  }

  byId('upcoming-event').classList.remove('forbidden');

  // everything is ok
  var event = events[0];
  event.start = new Date(event.startTime);
  event.end = new Date(event.endTime);

  var start = format_time(event.start);
  var end = format_time(event.end);
  var day = format_day(event.start);

  var arr = [];
  event.title && arr.push(event.title);
  // event.description  && arr.push(event.description);
  event.location  && arr.push(event.location);

  day && arr.push(day); /// NOTE: doesn't support multi-day events

  if (event.end - event.start != 86400000) {
    arr.push(start + ' - ' + end);
  } else {
    arr.push('All Day');
  }
  
  byId('upcoming-event').innerHTML = arr.join('<br/>');
  byId('upcoming-event').href = event.url;
}

byId('upcoming-event').onclick = function () {
  if (byId('upcoming-event').classList.contains('forbidden')) {
    chrome.extension.sendMessage("prompt-calendar-auth");
  }
}


if (/interactive|complete/.test(document.readyState)) {
  dom_ready();
} else {
  window.on("DOMContentLoaded", dom_ready);
}


function get_calendar_icon() {

  var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var date = new Date;

  var week_day = days[date.getDay()];
  var year = date.getFullYear();
  var month = months[date.getMonth()];
  var month_day = date.getDate();

  return '<div id="cal-icon-overlay"></div>' +
         '<div id="cal-icon">' +
          '<div id="cal-icon-content">' +
            '<div id="cal-icon-header">'+ month +'</div>' +
            '<div id="cal-icon-month-day">'+ month_day +'</div>' +
            '<div id="cal-icon-week-day">'+ week_day +'</div>' +
          '</div>' +
        '</div>';
}

byId("qnote-text").onfocus = function(e) {
  byId("qnote-editor").style.opacity = 1;
}

byId("qnote-text").onblur = function(e) {
  byId("qnote-editor").style.opacity = 0;
}

byId("qnote-editor").onmousedown = function(e) {
  e.preventDefault();
}
byId("qnote-editor").onclick = function(e) {
  byId("qnote-text").focus();
  var cmd = e.target.dataset.cmd;
  if (cmd)
    document.execCommand (cmd, false, null);
}


//
// Context menu (panel)
//

var apps_el = byId('apps-wrapper');
apps_el.on("contextmenu", context_click);
apps_el.on("mouseenter", load_context_menu_css);
var panel = $('.panel')[0];
panel.style.display = "none";
panel.on("click", panel_click);

function load_context_menu_css() {
  loadCSS('css/context_menu.css', 'context-menu-css');
}

function panel_click(e) {
  var id = panel.dataset.appid;
  var action = e.target.innerHTML;
  var className = e.target.className;
  var app = apps[id];
  var appLaunchUrl = turn_tags_in_url(app.appLaunchUrl);
  if (id) {
    if (className == 'panel-app-name' || className == 'panel-app-new-tab') {
      chrome.tabs.create({ 'url': appLaunchUrl, active: false });
    }
    else if (action == "Options") {
      if (app.optionsUrl)
        chrome.tabs.create({ 'url': app.optionsUrl });
    }
    else if (action == "Hide") {
      /// TODO: ...
    }
    else if (action == "Remove") {
      /// TODO: prompt, animation
      hide_panel();
      var after_uninstall = function () {
          bg.onUninstalled(id);
          window.location.hash = '#page=' + get_current_page();
          location.reload();
      }
      if (confirm('Remove "' + apps[id].name + '"?')) {
        if (id.indexOf('user_app') != -1)
          after_uninstall();
        else
          chrome.management.uninstall(id, after_uninstall);
      }
    }  
    else if (action == "Edit") {
      hide_panel();
      show_new_app_panel(function (iframe) {
        iframe.addEventListener('load', function () {
          var msg = {name: 'startEditingApp', app: app};
          iframe.contentWindow.postMessage(msg, '*');
        });
      });
    }
  }
}

function closestClass(el, className) {
  do {
    if (el.classList && el.classList.contains(className)) 
      return el;
  } while ((el = el.parentNode));
}

function context_click(e) {
  if (!e.button == RIGHT_BUTTON) return;
  // it was a click on an icon
  var el = closestClass(e.target, 'test-item');
  if (el) {
    var app = apps[el.id];
    var isUserApp = app.id.indexOf('user_app') != -1;
    panel.dataset.appid = el.id;
    panel.innerHTML = '' +
      //'<li class="panel-app-name">'+ app.name +'</li>' +
      '<li class="panel-app-name">Open in New Tab</li>' +
      (app.optionsUrl ? '<hr /><li>Options</li>' : '') +
      //'<li class="disabled">Hide</li>' +
      '<hr />' +
      (isUserApp ? '<li>Edit</li>' : '') +
      '<li>Remove</li>';

    panel.style.left = e.pageX + 'px';
    panel.style.top = e.pageY  + 'px';
    loadPanelsCSS(); 
    setTimeout(show_panel, 1);
    e.preventDefault();
  } else {
    hide_panel();
  }
}

function hide_panel() {
  panel.style.webkitTransition = "opacity .2s ease-out";
  panel.style.opacity = 0;
  setTimeout(function(){
    panel.style.display = "none";
  }, 200)
}

function show_panel() {
  panel.style.webkitTransition = "";
  panel.style.opacity = 1;
  panel.style.display = "block";
}


document.on("click", hide_panel);
document.on("keydown", hide_panel);
//chrome.management.getAll(function(apps_arr) {
//  console.dir(apps_arr);
//});


// Element.prototype.closest polyfill
(function (ELEMENT) {
  ELEMENT.matches = ELEMENT.matches || ELEMENT.mozMatchesSelector || ELEMENT.msMatchesSelector || ELEMENT.oMatchesSelector || ELEMENT.webkitMatchesSelector;
  ELEMENT.closest = ELEMENT.closest || function closest(selector) {
    var element = this;
    while (element) {
      if (element.matches(selector)) break;
      element = element.parentElement;
    }
    return element;
  };
}(Element.prototype))

// launch app w click
document.on("mouseup", function(e) {
  if (e.button == RIGHT_BUTTON) return true;
  var item = e.target.closest('.test-item');
  if (item) {
    var new_tab = (e.button == MIDDLE_BUTTON || e.ctrlKey);
    launch_app(item, new_tab);
    if (!new_tab) item.classList.add('pressed');
    // some apps may not launch in a diff window
    setTimeout(function () { // so remove .pressed
      item.classList.remove('pressed');
    }, 3000)
    return false;
  }
});

byId("time").onclick = function(e) {
  settings.time_format = (settings.time_format == '12') ? '24' : '12';
  refresh_date();
  save_options();
}

byId("clear-notifications").onclick = function(e) {
  byId('notifications').innerHTML = '';
  stored.notifications = '';
}

function save_options() {
  stored.settings = JSON.stringify(settings);
}

chrome.extension.onMessage.addListener(function(message) {
  if (message.name == "add_new_app" && message.id) {
    apps = bg.apps;
    var app = apps[message.id];
    html = get_app_html(app);
    cache_set_app_html(app, html);

    add_new_app_html(html);

    if (message.id.indexOf('user_app') == 0) {
      hide_new_app_panel();
    }
    go_last_page && go_last_page();
    logAppInstallURLForApp(app);
  }
  else if (message.name == "edit_app" && message.id) {
    apps = bg.apps;
    var app = apps[message.id];
    html = get_app_html(app);
    cache_set_app_html(app, html);
    replace_app_html(byId(message.id), html);
    hide_new_app_panel();
  }
});

function logAppInstallURLForApp(app) {
  var type = (app.id.indexOf('user_app') != -1) ? 'custom' : 'system';
  var domain = shortURLHost(app.appLaunchUrl) || app.id;
  ga('send', 'event', 'apps', type, domain);
}

function logAppLaunchURLForApp(app, cb) {
  var type;
  if (app.id.length == 32) 
    type = 'chrome';
  else 
    type = (app.id.indexOf('user_app') != -1) ? 'user' : 'system';
  var url = app.appLaunchUrl;
  var domain = shortURLHost(app.appLaunchUrl) || app.id;
  if (isFbqImportantTile(app, domain)) {
    fbq('track', 'TileClick', { id:app.id, name:app.name, domain:domain, url:url,
                                country:stored.GEO_country_code });
    adw('TileClick');
  }
  ga_cb('clickTracker.send', 'event', 'tile-click', domain, type + ' ## ' + url, cb);
}

function shortURLHost(url) { // https://ebay.com/something?key=val#hash
  if (!url) return url;
  var protocolless = url.split('://').pop();
  var parts = protocolless.split(/[?#]/)[0].split('/'); // [ebay.com, something]
  var domain = parts[0].toLowerCase().replace(/^www\./i, '');
  var firstPath = parts[1];
  if (firstPath && !/index/i.test(firstPath))
    domain += '/' + firstPath;
  return domain;
}

function isFbqImportantTile(app, domain) {
  if (/^(ebay|aliexpress|booking|amazon)$/i.test(app.id))  return true;
  if (/(^ebay|aliexpress|booking|amazon)\./i.test(domain)) return true;
  return false;
}

//
// Toolbar
//

make_toolbar_label_for_button(byId('focus-button'), on_focus_click);
make_toolbar_label_for_button(byId('background-button'));
make_toolbar_label_for_button(byId('notifications-button'));
make_toolbar_label_for_button(byId('qnotes-button'));
update_focus_button_title();

function on_focus_click() {
  settings.focus_mode = !settings.focus_mode;
  save_options();
  update_focus_button_title();
  if (settings.focus_mode) {
    document.documentElement.classList.add('focus');
    refresh_date();
  } else {
    location.reload();
    // in-app refresh would need more work (e.g. icons are not positioned)
    //document.documentElement.classList.remove('focus'); 
  }
}

function update_focus_button_title() {
  byId('focus-button').dataset.title = settings.focus_mode ? 'Leave Focus' : 'Focus';
}

function make_toolbar_label_for_button(button, onclick) {

  var toolbarButtonLabel = document.createElement('div');
  toolbarButtonLabel.className = 'toolbar-button-label';
  toolbarButtonLabel.style.opacity = 0;
  var hideAnimationTimeout;

  button.onmouseover = function () {
    if (!button.dataset.title) return;
    clearTimeout(hideAnimationTimeout);
    document.body.appendChild(toolbarButtonLabel);
    var myVCenter = toolbarButtonLabel.offsetHeight / 2;
    var focusVCenter = button.offsetTop + (button.offsetHeight/2);
    var myLeft = button.offsetLeft +  button.offsetWidth;
    toolbarButtonLabel.innerHTML = button.dataset.title;
    toolbarButtonLabel.style.top = (focusVCenter - myVCenter) + 'px';
    toolbarButtonLabel.style.left =  (myLeft + 24) + 'px';
    toolbarButtonLabel.style.opacity = 1;
  }

  button.onmouseleave = function () {
    toolbarButtonLabel.style.opacity = 0;
    hideAnimationTimeout = setTimeout(function () {
      toolbarButtonLabel.parentNode.removeChild(toolbarButtonLabel);
    }, 1000);
  }

  button.onclick = onclick;
}

// Draggable doesn't know about the search bar,
// so for loose coupling sake we handle that case here
(function () {
var is_scrolling = false;
document.on('keydown', function onkeydown(e) {
  var is_empty_input = (e.target.nodeName == 'INPUT' && !e.target.value);
  if (!is_scrolling && is_empty_input) {
    if (e.keyCode == 37)
      window.go_previous_page();
    if (e.keyCode == 39)
      window.go_next_page();
    is_scrolling = true;
    setTimeout(function() {
      is_scrolling = false;
    }, 300);
  }
});
})();


//
// Whatever Left At The End
//

// remove old Lorem ipsum notes
chrome.runtime.onInstalled.addListener(function (details) {
  if (details.reason == 'update') {
    if (stored.notes1.indexOf('Lorem ipsum') > -1) {
      delete stored.notes1;
    }
  }
});


chrome.extension.sendMessage({"name": "pageview"});
fbq('track', 'PageView', {content_name: 'Main', country: stored.GEO_country_code});

//// if is TEMP until tile click test
if ('true' == stored.testing_tiles_active)
  ga('clickTracker.send', 'pageview', { page: 'main.html' });


/*
setTimeout(function () {
  var img = document.createElement('img');
  img.src = "filesystem:chrome-extension://medcogigaddopcmahlhefiiabkklihoa/persistent/not-existing.png";
  document.body.appendChild(img);
}, 500);
*/

// "filesystem:chrome-extension://medcogigaddopcmahlhefiiabkklihoa/persistent/not-existing.png";
(function () {

if ('true' == stored.missing_images_help_shown) return;

function show_missing_images_badge() {
  var el = document.createElement('div');
  el.id = 'missing-images-help';
  el.className = 'helpful-message clickable';
  el.innerHTML = 'missing images?';
  el.style.cursor = 'pointer';
  el.onclick = show_missing_images_detailed_help;
  byId('search-form').appendChild(el);
}

function hide_missing_images_badge() {
  var el = byId('missing-images-help');
  if (el) el.parentNode.removeChild(el);
}

function show_missing_images_detailed_help() {
  hide_missing_images_badge();
  stored.missing_images_help_shown = 'true';
  stored.missing_images_help_shown_date = Date.now();
  window.location = "/questions.html#missing-images";
}

var missing_image_counter = 0;
document.on('error', function (e) {
  if (e.target.nodeName == 'IMG' && e.target.src.indexOf('filesystem:') === 0)
    if (++missing_image_counter == 2)
      show_missing_images_badge();
}, true);

})();


if (stored.SS_discrete_mouse_wheel == 'true' && 
    stored.SS_promo_clicked != 'true') {
  include_js('js/temp/sscr_promo.js');
}


/*
chrome.management.onInstalled.addListener(function(app) {
  if (app.isApp) {
    chrome.tabs.query({ currentWindow: true, active: true }, function(array) {
      console.dir(array[0])
    })
    window.location.hash = "#last";
    location.reload();
  }
});
*/


function loadCSS(src, id) {
  id = id || src;
  if (id && byId(id)) return;
  var css  = document.createElement('link');
  css.id   = id;
  css.rel  = 'stylesheet';
  css.type = 'text/css';
  css.href = src;
  document.head.appendChild(css);
}

function include_js(url, callback) {
  var script = document.createElement('script');
  script.onload = callback;
  script.src = url;
  document.head.appendChild(script);
}

if ('undefined' == typeof stored.test_facebook_tile_1 && stored.GEO_country_code)
  stored.test_facebook_tile_1 = (Math.random() < 0.3 && 'US' == stored.GEO_country_code);

function turn_tags_in_url(url) {
  if (is_ebay_url(url))
    return turn_tag_ebay(url);
  if (is_facebook_url(url) && is_facebook_testing() && !is_ublock())
    return turn_tag_facebook(url);
  //if (is_aliexpress_url(url))
  //  url = turn_tag_aliexpress(url);
  if (is_booking_url(url) && !is_ublock())
    return turn_tag_booking(url);
  //if (is_amazon_url(url))
  //  url = turn_tag_amazon(url);
  return url;
}

function is_facebook_testing () { return 'true' == stored.test_facebook_tile_1; }
function is_ublock() { return 'true' == stored.SD_ublock; }

function is_ebay_url(url) { 
  return /^https?:\/\/(www\.)?ebay\.(com|com\.au|ca|co\.uk|at|be|fr|de|it|nl|es|ch|ie)(\/|$)/i.test(url);
} 

// http://rover.ebay.com/rover/1/711-53200-19255-0/1?icep_ff3=1&pub=5575232646&toolid=10001&campid=5337987822&customid=&ipn=psmain&icep_vectorid=229466&kwid=902099&mtid=824&kw=lg
function turn_tag_ebay(url) { 
  try {
    var match;
    var ebayRe = /^https?:\/\/(?:www\.|deals\.|stores\.|)ebay\.([^\/]+)/i;
    if ((match = url.toLowerCase().match(ebayRe))) {
      var domain = match[1].toUpperCase();
      var codes  = ebayCodesForCountry[domain];
      if (!codes) {
        var country = localStorage.GEO_country_code;
        codes = ebayCodesForCountry[country] || ebayCodesForCountry['US'];
      }
      return 'http://rover.ebay.com/rover/1/' + codes[0] +
             //'/1?icep_id=114&ipn=icep&toolid=20004&campid=5337987822' + 
             '/1?icep_ff3=1&pub=5575232646&toolid=10001&campid=5337987822' + 
             '&customid=&ipn=psmain&icep_vectorid=' + codes[1] + 
             '&kwid=902099&mtid=824&kw=lg';
             //'&mpre=' + encodeURIComponent(url);
    }
  } catch (e) { 
    setTimeout(function () { throw e; }); // async error logging
  }
  return url;
}

// https://partnernetwork.ebay.com/epn-blog/2009/05/new-link-generator-tool-additional-information
var ebayCodesForCountry = { // Site Rotation ID, Vector ID
  "US": ["711-53200-19255-0",  "229466"],
  "CA": ["706-53473-19255-0",  "229529"],
  "UK": ["710-53481-19255-0",  "229508"],  "CO.UK": ["710-53481-19255-0",  "229508"],
  "AU": ["705-53470-19255-0",  "229515"], "COM.AU": ["705-53470-19255-0",  "229515"],
  "AT": ["5221-53469-19255-0", "229473"], 
  "BE": ["1553-53471-19255-0", "229522"],
  "FR": ["709-53476-19255-0",  "229480"],
  "DE": ["707-53477-19255-0",  "229487"], 
  "IT": ["724-53478-19255-0",  "229494"],
  "NL": ["1346-53482-19255-0", "229557"],
  "ES": ["1185-53479-19255-0", "229501"], 
  "CH": ["5222-53480-19255-0", "229536"], 
  "IE": ["5282-53468-19255-0", "229543"], 
};



function is_aliexpress_url(url) { 
  return url.indexOf('https://s.click.aliexpress.com/e/') == 0;
} 

function is_booking_url(url) { 
  return url.indexOf('https://www.booking.com/index.html?aid=') == 0;
} 

function turn_tag_aliexpress(url) { 
  if ('US' == localStorage.GEO_country_code)
    url = "https://s.click.aliexpress.com/e/AQ76uNz";
  return url;
}

function turn_tag_booking(url) { 
  //if ('US' == localStorage.GEO_country_code)
  //  url = "https://www.booking.com/index.html?aid=1195099";
  url = 'http://homenewtab.ampxdirect.com/booking';
  return url;
} 

// leaves smile subdomain alone
function is_amazon_url(url) { // com.au, com.br, com.mx
  return /^https?:\/\/(www\.|)amazon\.(com|ca|cn|co.uk|co.jp|fr|de|it|in|nl|es)(\.|\/|$)/i
         .test(url);
}

function turn_tag_amazon(url) { 
  try {
    var match;
    var amznRe = /^https?:\/\/(?:www\.)?amazon(\.[^\/]+)/i;
    if ((match = url.toLowerCase().match(amznRe))) {
      var matchedTLD = match[1];
      if (matchedTLD != '.com') return url;
      var country = localStorage.GEO_country_code || 'US';
      var localTLD = amazonTLDsForCountry[country];
      if (!localTLD) return url;
      return url.replace('amazon.com', 'amazon.' + localTLD);
    }
  } catch (e) { 
    setTimeout(function () { throw e; }); // async error logging
  }
  return url;
}

var amazonTLDsForCountry = { 
  "US": "com",
  "CA": "ca",
  "UK": "co.uk",
  "AU": "com.au",
  "BR": "com.br",
  "MX": "com.mx",
  "JP": "co.jp",
  "FR": "fr",
  "DE": "de",
  "IT": "it",
  "NL": "nl",
  "ES": "es",
  "CN": "cn",
  "IN": "in",
};

function is_facebook_url(url) {
  return /^https?:\/\/(www\.)?facebook\.com\/?$/i.test(url);
}
function turn_tag_facebook(url) {
  return 'http://homenewtab.ampxdirect.com/facebook';
}


