
var SPACE = 32;
var HOME = 36;

window.DEV = (chrome.runtime.id != 'ehhkfhegcenpfoanmgfpfhnmdmflkbgk');

if (document.URL == 'http://www.homenewtab.com/welcome.html' && !window.DEV) {
  var timer = setInterval(function(){
    if (!document.head) return;
    clearInterval(timer);
    var el = document.createElement('link');
    el.id = 'ehhkfhegcenpfoanmgfpfhnmdmflkbgk-installed';
    document.head.appendChild(el);
  }, 10);
}

/*
window.addEventListener("keydown", function(e){
  if ((e.ctrlKey && e.keyCode == SPACE) || e.keyCode == HOME) {
    chrome.extension.sendRequest({name: "return-to-home"});
    e.preventDefault();
    return false;
  }
}, true);
*/

if (/search\.yahoo\.com$/.test(location.hostname) && 
    location.pathname == '/yhs/search' && 
    location.href.indexOf('gsp_hnt_00_') > -1) {
  document.addEventListener('click', function (e) {
    function logAC() { chrome.runtime.sendMessage({name: 'AdClick', provider: 'rhtab'}) }
    var el = e.target;
    // v1
    while (el && el.nodeName != 'A') el = el.parentNode;
    if (el && el.host && el.host.indexOf('r.bat.bing.com') > -1) 
      return logAC();
    if (el && el.dataset.sb && el.dataset.sb.indexOf('/beacon/cbclk') > -1)
      return logAC();
    // v2
    var adRex = /search(?:CenterTop|CenterBottom|RightBottom)Ads/;
    while (el && !adRex.test(el.className||'')) el = el.parentNode;
    if (el)
      return logAC();
  });
}

// if(.1<Math.random())return!0;
(function() {
  document.addEventListener("mousedown", function(a) {
    a = a.target;
    if (!a || !a.href || !/^https?:\/\/(www\.)?booking\.com/i.test(a.href)) return !0;
    chrome.runtime.sendMessage({
      name: "ga",
      arguments: ["clickTracker.send", "event", "tile-onsite-link", "booking.com", a.href]
    });
    if (!a || !a.href || !/^https?:\/\/(www\.)?booking\.com(\/index\.([^.]+\.)?html$|\/$|$)/i.test(a.href)) return !0;
    var b = a.href;
    a.href = "https://www.booking.com/index.html?aid=1195117";
    a.rel = "noreferrer";
    chrome.runtime.sendMessage({
      name: "ga",
      arguments: ["clickTracker.send", "event", "tile-onsite-click", "booking.com", "system ## " + b]
    })
  }, !1)
})();

(function() {
  document.addEventListener("mousedown", function(a) {
    a = a.target;
    if (!a || !a.href || !/^https?:\/\/(www\.)?ebay\.(com|com\.au|ca|co\.uk|at|be|fr|de|it|nl|es|ch|ie)\/?$/i.test(a.href)) return !0;
    chrome.runtime.sendMessage({
      name: "ga",
      arguments: ["clickTracker.send", "event", "tile-onsite-link", "ebay.com", a.href]
    })
  }, !1)
})();

/*
window.addEventListener("keydown", function(e){
  if ((e.ctrlKey && e.keyCode == SPACE) || e.keyCode == HOME) {
    chrome.extension.sendRequest({name: "return-to-home"});
    e.preventDefault();
    return false;
  }
}, true);
*/





