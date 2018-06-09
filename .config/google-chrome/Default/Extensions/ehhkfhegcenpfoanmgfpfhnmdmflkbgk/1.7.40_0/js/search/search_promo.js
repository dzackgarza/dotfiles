
var hide_search_promo;

function show_search_promo() {

	!window.DEV;

	// exit conditions in Production
	// we already have permission
	if (chrome.history) return;
	// he already responded
	if (localStorage.FB_history_index_enabled != null) return;
	// it's too early to get the promo yet
	if (+new Date < localStorage.FB_search_promo_after && !window.DEV) return;
	//if (+new Date - localStorage.install_time < 60*60*1000) return; // 24*

	function save_and_publish_response(granted) {
		localStorage.FB_history_index_enabled = granted;
		localStorage.FB_history_index_user_response_time = +new Date;
		chrome.extension.sendMessage({
			action: "search-promo-response",
			accepted: granted
		});
		if (granted) {
			settings.search_bar = true;
			localStorage.settings = JSON.stringify(settings);
		}
	}

  byId('search-promo-accept').addEventListener('click', function () {
    chrome.permissions.request({
      permissions: ['history']
    }, function(granted) {
      console.log('history permission request: ' + granted);
      save_and_publish_response(granted);
      hide_search_promo();
    });
  });

  hide_search_promo = function () {
  	//byId('search-promo').classList.remove('start');
  	setTimeout(function () {
  		document.body.removeChild(link);
  	}, 100)
  }

  byId('search-promo-decline').onclick = function() {
  	save_and_publish_response(false);
  	hide_search_promo();
  }

	var link = document.createElement('link');
	link.rel = 'stylesheet';
	link.type = 'text/css';
	link.href = 'css/search_promo.css'
	document.body.appendChild(link);

	var img = document.createElement('img');
	img.src = 'img/search-promo.png';
	byId('search-promo').appendChild(img);

	byId('search-promo').style.display = '';
	setTimeout(function () {
		byId('search-promo').classList.add('start');
	}, 100);

}

window.addEventListener('load', function () {
	setTimeout(show_search_promo, 750);
});
