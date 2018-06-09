(function (module, window) {
    module.injectionStamp = 'pd-injected';
    module.checkInterval = 1000;
    module.injectionQuery = '.card__footer, .card__timers_body';

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
        var $cardTitle = $node.closest('.card').find('.card__title');

        if ($cardTitle.length == 0) {
            $cardTitle = $node.closest('.card-list_item').find('.card-list_item_title');
        }

        title = $.trim($cardTitle.text());
        url = $cardTitle.attr('href') || $node.closest('.card').attr('data-uuid');

        if (!url) {
            url = $node.closest('.card-list_item').attr('data-uuid');
        }

        return {
            title: title,
            url: url
        };
    };

    module.injectToNode = function ($node) {
        $node.attr(module.injectionStamp, true);
        $node.children().last().before('<pd-button></pd-button>');

        riot.mount('pd-button', module.getData($node));
    };

    $(function () {
        window.pdButtonTemplate = module.pdButtonTemplate;

        module.startTimer();
    });
})({}, window);
