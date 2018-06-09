
//
// Some people reported QuotaExceededError for LocalStorage
// This tries to clear out LS as a one off thing. 
//

var backupKeys = [
	'settings',
	'icons_order',
	'custom_apps',
	'user_app_id_inc',
	'user_app_ids', // + don't forget user_app_{id}
	'install_time',

	'FB_history_index_enabled',
	'FB_history_index_user_response_time',
	'FB_index_base_time',
	'FB_index_first_run_complete',
	'FB_index_is_building',
	'FB_index_ready',
	'FB_search_promo_after'
];

setTimeout(function () {

try {
  localStorage.TEST_quotaTest = Array((10*1024)+1).join('a');
} catch (e) {
	if (e && e.name == 'QuotaExceededError') {
		tryToFigureOutWhatWentWrong();
		clearLocalStorageButKeepAsMuchAsWeCan();
	}
} 
delete localStorage.TEST_quotaTest;

}, 1000);

function clearLocalStorageButKeepAsMuchAsWeCan() {

	console.log('clearLocalStorageButKeepAsMuchAsWeCan');

	var backupData = {};
	backupKeys.forEach(function (key) {
		backupData[key] = localStorage[key];
	});

	// user apps needs special treatment
	var user_app_ids = backupData.user_app_ids.split(',');
	user_app_ids.forEach(function (id) {
		if (!id) return;
		backupData[id] = localStorage[id];
	});

	// no turning back...
	localStorage.clear();

	// restore what we saved
	Object.keys(backupData).forEach(function (key) {
		localStorage[key] = backupData[key];
	});

	setTimeout(function () {
		location.reload();
	}, 1000);
}


//////////////////////////////////////////////////


function tryToFigureOutWhatWentWrong() {

	return; /// Save this for later


	var data = [];

	console.time('snapshot');

	if (localStorage.length > 1000) {
		// serious issue, tons of keys, don't even itarate
		// ...
	} if (localStorage.length > 200) { 
	  // relatively large number of keys 
		var stored = JSON.parse(JSON.stringify(localStorage));
		var keys = Object.keys(stored);
		keys.forEach(function (key) {
		   var len = stored[key].length;
		   if (len > 500)
		     data.push([key, len])
		})
	} else {
	  // few keys, one of them is big
		var keys = Object.keys(localStorage);
		keys.forEach(function (key) {
		   var len = localStorage[key].length;
		   if (len > 500)
		     data.push([key, len])
		})
	}

	console.timeEnd('snapshot');
}


/*
localStorage.test = '';
var MB = Array((1024*1024)+1).join('a');
for (var i = 0; i < 100; i++) {
  try {
     localStorage.test += MB;
     //console.log(i)
  } catch (e) {
   	console.log(i); 
   	console.log(JSON.stringify(localStorage).length / 1024 / 1024);
   	break; 
   }
}
*/