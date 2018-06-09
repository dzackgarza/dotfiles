
chrome.tabs.onCreated.addListener(function(tab) {
  //console.log(tab);
  tabs_history[tab.id] = []; 
});

chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {

  chrome.tabs.get(tabId, function(tab){
    if (!tab) return;
    // maintain 10 recently closed tabs
    recently_closed_tabs.pop();
    //recently_closed_tabs.unshift(tabs_history[tabId]);
    recently_closed_tabs.unshift(tab.url);
    delete tabs_history[tabId];
  })
  var app = tabs[tabId];
  if (app) {
    delete app.domain;
    delete app.tabId;
    delete tabs[tabId];
    delete bg.apps[app.id].tabId;
    bg.return_to_home();
  }
});

chrome.webNavigation.onDOMContentLoaded.addListener(function(details) {
  /*
  if (details.frameId == 0) {
    console.log(details.tabId + ": " + details.url)
  }
  */
});

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {

  //console.log(tabId + ": " + tab.status + " - " + tab.url + " - " + changeInfo.url)

  /// TODO: limit the number of history entries?
  if (changeInfo.url) {
    tabs_history[tabId] || (tabs_history[tabId] = []);
    tabs_history[tabId].push(changeInfo.url);
  }

  var app = tabs[tabId];
  if (app && changeInfo.url && get_domain(changeInfo.url) != app.domain) {
    delete app.domain;
    delete app.tabId;
    delete tabs[tabId];
  }
});



bg.return_to_home_hook = function(dataUrl, callback) {

  var overlay = document.getElementsByClassName('open-app-overlay')[0];
  overlay.style.opacity = 1;
  overlay.style.display = "block";

  //callback();
  //return;

  ///document.body.visibility = "hidden";
  var el = document.getElementById("screenshot-overlay");
  var img = document.createElement("img");
  el.style.cssText = "opacity:1; display:block;";

  //img.className = "screenshot";
  //img.src = dataUrl;
  //document.body.appendChild(img);
  //el.appendChild(img);
  el.style.backgroundImage = "url(" + dataUrl + ")";

  //page.style.visibility = "visible";
  callback();

  setTimeout(function(){

  var start = +new Date;
  var duration = 500;

  
  function step(timestamp) {
    timestamp || (timestamp = +new Date);
    var pos  = (timestamp - start) / (duration) + 0.1;
    var pos2 = (timestamp - start) / (duration*0.5) + 0.05;
    var pos3 = (timestamp - start) / (duration);
    pos  = pos  < 1 ? pos  : 1;
    pos2 = pos2 < 1 ? pos2 : 1;
    pos2 = pos3 < 1 ? pos3 : 1;
    var percentage = (easing(pos) * 50) + "%";
    el.style.top    = percentage
    el.style.right  = percentage;
    el.style.bottom = percentage;
    el.style.left   = percentage;
    el.style.opacity = 1 - easing(pos2);
    overlay.style.opacity = 1 - easing(pos3);
    if (pos < 1) {
      requestAnimationFrame(step);
    } 
    else {
      el.style.display = "none";
      overlay.style.display = "none";
    }
  }
  requestAnimationFrame(step);

  }, 10);
  
}
