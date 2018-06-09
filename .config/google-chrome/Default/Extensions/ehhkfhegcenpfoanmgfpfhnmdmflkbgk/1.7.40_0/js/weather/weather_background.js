(() => { // make sure arrow functions work

// Note: all data is queried and stored in imperial 
// it's up to the display layer to convert it to the user's preference
// (user's language is stored from Yahoo Weather response)
// The public always gets a cached version of weather / geo
// Only our private timer can initiate a fetch for updating caches.

var stored = localStorage;
var errorLogger = console.error.bind(console);

window.getLocalWeather         = getLocalWeather;
window.getCurrentGeo           = getCurrentGeo;
window.getConditionTextForCode = getConditionTextForCode;

var WEATHER_SOFT_CACHE_EXPIRE =  5 * MINUTES;  // start new fetch after this
var WEATHER_HARD_CACHE_EXPIRE =  3 * HOURS;    // for how long cache may be used if fetching fails
var WEATHER_FETCH_MIN_DELAY   =  1 * MINUTES;  // how soon to retry after failed fetch

var GEO_SOFT_CACHE_EXPIRE = 1 * HOURS;        // start new fetch after this
var GEO_HARD_CACHE_EXPIRE = Infinity;         // for how long cache may be used if fetching fails
window.geoFetchFirstDelay = geoFetchFirstDelay; 
// run background fetching automatically to update caches
setTimeout(_ => { 
    fetchAndPublishGeo(); 
    setInterval(fetchAndPublishGeo, GEO_SOFT_CACHE_EXPIRE);
}, geoFetchFirstDelay(GEO_SOFT_CACHE_EXPIRE));
setInterval(fetchAndPublishWeather, WEATHER_SOFT_CACHE_EXPIRE);
setTimeout(fetchAndPublishWeather, 5000);

ensureCountryCodeIsStored();

// public

function getLocalWeather() {
  return getCurrentGeo().then(fallbackToCachedWeatherForGeo)
                        .catch(updateCachedWeather);
}

// private

function fetchAndPublishWeather() {
  return getCurrentGeo().then(fetchWeatherForGeo).then(publishWeatherUpdate);
}

function fetchWeatherForGeo(geo) {
  var latLon     = keyFromGeo(geo);
  var url = 'https://api-ak.wunderground.com/api/c991975b7f4186c0/conditions' + 
            '/forecast10day/hourly10day/labels/v:2.0/bestfct:1/q/' + latLon + '.json?ttl=300';
  console.log('weather: getting data for ' + latLon, '|', timestamp());
  return getJSON(url)
                .then(getWeatherFromResponse)
                .then(weather => appendGeoAccuracy(weather, geo.accurate))
                .then(weather => saveWeatherToCache(latLon, weather))
}

// weather: { condition, forecast, location, astronomy, atmosphere }
function getWeatherFromResponse(res) {
  res.forecast = res.forecast.days;
  res.location = res.response.location;
  return res;
}

function appendGeoAccuracy(weather, accurate) {
  weather.accurate = accurate;
  weather.location.accurate = accurate;
  return weather;
}

function getCachedWeatherForGeoIfRecent(geo, expiration) {
  expiration = expiration || WEATHER_SOFT_CACHE_EXPIRE;
  try {
    if (keyFromGeo(geo) == stored.WTR_geo_key && 
        Date.now() - stored.WTR_last_updated < expiration) 
      return JSON.parse(stored.WTR_data);
  }
  catch (e) { console.error(e.stack) } 
}

function fallbackToCachedWeatherForGeo(geo) {
  var geoKey = keyFromGeo(geo);
  var cache = getCachedWeatherForGeoIfRecent(geoKey, WEATHER_HARD_CACHE_EXPIRE);
  if (cache) return cache;
  else       throw new Error('cached weather is missing or old');
}

// save should NOT throw or break a then chain
function saveWeatherToCache(geo, data) {
  if (!data) return;
  try {
    stored.WTR_data = JSON.stringify(data);
    stored.WTR_geo_key = keyFromGeo(geo);
    stored.WTR_last_updated = Date.now();
    console.log('weather: saved weather for ' + stored.WTR_geo_key, '|', timestamp());
  } catch (e) { console.error(e.stack) }
  return data;
}

function updateCachedWeather() {
  if (updateCachedWeather.running) return;
  updateCachedWeather.running = true;
  var onUpdateFinished = (_ => updateCachedWeather.running = false);
  return fetchAndPublishWeather().then(onUpdateFinished).catch(onUpdateFinished);
}

// save should NOT throw or break a then chain
function saveUserLanguageFromResponse(res) {
  if (res.query.lang) stored.language = res.query.lang;
  return res;
}

// save should NOT throw or break a then chain
function publishWeatherUpdate(data) {
  chrome.runtime.sendMessage({ name: 'weather.updated', data: data });
  return data;
}

function keyFromGeo(geo1, geo2) {
  if (geo1 && geo2)              // in: (lat, lon)
    return [geo1, geo2].join(',');
  else if (geo1.lat && geo1.lon) // in: ({lat, lon})
    return [geo1.lat, geo1.lon].join(',');
  return geo1;                   // in: "lat,lon" ?
}

function urlForForYQLQuery(q) {
  return "https://query.yahooapis.com/v1/public/yql" +
         "?q=" + encodeURIComponent(q) + 
         "&format=json&callback=";
         // "&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys";
}

// woeid 
// Note: tied more to Geo than Weather module

function getCurrentWoeid() {
  return getCurrentGeo().then(getCachedWoeidIfMatchesGeo).catch(fetchAndSaveWoeidForGeo);
}

function getCachedWoeidIfMatchesGeo(geo) {
  if (keyFromGeo(geo) == keyFromGeo(JSON.parse(stored.GEO_location))) 
    return stored.WTR_woeid;
  else 
    throw new Error('stored woeid missing');
}

function fetchAndSaveWoeidForGeo(geo) {
  var q = 'SELECT woeid FROM geo.places(1) WHERE text="('+ keyFromGeo(geo) +')"';
  var weatherURL = urlForForYQLQuery(q);
  console.log('weather: fetching woeid for ' + keyFromGeo(geo));
  return getJSON(weatherURL)
            .then(res => stored.WTR_woeid = res.query.results.place.woeid);
}

/*
chrome.runtime.onMessage.addListener(message => {
  if (message.name == "geo.updated") 
    fetchAndSaveWoeidForGeo(message.data);
});
*/

chrome.runtime.onMessage.addListener(message => {
  if (message.name == 'geo.set') {
    saveGeoResponseToCache(message.data)
    saveGeoCountryCodeToCache(message.data);
    fetchAndPublishWeather();
  } else if (message.name == 'geo.fetch') {
    fetchAndPublishGeo().then(fetchAndPublishWeather);
  }
});

//
// Geo
//

function getCurrentGeo() {
  return Promise.resolve(fallbackToCachedGeo());
}

function geoFetchFirstDelay(expiration) {
  var elapsed = Date.now() - (localStorage.GEO_last_updated || 0);
  return Math.max(expiration - elapsed, 0);
}

function fetchAndPublishGeo() {
  return fetchCurrentGeo().then(publishGeoUpdate).catch(errorLogger);
}

function fetchCurrentGeo() {
  return fetchAccurateGeo()
        .catch(fetchCurrentGeoByIP)
        .then(saveGeoResponseToCache);
}

function ensureCountryCodeIsStored() {
  if (!stored.GEO_country_code)
    fetchCurrentGeoByIP().then(saveGeoCountryCodeToCache);
}

function fetchCurrentGeoByIP() {
  // Note: service APIs are descibed at the bottom of this file
  // They must be listed in order of their accuracy
  var geoAPIs = [
    "http://ip-api.com/json",
    "http://www.geoplugin.net/json.gp",
    "http://api.snoopi.io/v1/",
    "http:/geo.homenewtab.com:8000/geoip"
    //"http://ipinfo.io/json", bad accuracy sometimes? 
  ];

  var geoPromises = geoAPIs.map(geoAPI => 
                      getJSON(geoAPI)
                        .then(normalizeGeoResponse)
                        .then(verifyGeoResponse));

  console.log('weather: fetching geo');

  return Promise.preferred(geoPromises);
}

function getCachedGeoIfRecent(expiration) {
  expiration = expiration || GEO_SOFT_CACHE_EXPIRE;
  try {
    if (Date.now() - stored.GEO_last_updated < expiration)
      return JSON.parse(stored.GEO_location);
  }
  catch (e) { console.error(e.stack) } 
}

function fallbackToCachedGeo() {
  return getCachedGeoIfRecent(GEO_HARD_CACHE_EXPIRE);
}

// save should NOT throw or break a then chain
function saveGeoResponseToCache(geo) {
  if (!geo) return;
  stored.GEO_location = JSON.stringify(geo);
  stored.GEO_last_updated = geo.timestamp || Date.now();
  if (geo.customCity)
    stored.GEO_custom_city = geo.customCity;
  else 
    delete stored.GEO_custom_city;
  //console.log('weather: saved geo ' + stored.GEO_location);
  return geo;
}

// save should NOT throw or break a then chain
function saveGeoCountryCodeToCache(geo) {
  if (geo) stored.GEO_country_code = geo.countryCode;
  return geo;
}

// save should NOT throw or break a then chain
function publishGeoUpdate(data) {
  chrome.runtime.sendMessage({ name: 'geo.updated', data: data });
  return data;
}

function normalizeGeoResponse(res) {
  var normal = {};
  normal.city = res.city || res.City;
  normal.countryCode = res.countryCode || res.CountryCode || res.geoplugin_countryCode;
  normal.lat  = Number(res.lat || res.Latitude  || res.geoplugin_latitude);
  normal.lon  = Number(res.lon || res.Longitude || res.geoplugin_longitude);
  if (res.loc) {
    normal.lat = Number(res.loc.split(',')[0]);
    normal.lon = Number(res.loc.split(',')[1]);
  }
  return normal;
}

function verifyGeoResponse(res) {
  return (res.lat && res.lon)  // city no longer needed, it's a different fetch
         ? res
         : Promise.reject("missing field from geo response");
  // 'throw' might trigger error logger service
}

// Accurate Geo (dev: dfoifbgceijmbinnoobejmmdgeeelglf)
var WEATHER_EXT_ID = window.DEV ? 'foomlpdinaehlbhlncohiekomfdnicbj'
                                : 'foomlpdinaehlbhlncohiekomfdnicbj';

function fetchAccurateGeo() {
  return new Promise((resolve, reject) => {
    var port = chrome.runtime.connect(WEATHER_EXT_ID);
    port.postMessage({ name: 'geo.request', options: { maximumAge: 30*MINUTES } });

    port.onMessage.addListener(function(msg) {
      port.disconnect(); // we only kept the port alive so event page is not suspended
      if ('geo.response.success' == msg.name) {
        resolve(geoFromAccurateGeoResponse(msg.data));
      } else if ('geo.response.error' == msg.name) {
        reject(msg.error.message);
        throw new Error('geo external: ' + msg.error.message);
      } else {
        reject(msg);
        throw new Error('geo external: ' + JSON.stringify(msg));
      }
    });

    port.onDisconnect.addListener(function () {
      reject('port not available');
      //throw new Error('weather external extension disconnected (not installed?)');
    });
  });
}

function geoFromAccurateGeoResponse(data) {
  return  { // 4th decimal is 11m precision 
    lat : Number(data.coords.latitude.toFixed(4)), 
    lon : Number(data.coords.longitude.toFixed(4)),
    timestamp: data.timestamp,
    accurate : true 
  };
}

chrome.management.onEnabled.addListener(ext => {
  if (ext.id == WEATHER_EXT_ID)
    setTimeout(_ => fetchAndPublishGeo().then(fetchAndPublishWeather), 3000);
});


//
// Projax
//

function ajax(method, url) {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    if ('POST' == method) {
      var postParams = url.split('?')[1];
      url = url.split('?')[0];
    }
    xhr.open(method, url, true);
    if ('POST' == method)
      xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onload = () =>
     (xhr.status >= 200 && xhr.status < 300)
        ? resolve(xhr.responseText)
        : reject(xhr.statusText);
    xhr.onerror = () => 
      reject(xhr.statusText);
    xhr.send(postParams);
  });
}

