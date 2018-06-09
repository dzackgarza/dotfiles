riot.tag('pd-button', pdButtonTemplate, function(opts) {
    var component = this;

    component.add = function (e) {
        var url = window.location.href;
        var title = document.title;

        if (opts && opts.url && opts.title) {
            url = opts.url;
            title = opts.title;
        }

        if (!url) {
            return false;
        }

        chrome.runtime.sendMessage({
            to: 'pomodone',
            action: 'add',
            data: {
                url: url,
                title: title,
                service: opts.service || ''
            }
        });

        e.stopPropagation();

        return false;
    };
});
