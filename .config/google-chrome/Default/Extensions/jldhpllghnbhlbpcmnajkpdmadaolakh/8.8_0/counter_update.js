if(window.location.pathname == '/app') {
    old_count = null;
    old_is_overdue = null;

    setInterval(function() {
        var data_node = document.getElementById('extension_data');
        if (!data_node) return

        var count_today = parseInt(data_node.getAttribute("data-count-today"))
        var count_overdue = parseInt(data_node.getAttribute("data-count-overdue"))

        var total_count = count_today + count_overdue;
        var is_overdue = count_overdue > 0;

        if(total_count != old_count || is_overdue != old_is_overdue) {
            var data = {
                'type': 'update_badge',
                'total_count': total_count,
                'is_overdue': is_overdue
            }

            chrome.extension.sendRequest(data, function() {});
            old_count = total_count;
            old_is_overdue = is_overdue;
        }

    }, 1000);
}
