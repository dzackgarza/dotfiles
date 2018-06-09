

(function(){

///stored.twitter_since_id = "193027013819371523";
stored.tweets || (stored.tweets = "");

var MAX_TWEETS = 20;

var base_url = "https://api.twitter.com/1/statuses/home_timeline.json?include_entities=1"
   //+ "&include_entities=1&include_available_features=1&contributor_details=true&pc=true"; &interval=90000


stored.tweets || (stored.tweets = "");


function processTweets(tweets) {

  if (!tweets.length) return;

  stored.twitter_since_id = tweets[0].id_str;

  var new_tweets = [];
  // going backwards is neccessary to get proper order by time DESC
  for (var i = tweets.length; i--;) {
    var tweet = tweets[i];
    var text = transformTweetLinks(tweet);
    text = transformTweetText(text);
    //tweet.user.screen_name = "@" + tweet.user.screen_name;
    var title = '<a href="https://twitter.com/' + tweet.user.screen_name + '" target="_blank">' + tweet.user.name + '</a>';
    new_tweets.push(tweet.id_str + FIELD_SEPARATOR + tweet.user.name + FIELD_SEPARATOR + text);
    create_notification('twitter', tweet.user.name, text);
    ///console.log(JSON.stringify(tweet));
  }

  var old_tweets = stored.tweets.split(ITEM_SEPARATOR);
  new_tweets.concat(old_tweets);
  new_tweets = new_tweets.slice(0, MAX_TWEETS);

  setTimeout(function() {
    stored.tweets = new_tweets.join(ITEM_SEPARATOR);
  }, 1000);

}

var pollInterval = FETCH_INTERVAL || 1000 * 30;  // 10 seconds

function scheduleRequest() {
  window.setTimeout(check, pollInterval);
}

function updateUnreadCount(unread) {
  set_indicator("twitter", unread);
}

function check() {
  getTimelineTweets();
  scheduleRequest();
}

function getTimelineTweets() { 
  url = base_url + (stored.twitter_since_id ? "&since_id=" + stored.twitter_since_id : "");
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.setRequestHeader('X-PHX','true');
  req.setRequestHeader('X-Requested-With','XMLHttpRequest');
  req.setRequestHeader('X-Twitter-Polling','true');
  req.onerror = function() {
    console.log("an error occurred");
  };
  req.onload = function() {
    var xml = this.responseText;
    if (this.status == 200) {
      processTweets(JSON.parse(this.responseText));
    }
    req = req.onload = req.onerror = null;
  };
  req.send(null);
}

// from silver bird
var transforms = [
  {
    //create links (based on John Gruber's pattern from
    //http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
    //'expression': /\b((([\w-]+):\/\/?|www[.])[^\s()<>]+((\([\w\d]+\))|([^,.;:'"`”“)~\s]|\/)))/gi,
    'expression': /\b(http:\/\/t\.co\/[a-z0-9_]+)/gi,
    'replacement': function() {
      var url = RegExp.$1;
      
      /*
      var scheme = RegExp.$3;
      if (scheme && !(/^(https?|ftp)$/i.exec(scheme))) {
        // possibly dangerous scheme, suppress it
        return url;
      }
      */

      var link = document.createElement("a");
      link.target = "_blank";
      link.href = url;
      link.textContent = url;
      return link.outerHTML;
    }
  }, {
    //create hash search links
    'expression': /([^&\w]|^)(#([\w\u0080-\uffff]*))((?=([^<])*?<a)|(?!.*?<\/a>))/gi,
    'replacement': function() {
      var header = RegExp.$1;
      var label  = RegExp.$2;
      var term   = RegExp.$3;

      var link = document.createElement("a");
      link.target = "_blank";
      link.href = "https://twitter.com/#!/search/%23" + term;
      link.textContent = "#" + term;
      return header + link.outerHTML;
  }
  }, {
    //create users links
    'expression': /(@(\w*)(\/\w+)?)((?=([^<])*?<a)|(?!.*?<\/a>))/gi,
    'replacement':
    function() {
      var username = RegExp.$2;
      var listPath = RegExp.$3 || "";
      var link = document.createElement("a");
      var linkText = username + listPath;

      link.target = "_blank";
      link.href = "https://twitter.com/" + username + listPath;
      link.textContent = linkText;
      return "@" + link.outerHTML;
    }
  }
];

function transformTweetText(text) {
  // we start from 1 to ignore transforming URLS
  // it is done by entities provided by Twitter API

  // currently: t.co seems to stay in so let's transform those links
  for (var i = 1; i < transforms.length; i++) {
    var t = transforms[i];
    text = text.replace(t.expression, t.replacement);
  }
  return text;
}

function transformTweetLinks(tweet) {
  var text = tweet.text;
  var entities = tweet.entities;
  var start = "";
  if (tweet.retweeted_status) {
    var retweet = tweet.retweeted_status;
    entities = retweet.entities;
    text = retweet.text;
    var start =  'RT <a href="https://twitter.com/'+ retweet.user.screen_name +'" target="_blank">@' + retweet.user.screen_name + '</a>: ';
    //var start =  'RT @<a href="https://twitter.com/'+ retweet.user.screen_name +'" target="_blank">' + retweet.user.screen_name + '</a>: ';
  }

  var urls = [].concat(entities.urls||[], entities.media||[]);
  var text_out = text;
  for (var i = 0; i < urls.length; i++) {
    var url = urls[i];
    text_out = text_out.replace(url.url, '<a href="'+ url.url +'" target="_blank">' + url.display_url + '</a>');
  }

  // hashtags [text, indices]
  // user_mentions [id_str, name, screen_name, indices]
  // ...

  // replace remaining t.co inner links
  text_out = text_out.replace(/(?:[^"'\w])(https?:\/\/t\.co\/[a-z0-9_]+)/gi, '<a href="$1" target="_blank">$1</a>');

  text_out = start + text_out;
  return text_out;
}

//window.addEventListener("DOMContentLoaded", check, false);
check();

})();



/*
https://api.twitter.com/1/direct_messages.json?count=50&include_entities=true

[{
  "recipient": {
    "id_str": "137002698",
    "id": 137002698,
    "notifications": false,
    "profile_text_color": "333333",
    "profile_image_url": "http:\/\/a0.twimg.com\/profile_images\/891437307\/q1198846148_622_normal.jpg",
    "friends_count": 81,
    "profile_background_image_url_https": "https:\/\/si0.twimg.com\/images\/themes\/theme1\/bg.png",
    "default_profile_image": false,
    "followers_count": 49,
    "favourites_count": 28,
    "profile_sidebar_border_color": "C0DEED",
    "location": "",
    "utc_offset": 3600,
    "name": "Bal\u00e1zs Galambosi",
    "profile_background_tile": false,
    "profile_sidebar_fill_color": "DDEEF6",
    "protected": false,
    "lang": "en",
    "default_profile": true,
    "time_zone": "Budapest",
    "contributors_enabled": false,
    "profile_background_color": "C0DEED",
    "description": "Developer of SmoothScroll extension for Google Chrome.",
    "geo_enabled": false,
    "profile_image_url_https": "https:\/\/si0.twimg.com\/profile_images\/891437307\/q1198846148_622_normal.jpg",
    "listed_count": 0,
    "profile_background_image_url": "http:\/\/a0.twimg.com\/images\/themes\/theme1\/bg.png",
    "show_all_inline_media": false,
    "following": false,
    "statuses_count": 415,
    "profile_link_color": "0084B4",
    "follow_request_sent": false,
    "url": "https:\/\/github.com\/galambalazs\/smoothscroll",
    "is_translator": false,
    "screen_name": "galambalazs",
    "profile_use_background_image": true,
    "verified": false,
    "created_at": "Sun Apr 25 14:10:03 +0000 2010"
  },
  ...
  ]

  */