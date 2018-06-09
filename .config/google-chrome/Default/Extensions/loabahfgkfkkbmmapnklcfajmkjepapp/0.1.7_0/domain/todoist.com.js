(function (module, window) {
    module.injectionStamp = 'pd-injected';
    module.checkInterval = 6000;
    module.injectionQuery = '.task_item td.menu';

    module.path = chrome.extension.getURL('');

    module.pdButtonTemplate =
        '<a href="pomodone://app" class="pomodone_ext__icon" onclick="{ this.add }">' +
            '<span class="pomodone_ext__icon_image" style="background-image: url(' + module.path + 'icon128.png);"></span>' +
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

        title = $node.closest('.task_item').find('.text').text();
        url = 'https://todoist.com/showTask?id=' + $node.closest('.task_item').attr('id').substr(5);

        return {
            title: title,
            url: url,
            service: 'todoist'
        };
    };

    module.injectToNode = function ($node) {
        $node.attr(module.injectionStamp, true);
        $node.prepend('<pd-button></pd-button>');

        riot.mount($node.find('pd-button').first(), 'pd-button', module.getData($node));
    };

    $(function () {
        window.pdButtonTemplate = module.pdButtonTemplate;

        module.startTimer();
    });
})({}, window);
