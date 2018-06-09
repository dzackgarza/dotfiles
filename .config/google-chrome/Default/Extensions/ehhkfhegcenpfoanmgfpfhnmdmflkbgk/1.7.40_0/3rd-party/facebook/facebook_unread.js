

//(function() {

var url = "https://www.facebook.com/ajax/mercury/threadlist_info.php?__pc=EXP1%3ADEFAULT&dpr=3";
var url = "https://www.facebook.com/ajax/mercury/threadlist_info.php?dpr=2";

var gParams = {
client:"jewel",
"inbox[offset]":0,
"inbox[limit]":10,
//"inbox[filter]":'',
"__a":1,
"__dyn":"...",
//"__req":"j",//
"fb_dtsg":"...",
//"__user":1294246538,
//"ttstamp":"265817181831095510284748982586581696511745856581519075",
//"__rev":2229261 
};

window.addEventListener('message', function (m) {
  var message = m.data;
  if (message.action != 'fetch_facebook_unseen_messages') return;
  if (!message.data) return;
  //window.parent.postMessage('fetch_facebook_unseen_messages', "*");

  console.log('iframe', 'fetch_facebook_unseen_messages');

  gParams.__a = message.data.__a;
  gParams.__dyn = message.data.__dyn;
  gParams.fb_dtsg = message.data.fb_dtsg;
  fetchUnreadMessagesWithParams(gParams);
});

function fetchUnreadMessagesWithParams(params) {
  var http = new XMLHttpRequest();
  params = serialize(params);
  http.open("POST", url, true);
  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  //http.setRequestHeader("Content-length", params.length);
  //http.setRequestHeader("Connection", "close");

  http.onreadystatechange = function() {
      if (http.readyState == 4 && http.status == 200) {
        //console.log('iframe', http.responseText);
        //window.parent.postMessage(http.responseText, "*");
        //window.parent.postMessage({action: 'fb responded', data: http.responseText}, "*");
        processThreadsText(http.responseText);
      }
  }
  http.send(params);
}

function serialize(obj, prefix) {
  var str = [];
  for(var p in obj) {
    if (obj.hasOwnProperty(p)) {
      var k = prefix ? prefix + "[" + p + "]" : p, v = obj[p];
      str.push(typeof v == "object" ?
        serialize(v, k) :
        k + "=" + encodeURIComponent(v)); //encodeURIComponent(k)
    }
  }
  return str.join("&");
}

// for (;;);{... data

function processThreadsText(text) {
  text = text.slice(text.indexOf('{'));
  var data;
  try {
    data = JSON.parse(text);
    if (data.error) throw new Error(data.errorSummary);
    data = data.payload;
    if (!data) throw new Error("no payload for threads");
  } catch (e) {
    console.error('FB: parsing threads', e);
    return;
  }

  var users_table = {};
  if (!data.participants) return;
  data.participants.forEach(function (user) {
    users_table[user.fbid] = user;
  });
  
  // NOTE: tread_id and thread_fbid are different!
  // thread_fbid:"514252233" vs thread_id:"DeYTOBl4WcL1LLvls4P4Tg"


  // thread.last_message_timestamp
  // thread.last_read_timestamp

  // v1 , collect stuff mentioning unseen, then filter threads by what we collected
  var unseen_thread_ids_table = {};
  var unseen_thread_fbids_table = {};
  var unseen_other_user_fbids_table = {};

  data.unseen_thread_fbids.forEach(function (unseen_thread) {
    (unseen_thread.thread_ids||[]).forEach(function (thread_id) {
      unseen_thread_ids_table[thread_id] = true;
    });
    (unseen_thread.thread_fbids||[]).forEach(function (thread_id) {
      unseen_thread_fbids_table[thread_id] = true;
    });
    (unseen_thread.other_user_fbids||[]).forEach(function (thread_id) {
      unseen_other_user_fbids_table[thread_id] = true;
    });
  });

  var unseen_threads = data.threads.filter(function (thread) {
    return (unseen_thread_ids_table[thread.thread_id] || 
            unseen_thread_fbids_table[thread.thread_fbid] || 
            unseen_other_user_fbids_table[thread.other_user_fbid]);
  });

  // v2: concentrate on unread count of threads (but unread will stay unread)
  //var unseen_threads = data.threads.filter(function (thread) {
  //  return thread.unread_count;
  //});


  var unseenMessages = unseen_threads.map(function (thread) {
    var sender_fbid = thread.snippet_sender.replace('fbid:', ''); // or other_user_fbid
    var sender_name = users_table[sender_fbid].name;
    var sender_short_name = users_table[sender_fbid].short_name;

    return {
      thread_fbid  : thread.thread_fbid,
      sender_fbid  : sender_fbid,
      sender_name  : sender_name,
      sender_short_name: sender_short_name,
      snippet : thread.snippet,
      timestamp: thread.last_message_timestamp,
    }
  });

  window.parent.postMessage({action: 'unseen_messages', data: unseenMessages}, "*");
}



window.addEventListener('error', 
  function(message, source, lineno, colno, error) {
  //window.parent.postMessage(source + ':' + lineno + ' - ' + message + ' -- ' + error, "*");
  //window.parent.postMessage(arguments, "*");
});

//})();