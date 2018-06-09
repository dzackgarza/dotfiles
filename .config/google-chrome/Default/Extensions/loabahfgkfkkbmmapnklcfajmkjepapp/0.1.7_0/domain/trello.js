(function (module, window) {
    module.injectionStamp = 'pd-injected';
    module.checkInterval = 1000;
    module.injectionQuery = '.card-detail-window .window-sidebar .other-actions .u-clearfix';
    module.infoInjectionQuery = '.card-detail-window .card-detail-data';

    module.path = chrome.extension.getURL('');

    module.pdButtonTemplate =
        '<a href="pomodone://app" class="button-link" onclick="{ this.add }">' +
            '<span class="icon-sm" style="background: url(' + module.path + 'icon128.png); background-size: cover; vertical-align: middle;"></span> <span style="vertical-align: middle;">PomoDone It!</span>' +
        '</a>';

    module.pdInfoTemplate = `
        <div if={!view.isHidden} class="pomodone_message">
            <img class="pomodone_message__icon" src="${module.path}icon128.png" />
            <div if={!view.isFetching}>Time spent: <strong>{view.spentTime}</strong></div>
            <div if={view.isFetching}>Updating...</div>
        </div>
    `;

    module.startTimer = function () {
        window.setInterval(function () {
            $(module.injectionQuery).each(function () {
                module.checkNode($(this), function ($node) {
                    module.injectButtonToNode($node);
                });
            });
            $(module.infoInjectionQuery).each(function () {
                module.checkNode($(this), function ($node) {
                    module.injectInfoToNode($node);
                });
            });
        }, module.checkInterval);
    };

    module.checkNode = function ($node, cb) {
        if (!$node.attr(module.injectionStamp)) {
            cb && cb($node);
        }
    };

    module.injectButtonToNode = function ($node) {
        $node.attr(module.injectionStamp, true);
        $node.prepend('<pd-button></pd-button>');
        riot.mount('pd-button', { service: 'trello' });
    };

    module.injectInfoToNode = function ($node) {
        $node.attr(module.injectionStamp, true);
        $node.prepend('<pd-info></pd-info>');
        riot.mount('pd-info', { service: 'trello' });
    };

    $(function () {
        window.pdButtonTemplate = module.pdButtonTemplate;
        window.pdInfoTemplate = module.pdInfoTemplate;

        module.startTimer();
    });

})({}, window);
