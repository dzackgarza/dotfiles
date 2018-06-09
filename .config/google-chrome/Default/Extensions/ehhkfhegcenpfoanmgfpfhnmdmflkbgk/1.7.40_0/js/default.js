var default_settings = {
  fetch_interval:     '5',
  time_format:        '24',
  background_image:    '../img/backgrounds/34.jpg',
  background_style:    'stretch',
  background_gradient: true,
  background_fadein:   true,
  notifications:       {},
  search_bar:          true,
  search_fullscreen:   true
}

var manifest = chrome.runtime.getManifest();

window.APP_ID = chrome.runtime.id;
window.APP_NAME = manifest.name;
window.APP_VERSION = manifest.version;
window.DEV = (window.APP_ID != 'ehhkfhegcenpfoanmgfpfhnmdmflkbgk');
window.SEARCH_ORIGIN = 'http://www.homenewtabsearch.com';
//window.SEARCH_ORIGIN = 'http://homenewtabsearch.com.s3-website-us-east-1.amazonaws.com';///
window.SEARCH_URL    = window.SEARCH_ORIGIN + "/?instant";

if (localStorage.cf_test_review == 'true') {
  window.SEARCH_URL = window.SEARCH_ORIGIN + "/cf/?instant";
}

var SECONDS = 1000;
var MINUTES = 60*SECONDS;
var HOURS   = 60*MINUTES;
var DAYS    = 24*HOURS;

var stored = localStorage;
var settings = {};
try {
  if (stored.settings) settings = JSON.parse(stored.settings);
} catch (e) {
  console.log('ERROR: settings has invalid JSON: ' + stored.settings);
  // throw new Error('...');
}
defaults(settings, default_settings);

function get_days_since_install() {
   return Math.floor((Date.now() - stored.install_time) / DAYS) || 0;
}

if (window.location.pathname == '/background.html') {

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  if (window.DEV) window['ga-disable-UA-2437922-29'] = true;
  if (window.DEV) window['ga-disable-UA-2437922-36'] = true;

  //function ga() { if (!window.DEV) return ga_real.apply(this, arguments); }

  ga('create', 'UA-2437922-29', 'auto', { 'anonymizeIp': true, 'allowLinker': true });
  ga('set', 'checkProtocolTask', null); // ext context
  ga('require', 'linker');
  ga('linker:autoLink', ['homenewtab.com']);
  ga('set', {
    'appName'    : window.APP_NAME,
    'appId'      : window.APP_ID,
    'appVersion' : window.APP_VERSION
  });

  ga('send', 'pageview', { page: 'background.html' });



  //// TEMP until tile click test ////////////////////////////////////////////
  (function () {
  var custom_apps_temp = {};
  try { custom_apps_temp = JSON.parse(stored.custom_apps||'{}'); } catch (e) { }

  if ('undefined' == typeof stored.test_tiles_group_1) { // 1
    var is_test_running = (typeof custom_apps_temp.ebay != 'undefined');
    stored.test_tiles_group_1 = is_test_running;
  }
  if ('undefined' == typeof stored.test_tiles_group_2) { // 2
    var group_2_addition = Math.random() < 0.10;
    stored.test_tiles_group_2 = ('true' == stored.test_tiles_group_1 || group_2_addition);
  }
  window.testing_tiles_active = ('true' == stored.test_tiles_group_2);
  if ('undefined' == typeof stored.test_tiles_group_3) { // 3
    var group_3_addition = Math.random() < 0.10;
    stored.test_tiles_group_3 = ('true' == stored.test_tiles_group_2 || group_3_addition);
  }
  stored.testing_tiles_active = stored.test_tiles_group_3;
  })();
  ///////////////////////////////////////////////////////////////////////


  ga('create', 'UA-2437922-36', 'auto', 'clickTracker');
  ga('clickTracker.set', 'checkProtocolTask', null); // ext context
  ga('clickTracker.set', {
    'appName'    : window.APP_NAME,
    'appId'      : window.APP_ID,
    'appVersion' : window.APP_VERSION
  });


  // fb
  if (!window.DEV) {
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    var days_since_install = get_days_since_install();
    fbq('init', '425558794490797'); 
    fbq('track', 'PageView', {
      content_name          : 'Background',
      country               : stored.GEO_country_code,
      app_version           : window.APP_VERSION,
      opt_search_bar        : settings.search_bar,
      install_time          : +stored.install_time || Date.now(),
      days_since_install    : days_since_install,
      lifetime_days         : days_since_install,
      lifetime_searches     : +stored.lifetime_searches || 0,
      avg_weekly_searches   : +stored.lifetime_searches / (days_since_install/7)  || 0,
      avg_monthly_searches  : +stored.lifetime_searches / (days_since_install/30) || 0,
      lifetime_ad_clicks    : +stored.lifetime_ad_clicks || 0,
      avg_weekly_ad_clicks  : +stored.lifetime_ad_clicks / (days_since_install/7)  || 0,
      avg_monthly_ad_clicks : +stored.lifetime_ad_clicks / (days_since_install/30) || 0,
   });
  } else { window.fbq = function () {}; }

  // g adwords
  include_js('https://www.googleadservices.com/pagead/conversion_async.js');
  var adw_labels = {
    'Search'    : 'EgpsCKvkjHEQ_a-14QM', 'AdClick' : 'ePV-CKfopXEQ_a-14QM', 
    'TileClick' : 'K1yJCOXljHEQ_a-14QM', 'Install' : 'MO4tCLb4iXEQ_a-14QM'
  };

  window.adw = function (name, value, currency) {
    var w = window;
    w.google_conversion_id = 1009604605;
    w.google_conversion_label = adw_labels[name] || name;
    w.google_remarketing_only = false;
    //w.google_conversion_value = 0.01;
    //w.google_conversion_currency = "USD";
    w.google_conversion_format = "3";
    var opt = { onload_callback: function(){} };
    if (typeof w.google_trackConversion == 'function') {
      w.google_trackConversion(opt);
    }
  };
  if (window.DEV) window.adw = function () {};

} else {
  window.ga = function () {
    chrome.runtime.sendMessage({ 
      name: 'ga', 
      arguments: [].slice.call(arguments) 
    });
  };
  window.ga_cb = function () { // last arg can be the callback function
    var args, cb;
    var lastArg = [].slice.call(arguments).pop();
    if ('function' == typeof lastArg) {
      args = [].slice.call(arguments, 0, -1);
      cb = createFunctionWithTimeout(lastArg, 1000);
    } else {
      args = [].slice.call(arguments);
    }
    chrome.runtime.sendMessage({ 
      name: 'ga_cb', 
      arguments: args
    }, cb);
  };
  window.fbq = function () {
    chrome.runtime.sendMessage({ 
      name: 'fbq', 
      arguments: [].slice.call(arguments) 
    });
  };
  window.adw = function () {
    chrome.runtime.sendMessage({ 
      name: 'adw', 
      arguments: [].slice.call(arguments) 
    });
  };
}

function save_options() {
  stored.settings = JSON.stringify(settings);
}

function defaults(a, b) {
  for (var i in b)
    if (!a.hasOwnProperty(i) && b.hasOwnProperty(i))
      a[i] = b[i];
  return a;
}

function createFunctionWithTimeout(callback, opt_timeout) {
  var called = false;
  function fn() {
    if (!called) {
      called = true;
      callback();
    }
  }
  setTimeout(fn, opt_timeout || 1000);
  return fn;
}

function include_js(url, callback) {
  var script = document.createElement('script');
  script.onload = callback;
  script.src = url;
  document.head.appendChild(script);
}
