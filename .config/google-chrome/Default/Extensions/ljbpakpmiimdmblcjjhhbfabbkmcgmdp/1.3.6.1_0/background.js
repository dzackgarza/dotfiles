/*
 * Pause History Button
 * Copyright (C) 2014-2017, Melanto Ltd. All Rights Reserved
 * www.singleclickapps.com 
 *
 */


var settings;
var rightMnuId = null;
var lastIntervalInSeconds = 60;
var lastCleaned = 0; //the timestamp of last cleanup will sit here
var goodByeMode = false; //we need this for knowing when we just turn off the extension...


function startOrRefresh(){
	loadSavedSettings();	
	rightMnuOnOff();	
}
startOrRefresh();

chrome.browserAction.onClicked.addListener(function() {
  //on click event...
  onClickHandler();
});


function loadSavedSettings() {
	//console.log(chrome.runtime.id);
	// buttonSettings
	if (!window.localStorage.buttonSettings) {
		window.localStorage.buttonSettings = JSON.stringify({ "addToMnu": false,	"blockDownloads": false });
	}
	settings = JSON.parse(window.localStorage.buttonSettings);
	if (!window.localStorage.historyDisabled) {
			window.localStorage.historyDisabled =  'false'; //this should be first start -- disable on/off flag (on install it is disabled and history is "on")
		} 

    // icon is now inside prefs->colored Icon ...etc.
         if (settings.redIcon) icon = 'red'
    else if (settings.greenIcon) icon = 'green'
    else if (settings.purpleIcon) icon = 'purple'
    else if (settings.beigeIcon) icon = 'beige'
    else if (settings.yellowIcon) icon = 'yellow' 
    else if (settings.ownIcon) icon = 'own'
    else icon = 'icon';
    updateIcon(icon);
     
	// app version
	var currVersion = getVersion();
	var prevVersion = window.localStorage.button_Version;
	if (currVersion != prevVersion) {
		if (typeof prevVersion == 'undefined') {
			onInstall();
		} else {
			onUpdate();
		}
		window.localStorage.button_Version = currVersion;
	}
	updateState();
}

//update icon
function updateIcon(icon) {
    if (icon=="own") {
        //load customer selected icon from storage
         //load custom icon, if set
        if (settings.ownIcon){
            var img = new Image();
            img.onload = function(){
                var canvas = document.createElement('canvas');
                                    canvas.width = img.width;
                                    canvas.height = img.height;

                                    var context = canvas.getContext('2d');
                                       context.drawImage(img, 0, 0);             
                                    // ...draw to the canvas...
                                    var imageData = context.getImageData(0, 0, 19, 19);
                chrome.browserAction.setIcon({imageData:imageData});
            };
            img.setAttribute("src", settings.storedCanvas);
           // document.getElementById('destination').appendChild(img);

        }
    } else 
        chrome.browserAction.setIcon({path:icon + ".png"});
   
}

//set on uninstall url
chrome.runtime.setUninstallURL('https://singleclickapps.com/history-on-off/removed-chrome.html');

// Check if this is new version
function onInstall() {
	
	if (navigator.onLine) {
		chrome.tabs.create({url: 'https://singleclickapps.com/history-on-off/postinstall-chrome.html'});
	}
}
function onUpdate() {
	
	if (navigator.onLine) {
		//chrome.tabs.create({url: 'https://singleclickapps.com/history-on-off/info-1-3-chrome.html'});
	}
}
function getVersion() {
	var details = chrome.app.getDetails();
	return details.version;
}

function rightMnuOnOff() {

	if (settings.addToMnu && !rightMnuId) {
		
		rightMnuId = chrome.contextMenus.create({
			"title" : "History On/Off",
			"type" : "normal",
			"contexts" : ["page", "frame", "selection", "link", "editable", "image", "video", "audio", "page_action"],
			"onclick" : onClick()
		});
		
	}

	if (!settings.addToMnu && rightMnuId) {
		
		chrome.contextMenus.remove(rightMnuId);
		rightMnuId = null;
		
	}

}

