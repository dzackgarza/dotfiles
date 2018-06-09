	
(function(){

var console = { log: function(){} };

//time gap between two pollings		
var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds
//time between two unread mail countings
var foldercountInterval = FETCH_INTERVAL || 1000*60  // 1 minute

	
//utility varaibles for counting
	//counts unsucessful pollings
	var	errCount=0;
    var notLoggedInCount=0; 	
	var oldTotalNew=0;
	//accumulated new mails
	var totalNew = 0;
	//displayed accumulated new mails
	var displaytotal = 0;
	//time that checking for new mails happened
	var lastCheckTime = "";
	//total unread mails
	var oldUnreadCount=0;
	var newUnreadCount=0;
	//specialize the first run
	var firstTime=true;
	//total number of mails in inbox
	var totalMails = 0;

var description="";
//decides whether to alert the user
var stop_alerts=false;

//mail URL List
	//URL for yahoo mail box
	var yahooMail = "http://mail.yahoo.com/";
	var defaultcheckURL = "http://api2.my.yahoo.com/2.0/content/widgetcount";   //assign this to checkURL
	var checkURL = defaultcheckURL;
	//var checkURL = "http://update.toolbar.yahoo.co.jp/slv/v4/not";   //for Japan
	//normally used address
	var mailFolderURL =  "http://us.mg1.mail.yahoo.com/ws/mail/v1/formrpc?m=ListFolders&appid=YahooMailRC";

//set the place where message box should appear
var xPosition = screen.width-200;
var yPosition = screen.height-150;	


//This is where the background functionality begins

function init() {
	firstTime = true;
	//getMailFolderCount();
   // checkMail();
	check();
}

function check()
{
	getMailFolderCount();
	checkMail();
	scheduleRequest();
}
//set timer for the next iteration

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}


/* ========== MAIL PROTOCOL FUNCTIONS ========== */

function getMailFolderCount() { 
		// Doesn't work for Yahoo Japan.
		if (checkURL == "http://update.toolbar.yahoo.co.jp/slv/v4/not" ) return;
		var theURL = mailFolderURL;
		console.log("Getting mail folder info at " + theURL);
		
		try {
			// Create a new XMLHttpRequest object so it doesn't interfere with checking for mail.
			
			var requester = new XMLHttpRequest();
			requester.open("GET", theURL, true);
			requester.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
			requester.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
			requester.onerror = function() {
				// An error occurred, notify user
				console.log("an error occurred");
				this.abort();
			}
			requester.onload = function() {
				
				console.log("getMailFolderCount request status (" + this.status + ")");
				if (this.readyState==4) {
					console.log("ReponseText: " + this.responseText);
					
					if (this.status == 200) {
						handleSuccess();
						var xmldoc = this.responseXML;
						var folders = xmldoc.getElementsByTagName('folder');
						var unread = 0;
						var total = 0;
						for (var i=0; i<folders.length; i++) {
							if ((folders.item(i).getAttribute("isSystem") == "false") || (folders.item(i).firstChild.getAttribute("name") == "Inbox")) {
								unread = unread + parseInt(folders.item(i).getAttribute("unread"));
								total = total + parseInt(folders.item(i).getAttribute("total"));
							}
						}
						console.log("Folders: " + folders.length + ", Unread: " + unread + ", Total: " + total);
						newUnreadCount=unread;
						totalMails=total;
						//if first time this is running


						updateUnreadCount();
						
						
						//ready for next read
						oldUnreadCount=newUnreadCount;
					}
					else if (this.status == 500) {
						var xmldoc = this.responseXML;
						var code = xmldoc.getElementsByTagName('code').item(0);
						if ((typeof(code) != "undefined") && code && code.firstChild) {
						
							if (code.firstChild.data == "Client.ExpiredCredentials") {
															notLoggedInCount=notLoggedInCount+1;
								notLoggedInCount=notLoggedInCount+1;
								if(notLoggedInCount == 5){
									if(stop_alerts == false )
									{
										openErrorMessage();		//alert("Please log into Yahoo Mail. Credential expired.");
									}
								}
								return;
							}
							// Need new session id
							else if (code.firstChild.data == "Client.ClientRedirect.SessionIdReissue") {
								var newURL = xmldoc.getElementsByTagName('url').item(0);
								if ((typeof(newURL) != "undefined") && newURL && newURL.firstChild) {
									console.log("Redirection URL: " + newURL.firstChild.data);
									mailFolderURL = newURL.firstChild.data;
									getMailFolderCount();
								}
							}
						}
					}
					else {
						var xmldoc = this.responseXML;
						var reasonText = "none";
						if (xmldoc) {
						 	var message = xmldoc.getElementsByTagName('message').item(0);
						 	if ((typeof(message) != "undefined") && message && message.firstChild) reasonText = message.firstChild.data;
						}
						console.log("Could not retrieve folder count. Reason: " + reasonText);
					}
				}
			} 
			// If xmlHttpReq is ready, send request
			if (requester.readyState == 1) {		
				requester.send(null);
			}
			// if it is not ready try again 
			else {
				console.log("getMailFolderCount readyState = " + requester.readyState + ", retrying in 2 seconds.");
				requester.abort();
			
			}
		}
		catch (ex)
		{
			console.log("error thrown" +ex);
		}

	}





 function checkMail() {

		// set correct URLs	
		console.log("Checking mail for " +checkURL);
		// Initialize XMLHttpRequest object 
		console.log("xmlHttpReq not created yet, so creating it.");
		xmlHttpReq = new XMLHttpRequest();
		xmlHttpReq.open("GET",checkURL, true);
		xmlHttpReq.setRequestHeader('Cache-Control','no-cache, must-revalidate, proxy-revalidate');
		xmlHttpReq.setRequestHeader('Pragma','no-cache, must-revalidate, proxy-revalidate');
		xmlHttpReq.onerror = function() {
			// An error occurred, notify user
			xmlHttpReq.abort();
			xmlHttpReq = null;  // needed or send won't do anything
			console.log("fail counts"+errCount);
			handleError();		
		}
	xmlHttpReq.onload = function() {
			
			if (xmlHttpReq.readyState==4) {
				
				if (xmlHttpReq.status == 200) {
					handleSuccess();
					var response = xmlHttpReq.responseText;
					console.log("Response: " + response);
					var result = null;
					if (checkURL == defaultcheckURL) {
						var xmldoc = xmlHttpReq.responseXML;
						var description = xmldoc.getElementsByTagName('description').item(0);
						if ((typeof(description) != "undefined") && description && description.firstChild) {
							result = description.firstChild.data;
							console.log("Result: " + result);
						}
						// not logged in 
						else {
							console.log("Say user to log in");
							notLoggedInCount=notLoggedInCount+1;
							if(notLoggedInCount == 5){
								if(stop_alerts == false )
								{
									openErrorMessage();		//alert("Please log into Yahoo Mail.");
								}
								setLoggedOutState();
							}
							return;
						}
					}
					// for japan people
					else if (checkURL == "http://update.toolbar.yahoo.co.jp/slv/v4/not") {
						if (/\s(\d+)\s.*yahoo/.test(response))	result = RegExp.$1;
							console.log("Japaneese");
							console.log("Result:" + result);
					}
					
					
					if(notLoggedInCount>5){
					notLoggedInCount=0;
					setLoggedInState();
					}
					var now = new Date();
					var hours = now.getHours();
					var minutes = now.getMinutes();
					if (minutes < 10) minutes = "0" + minutes;
				    lastCheckTime = "(" + hours + ":" + minutes + ")";
					localStorage["lastCheckTime"] = lastCheckTime;
	
					try {
						if (!result) {
							console.log("no mail");
							// say user that he has no new mails
						}
						else {
							console.log("new mail: " + result + " messages");
							console.log("alert user: " + result + " messages");
							
							
							totalNew= result;
							
							if(totalNew>oldTotalNew){
							 displaytotal+=1;
							 updateUnreadCount();
							 oldTotalNew=totalNew;
							}

						}
					}
					catch(ex) {
						console.log(ex, 1);
					}
				}
				//if status is not 200
				else {
					console.log("Bad status, showing error\n" + xmlHttpReq.getAllResponseHeaders());
				}
			}
		}
		
		
		// If xmlHttpReq is ready, send request
		if (xmlHttpReq.readyState == 1) {
			xmlHttpReq.send(null);
		}

		
	}
  
 /*---------------------    -------------------------------*/
  
  
  
  //update the GUI
function updateUnreadCount() {

		if(totalNew!=0){
			description = displaytotal +" total new mails\n"+newUnreadCount+" unread mails";
		}
		
		set_indicator("yahoo-mail", newUnreadCount);

		//work according to preferences	
		if(stop_alerts == false ){			

			console.log("stop alert is false");
			//alert("you have a new mail");
			openPopup();
		}	
	}
  
function handleError(){
	 errCount+=1;
	 if(errCount==7)
	 {
		 console.log("Mail Server not responding. Alert");
		// alert("Yahoo Mail Server is not responding. Maybe you are offline"); 
	 } 
} 
  


function handleSuccess()
{
	if(errCount>7)
	{
		//alert("Yahoo Mail server is responding. Mail alerting service is started.");
		errCount=0;
	}
} 

  
function openPopup() {
	/*
  SW=window.open('popup.html','NewWin','toolbar=no,status=no,width=300,height=135')  
  SW.moveTo(xPosition,yPosition);  // change the #s at the left to adjust the place the popup should open
  //SW.moveTo(670,950); 
  setTimeout(function(){
  	closeWin(SW);
  }, 5000);
  */
}

function openErrorMessage() {
	/*
  SW=window.open('error message popup.html','NewWin','toolbar=no,status=no,width=300,height=135')  
  SW.moveTo(xPosition,yPosition);  // change the #s at the left to adjust the place the popup should open
  //SW.moveTo(670,950); 
  setTimeout(function(){
  	closeWin(SW);
  }, 5000);
  */
}

function closeWin(newWindow) {
newWindow.close();				// close small window and depart
}
  

window.addEventListener("DOMContentLoaded", init, false);


})();
///console.log("icon selected testlast:"+iconPath);
