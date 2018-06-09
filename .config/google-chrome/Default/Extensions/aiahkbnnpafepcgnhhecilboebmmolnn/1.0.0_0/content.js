chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.message == "getLinks") {
		var links = [];
		$("a").each(function(i, el) {
			links.push({ "url": el.href, "description": $(el).text() });
		});
		chrome.runtime.sendMessage({ "message": "links", "links": links });
	}
});