function onClick() { //for the context menu
	return function() { // don't forget it must RETURN Fx(), 
  		//on click event...
	  	onClickHandler();
	}
}

function onClickHandler(){
  //on click event...
    if(!window.localStorage.historyDisabled) {
			window.localStorage.historyDisabled =  'true'; //this is first click, so -- disable history flag is added and set to true
			window.localStorage.timeStamp = (new Date()).getTime();
			goodByeMode=false;
		}
	else{
			curr = window.localStorage.historyDisabled;
			if(curr=='true'){ 
				window.localStorage.historyDisabled = 'false'; 
				goodByeMode = true;
				deleteHistory();
				
			} else { 
				window.localStorage.historyDisabled = 'true'; 
				window.localStorage.timeStamp = (new Date()).getTime();
			}
		}
	updateState();
}

// delete history items when created:
chrome.history.onVisited.addListener( function(historyItem) {
	if (window.localStorage.historyDisabled == 'true') {
	    chrome.history.deleteUrl({ "url": historyItem.url });
		//console.log(historyItem.url);
	}
	// NB: This is not fired all the time by Chrome browser, unfortunately (for example on youtube videos or when downloading
	// it often misses to fire this event and as a result -- we get items added to history when we want them out ;-(
	// all the handlers at bottom are here to fix this wrong behavior
});

/*chrome.downloads.onCreated.addListener( function(downloadItem) {  //this will prevent any download, but I decided to remove this option
	if (window.localStorage.historyDisabled == 'true') {
	    if(settings.blockDownloads){
			chrome.downloads.erase( { "id": downloadItem.id } );
			//chrome.history.deleteUrl({ "url": downloadItem.url });
			//console.log(downloadItem.id);
		}
	}
});*/

function deleteHistory(){
	
		//chrome.history.deleteRange({ "startTime": JSON.parse(window.localStorage.timeStamp), "endTime": (new Date()).getTime() }, function(){} );
		//chrome.history.deleteRange({ "startTime": 0297033393594, "endTime": 1397033724290 }, function(){ } );
		//chrome.history.deleteAll(function(){ });
		//console.log({ "startTime": JSON.parse(window.localStorage.timeStamp), "endTime": (new Date()).getTime() })
		// commented above because these just don't work (chrome bug?)
		
		/* 	
			all the tabs/windows handlers at bottom will invoke this, also when you resume history this will be executed; 
			we just force clean history (because 'chrome.history.onVisited' handler above is not fired on every single history add -- see youtube
		   	(video download started without onVisited event fired?) or when you click to download file (seems that downloads are added w/o firing event too))... 
		*/
		
		// NB: BE SURE YOU INVOKE THIS ONLY WHEN HISTORY IS DISABLED, OR WHEN YOU JUST TURNED IT ON AFTER SOME USE (GOODBYE MODE)		
		if (window.localStorage.historyDisabled == 'false'){ 
			if(!goodByeMode){
				return;
			} else {
				goodByeMode=false; //we just stopped the extension, but let's proceed with the final cleanup
			}	
		}
		
		if(!window.localStorage.timeStamp)return; //something went wrong when turning historyDisabled flag to true (not saved in local store)
		
		// don't force cleanup too often! we want at least 15 seconds before invoking this cleaner again...
		
		if(lastCleaned==0){
			//this is the first start of this deleteHistory() function...
		} else {
			//lastCleaned = the last time we processed the browser cleanup
			timeNow = (new Date()).getTime(); 
			//console.log(timeNow - lastCleaned);
			if( (timeNow - lastCleaned)<10000 ){ //we put 10 seconds here, because the setTimer minimum is 15 but there are wasted miliseconds anyway...
				//too soon, go away!					
				if (window.localStorage.historyDisabled == 'true'){ //only skip when app is working, on resume -- go with final cleanup
					//if we are closing windows, we may get all of them closed (like on chrome exit), then please go clean no matter what
						chrome.windows.getAll({"populate" : false}, function(windows){
							//console.log(windows.length); //number of open windows right now...
							if(windows.length<1){
								// no more open pages, force last final cleanup																
							} else {
								// there are open windows
								//console.log('too soon!');
								return;
							}
						});
						
					} 
			}
		}		 
		lastCleaned = (new Date()).getTime(); //set last cleaned timestamp for the check above
		
		selectedTimeFrame =  JSON.parse(window.localStorage.timeStamp); //this was set when we turned the "pause history" state on
		
		//disabled due to opera issues(!?!): window.localStorage.timeStamp = (new Date()).getTime(); //reset timestamp, probably(?) will save few milliseconds?
		
		chrome.browsingData.remove({
		  "since": selectedTimeFrame
		}, {
		  "appcache": false,
		  "cache": false,
		  "cookies": false,
		  "downloads": settings.blockDownloads,
		  "fileSystems": false,
		  "formData": false,
		  "history": true,
		  "indexedDB": false,
		  "localStorage": false,
		  "pluginData": false,
		  "passwords": false,
		  "webSQL": false
		}, function(){ // callback
			//console.log(window.localStorage.timeStamp +' | '+ settings.xSeconds); 
			}
		); //end browserData cleaning
		
		
	}

