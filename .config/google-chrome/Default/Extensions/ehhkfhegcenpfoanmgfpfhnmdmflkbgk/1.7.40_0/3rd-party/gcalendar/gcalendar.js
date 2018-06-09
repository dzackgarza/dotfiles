(function() {

// TODO
//
// TEMP: remove Google Caledanr support until a fix is found for this issue: 
//
// Your item is making a large volume of requests to Calendar API service. It makes apiary calendar requests with developer_project_id set to 0 and results in high volume of dailyLimitExceededUnreg 403 errors. Please ensure that your item does not make requests that are triggering forbidden responses.
//
window.GCAL_checkAuth = function () {};
return;



// RELEASE: 1024356103437-t90vgokgf8d7fi0cef1imopvgsh02pvl
// DEBUG:   1024356103437-kb5uconje3r0p2rgemdgv7cmlmfo3a7k
var CLIENT_CODE = window.DEV 
                ? '1024356103437-kb5uconje3r0p2rgemdgv7cmlmfo3a7k'
                : '1024356103437-t90vgokgf8d7fi0cef1imopvgsh02pvl';
var CLIENT_ID = CLIENT_CODE + '.apps.googleusercontent.com';

var SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"];

// Time between server polls = 30 minutes.
var POLL_INTERVAL =  FETCH_INTERVAL || 1000 * 30;  // 10 seconds

/////////////////////////////////////////////////////////////////////

var LOCALSTORAGE_PREFIX = "GCAL_";
var pollUnderProgress = false;
var defaultAuthor = '';
var isMultiCalendar = false;

//This is used to poll only once per second at most, and delay that if
//we keep hitting pages that would otherwise force a load.
var pendingLoadId_ = null;
var isAuthorized = false;

// after first auth this stays 'true' even if our token expires, 
// and isAuthorized becomes 'false'
var wasAuthorizedBefore = false; 


/////////////////////////////////////////////////////////////////////


CalendarManager = {};

// multi calendar later:
//  localStorageSet('calendars', calendars);

/**
 * Polls the server to get the feed of the user.
 */
CalendarManager.pollServer = function() {
  if (! pollUnderProgress) {
    localStorageSet('eventList', []);
    pollUnderProgress = true;
    pendingLoadId_ = null;
    localStorageSet('calendars', []);
    localStorageSet('lastPollTime', Date.now());

    listUpcomingEvents(function(events) {
      pollUnderProgress = false;
      if (!events || !events.length) {
        console.log('GCAL: No events');
        localStorageSet('nextEvent', null);
        return;
      }

      handleFetchedEvents(events);
    });
  }
};

function handleFetchedEvents(events) {
  var eventList = localStorageGet('eventList', []);

  events.forEach(function (baseEvent) {

    var event = {};
    event.startTime = +new Date(baseEvent.start.dateTime || baseEvent.start.date);
    event.endTime = +new Date(baseEvent.end.dateTime || baseEvent.end.date);
    event.title = baseEvent.summary;
    event.location = baseEvent.location;
    event.url = baseEvent.htmlLink;
    event.id = baseEvent.id;

    //if (event.startTime > Date.now()) {
      eventList.push(event);
    //}
  });
  localStorageSet('eventList', eventList);
  chrome.runtime.sendMessage({
    name : 'upcoming-event', 
    data : eventList
  });
}

var DATE_TIME_REGEX =
  /^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\.\d+(\+|-)(\d\d):(\d\d)$/;
var DATE_TIME_REGEX_Z = /^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\.\d+Z$/;
var DATE_REGEX = /^(\d\d\d\d)-(\d\d)-(\d\d)$/;

/**
* Convert the incoming date into a javascript date.
* @param {String} rfc3339 The rfc date in string format as following
*     2006-04-28T09:00:00.000-07:00
*     2006-04-28T09:00:00.000Z
*     2006-04-19.
* @return {Date} The javascript date format of the incoming date.
*/
function rfc3339StringToDate(rfc3339) {
  var parts = DATE_TIME_REGEX.exec(rfc3339);

  // Try out the Z version
  if (!parts) {
    parts = DATE_TIME_REGEX_Z.exec(rfc3339);
  }

  if (parts && parts.length > 0) {
    var d = new Date();
    d.setUTCFullYear(parts[1], parseInt(parts[2], 10) - 1, parts[3]);
    d.setUTCHours(parts[4]);
    d.setUTCMinutes(parts[5]);
    d.setUTCSeconds(parts[6]);

    var tzOffsetFeedMin = 0;
    if (parts.length > 7) {
      tzOffsetFeedMin = parseInt(parts[8], 10) * 60 + parseInt(parts[9], 10);
      if (parts[7] != '-') { // This is supposed to be backwards.
        tzOffsetFeedMin = -tzOffsetFeedMin;
      }
    }
    return new Date(d.getTime() + tzOffsetFeedMin * 60 * 1000);
  }

  parts = DATE_REGEX.exec(rfc3339);
  if (parts && parts.length > 0) {
    return new Date(parts[1], parseInt(parts[2], 10) - 1, parts[3]);
  }
  return null;
}

/*
 * Function runs on completed navigation with a url of google applications.
 * @param {details} details of the completed web navigation.
 */
function onCompleted(details) {
  var url = details.url;

  if ((url.indexOf('calendar.google.com/calendar/') != -1) ||
      ((url.indexOf('www.google.com/a/') != -1) &&
      (url.lastIndexOf('/acs') == url.length - 4)) ||
      (url.indexOf('www.google.com/accounts/') != -1)) {

    if (pendingLoadId_) {
      clearTimeout(pendingLoadId_);
      pendingLoadId_ = null;
    }

    // try to poll in 2 second [which makes the redirects settle down]
    pendingLoadId_ = setTimeout(CalendarManager.pollServer, 2000);
  }
}

function onInstalled() {
  CalendarManager.pollServer();
  localStorageSet('lastPollTime', 0);
  localStorageSet('nextEvent', null);
}

isMultiCalendar = localStorageGet('multiCalendar', false);
chrome.runtime.onInstalled.addListener(onInstalled);
chrome.webNavigation.onCompleted.addListener(onCompleted,
    {url: [{hostSuffix: 'calendar.google.com', pathPrefix: '/calendar'},
           {hostSuffix: 'www.google.com', pathPrefix: '/accounts'},
           {hostSuffix: 'www.google.com', pathPrefix: '/a'}]});

/////////////////////////////////////////////////////////////////////

function promptForAuth() {
  gapi.auth.authorize({
    'client_id' : CLIENT_ID,
    'scope'     : SCOPES,
    'immediate' : false // true means background mode, false opens a prompt
  }, handleAuthResult);
  setTimeout(checkAuthRecur, 2000);
}

/**
 * Check if current user has authorized this application.
 */
window.GCAL_checkAuth = checkAuth;

function checkAuthRecur() {
  if (isAuthorized) 
    return console.log('GCAL: alredy isAuthorized, checkAuthRecur');
  checkAuth();
  setTimeout(checkAuthRecur, 2000);
}

function checkAuth() {
  if (isAuthorized) 
    return console.log('GCAL: alredy isAuthorized, checkAuth');
  requestAuth();
}

function requestAuth() {
  setTimeout(function () {
    //gapi.client.setApiKey(apiKey);
    gapi.auth.authorize({
      'client_id' : CLIENT_ID,
      'scope'     : SCOPES,
      'immediate' : true // true means background mode, false opens a prompt
    }, handleAuthResult);
  }, 1);
}

/**
 * Handle response from authorization server.
 *
 * @param {Object} authResult Authorization result.
 */
function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    // Hide auth UI, then load client library.
    //authorizeDiv.style.display = 'none';
    isAuthorized = true;
    wasAuthorizedBefore = true;
    CalendarManager.pollServer();
  } else {
    // Show auth UI, allowing the user to initiate authorization by
    // clicking authorize button.
    //authorizeDiv.style.display = 'inline';
    isAuthorized = false;
    console.error('GCAL: handleAuthResult: set isAuthorized to false');
  }
}

