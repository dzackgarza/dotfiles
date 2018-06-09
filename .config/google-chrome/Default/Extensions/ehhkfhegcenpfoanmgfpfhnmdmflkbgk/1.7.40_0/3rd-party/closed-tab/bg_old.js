// from sexy undo

var default_c_settings = {
	showClear:true,
	showBadge:true, 
	showTime:true, 
	showSearch:true,
	boldFont:false,
	saveHistory:true,
	ctrlZ:true,
	menuTop:false,
	disableDClick:false,
	appendTab:false,
	numLimit:20,
	numItems:10,
	numLines:0
};


// Show |url| in a new tab.
function showUrl(id,closewindow) { 
	var splitValue = localStorage["ClosedTab-"+id].split("%%");
	var url = splitValue[2];
	var index = parseInt(splitValue[3]);
	delete localStorage["ClosedTab-"+id];
	localStorage["closedTabCount"] --;

	if (chrome.extension.getBackgroundPage().c_settings.appendTab == true) index=999999;

	if (closewindow==true){
		chrome.tabs.create({"url": url, "index": index,"selected":true});  
		window.close();
	}else{
		chrome.tabs.create({"url": url, "index": index,"selected":false});  
	}
}



function init_closed_tabs(){
	var allowClearing = true;
	if (localStorage["c_settings"]==undefined){ //frist time install?
		localStorage["c_settings"]=JSON.stringify(default_c_settings); 
		localStorage["minimumTabInc"] = 0;
		localStorage["uniqueTabInc"] = 0;
		localStorage["closedTabCount"] = 0;
		allowClearing=false;
	}
	c_settings = JSON.parse(localStorage["c_settings"]);
	chrome.extension.getBackgroundPage().c_settings = c_settings;

	if (allowClearing && !c_settings.saveHistory) resetData();
}

function resetData()
{	
	///localStorage.clear();
	
	localStorage["minimumTabInc"] = 0;
	localStorage["uniqueTabInc"] = 0;
	localStorage["closedTabCount"] = 0;
	localStorage["c_settings"] = JSON.stringify(chrome.extension.getBackgroundPage().c_settings);
	
	/*chrome.tabs.getAllInWindow(null, function(tabsInWindow) {
		for (var i=0; i<tabsInWindow.length; i++) {
			AddNewTab(tabsInWindow[i].id,null, tabsInWindow[i]);
		}
	});*/
}

/////////////////////////////////////////////////

// Replace HTML tags < >
function quote(s) {
  var s1=s;
  s1 = s1.replace(new RegExp("<", "g"), "&lt;");
  s1 = s1.replace(new RegExp(">", "g"), "&gt;");
  return s1;
}

/*
chrome.extension.onRequest.addListener(function(request, sender, sendResponse) {
  if (request == "ctrlZ") {
    if (true ||chrome.extension.getBackgroundPage().c_settings.ctrlZ) {
  	  for (i = localStorage["uniqueTabInc"] - 1; i>=0; i--){
  			if (localStorage["ClosedTab-"+i]){
  				showUrl(i,false);
  				return;
  			}
  	  }
    }
  }
});
*/

function AddNewTab(tabId, changeInfo, tab) {

  var insertThis = tab.url+"%%"+tab.index;
  insertThis += "%%";

  if(tab.title != null)
    insertThis += quote(tab.title);
  else
    insertThis += tab.url;

  if (tab.incognito==true)
		insertThis += "%%1";
  else
		insertThis += "%%0";
  
  localStorage["TabList-"+tabId] = insertThis;
}

chrome.webNavigation.onTabReplaced.addListener(function (details) {
	chrome.tabs.get(details.tabId, function (tab) {
		AddNewTab(details.tabId, null, tab);
	});
});

chrome.tabs.onUpdated.addListener(AddNewTab);

chrome.tabs.onRemoved.addListener(function(tabId, info)  {
  // Should we record this tab?
  if (!localStorage["TabList-"+tabId]) return;
  var splitValue = localStorage["TabList-"+tabId].split("%%");
  var url = splitValue[0];
  var re = /^(http:|https:|ftp:|file:)/;
  if (url && re.test(url)) {
		var exists = -1;
		for (i = localStorage["uniqueTabInc"] - 1; i>=0; i--){
			var closedTab=localStorage["ClosedTab-"+i];
			if (closedTab){
				var split = closedTab.split("%%");
				if (split[2]===url){
					exists=i;
				}
				break;
			}
		}
		var digital = new Date();
		if (exists!=-1){
			localStorage["ClosedTab-"+exists] = tabId + "%%" + digital.getTime() + "%%" + localStorage["TabList-"+tabId];
		}else{
			localStorage["ClosedTab-"+localStorage["uniqueTabInc"]] = tabId + "%%" + digital.getTime() + "%%" + localStorage["TabList-"+tabId];
			var uniqueTabInc = localStorage["uniqueTabInc"] ++;
			//localStorage["closedTabCount"];

			// Code for deleting last TAB
			if (localStorage["closedTabCount"]>=chrome.extension.getBackgroundPage().settings.numLimit){
				for (i = localStorage["minimumTabInc"]; i<uniqueTabInc; i++){
					var closedTab=localStorage["ClosedTab-"+i];
					if (closedTab){
						localStorage["minimumTabInc"]=i;
						delete localStorage["ClosedTab-"+i];
						break;
					}
				}
			}else{
				localStorage["closedTabCount"] ++;
			}
			//setBadgeText();
		}
  }
  delete localStorage["TabList-"+tabId];
});

init_closed_tabs();