formatTime = function (seconds) {
    var sec_num = parseInt(seconds, 10);
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = hours+':'+minutes+':'+seconds;
    return time;
}

riot.tag('pd-info', pdInfoTemplate, function(opts) {
    var component = this;
    var url = window.location.href;

    component.view = {
        spentTime: null,
        isFetching: true,
        isHidden: true
    };

    function update (url, token) {
        var data = new FormData();

        component.view.isHidden = false;
        component.view.isFetching = true;
        component.update();

        data.append('url', url);
        data.append('token', token);

        fetch('https://my.pomodoneapp.com/extension/item/', {
            method: 'POST',
            body: data
        }).
        then(function (res) { return res.json() }).
        then(function (data) {
             component.view = {
                 spentTime: formatTime(data.time),
                 isFetching: false
             }
             component.update();
        });
    }

    chrome.storage && chrome.storage.sync.get({
        options: {}
    }, function(settings) {
        if (settings.options.apiKey) {
            update(location.href, settings.options.apiKey);
        }
    });
});
