
// Copyright (c) 2015 Balázs Galambosi (galambalazs@yahoo.co.uk)
var fullUrlRegex = /(?:(?:https?|ftp|chrome|chrome-extension):\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])/gi;

var nakedUrlRegex = /^[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\/?$/gi;

var suggestionsForShortcuts = {
  'google': 'google.com',
  'go': 'google.com',
  'g': 'google.com',
  'gmail': 'gmail.com',
  'gm': 'gmail.com',
  'youtube': 'youtube.com',
  'you': 'youtube.com',
  'yo': 'youtube.com',
  'facebook': 'facebook.com',
  'face': 'facebook.com',
  'fac': 'facebook.com',
  'fa': 'facebook.com',
  'f': 'facebook.com',
  'hotmail': 'hotmail.com',
  'amazon': 'amazon.com',
  'am': 'amazon.com',
  'a': 'amazon.com',
  //'google maps': 'https://www.google.com/maps',
  'maps': 'maps.google.com',
  //'google translate': 'https://translate.google.com/',
  'translate': 'translate.google.com',
  //'google drive': 'https://drive.google.com/drive/',
  'docs': 'docs.google.com',
  'drive': 'drive.google.com',
  'dr': 'drive.google.com',
  //'google calendar': 'https://www.google.com/calendar/',
  'calendar': 'calendar.google.com',
  'twitter': 'twitter.com',
  'tw': 'twitter.com',
  'yahoo': 'yahoo.com',
  'ya': 'yahoo.com',
  'ebay': 'ebay.com',
  'eb': 'ebay.com',
  'e': 'ebay.com',
  'reddit': 'reddit.com',
  'pinterest': 'pinterest.com',
  'linkedin': 'linkedin.com',
  'netflix': 'netflix.com',
  'instagram': 'instagram.com',
  'imdb': 'imdb.com'
};

var linksForShortcuts = {
  'google': 'https://www.google.com/',
  'go': 'https://www.google.com/',
  'g': 'https://www.google.com/',
  'gmail': 'https://mail.google.com/mail/u/0/#inbox',
  'gm': 'https://mail.google.com/mail/u/0/#inbox',
  'youtube': 'https://www.youtube.com/',
  'you': 'https://www.youtube.com/',
  'yo': 'https://www.youtube.com/',
  'facebook': 'https://www.facebook.com/',
  'face': 'https://www.facebook.com/',
  'fac': 'https://www.facebook.com/',
  'fa': 'https://www.facebook.com/',
  'f': 'https://www.facebook.com/',
  'hotmail': 'https://dub122.mail.live.com/default.aspx?rru=inbox',
  'amazon': 'http://www.amazon.com/',
  'am': 'http://www.amazon.com/',
  'a': 'http://www.amazon.com/',
  'google maps': 'https://www.google.com/maps',
  'maps': 'https://www.google.com/maps',
  'google translate': 'https://translate.google.com/',
  'translate': 'https://translate.google.com/',
  'google drive': 'https://drive.google.com/drive/',
  'docs': 'https://docs.google.com/',
  'drive': 'https://drive.google.com/drive/',
  'dr': 'https://drive.google.com/drive/',
  'google calendar': 'https://www.google.com/calendar/',
  'calendar': 'https://www.google.com/calendar/',
  'twitter': 'https://twitter.com/',
  'tw': 'https://twitter.com/',
  'yahoo': 'https://www.yahoo.com/',
  'ya': 'https://www.yahoo.com/',
  'ebay': 'http://www.ebay.com/',
  'eb': 'http://www.ebay.com/',
  'e': 'http://www.ebay.com/',
  'reddit': 'https://www.reddit.com/',
  'pinterest': 'https://www.pinterest.com/',
  'linkedin': 'https://www.linkedin.com/',
  'netflix': 'https://www.netflix.com/',
  'instagram': 'https://instagram.com/',
  'imdb': 'http://www.imdb.com/'
};


function suggest_init() {

  var throttle=function(){return function(d,a){a||(a=100);var b,c;return function(){if(b)c=true;else{var e=this,f=arguments;d.apply(e,f);b=setTimeout(function(){if(c){d.apply(e,f);c=false}b=null},a)}}}}();
  function debounce(func, wait, immediate) {
    var timeout;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  };
  function byId(id) { return document.getElementById(id); }

  var ajax_requests = {};
  var ajax_id = 0;
  var lastXhr;
  function ajax(url, callback) {
    ajax_id += 1;
    var xhr = new XMLHttpRequest();
    stop_last_request();
    lastXhr = xhr;
    ajax_requests[ajax_id] = xhr;
    xhr.onload = function () {
      callback(JSON.parse(xhr.responseText));
      delete ajax_requests[ajax_id];
    };
    xhr.open('GET', url, true);
    xhr.send(null);
  }

  function stop_last_request() {
    if (lastXhr) {
      lastXhr.onload = null;
      lastXhr.abort();
      lastXhr = null;
    }
  }

  function stop_all_requests() {
    stop_last_request();
    /*
    Object.keys(ajax_requests).forEach(function (key) {
      ajax_requests[key].onload = null;
      ajax_requests[key].abort();
    });
    ajax_requests = {};
    */
  }



  var q = document.forms['search-form'].p;
  q.parentNode.style.position = "relative";
  q.parentNode.style.padding = "0";
  q.type = "text";
  q.autocomplete = "off";

  var offsetLeft = q.offsetLeft;
  var offsetTop  = q.offsetTop;
  var suggestions = document.createElement("ul");
  suggestions.id = "suggestions";
  suggestions.style.visibility = 'hidden';
  //suggestions.style.top  = (offsetTop + 21) + "px";
  //suggestions.style.left = offsetLeft + "px";
  q.parentNode.appendChild(suggestions);

  var silver_suggest = document.createElement("div");
  silver_suggest.id = "silver-suggest";
  silver_suggest.style.top  = (offsetTop + 8) + "px";
  silver_suggest.style.left = (offsetLeft + 10) + "px";
  q.parentNode.appendChild(silver_suggest);


  function qsubmit(e) {
    search(e);
    //if (!e.defaultPrevented) {
      //document.forms["search-form"].submit();
      //chrome.extension.sendMessage({"name": "search-event"});
    //}
  }


  /*

  #suggestions    { width:301px; position:absolute; z-index:6; visibility:hidden; border:2px solid #f0f0f0; background:#222; opacity:0.96; border-radius:6px; -moz-border-radius:6px; box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); -moz-box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); -webkit-box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); }
  #suggestions ul { list-style-type:none; padding-top:5px; font-size:11px; }
  #suggestions li a,#suggestions li a:link,#suggestions li a:visited { display:block; cursor:default; font-weight:bold; color:#fff; text-decoration:none; padding:2px 5px; }
  #suggestions li a:hover, #suggestions li a.active { background:#c4c4c4; color:#000; text-shadow:0 0 0.1em #fff; }

  */

  window.addEventListener("click", function(e) {
    if (!e.target.nodeName != 'INPUT') {
      suggestions.style.visibility = 'hidden';
      silver_suggest.innerHTML = '';
    }
  }, false);

  var suggs = suggestions.getElementsByTagName('li');

  var is_first_keydown = true;

  // arrow keys
  function keydown(e) {

      initSearchIframe();
      // warm up initial connection and SSL
      /*if (is_first_keydown) {
        (new Image()).src = "https://homenewtab.com/blank.gif";
        is_first_keydown = false;
      }*/

      var key = e.keyCode;
    
      if (key == 13) {
        stop_all_requests();
        qsubmit(e);
        return false;
      } else {
        byId("search-results").style.display = "none";
      }

      // return if there ares no suggestions
      if (!suggestions.innerHTML) return true;
      
      // collect link elements  
      var len, i;
      
      // resume if needed
      if (suggestions.style.visibility === 'hidden') {
        suggestions.style.visibility = 'visible';
        console.log('resume: ' +  suggestions.style.visibility);
        return true;
      }

      //if ( key >= 65 && key <= 90 && !e.ctrlKey) {
      if ( key !== 8 && key !== 39 && key !== 40) {
        var term = this.value + String.fromCharCode(key+32);
        if (silver_suggest.innerHTML.indexOf(term) !== 0) 
          silver_suggest.innerHTML = "";
      }

      // handle event
      switch (e.keyCode) {  

          case 8: // backspace
            if (silver_suggest.textContent) {
              var term = this.value.slice(0, -1);
              silver_suggest.innerHTML = 
                  get_silver_suggest_html(term, silver_suggest.textContent);
            }
            return true;
          break;
      
          case 38: // up
          silver_suggest.innerHTML = '';
          len = suggs.length-1;
          for ( i = len+1; i--; ) {
            if ( suggs[i].className ) {
              suggs[i].className = "";
              if ( suggs[i-1] ) {
                suggs[i-1].className = "active";
                q.value = suggs[i-1].innerHTML;
                return false;
              }
            }
          } 
          suggs[len].className = "active";  
          q.value = suggs[len].innerHTML;
          break;  
            
          case 40: // down
          silver_suggest.innerHTML = '';
          for ( i = 0, len = suggs.length-1; i <= len; i++ ) {   
            if ( suggs[i].className ) {
              suggs[i].className = "";
              if ( suggs[i+1] ) {
                suggs[i+1].className = "active";
                q.value = suggs[i+1].innerHTML;
                return false;
              }
            }
          }   
          suggs[0].className   = "active";    
          q.value = suggs[0].innerHTML;
          break;   

   
          case 39: // right (siver-suggest)
          //q.value = suggestions.childNodes[0].textContent;
          q.value = silver_suggest.textContent;
          // request new suggestion
          keyup.call(vmeginput);
          break;
                    
          //case 13: // enter
          //qsubmit(e);
          //return false;
          
          case 27: // esc
          suggestions.style.visibility = "hidden";
          return false;

          default: return true;
       } // #end switch

      
      return false;
  }

  ///////////////////////////////////////////////////

  //
  // suggestions
  //

  function keyup(e) {
    
    var key = e.keyCode;

    // not (up|down|enter|esc|backspace)
    if ( key !== 38 && key !== 40 && key !== 13 && key !== 27) {
      
      var term = this.value;
      
      if (term) {

        // get suggestions and silver suggest
        var url = 'http://google.com/complete/search?client=firefox&q=' + 
                  encodeURIComponent(term);

        ajax(url, function(reponse) {

          var words = reponse[1].slice(0,5);
          suggestions.innerHTML = words.length ? "<li>" + words.join("</li><li>")  + "</li>" : "";
          suggestions.style.visibility = words.length ? "visible" : "hidden";

          // silver suggest
          var first_sugg = suggs.length ? suggs[0].innerHTML : '';
          if (first_sugg.indexOf(term) === 0) { //backpace is handled onkeydown
            //silver_suggest.innerHTML = first_sugg;
            silver_suggest.innerHTML = get_silver_suggest_html(term, first_sugg);
          } else {
            silver_suggest.innerHTML = "";
          }

          if (suggestionsForShortcuts[term]) {
            silver_suggest.innerHTML = get_silver_suggest_html(term, suggestionsForShortcuts[term]);
          }
        });

      } else {
        suggestions.style.visibility = "hidden";
        silver_suggest.innerHTML = "";
      }
      
      // prevent default
      return false; 
    }
  }

  q.onkeyup = keyup; // debounce(keyup, 100)
  q.onkeydown = keydown;

  function get_silver_suggest_html(term, first_sugg) {
    return "<span>" + first_sugg.slice(0, term.length) + "</span>" + 
            first_sugg.slice(term.length)
  }

  suggestions.onclick = function(e) {
    if (e.target.nodeName.toLowerCase() == 'li') {
      q.value = e.target.innerHTML;
      qsubmit(e);
    }
  }



  //
  // Real-time results
  //

  byId("search-button").onclick = function(e) {
    qsubmit(e);
  }
  //document.forms["search-form"].p

  function isValidIp(address) {
      var parts = address.split('://');
      var ip = parts[1] || parts[0];
      parts = ip.replace(/[\[\]]/g, '').split('.');
      for (var i = parts.length; i--;) {
          if (isNaN(parts[i]) || parts[i] < 0 || parts[i] > 255) {
              return false;
          }
      }
      return (parts.length == 4);
  }

  // /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
  // https://gist.github.com/dperini/729294



  function search(e) {
    e.preventDefault();
    var term = byId("search-input").value.trim();
    if (!term) return;
    if (linksForShortcuts[term]) {
      chrome.extension.sendMessage({"name": "search-event-url"});
      window.location = linksForShortcuts[term];
      return;
    }
    if (fullUrlRegex.test(term) || nakedUrlRegex.test(term) || isValidIp(term)) {
      if (term.indexOf('://') == -1) {
        term = 'http://' + term;
      }
      chrome.extension.sendMessage({"name": "search-event-url"});
      window.location = term;
      return;
    }

    chrome.extension.sendMessage({"name": "search-event"});
    suggestions.style.visibility = "hidden";
    silver_suggest.innerHTML = "";
    //loadSearchUrl(url);
    var hash = "#q=" + encodeURIComponent(term);
    byId("search-results").src = urlWithNewHash(byId("search-results").src, hash);
    byId("search-results").style.display = "block";
  }


  function initSearchIframe() {
    if (initSearchIframe.done) return;
    initSearchIframe.done = true;

    var searchTimeout;
    searchTimeout = setTimeout(function () {
      chrome.extension.sendMessage({"name": "search-error"});
    }, 3*1000);
    byId("search-results").onload = function () {
      clearTimeout(searchTimeout);
    };

    byId("search-results").src = "http://www.homenewtab.com/instant.html?instant";
  }

  byId("search-input").onchange = initSearchIframe;
  byId("search-input").onmousedown  = initSearchIframe;


  document.forms["search-form"].onsubmit = function (e) {
    e.preventDefault();
  }
  //document.forms["search-form"].onsubmit = function () {
  //  chrome.extension.sendMessage({"name": "search-event"});
  //}

  window.addEventListener("click", function(e) {
    if (!isElementDescendantOf(e.target, byId("search-form")) && e.target.nodeName != 'INPUT') {
      //byId("search-results").src = 'about:blank';
      byId("search-results").style.display = "none";
    }
  }, false);


  window.addEventListener("click", function(e) {
    var el = document.activeElement;
    if (/input|textarea/i.test(el.nodeName) || el.isContentEditable) {
      return;
    }
    if (el != byId("search-input"))
      byId("search-input").focus();
  }, false);

  chrome.extension.sendMessage({"name": "pageview"});

}

window.addEventListener("DOMContentLoaded", suggest_init, false);



// helper
function isElementDescendantOf(el, ancestor) {
  while (el = el.parentNode) {
    if (el === ancestor) return true;
  }
  return false;
}

var dummyLink = document.createElement('a');
function urlWithNewHash(url, newHash) {
  dummyLink.href = url;
  dummyLink.hash = newHash;
  return dummyLink.href;
}