function post(url) {
  return ajax("POST", url);
}

function get(url) {
  return ajax("GET", url);
}

function getJSON(url, callback) {
  return get(url).then((responseText) => JSON.parse(responseText));
}

function postJSON(url, callback) {
  return post(url).then((responseText) => JSON.parse(responseText));
}

function XHRStatus(req) {
  return { status: req.status, statusText: req.statusText }
}

function reflect(promise) {
    return promise.then(function(v){ return {v:v, status: "resolved" }},
                        function(e){ return {e:e, status: "rejected" }});
}

function whateverTheOutcome(promise) {
  return reflect(promise);
}

function timestamp() {
  return (new Date).toISOString().slice(0, -1);
}


/////////////////////////////////////////////////////////////////////////////

//
// Weather conditions
//

function getConditionTextForCode(code) {
  var table = getConditionTextForCodeTable();
  conditionTextForCode = code => table[code];
  return conditionTextForCode(code);
}

// https://output.jsbin.com/joquqiq
function getConditionTextForCodeTable() {
  return {
    0: "tornado",
    1: "tropical storm",
    2: "hurricane",
    3: "severe thunderstorms",
    4: "thunderstorms",
    5: "mixed rain and snow",
    6: "mixed rain and sleet",
    7: "mixed snow and sleet",
    8: "freezing drizzle",
    9: "drizzle",
    10: "freezing rain",
    11: "showers",
    12: "showers",
    13: "snow flurries",
    14: "light snow showers",
    15: "blowing snow",
    16: "snow",
    17: "hail",
    18: "sleet",
    19: "dust",
    20: "foggy",
    21: "haze",
    22: "smoky",
    23: "blustery",
    24: "windy",
    25: "cold",
    26: "cloudy",
    27: "mostly cloudy (night)",
    28: "mostly cloudy (day)",
    29: "partly cloudy (night)",
    30: "partly cloudy (day)",
    31: "clear (night)",
    32: "sunny",
    33: "fair (night)",
    34: "fair (day)",
    35: "mixed rain and hail",
    36: "hot",
    37: "isolated thunderstorms",
    38: "scattered thunderstorms (night)", // night was missing
    39: "scattered thunderstorms (day)",   // day was missing
    40: "scattered showers",
    41: "heavy snow",
    42: "scattered snow showers",
    43: "heavy snow",
    44: "partly cloudy",
    45: "thundershowers",
    46: "snow showers",
    47: "isolated thundershowers",
    3200: "not available" 
  };
}

