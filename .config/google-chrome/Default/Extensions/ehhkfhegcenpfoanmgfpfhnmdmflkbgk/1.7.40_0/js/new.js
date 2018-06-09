var newStart = Date.now();

var newInstallTime = +localStorage.SRV_conf_new_install_time || 1492716798000;
var newInstall = !localStorage.install_time || (+localStorage.install_time > newInstallTime);
// 1476991998000

(function () {

var search_bar;
try {
  search_bar = JSON.parse(localStorage.settings||'{}').search_bar;
} catch (e) {
  console.log('ERROR: settings has invalid JSON: ' + localStorage.settings);
  // throw new Error('...');
}

if (search_bar === false || newInstall) return;

//
// Catch fast typers before input gets focus
//

var fastChars = '';

function onFastKeyPress(e) {
	fastChars += String.fromCharCode(e.charCode);
}

function onFastFocus(e) {
	if (e.target.id && e.target.id == 'search-input') {
		window.removeEventListener('keypress', onFastKeyPress, true);
		window.removeEventListener('focus', onFastFocus, true);
		e.target.value = fastChars + e.target.value;
	}
}

window.addEventListener('keypress', onFastKeyPress, true);
window.addEventListener('focus', onFastFocus, true);


//
// Back button & refresh
//

// CODE BELOW WAS USED UNTIL CHROME 49

/// in case backButton.html stops working:
var backNewURL = chrome.runtime.getURL("index.html") + '?search';

// need this to focus on the search bar after coming back for more results
///var backNewURL = 'http://www.homenewtabsearch.com/backButton.html';
var backExtURL = chrome.runtime.getURL("index.html");
var hash = window.location.hash;

if (location.href.indexOf(backExtURL) == 0 && 
		location.search == '?back') {
	document.write('<!--');
	window.stop();
	window.location.href = backNewURL + hash;
	return;
}
if (location.href.indexOf(backExtURL) == 0 && 
		location.search == '?new') {
	history.replaceState({}, '', 'index.html?back');
}


//
// Mac only new tab
//

if (!/mac/i.test(navigator.userAgent)) return;
if (window.location.search) return;

document.documentElement.style.display = 'none';
document.write('<!--'); // '<noscript>'
window.stop();
//window.location.href = 'http://www.homenewtabsearch.com/newtab.html';

return;




////////////////////////////////////////////////////////////////////

// OLD CODE NEVER USED

/*

		//if (window.location.search || top != self) return;
		if (window.location.pathname == '/new.html' || top != self) return;

		chrome.tabs.create({ url: chrome.runtime.getURL("new.html") }); // index.html?
		window.close();
		 // index.html?
*/
	
		//window.location.search = '?sfsasfsa';
		/*
		chrome.tabs.query({currentWindow: true, active : true},	function (tabs) {
			var myID = tabs[0].id;
			if (!tabs[0].index) return;
			chrome.tabs.query({currentWindow: true, index : tabs[0].index-1}, function (tabs) {
		  	console.log(tabs);
		  	chrome.tabs.update(tabs[0].id, { active:true }, function () {
		  		//window.location.search = '?sfsasfsa';
	
		  			chrome.tabs.update(myID, { active: true });
		  
		  	});
		  })
		})
	*/

		/*
		chrome.tabs.update({ active:false });
		window.addEventListener('load', function () {
			chrome.tabs.update({ active:false });
			//chrome.tabs.reload();
		});
	
		setTimeout(function () {
			chrome.tabs.update({ active:false });
			//window.location.search = '?sfsasfsa';
		}, 3000);
		*/

		//chrome.tabs.update({ url: chrome.runtime.getURL("index.html?search") });
		/*chrome.tabs.query({currentWindow: true, active : true},
		  function (tabs) {
		  	chrome.tabs.create({ url: chrome.runtime.getURL("index.html?search") });
		  	chrome.tabs.remove(tabs[0].id);
		  }
		)*/

	//document.getElementById('iframe').src = 'index.html';


function parseHash(hash) {
	hash = hash || location.hash;
	var parts = hash.replace(/^#/, '').split('&');
	return parts.map(function (pair) {
	  var keyvalue = decodeURIComponent(pair).split('=');  
		return { key: keyvalue[0], value: keyvalue[1] }
	});
}

function stringifyHash(hash) {

}


})();
