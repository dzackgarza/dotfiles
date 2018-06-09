(function(){document.body.appendChild(document.createElement('script')).src='https://s3.amazonaws.com/BoomerangForGmail/bookmarklet/b4g_bookmarklet.js?v=1';})();

// Message-passing: Web Page to Content-script
window.addEventListener("message", function(event) {
	// We only accept messages from ourselves
	if (event.source != window){
		return;
	}

	if (event.data.type && (event.data.type == "B4G_TRACK_EVENT")) {
		var trackedEventData = event.data.trackedEventData;
		chrome.runtime.sendMessage({greeting: "track_event", data: trackedEventData});
	}
	else if (event.data.type && (event.data.type == "B4G_RESPONDABLE_INPUT")) {
		// Message-passing: Content-script to Background page
		chrome.runtime.sendMessage({greeting: "respondable_input", composeBodyText: event.data.composeBodyText, subject: event.data.subject});
	}
}, false);

// Message-passing: Background page to Content-script
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		if (request.greeting == "respondable_output") {
			// Message-passing: Content-script to web page
			window.postMessage({ type: "B4G_RESPONDABLE_OUTPUT", metrics: request.metrics }, "*");
		}
});


var _params;
function parse_url_params() {
	_params = {};
	var loc = window.location.toString();
	var idxQ = loc.indexOf("?");
	var idxH = loc.lastIndexOf("#");
	if(idxQ < 0) { return; }
	if(idxH < 0) { idxH = loc.length; }
	var pairs = loc.substring(idxQ + 1, idxH).split("&");
	pairs.forEach(function(pair) {
		var idxE = pair.indexOf("=");
		_params[pair.substr(0, idxE)] = pair.substr(idxE + 1);
	});
}
parse_url_params();

if (_params["b4g_troubleshoot"] === "1"){
	// look for extension conflicts and make them known to the bookmarklet
	chrome.runtime.sendMessage({greeting: "list_extensions"}, function(response) {});
	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {
			if (request.greeting == "extensions"){
				var extensionsArray = [];	
				var extensions = request.extensions;
				for (var i=0; i<extensions.length; i++){
					var extension = extensions[i];
					var extensionName = extension.shortName;
					if (extension.enabled){
						extensionsObject = {"id": extension.id,
							"name": extensionName};
						extensionsArray.push(extensionsObject);
					}
				}
				localStorage.setItem("b4g_extensions", JSON.stringify(extensionsArray));
			}
		}
	);
}