/**
 * Initiate auth flow in response to user clicking authorize button.
 *
 * @param {Event} event Button click event.
 */
function handleAuthClick(event) {
  gapi.auth.authorize(
    {client_id: CLIENT_ID, scope: SCOPES, immediate: false},
    handleAuthResult);
  return false;
}

/**
 * Load Google Calendar client library. List upcoming events
 * once client library is loaded.
 */
function loadCalendarApi(callback) {
  if (!isAuthorized) {
    pollUnderProgress = false; 
    console.error('GCAL: loadCalendarApi: isAuthorized is false');
    return; // callback(error) ?
  }
  gapi.client.load('calendar', 'v3', callback);
}

function listUpcomingEvents(callback) {
  loadCalendarApi(function () {
    listUpcomingEventsApiLoaded(callback);
  })
}

/**
 * Print the summary and start datetime/date of the next ten events in
 * the authorized user's calendar. If no events are found an
 * appropriate message is printed.
 */
function listUpcomingEventsApiLoaded(callback) {
  var request = gapi.client.calendar.events.list({
    'calendarId': 'primary',
    'timeMin': (new Date()).toISOString(),
    'showDeleted': false,
    'singleEvents': true,
    'maxResults': 10,
    'orderBy': 'startTime'
  });

  request.execute(function(res) {
    // 401: Invalid Credentials (reason: authError)
    // 403: Daily Limit for Unauthenticated Use Exceeded. (reason: dailyLimitExceededUnreg)
    if (res.error && (res.error.code == 401 || res.error.code == 403)) {
      isAuthorized = false;
      requestAuth(); // it'll refetch events upon success
      pollUnderProgress = false; // TODO: doesn't really belong here
      return;
    }
    var events = res.items;
    callback && callback(events);
  });
}

