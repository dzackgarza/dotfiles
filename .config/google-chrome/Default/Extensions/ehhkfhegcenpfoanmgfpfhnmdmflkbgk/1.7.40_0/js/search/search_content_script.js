(function() {

window.addEventListener('message', function (e) {
  var name = e.data && e.data.name;
  if ('search.api' == name || 'search.api_raw' == name) {
    chrome.runtime.sendMessage(e.data, function (response) {
      window.postMessage(response, '*');
    });
  }
});


function setInitData() {
  document.documentElement.dataset.homenewtab  = true;
  document.documentElement.dataset.countryCode = localStorage.GEO_country_code;
}

if (document.documentElement)
  setInitData();
else
  window.addEventListener('DOMContentLoaded', setInitData);

if (!localStorage.GEO_country_code) {
	chrome.runtime.sendMessage({ name: 'geo.getCountryCode' }, function (response) {
		if (response.success && response.data) 
			localStorage.GEO_country_code = response.data;
	});
}

})();