// update icons and badges

function updateState(){
    laserExtensionId = "nnfehgmkbbbhbadghlfkjekjkneppdak"; 
	if (window.localStorage.historyDisabled == 'true') {
		changeBadge('off', 'X');
		chrome.browserAction.setTitle({"title":"History Disabled. Click to Enable."});
        chrome.runtime.sendMessage(laserExtensionId, {historyOff: true});
		
	} else {
		changeBadge('on', '');
		chrome.browserAction.setTitle({"title":"Click to Disable History."});
		chrome.runtime.sendMessage(laserExtensionId, {historyOff: false});
	}
}

function changeBadge(bgr, txt) {
    var bgr_values = {        
        "off": [215, 40, 40, 255],
		"on": [100, 200, 0, 255]
    };
    chrome.browserAction.setBadgeText({ "text": txt });
    chrome.browserAction.setBadgeBackgroundColor({ "color": bgr_values[bgr] });   
}



// intercept all windows changes (we need onCreate and onRemove handlers only)
chrome.windows.onCreated.addListener(function(){ //on every new wwindow, cleanup and check to restart timer
	deleteHistory();
	});
chrome.windows.onRemoved.addListener(function(){ //on every closed wwindow, cleanup and check to kill timer
	deleteHistory();
	});
// and go watch all tab changes to be able to cleanup soon after anything is missed, all because of the Chrome not firing chrome.history.onVisited properly...	
chrome.tabs.onCreated.addListener(function(){ //on every new tab
	deleteHistory();
	});		
chrome.tabs.onRemoved.addListener(function(){ //on every closed tab
	deleteHistory();
	});	
chrome.tabs.onUpdated.addListener(function(){ //on every tab update
	deleteHistory();
	});	
chrome.tabs.onActivated.addListener(function(){ //on every tab onActivated
	deleteHistory();
	});		
chrome.tabs.onReplaced.addListener(function(){ //on every tab onReplaced
	deleteHistory();
	});		
	
// For status requests API: *******************
// https://developer.chrome.com/apps/messaging
// ********************************************

chrome.runtime.onMessageExternal.addListener(
  function(request, sender, sendResponse) {
      
      //DON'T CHANGE THAT! *************************************
      pluginsExtensionLive = "mmcblfncjaclajmegihojiekebofjcen";
      
      //set the temp dev. extension here: **********************
      pluginsExtensionDevel = "mbcmhmphfnhcnninlpapnodidafadfmn"; //changes with dev.version!
      
      //set the APP here: **********************
      pluginsApp= "nnfehgmkbbbhbadghlfkjekjkneppdak"; 
      
      
    if ( (sender.id != pluginsExtensionLive) && (sender.id != pluginsExtensionDevel) && (sender.id != pluginsApp) ){
      return;  // don't allow this extension access
    } else {
        
        if(request.switchState){
            //command sent to switch state
            onClickHandler();
        }
        
      if (window.localStorage.historyDisabled == 'true'){ sendResponse({historyDisabled: true}); }
      else {sendResponse({historyDisabled: false});}
    }
  });
