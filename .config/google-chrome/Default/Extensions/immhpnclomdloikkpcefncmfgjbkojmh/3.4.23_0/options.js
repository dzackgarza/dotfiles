if (document.readyState === 'complete' || document.readyState !== 'loading') {
    domReady();
} else {
    document.addEventListener('DOMContentLoaded', domReady);
}

function getHostNameFromUrl(url) {
    var anchor = document.createElement('a');
    anchor.href = url;
    return anchor.hostname;
}

function enableDisableSubOptions() {
    document.getElementById('cbReplaceTwitterEmojis').disabled = !document.getElementById('cbTranslateEmojis').checked;
    document.getElementById('cbReplaceGoogleEmojis').disabled = !document.getElementById('cbTranslateEmojis').checked;
}

function domReady() {
    document.getElementById('linkAddHostNameBlacklist').addEventListener('click', addBlacklistedHostNameFromTextbox);
    document.getElementById('linkRemoveHostNamesBlacklist').addEventListener('click', removeBlacklistedHostNames);

    document.getElementById('linkAddHostNameWhitelist').addEventListener('click', addWhitelistedHostNameFromTextbox);
    document.getElementById('linkRemoveHostNamesWhitelist').addEventListener('click', removeWhitelistedHostNames);

    document.getElementById('btnSave').addEventListener('click', saveOptions);

    document.getElementById('currentHostName').addEventListener('keypress', function(e) {
        if (e.which == 13) addBlacklistedHostNameFromTextbox();
    });

    document.getElementById('cbTranslateEmojis').addEventListener('click', enableDisableSubOptions);

    chrome.tabs.query({
        'active': true,
        'lastFocusedWindow': true
    }, function(tabs) {

        if (tabs[0].openerTabId) {
            chrome.tabs.get(tabs[0].openerTabId, function(innerTab) {
                document.getElementById('currentHostName').value = getHostNameFromUrl(innerTab.url);
            });
        }

    });

    chrome.storage.sync.get('emojiInputTranslateEmojis', function(object) {
        if (object['emojiInputTranslateEmojis'] == false) document.getElementById('cbTranslateEmojis').checked = false;
        enableDisableSubOptions();
    });

    chrome.storage.sync.get('emojiInputDeclutterVariations', function(object) {
        if (object['emojiInputDeclutterVariations'] == false) document.getElementById('cbDeclutterVariations').checked = false;
    });

    chrome.storage.sync.get('emojiInputReplaceTwitterEmojis', function(object) {
        if (object['emojiInputReplaceTwitterEmojis'] == false) document.getElementById('cbReplaceTwitterEmojis').checked = false;
    });

    chrome.storage.sync.get('emojiInputReplaceGoogleEmojis', function(object) {
        if (object['emojiInputReplaceGoogleEmojis'] == false) document.getElementById('cbReplaceGoogleEmojis').checked = false;
    });

    chrome.storage.sync.get('emojiInputAutoCategory', function(object) {
        if (object['emojiInputAutoCategory'] == false) document.getElementById('cbAutoCategory').checked = false;
    });

    chrome.storage.sync.get('emojiInputAutoInsert', function(object) {
        if (object['emojiInputAutoInsert'] == false) document.getElementById('cbAutoInsert').checked = false;
    });

    chrome.storage.sync.get('emojiInputInsertByTyping', function(object) {
        if (object['emojiInputInsertByTyping'] == false) document.getElementById('cbInsertByTyping').checked = false;
    });

    chrome.storage.sync.get('emojiInputAutoCopy', function(object) {
        if (object['emojiInputAutoCopy'] == true) document.getElementById('cbAutoCopy').checked = true;
    });

    chrome.storage.sync.get('emojiInputAutoCloseWindow', function(object) {
        if (object['emojiInputAutoCloseWindow'] == true) document.getElementById('cbAutoCloseWindow').checked = true;
    });

    chrome.storage.sync.get('emojiInputHideCopyBox', function(object) {
        if (object['emojiInputHideCopyBox'] == true) document.getElementById('cbHideCopyBox').checked = true;
    });


    chrome.storage.sync.get('emojiInputEmojiStyle', function(object) {
        if (typeof object['emojiInputEmojiStyle'] == 'undefined') return false;

        document.querySelectorAll('#selEmojiStyle option').forEach(function(element) {
            if (element.value == object['emojiInputEmojiStyle']) element.selected = true;
        });
    });

    chrome.storage.sync.get('emojiInputBlacklist', function(object) {
        if (typeof object['emojiInputBlacklist'] == 'undefined') return false;

        var BlacklistSites = object['emojiInputBlacklist'].split(',');
        for (var site in BlacklistSites) {
            addBlacklistedHostName(BlacklistSites[site]);
        }
    });

    chrome.storage.sync.get('emojiInputWhitelist', function(object) {
        if (typeof object['emojiInputWhitelist'] == 'undefined') return false;

        var WhitelistSites = object['emojiInputWhitelist'].split(',');
        for (var site in WhitelistSites) {
            addWhitelistedHostName(WhitelistSites[site]);
        }
    });

}

