/*

(function () {

if (/interactive|complete/i.test(document.readyState))
  init();
else
  window.addEventListener('DOMContentLoaded', init);

function init() {
  if (document.body.dataset.homeSearchBadge) return;
  document.body.dataset.homeSearchBadge = 'set';

  var css = document.createElement('link');
  css.rel="stylesheet";
  css.type="text/css";
  css.href=chrome.runtime.getURL('/css/search_badge.css');
  document.head.appendChild(css);

  var style = document.createElement('style');
  style.textContent = '.e_::before { content:"'+ getAdText() +'" }';
  document.head.appendChild(style);
}

function getAdText() {
  var adText = 'ad';
  try {
    var megaLabel = document.getElementById('megaLabel');
    var googAdText = megaLabel.getElementsByTagName('a')[0].textContent.trim();
    adText = googAdText.replace('Google', '').replace(/[-]/, ' ').trim();
    adText = adText.split(/\s/)[0]; // first word
    adText = capitalizeFirstLetter(adText);
  } catch (e) {}
  return adText;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

})();
*/

/*
{
     "matches": [ "*://cse.google.com/cse*" ],
     "js":  [ "js/search/search_badge.js" ],
     "run_at": "document_start",
     "all_frames": true
} 
*/