/////////////////////////////////////////////////////////////////////

//
// LocalStorage
//

/**
 * Sets |key| as |value| in localStorage. |value| may be any JavaScript object;
 * this method will automatically stringify to JSON if needed.
 */
function localStorageSet(key, value) {
  if (typeof value == 'undefined') {
    // Don't try to stringify undefined, or bad things may happen (particularly
    // in localStorageGet, so let's be consistent).
    delete localStorage[LOCALSTORAGE_PREFIX + key];
  } else {
    localStorage[LOCALSTORAGE_PREFIX + key] = JSON.stringify(value);
  }
}

/**
 * Gets the JavaScript object at |key| from localStorage, defaulting to |deflt|
 * if it hasn't been set. Assumes that the value was written by localStorageSet
 * (i.e. stored as JSON).
 */
function localStorageGet(key, deflt) {
  var value = localStorage[LOCALSTORAGE_PREFIX + key];
  var returnValue;
  try {
    returnValue = (typeof value == 'undefined') ? deflt : JSON.parse(value);
  } catch (e) {
    logError(new Error("ERROR: gcalendar localStorageGet: " + key));
    throw new Error("gcalendar localStorageGet: " + key + " => " + value);
  } 
  return returnValue;
}

/////////////////////////////////////////////////////////////////////

/*
 * Fires once per minute to fetch
 */
function refetch() {
  CalendarManager.pollServer();
}

refetch();
window.setInterval(refetch, POLL_INTERVAL);

function onMessage(request, sender, sendResponse) {
  if (request == "get-calendar-events") {
    isAuthorized
      ? sendResponse(localStorageGet('eventList'))
      : sendResponse('forbidden');
  } 
  else if (request == "prompt-calendar-auth") {
    promptForAuth();
  } 
}

window.get_calendar_events = function() {
  return localStorageGet('eventList');
}

chrome.extension.onMessage.addListener(onMessage);

})();