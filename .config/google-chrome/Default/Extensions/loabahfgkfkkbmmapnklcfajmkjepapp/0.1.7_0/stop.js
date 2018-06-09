var template = `
<div class="blocked">
    <div class="blocked__icon">
        <span class="blocked__icon_item fa fa-ban"></span>
    </div>
    <h2 class="card__timer_title content__text-multiline_ellipsis">
        Pomodone App blocks this page.<br>
        Get back to work on this task:
    </h2>
    <p class="card__timer_title" style="margin: 20px 0 0 0;"><strong>{ card.title }</strong></p>
</div>
`;

riot.tag('blocked', template, function (opts) {
    var component = this;

    chrome.runtime.sendMessage({
        to: 'pomodone',
        action: 'getStatus'
    }, null, function (response) {
        if (response) {
            component.timer = response.timer;
            component.card = response.card;

            component.update();
        }
    });
});

riot.mount('*');
