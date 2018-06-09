(function (module, window) {
    module.injectionStamp = 'pd-injected';
    module.checkInterval = 1000;
    module.injectionQuery = '.docs-titlebar-buttons';

    module.path = chrome.extension.getURL('');

    module.pdButtonTemplate =
        '<a href="pomodone://app" style="color: inherit; margin: 2px 0 0 9px; position: relative; z-index: 9999; cursor: pointer; display: inline-block; vertical-align: middle;" class="" onclick="{ this.add }">' +
            '<span class="pomodone_ext__icon_image" style="display: inline-block; width: 24px; height: 24px; background-size: cover; background-image: url(' + module.path + 'icon128.png);"></span>' +
        '</a>';

    module.startTimer = function () {
        window.setInterval(function () {
            $(module.injectionQuery).each(function () {
                module.checkNode($(this));
            });
        }, module.checkInterval);
    };

    module.checkNode = function ($node) {
        if (!$node.attr(module.injectionStamp)) {
            module.injectToNode($node);
        }
    };

    module.getData = function ($node) {
        var title;
        var url;

        title = $('.docs-title-inner').text();
        url = location.href;

        return {
            title: title,
            url: url
        };
    };

    module.injectToNode = function ($node) {
        $node.attr(module.injectionStamp, true);
        $node.append('<pd-button></pd-button>');

        riot.mount('pd-button', module.getData($node));
    };

    $(function () {
        window.pdButtonTemplate = module.pdButtonTemplate;

        module.startTimer();
    });
})({}, window);