// Possible rules:
// windy hour: Minimal chance of rain, Cloudcover 60-, Wind 20+, (clear, of few clouds)
// windy day:
// if rain: 1- in -> change 'pop' to 0%

//
// Geo services
//
// give this guy a medal :)
// http://stackoverflow.com/a/35123097/378024
//
// http://ip-api.com/json (callback=?)
//   { city:"<CITY>", lat: <LAT>, lon: <LON> }
// http://ipinfo.io/json
//   { "city": "<CITY>", "loc": "<LAT>,<LON>" }
// http://www.geoplugin.net/json.gp
//   { geoplugin_city:"", geoplugin_latitude:"<LAT>", geoplugin_longitude:"<LON>" }
//   Note: city was sometimes empty
//
// https://ip-json.rhcloud.com/json
//  { ... }
// 
// http://api.snoopi.io/v1/
//
// http://gd.geobytes.com/GetCityDetails?callback=?
//   Wrong location!
//

//
// IP Services
//
// https://l2.io/ip
// https://api.ipify.org  (https://api.ipify.org?format=jsonp&callback=?)
//

//
// User Language (from HTTP Request Header echo services)
//
// https://httpbin.org/headers
// https://ajaxhttpheaders1.appspot.com/?callback=c
//

// http://developer.yahoo.com/weather/#codes
// code = code.replace(/ /g, '-').replace('(day)', 'd').replace('(night)', 'n')
// class = wc-CODE

function getDummyGeo() {
  return Promise.resolve({ lat: 37.416275, lon: -123.025092 });
}

})();
