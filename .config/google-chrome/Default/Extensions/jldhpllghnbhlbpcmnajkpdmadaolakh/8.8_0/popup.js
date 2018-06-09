var DOMAIN = 'chrome.todoist.com';

window.addEventListener('message', function(e) {
    var BG_PAGE = chrome.extension.getBackgroundPage();
    var str_data = e.data;

    if(str_data && str_data.indexOf('SWITCH_URL:') != -1) {
        str_data = str_data.replace('SWITCH_URL:', '');

        chrome.tabs.getSelected(null, function(tab) {
            if(tab) {
                chrome.tabs.update(tab.id, {url: str_data});
            }
        });
    }
    else if(str_data && str_data.indexOf('UPDATE_COUNT:') != -1) {
        str_data = str_data.replace('UPDATE_COUNT:', '');

        var counts = JSON.parse(str_data);
        BG_PAGE.updateBadge(counts.today + counts.overdue,
                            counts.overdue > 0);
    }
    else if(str_data && str_data.indexOf('DISABLE_TOOLTIP:') != -1) {
        RateMe.disable();
        RateMe.disableViaAjax();
    }
    else if(str_data && str_data.indexOf('RESET_TOOLTIP:') != -1) {
        RateMe.reset();
    }
    else if(str_data.match(/^https?/)) {
        BG_PAGE.setFrameLocation(str_data);
    }
}, false);


function init() {
    window.BG_PAGE = chrome.extension.getBackgroundPage();
    TODOIST_FRAME = document.getElementById('todoist_frame');

    var last_location = BG_PAGE.getFrameLocation();

    if(last_location && last_location.indexOf('todoist.com/app') != -1)
        TODOIST_FRAME.src = last_location;
    else
        TODOIST_FRAME.src = "https://"+DOMAIN+"/?mini=1";

    setInterval(postLocationAndTitle, 200);
    setInterval(RateMe.maybeShow, 1000);

    RateMe.increaseOpenCount();
}


function postLocationAndTitle() {
    var cur_location = BG_PAGE.getCurrentLocationAndTitle();
    var data_to_send = cur_location.location + '--/--' + cur_location.title;
    TODOIST_FRAME.contentWindow.postMessage(data_to_send, '*');
}


document.addEventListener('DOMContentLoaded', function() {
    init();
});


/*
 * Rating counter
 * ----
 * Every 15th open we check to see if we should present a tip
 * to the user asking to rate us.
 *
 * This data is stored locally.
 */
RateMe = {

    // How many opens do the user need to do before we ask them to
    // rate us.
    //show_on_open: 15,
    show_on_open: 2,

    increaseOpenCount: function() {
        var session = BG_PAGE.getSession();

        if(session['rating_disabled'] == 'yes')
            return ;

        var cur_count = parseInt(session['open_count']) || 0;
        cur_count++;

        RateMe.open_count = session['open_count'] = cur_count;
    },

    maybeShow: function() {
        if(BG_PAGE.getSession()['rating_disabled'] == 'yes')
            return ;

        if(RateMe.open_count >= RateMe.show_on_open) {
            if(RateMe.server_seen_value == 'not_seen')
                RateMe.showTooltip();
            else
                RateMe.setShouldShowTooltip();
        }
    },

    disable: function() {
        var session = BG_PAGE.getSession();
        session['rating_disabled'] = 'yes';
    },

    disableViaAjax: function() {
        doGetRequest('https://'+ DOMAIN +'/Tooltips/markAsSeen?name=chrome_rating');
    },

    showTooltip: function() {
        var todoist_frame = document.getElementById('todoist_frame');
        var iframe_loc = BG_PAGE.getFrameLocation();

        if(iframe_loc && iframe_loc.indexOf('/app') != -1) {
            var msg = JSON.stringify({
                'type': 'USER_TOOLTIP',
                'message': 'rate_chrome_plugin',
                'action_url': 'https://chrome.google.com/webstore/detail/todoist-to-do-list-and-ta/jldhpllghnbhlbpcmnajkpdmadaolakh/reviews'
            });

            todoist_frame.contentWindow.postMessage(msg, '*');
        }
    },

    server_seen_value: undefined,
    setShouldShowTooltip: function() {
        doGetRequest('https://'+DOMAIN+'/Tooltips/isSeen?name=chrome_rating',
                     function(xhr) {
                         var text = xhr.responseText;

                         if(text == 'not_seen') {
                            RateMe.server_seen_value = 'not_seen';
                            RateMe.showTooltip();
                         }
                         else {
                             RateMe.disable();
                         }
                     },
                     RateMe.reset);
    },

    reset: function() {
        var session = BG_PAGE.getSession();

        if(session['rating_disabled'])
            delete session['rating_disabled'];

        RateMe.open_count = session['open_count'] = 0;
        doGetRequest('https://'+DOMAIN+'/Tooltips/resetSeen?name=chrome_rating');
    }

}


//--- Helpers ----------------------------------------------
doGetRequest = function(url, callback, errback) {
    var xhr = new XMLHttpRequest();

    xhr.open('GET', url, true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if(callback)
                callback(xhr);
        }
        else if(xhr.readyState == 4 && xhr.status == 403) {
            if(errback)
                errback(xhr);
        }
    }
    xhr.send(null);
}
