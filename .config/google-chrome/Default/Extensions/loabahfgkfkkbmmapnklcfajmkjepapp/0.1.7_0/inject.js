(function (window) {
    var body = document.querySelector('body');

    function block () {
        var iframe = document.createElement('iframe');

        if (document.getElementById('pomodoneBlocker')) {
            return false;
        }

        iframe.style.position = 'fixed';

        iframe.style.top = '0';
        iframe.style.right = '0';
        iframe.style.left = '0';
        iframe.style.bottom = '0';
        iframe.style.height = '100%';
        iframe.style.width = '100%';
        iframe.style.zIndex = '420000';
        iframe.style.border = 'none';

        iframe.id = 'pomodoneBlocker';
        iframe.src = chrome.extension.getURL('stop.html');
        body.appendChild(iframe);

        console.info('[pd]: block');
    }

    function unblock () {
        console.info('[pd]: unblock');

        try {
            body.removeChild(document.getElementById('pomodoneBlocker'));
        } catch (err) {}
    }

    chrome.runtime.onMessage.addListener(function (msg) {
        if (msg.action == 'block') {
            block();
        }

        if (msg.action == 'unblock') {
            unblock();
        }
    });

})(window);
