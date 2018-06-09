
function byId(id, base) { return (base||document).getElementById(id); }

if (settings.search_bar) {
  document.documentElement.classList.add('show-search')
  //byId("search-box").style.display = "block";
  //byId("apps-slider").style.paddingTop = "54px";
}
if (settings.focus_mode) {
  document.documentElement.classList.add('focus');
}

(function () {

// kick off loading background image as soon as possible
var bg = settings.background_image;

// v1
//(new Image).src = settings.background_image;

// v2
//document.documentElement.style.backgroundImage = 'url(' + bg + ')';

// v3
(new Image).src = settings.background_image;
var css = document.createElement('style');
css.textContent = '#page { background:url('+ bg +') }';
document.head.appendChild(css);


//var bg = 'filesystem:chrome-extension://' + chrome.runtime.id + '/persistent/background.jpg';

// v4
/*
var img = new Image;
img.onload = img.onerror = function init_background() {
  if (/interactive|complete/i.test(document.readyState)) {
    //byId('page').style.backgroundImage = 'url(' + bg + ')';
    if (!settings.background_fadein) { // don't fade in
      prepare_background();
      show_background();
    } else {
      document.body.style.webkitTransition = 'opacity .5s';
      prepare_background();
      setTimeout(show_background, 1);
    }
  } else {
    window.addEventListener('DOMContentLoaded', init_background);
  }
};

img.src = bg;
*/
})();

function prepare_background() {
  change_background();
  change_background_style()
  change_background_gradient()
}

function show_background() {
  document.body.style.opacity = 1;
}


window.addEventListener('DOMContentLoaded', function () {
  change_background_style()
  ///change_background() // handled by style.css
  change_background_gradient()
  if (settings.background_fadein)
    change_background()
  else 
    show_background();
});


function change_background(crossfade) {
  var bg = settings.background_image;
  if (!settings.background_fadein) { // don't fade in
    byId('page').style.backgroundImage = 'url(' + bg + ')';
  } 
  else { // fade in
    document.body.style.opacity = 0;
    var img = new Image;
    img.onload = img.onerror = function() {
      //if (!crossfade) fadeIn();
      byId('page').style.backgroundImage = 'url(' + bg + ')';
      document.body.style.webkitTransition = 'opacity .5s';
      document.body.style.opacity = 1;
    };
    img.src = bg;
    //if (crossfade) setTimeout(fadeIn, 500);
  }
  //if (crossfade) {
  //  document.body.style.backgroundColor = '#000';
  //  //byId('page').style.webkitTransition = 'opacity .15s ease-in-out';
  //}
}

function change_background_gradient() {
  if (!settings.background_gradient) {
    byId('page-gradient').style.backgroundImage = 'none';
  } else {
    byId('page-gradient').style.backgroundImage = '';
  }
}

function change_background_style() {
  var page = byId('page');
  var style = settings.background_style;
  if ('fill' == style) {
    page.style.backgroundSize = 'cover';
    //page.style.backgroundRepeat = 'repeat';
  } else if  ('stretch' == style) {
    page.style.backgroundSize = '100% 100%';
  } else {
    page.style.backgroundSize = '';
  }
}

function clone(obj) {
  var copy = {};
  for (var i in obj)
    if (obj.hasOwnProperty(i))
      copy[i] = obj[i];
  return copy;
}

// preload images so the don't "blink'
(function () {
  var bg = chrome.extension.getBackgroundPage();
  if (!bg) return;
  var apps = bg.apps;
  if (!apps) return;
  var ordered = localStorage.icons_order.split(',');
  for (var j = 0; j < ordered.length; j++) {
      var id  = ordered[j];
      var app = apps[id];
      if (app && id.length != 32) {
        new Image().src = app.icons[0].url;
      }
  }
})();


/*
// Debug
document.addEventListener('load', function (e) {
  if ((e.target.src||'').indexOf('background') != -1)
  console.log(e.target.src)
}, true)
*/