
// Copyright (c) 2016 Balázs Galambosi 
// @galambalazs, galambalazs@yahoo.co.uk

var fullUrlRegex = /(?:(?:https?|ftp|chrome|chrome-extension):\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])/gi;

var nakedUrlRegex = /^[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\/?$/gi;

var throttle=function throttle(){return function(d,a){a||(a=100);var b,c;return function(){if(b)c=true;else{var e=this,f=arguments;d.apply(e,f);b=setTimeout(function(){if(c){d.apply(e,f);c=false}b=null},a)}}}}();
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
}

// return true if you wanna override
var searchOverride = function (term) { };

function suggest_init() {

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
      var response;
      try { 
        response = JSON.parse(xhr.responseText) 
      } catch(e) {
        // returned error HTML e.g. because: organization's  URL Filtering policy
        console.error('ERROR: search suggest response has invalid JSON: ', xhr.responseText);
        logError(new Error('ERROR: search suggest response has invalid JSON: '), term + ' ## ' + xhr.responseText.slice(0, 15));
        //ga('send', 'event', 'debug', 'error-search-suggest-json-parse', xhr.responseText);
        if (xhr.responseText.indexOf('malformed or illegal') != -1)
          ga('send', 'event', 'debug', 'error-search-suggest-url', url);
      } // TODO: error logging
      
      callback(response);
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
  //q.type = "text";
  //q.autocomplete = "off";

  var suggestions = document.createElement("ul");
  suggestions.id = "suggestions";
  suggestions.style.display = 'none';
  q.parentNode.appendChild(suggestions);

  var silver_suggest_el = document.createElement("div");
  silver_suggest_el.id = "silver-suggest";
  q.parentNode.appendChild(silver_suggest_el);

  requestAnimationFrame(function () { // prevent forced layout
    var offsetLeft = q.offsetLeft, offsetTop  = q.offsetTop;
    silver_suggest_el.style.top  = (offsetTop + 0) + "px"; //8
    silver_suggest_el.style.left = (offsetLeft + 9+2) + "px";
    //suggestions.style.top  = (offsetTop + 21) + "px";
    //suggestions.style.left = offsetLeft + "px";
  });

  /*

  #suggestions    { width:301px; position:absolute; z-index:6; display:none; border:2px solid #f0f0f0; background:#222; opacity:0.96; border-radius:6px; -moz-border-radius:6px; box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); -moz-box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); -webkit-box-shadow:4px 4px 5px rgba(0, 0, 0, 0.4); }
  #suggestions ul { list-style-type:none; padding-top:5px; font-size:11px; }
  #suggestions li a,#suggestions li a:link,#suggestions li a:visited { display:block; cursor:default; font-weight:bold; color:#fff; text-decoration:none; padding:2px 5px; }
  #suggestions li a:hover, #suggestions li a.active { background:#c4c4c4; color:#000; text-shadow:0 0 0.1em #fff; }

  */

  window.on("click", function(e) {
    if (e.target.nodeName != 'INPUT') {
      suggestions.style.display = 'none';
      remove_silver_suggest();
    }
  });

  var suggs = suggestions.getElementsByTagName('li'); // live collection

  var is_first_keydown = true;

  // arrow keys

  function update_searchbox(value) {
    if (value && value.dataset)
      value = value.dataset.term;
    q.value = value;
    // simple value change doesn't trigger change event by default
    var e = document.createEvent("HTMLEvents");
    e.initEvent("change", false, true);
    q.dispatchEvent(e);
  }

  var last_key, is_backspace_sequence;

  function keydown(e) {

      // warm up initial connection and SSL
      /*if (is_first_keydown) {
        (new Image()).src = "https://homenewtab.com/blank.gif";
        is_first_keydown = false;
      }*/

      var key = e.keyCode;

      is_backspace_sequence = (last_key == 8 && key == 8);
      last_key = key;

      if (key == 17 || key == 16 || key == 91) { // Ctrl | Shift | CMD
        return true;
      } else if (key == 13) { // enter
        stop_all_requests();
        search(e);
        return false;
      } else {
        if (!settings.search_fullscreen) {
          byId("search-results-wrap").style.display = "none";
        }
      }

      // return if there ares no suggestions
      if (!suggestions.innerHTML) return true;
      
      // collect link elements  
      var len, i;
      
      // resume if needed
      if (suggestions.style.display === 'none') {
        suggestions.style.display = 'block';
        //console.log('resume: ' +  suggestions.style.display);
        return true;
      }

      //if ( key >= 65 && key <= 90 && !e.ctrlKey) {
      if ( key !== 8 && key !== 39 && key !== 40) {    
        //var term = this.value + String.fromCharCode(key+32);
        //update_silver_suggest_term(term);
      }

      // used Ctrl+A or equivalent should auto complete suggestion
      setTimeout(function () {
        if (window.silver_suggest.suggestion && q.value && 
            q.selectionEnd - q.selectionStart == q.value.length) {
          update_searchbox(window.silver_suggest.suggestion);
          update_silver_suggest_term(window.silver_suggest.suggestion);
          q.selectionStart = 0;
          //q.selectionEnd = window.silver_suggest.suggestion.length;
          return true;
        }
      }, 1);

      // handle event
      switch (e.keyCode) {  
          case 8: // backspace
            if (window.silver_suggest.suggestion) {
              var term = this.value.slice(0, -1);

              // hitting it continously disables silver suggest
              remove_silver_suggest();

              // first hit just removes current suggestions (not removing a single char)
              if (!is_backspace_sequence) {
                e.preventDefault();
              }
            }
            return true;
          break;

          // TODO: case 46:  // delete 
      
          case 38: // up
          remove_silver_suggest();
          len = suggs.length-1;
          for ( i = len+1; i--; ) {
            if ( suggs[i].classList.contains("active") ) {
              suggs[i].classList.remove("active")
              if ( suggs[i-1] ) {
                suggs[i-1].classList.add("active")
                update_searchbox(suggs[i-1]);
                return false;
              }
            }
          } 
          suggs[len].classList.add("active") 
          update_searchbox(suggs[len]);
          return false;
            
          case 9:  // tab
          case 40: // down
          remove_silver_suggest();
          for ( i = 0, len = suggs.length-1; i <= len; i++ ) {   
            if ( suggs[i].classList.contains("active") ) {
              suggs[i].classList.remove("active");
              if ( suggs[i+1] ) {
                suggs[i+1].classList.add("active");
                update_searchbox(suggs[i+1]);
                return false;
              }
            }
          }   
          suggs[0].classList.add("active"); 
          update_searchbox(suggs[0]);
          return false;  


          case 39: // right (siver-suggest)
          //q.value = suggestions.childNodes[0].textContent;
          if (window.silver_suggest.suggestion) {
            update_searchbox(window.silver_suggest.suggestion);
            update_silver_suggest_term(window.silver_suggest.suggestion);
          }
          break;

          case 37: // left (siver-suggest)
          if (window.silver_suggest.suggestion) {
            //update_searchbox(window.silver_suggest.suggestion);
            remove_silver_suggest();
            e.preventDefault();
            return false;
          }
          break;

          //case 13: // enter
          //search(e);
          //return false;
          
          case 27: // esc
          suggestions.style.display = "none";
          hide_search_bg_overlay();
          return false;

          default: return true;
       } // #end switch

      
      return true;
  }

  ///////////////////////////////////////////////////

  //
  // suggestions
  //

  function term_changed(e) {

    var originalTerm = this.value; // no alterations like trimming
    var term = this.value;         // may be altered

    term = term.replace(/\s+/g, ' ').trim();

    // async function use this to validate they are still relevant
    window.currentSearchTerm = term; 

    if (term && term.length < 100) { // 100 char limit for Google suggest

      var requetsCompleteCount = 0;
      var historyAndBookmarksSuggestions = [], searchEngineSuggestions;

      function requestDone() {
        if (++requetsCompleteCount == 2) updateSuggestions();
      }

      (function () {

        // no index could be: no permission or still building
        if (localStorage.FB_index_ready != 'true') {
          requestDone();
          return;
        }

        if (term.indexOf(' ') != -1) {
          remove_silver_suggest();
          requestDone();
          return;
        }

        if (is_backspace_sequence) {
          requestDone();
          return;
        }

        // if he's just keep typing the suggestion we already have
        if (startsWith(window.silver_suggest.suggestion, term)) {
          requestDone();
          update_silver_suggest_term(term);
          return;
        }

        // he's typing something new, look for suggestions
        remove_silver_suggest();
        term = term.trim();

        if (!window.getHistoryBookmarksSuggestions) 
          return requestDone();

        getHistoryBookmarksSuggestions(term, function (suggestions) {
          historyAndBookmarksSuggestions = suggestions;
          requestDone();

          // Silver URL suggest handled here to be fast (don't wait for Google Suggest)
          // Good UX when typing one letter and hitting enter. (e.g. f + ENTER)
          var suggestion = historyAndBookmarksSuggestions[0];
          if (!suggestion) return;
          // need some kind of quality to even display it
          if (suggestion.frecency < 200) return;
          var silverURL = dashlessending(wwwless(protocolless(suggestion.url)));
          if (startsWith(silverURL, term)) {
            set_silver_suggest(term, silverURL, 
                               suggestion.url, suggestion.title, suggestion.frecency);
          } 
        });
      })();

      // get suggestions and silver suggest
      var url = 'http://google.com/complete/search?client=firefox&q=' + // &hl=en
                encodeURIComponent(term);
      ajax(url, function(reponse) {
        // term changed we are no longer relevant
        if (!reponse || window.currentSearchTerm != originalTerm) return;

        searchEngineSuggestions = reponse[1].slice(0,5);
        requestDone();
      });

      function updateSuggestions() {
        var topHit;

        // to display TOP hit or not
        (function () {
          var suggestion = historyAndBookmarksSuggestions[0];

          if (!suggestion) return;
          // need some kind of quality to even display it
          if (suggestion.frecency < 200) return;

          var silverURL = dashlessending(wwwless(protocolless(suggestion.url)));
          if (startsWith(silverURL, term)) {
            // moved up to handle it fast in getHistoryBookmarksSuggestions callback
          } else {

            // need exact match inside url if using dot anywhere
            if (term.indexOf('.') != -1 && suggestion.url.indexOf(term) == -1) 
              return;
            if (isNumeric(term))
              return;
            if (suggestion.frecency < 10*1000) 
              return;
            if (term.length < 3) 
              return

            // don't like doing this here, but for Top Hit we needs slightly different
            // ranking mechanism which highly favors shorter urls
            historyAndBookmarksSuggestions.forEach(function (row) {
              var shortness = Math.max(100-row.url.length, 0);
              row.frecency += ~~((shortness/100) * 100*1000); // 100*1000
            });
            historyAndBookmarksSuggestions.sort(function (a, b) {
              return b.frecency - a.frecency;
            });

            topHit = historyAndBookmarksSuggestions[0];
          }
        })();

        var words = searchEngineSuggestions;
        var html = words.reduce(function (html, word) {
          return html + '<li data-term="' + word + '">' + word + '</li>';
        }, '');
        if (topHit) {
         topHit.url = dashlessending(httpless(topHit.url));
         var tokens = term.split(/[^a-z0-9\u00E0-\u00FC]+/i);
         var topHitHTML = highlightMatchesHTML(topHit.url, tokens);
         if (topHit.title) {
            var title = highlightMatchesHTML(topHit.title, tokens);
            title ='<span> &ndash; ' + topHit.title + '</span>';
         }
         html = '<li class="top-hit" data-term="' + topHit.url + '">' + 
                  topHitHTML + title + 
                '</li>'  + 
                html;
          // <span></span>
          //words.unshift(topHit);
        }
        suggestions.innerHTML = html;
        suggestions.style.display = (words.length || topHit)  ? "block" : "none";
      }
    } else {
      suggestions.style.display = "none";
      silver_suggest_el.innerHTML = "";
      //location.search = '?back';
      history.replaceState({}, '', 'index.html?back');
      //hide_search_bg_overlay(); this might distract the user
    }
    
    // prevent default
    return false; 
  }

  q.oninput = term_changed;
  q.onkeydown = keydown; // debounce(keyup, 100)

  (function (G) {
    var prerender_id = 'silver_suggest_prerender';
    function addListener(name, fn) {
      window.addEventListener('silver_suggest.' + name, fn);
    }
    function publish(name) {
      window.dispatchEvent(new Event('silver_suggest.' + name));
    }
    function reset_silver_suggest(keep_prerender) {
      G.silver_suggest = {
        el:         silver_suggest_el,
        suggestion: '',
        url:        '',
        term:       '',
        title:      '',
        frecency:   -1,
        addListener: addListener
      };
      silver_suggest_el.innerHTML = '';
      publish('hide');
      if (!keep_prerender) cancel_prerender(prerender_id);
    }
    function get_silver_suggest_html(e) {
      e || (e = G.silver_suggest);
      var title = e.title ? ' &ndash; ' + e.title : '';
      if (e.term == e.suggestion) e.title = '';
      return "<span id='silver-match'>" + e.suggestion.slice(0, e.term.length) + "</span>" + 
             "<span id='silver-rest'>"  + e.suggestion.slice(e.term.length) + "</span>" +
             "<span id='silver-title'>" + title + "</span>"
    }
    function set_silver_suggest(term, suggestion, url, title, frecency) {
      if (term) {
        if (term)       G.silver_suggest.suggestion  = suggestion;
        if (suggestion) G.silver_suggest.url         = url;
        if (url)        G.silver_suggest.term        = term;
        if (title)      G.silver_suggest.title       = title;
        if (frecency)   G.silver_suggest.frecency    = frecency;
      } 
      var is_full_completion = (G.silver_suggest.term == G.silver_suggest.suggestion);
      if (G.silver_suggest && !is_full_completion) {
        silver_suggest.el.innerHTML = get_silver_suggest_html(G.silver_suggest);
        publish('show');
        if (G.silver_suggest.term.length > 1 && 
            G.silver_suggest.frecency > 10*1000) {
          prerender(silver_suggest.url, prerender_id);
        }
      } else {
        reset_silver_suggest(is_full_completion);
      }
    }
    function update_silver_suggest_term(term) {
      if (startsWith(G.silver_suggest.suggestion, term)) {
        G.silver_suggest.term = term;
        set_silver_suggest();
      } else {
        reset_silver_suggest();
      }
    }
    reset_silver_suggest();

    G.update_silver_suggest_term = update_silver_suggest_term;
    G.set_silver_suggest = set_silver_suggest;
    G.remove_silver_suggest = reset_silver_suggest;
  })(window);


  byId("search-input").on('mousedown', function () {
    if (window.silver_suggest.suggestion) {
      byId("search-input").value = window.silver_suggest.suggestion;
      update_silver_suggest_term(window.silver_suggest.suggestion);
    }
  });

  suggestions.onclick = function(e) {
    if (e.target.nodeName.toLowerCase() == 'li') {
      remove_silver_suggest();
      update_searchbox(e.target);
      search(e);
    }
  }
  suggestions.onmousedown = function () {
    var active = $('.active', suggestions)[0];
    if (active) active.classList.remove('active');
  }
  


  //
  // Real-time results
  //

  byId("search-button").onclick = function(e) {
    search(e);
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
    var term = window.silver_suggest.url || byId("search-input").value.trim();
    if (!term) return;
    if (fullUrlRegex.test(term) || nakedUrlRegex.test(term) || isValidIp(term)) {
      if (term.indexOf('://') == -1) {
        term = 'http://' + term;
      }
      chrome.extension.sendMessage({name: "search-event-url", url:term});
      suggestions.style.display = 'none';
      if (window.silver_suggest.suggestion) {
        byId("search-input").value = window.silver_suggest.suggestion;
        silver_suggest_el.style.display = 'none';
        chrome.extension.sendMessage({name: "search-event-url-suggested", url:term});
      }
      //document.body.style.transition = 'opacity .35s ease-in-out';
      //document.body.style.opacity = .75;
      byId("search-input").classList.add('navigating');
      window.location = term;
      return;
    }

    chrome.extension.sendMessage({"name": "search-event"});
    suggestions.style.display = "none";
    remove_silver_suggest();

    if (searchOverride(term)) {
      return;
    }

    var hash = "#q=" + encodeURIComponent(term);
    //location.hash = hash; // remember term for this page in case he comes back
    ////history.replaceState({}, '', 'index.html?back' + hash);
    //byId("search-results").src = urlWithNewHash(byId("search-results").src, hash);
    ////byId("search-results").src = window.SEARCH_URL + hash;
    updateSearchIframe(hash, term);
    byId("search-results-wrap").style.display = "block";
    show_search_bg_overlay();
  }

  function initSearchIframe(param) {
    if (initSearchIframe.done) return;
    initSearchIframe.done = true;

    var searchTimeoutSlow3 = setTimeout(function () {
      chrome.extension.sendMessage({"name": "search-timeout-3"});
    }, 3*SECONDS);
    var searchTimeoutSlow5 = setTimeout(function () {
      chrome.extension.sendMessage({"name": "search-timeout-5"});
      //reloadIframe(byId("search-results"));
    }, 5*SECONDS);

    function cleanupTimeouts() {
      clearTimeout(searchTimeoutSlow3);
      clearTimeout(searchTimeoutSlow5);
    }

    byId("search-results").onload = function (e) {
      cleanupTimeouts();
      console.log(e.type);
      console.timeEnd('search-iframe');
      console.time('search-iframe');
    };
    
    console.time('search-iframe');
    window.on('message', function (e) {
      var name = e.data && e.data.name;
      var searchFrameWin = frames['search-results'].contentWindow;
      if ('DOMContentLoaded' == e.data) {
        cleanupTimeouts();
        if (stored.TEST_search_fullscreen == 'true') {
          searchFrameWin.postMessage('show.opt-fullscreen-search', '*');
        }
      }
      else if ('set.opt-fullscreen-search' == name) {
        settings.search_fullscreen = e.data.value;
        save_options();
        ga('send', 'event', 'option', 'search-fullscreen', e.data.value);
        location.reload();
      }
      else if ('search.query-changed' == name) {
        var qNewValue = e.data.data;
        if (qNewValue && qNewValue != q.value) q.value = qNewValue;
      }
      console.log(e.data);
      console.timeEnd('search-iframe');
      console.time('search-iframe');
    });

    if (settings.search_fullscreen) {
      var wrap = byId('search-results-wrap');
      wrap.style.cssText = "display:none; position: absolute; bottom: 0; top: 47px; width: 100%;";
      document.body.appendChild(wrap);
      
      var img = document.createElement('img');
      img.id = "search-logo";
      img.src = "/icons/home.png";
      //img.src ="/icons/search-logo.png"
      //img.style.cssText = "width: 95px; height: 37px; left: 14px; position: absolute; display:none";
      img.style.cssText = "width: 36px; height: 36px; left: 75px; position: absolute; display:none";
      byId("search-box").insertBefore(img, byId("search-box").firstChild);
    }

    byId("search-results").src = window.SEARCH_URL;
  }

  function updateSearchIframe(hash, term) {
    initSearchIframe();

    if (settings.search_fullscreen && 'string' == typeof hash) {
      document.documentElement.classList.add('search-fullscreen');
      document.body.insertBefore(byId("search-box"), document.body.firstChild);
      byId("search-input").focus();
      byId("search-results").classList.add('overlay-cover');
      byId("search-logo").style.display = '';
      byId("page").style.display = 'none';
    }

    if ('string' == typeof hash) {
      history.replaceState({}, '', 'index.html?back' + hash);
      byId("search-results").src = window.SEARCH_URL + hash;
      document.title = term + ' - Search';
      setTimeout(function () { byId("search-results").focus() }, 1);
      setTimeout(function () { byId("search-input").focus() }, 10);
    } else {
      byId("search-results").src = window.SEARCH_URL;
    }
  }

  //byId("search-input").on('focus', initSearchIframe);
  //byId("search-input").on('input', initSearchIframe);

  if (!newInstall) {
    byId("search-input").on('mousedown', initSearchIframe);
    byId("search-input").on('keydown', initSearchIframe);
  }

  if (location.hash && startsWith(location.hash, '#q=')) {
    var term = decodeURIComponent(location.hash.replace(/^#q=/i, ''));
    updateSearchIframe(location.hash, term);
    update_searchbox(term);
    byId("search-results-wrap").style.display = "block";
    show_search_bg_overlay();
  }

  document.forms["search-form"].onsubmit = function (e) {
    e.preventDefault();
  }
  //document.forms["search-form"].onsubmit = function () {
  //  chrome.extension.sendMessage({"name": "search-event"});
  //}

  window.on("click", function(e) {
    if (!isElementDescendantOf(e.target, byId("search-form")) && e.target.nodeName != 'INPUT') {
      //byId("search-results").src = 'about:blank';
      byId("search-results-wrap").style.display = "none";
      hide_search_bg_overlay();
    }
  });


  window.on("click", function(e) {
    var el = document.activeElement;
    if (/input|textarea/i.test(el.nodeName) || el.isContentEditable) {
      return;
    }
    if (el != byId("search-input"))
      byId("search-input").focus();
  });

  silver_suggest.addListener('hide', function () {
    window.dispatchEvent(new Event('cursor.show'));
  });
  silver_suggest.addListener('show', function () {
    window.dispatchEvent(new Event('cursor.hide'));
  });

  function showSearchLoadingIndicator() {
    var el = document.createElement('img');
    el.src = 'img/loading.gif';
    el.id = 'loading';
    el.className = 'spinner';
    var iframe = byId("search-results");
    el.style.top  = iframe.offsetTop  + iframe.offsetHeight/ 2 + 'px';
    el.style.left = iframe.offsetLeft + iframe.offsetWidth / 2 + 'px';
    document.body.appendChild(el);
  }

  function hideSearchLoadingIndicator() {
    var loading = byId('loading');
    if (loading) document.body.removeChild(loading);
  }

  function show_search_bg_overlay() {
    if (settings.search_fullscreen) return;
    if (byId('search-bg-overlay')) return;
    var bg_overlay = document.createElement('div');
    bg_overlay.id = 'search-bg-overlay';
    bg_overlay.style.opacity = 0;
    document.body.appendChild(bg_overlay);
    setTimeout(function () { bg_overlay.style.opacity = 1 }, 1);
  }

  function hide_search_bg_overlay() {
    var bg_overlay = byId('search-bg-overlay');
    bg_overlay && bg_overlay.parentNode.removeChild(bg_overlay);
  }

}

window.on("DOMContentLoaded", suggest_init);



//
// Prerender
//

var prerenderTimers = {};
var prerenderedURLs = {};

function prerender(url, id) {
  id || (id = 'prerender');
  if (url == prerenderedURLs[id]) {
    //prerender_schedule_cancel();
    return;
  }
  clearTimeout(prerenderTimers[id]);
  prerenderTimers[id] = setTimeout(function () {
    //     var hint  = document.getElementById(rel) || document.createElement('link');
    var hint  = document.getElementById(id);
    if (hint) {
      hint.rel  = '';
    } else {
      hint = document.createElement('link');
      hint.id = id;
    }
    hint.rel  = 'prerender';
    hint.href = url;
    prerenderedURLs[id] = url;
    $('head')[0].appendChild(hint);
    //prerender_schedule_cancel(id);
  }, 500);
}

function cancel_prerender(id) {
  id || (id = 'prerender');
  var hint = byId(id); 
  if (hint) hint.rel = '';
  prerenderedURLs[id] = '';
}

//
// UI Feedback about indexing
//

(function () {

chrome.runtime.onMessage.addListener(function indexComplete(message) {
  if (message.action == "search-indexing-start") {
    show_indexing_info();
  } else if (message.action == "search-indexing-complete") {
    hide_indexing_info();
  } else if (message.action == "search-indexing-error") {
    hide_indexing_info();
  }
});

window.on('DOMContentLoaded', show_indexing_info);

var indexing_info_timer;

function show_indexing_info() {
  if (localStorage.FB_index_is_building == 'true' &&
      localStorage.FB_index_first_run_complete != 'true') {
    var indexing_el = document.createElement('div');
    indexing_el.id = 'search-indexing';
    indexing_el.className = 'helpful-message';
    indexing_el.innerHTML = 'indexing urls...';
    byId('search-form').appendChild(indexing_el);
    /*var dots = 0;
    var indexing_info_timer = setInterval(function () {
      if (++dots > 3) dots = 0;
      indexing_el.innerHTML = 'indexing urls' + Array(dots+1).join('.');
    }, 500);*/
  }
}

function hide_indexing_info() {
  clearTimeout(indexing_info_timer);
  var indexing_el = byId('search-indexing');
  if (indexing_el) {
    indexing_el.parentNode.removeChild(indexing_el);
  }
}

})();



//
// Helpers
//

function isElementDescendantOf(el, ancestor) {
  while ((el = el.parentNode)) {
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

function protocolless(url) {
  return url.replace(/^[^:]+:\/\//i, '');
}

function wwwless(url) {
  return url.replace(/^www\./i, '');
}

function httpless(url) {
  return url.replace(/^http:\/\//i, '');
}

function dashlessending(url) {
  return url.replace(/\/$/i, '');
}

function highlightMatchesHTML(text, tokens) {
  var re = new RegExp('(' + tokens.join('|') + ')', 'gi');
  return text.replace(re, '<b>$1</b>');
}

function isNumeric(str) {
  return /^\d+$/.test(str);
}

function startsWith(str, start) {
  return str.indexOf(start) === 0;
}

function reloadIframe(iframe) {
  var oldSrc = iframe.src;
  iframe.src = 'about:blank';
  setTimeout(function () {
    iframe.src = oldSrc; 
  }, 1);
}

/*
window.on('DOMContentLoaded', function () {
  //['input[type="text"]', 'textarea'].forEach(addCursorToElement);
  addCursorToElement(byId('search-input'));
});
*/

// Resize search bar

(function () {

if (!settings.search_bar || settings.search_fullscreen) return;

function onWindowSizeChange() {
  var height = Math.min((window.innerHeight - 60), 900);
  byId('search-results').style.height = height + 'px';
}

window.addEventListener('resize', debounce(onWindowSizeChange, 150));
window.addEventListener('DOMContentLoaded', onWindowSizeChange);
setTimeout(onWindowSizeChange, 1);

})();

//
// Voice search 
//

(function () {
if (!settings.search_bar) return;
window.addEventListener('keydown', function (e) { // code:"Period"
  if (e.keyCode == 190 && e.shiftKey && (e.ctrlKey || e.metaKey) && !e.altKey)
    document.getElementById('microphone-button').click();
})
})();

//
// Direct search
//

(function () {

var US_geo = ('US' == localStorage.GEO_country_code);

// TODO: chrome.storage.sync
if ('undefined' == typeof localStorage.rhtab_direct_test_1) {
  localStorage.rhtab_direct_test_1 = Math.random() < 0.5;
}
if ('undefined' == typeof localStorage.rhtab_direct_test_2) {
  //var rh1 = ('true' == localStorage.rhtab_direct_test_1);
  //localStorage.rhtab_direct_test_2 = rh1 || (Math.random() < 0.5); // 75%
  ////localStorage.rhtab_direct_test_2 = localStorage.rhtab_direct_test_1;
  localStorage.rhtab_direct_test_2 = 'true';
}
if ('undefined' == typeof localStorage.insp_direct_test_1) {
  localStorage.insp_direct_test_1 = Math.random() < 0.5;
}
if ('undefined' == typeof localStorage.insp_direct_test_2) {
  localStorage.insp_direct_test_2 = ('true' == localStorage.insp_direct_test_1 && 
                                     Math.random() < 0.5);
}

if ('false' === localStorage.insp_direct_test_2) {
  localStorage.rhtab_direct_test_2 = 'true';
}


// RHTab
//US|GB|CA|FR|NZ
if ('true' == localStorage.rhtab_direct_test_2 && US_geo) {
  //onRHTabLoaded();
  var script = document.createElement('script');
  script.onload = onRHTabLoaded;
  script.src = "/js/lib/rhtab.js";
  document.head.appendChild(script);
} else if (US_geo || 'true' == localStorage.insp_direct_test_2) {
  searchOverride = function (term) {
    document.body.style.display = 'none';
    ga_cb('send', 'event', 'search', 'search-infospace-direct', function () {
      window.location = "http://www.homenewtabsearch.com/i/" +
                        "?q=" + encodeURIComponent(term);
    });
    return true;
  }
}

function onRHTabLoaded() {
  var feed = Feed.getInstance('gsp_hnt_00_00');
  searchOverride = function (term) {
    document.body.style.display = 'none'; //.opacity = 0;
    ga_cb('send', 'event', 'search', 'search-yahoo-direct', function () {
      feed.search(term);
      //window.location = "http://searchmake.com/?a=gsp_hnt_00_00&q=" + encodeURIComponent(term);
    });
    return true;
  }
}

})();

//
// Legal links
//

if (stored.install_time > 1523998115732) {
  byId('legal-buttons').style.display = '';
}