function addBlacklistedHostNameFromTextbox() {
    var hostnameToAdd = document.getElementById('currentHostName').value.toLowerCase();

    if (hostnameToAdd.indexOf('http') > -1) hostnameToAdd = getHostNameFromUrl(hostnameToAdd);

    var addable = true;

    document.querySelectorAll('#selectBlacklist option').forEach(function(element) {
        if (hostnameToAdd == element.value.toLowerCase()) {
            addable = false;
            return false;
        }
    });

    if (addable == true) {
        addBlacklistedHostName(hostnameToAdd);
        saveBlacklist();
    }
}

function addBlacklistedHostName(hostnameToAdd) {
    if (hostnameToAdd.trim() == '') return false;
    var option = document.createElement("option");
    option.text = hostnameToAdd;
    document.getElementById('selectBlacklist').add(option, 0);
}


function removeBlacklistedHostNames() {
    document.querySelectorAll('#selectBlacklist option:checked').forEach(function(element) {
        element.parentElement.removeChild(element);
    });

    saveBlacklist();

}


function saveBlacklist() {
    var hostnames = Array();

    document.querySelectorAll('#selectBlacklist option').forEach(function(element, index) {
        hostnames[index] = element.value;
    });

    chrome.storage.sync.set({
        'emojiInputBlacklist': hostnames.join(',')
    }, function() {

    });
}

function addWhitelistedHostNameFromTextbox() {
    var hostnameToAdd = document.getElementById('currentHostName').value.toLowerCase();

    if (hostnameToAdd.indexOf('http') > -1) hostnameToAdd = getHostNameFromUrl(hostnameToAdd);

    var addable = true;

    document.querySelectorAll('#selectWhitelist option').forEach(function(element) {
        if (hostnameToAdd == element.value.toLowerCase()) {
            addable = false;
            return false;
        }
    });

    if (addable == true) {
        addWhitelistedHostName(hostnameToAdd);
        saveWhitelist();
    }
}

function addWhitelistedHostName(hostnameToAdd) {
    if (hostnameToAdd.trim() == '') return false;
    var option = document.createElement("option");
    option.text = hostnameToAdd;
    document.getElementById('selectWhitelist').add(option, 0);
}


function removeWhitelistedHostNames() {
    document.querySelectorAll('#selectWhitelist option:checked').forEach(function(element) {
        element.parentElement.removeChild(element);
    });

    saveWhitelist();

}


function saveWhitelist() {
    var hostnames = Array();

    document.querySelectorAll('#selectWhitelist option').forEach(function(element, index) {
        hostnames[index] = element.value;
    });

    chrome.storage.sync.set({
        'emojiInputWhitelist': hostnames.join(',')
    }, function() {

    });
}

function saveTranslateEmojis() {
    chrome.storage.sync.set({
        'emojiInputTranslateEmojis': document.getElementById('cbTranslateEmojis').checked
    }, function() {

    });
}

function saveDeclutterVariations() {
    chrome.storage.sync.set({
        'emojiInputDeclutterVariations': document.getElementById('cbDeclutterVariations').checked
    }, function() {

    });
}

function saveReplaceTwitterEmojis() {
    chrome.storage.sync.set({
        'emojiInputReplaceTwitterEmojis': document.getElementById('cbReplaceTwitterEmojis').checked
    }, function() {

    });
}

function saveReplaceGoogleEmojis() {
    chrome.storage.sync.set({
        'emojiInputReplaceGoogleEmojis': document.getElementById('cbReplaceGoogleEmojis').checked
    }, function() {

    });
}

function saveAutoCategory() {
    const value = document.getElementById('cbAutoCategory').checked;
    chrome.runtime.sendMessage({action: value ? "auto_emocat_on" : "auto_emocat_off"});

    chrome.storage.sync.set({
        'emojiInputAutoCategory': value
    }, function() {

    });
}

function saveAutoInsert() {
    chrome.storage.sync.set({
        'emojiInputAutoInsert': document.getElementById('cbAutoInsert').checked
    }, function() {

    });
}

function saveInsertByTyping() {
    chrome.storage.sync.set({
        'emojiInputInsertByTyping': document.getElementById('cbInsertByTyping').checked
    }, function() {

    });
}

function saveAutoCopy() {
    chrome.storage.sync.set({
        'emojiInputAutoCopy': document.getElementById('cbAutoCopy').checked
    }, function() {

    });
}

function saveAutoCloseWindow() {
    chrome.storage.sync.set({
        'emojiInputAutoCloseWindow': document.getElementById('cbAutoCloseWindow').checked
    }, function() {

    });
}

function saveHideCopyBox() {
    chrome.storage.sync.set({
        'emojiInputHideCopyBox': document.getElementById('cbHideCopyBox').checked
    }, function() {

    });
}

function saveEmojiStyle() {
    chrome.storage.sync.set({
        'emojiInputEmojiStyle': document.getElementById('selEmojiStyle').value
    }, function() {

    });
}

function saveOptions() {
    saveBlacklist();
    saveWhitelist();
    saveTranslateEmojis();
    saveDeclutterVariations();
    saveReplaceTwitterEmojis();
    saveReplaceGoogleEmojis();
    saveEmojiStyle();
    saveAutoCategory();
    saveAutoInsert();
    saveInsertByTyping();
    saveAutoCopy();
    saveHideCopyBox();
    saveAutoCloseWindow();
    document.querySelectorAll('#msgResult')[0].innerHTML = 'Settings saved';
    setTimeout(function() { document.querySelectorAll('#msgResult')[0].textContent = ''; }, 2000);
}