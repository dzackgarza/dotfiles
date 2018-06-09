// todo add option for which pane to start by default
// add favorite emoji option
// allow removal of recent via right click
if (document.readyState === 'complete' || document.readyState !== 'loading') {
    init();
} else {
    document.addEventListener('DOMContentLoaded', init);
}

var emoji = new EmojiConvertor();

var autoInsert = true;
var autoCopy = false;
var autoCloseWindow = false;
var declutterVariations = true;

var arrBanners = [
    'other_extensions_2',
    'other_extensions_3',
    'other_extensions_1',
    'emoji_stuff_logo',
    'social_icons'
];

var currBanner = 0;
var prevBanner = arrBanners.length - 1;
var bannerRotator;

function initializeBanners() {
    rotateBanners();
    startBannerRotation();
    document.getElementById('placeholder').addEventListener('mouseover', stopBannerRotation);
    document.getElementById('placeholder').addEventListener('mouseout', startBannerRotation);
}

function stopBannerRotation() {
    clearInterval(bannerRotator);
}

function startBannerRotation() {
    bannerRotator = setInterval(rotateBanners, 4000);
}

function rotateBanners() {

    var bannerToFadeOut = document.getElementById(arrBanners[prevBanner]);
    bannerToFadeOut.classList.remove('fadingIn');
    bannerToFadeOut.classList.remove('fadingOut');

    var bannerToFadeIn = document.getElementById(arrBanners[currBanner]);
    bannerToFadeIn.classList.add('fadingIn');

    setTimeout(function() {
        bannerToFadeIn.classList.add('fadingOut');
        bannerToFadeIn.classList.remove('fadingIn');
    }, 2000);

    currBanner++;
    prevBanner = currBanner - 1;

    if (currBanner >= arrBanners.length) {
        currBanner = 0;
        prevBanner = arrBanners.length - 1;
    }

}

function getSelectionStart(o) {
    if (o.createTextRange) {
        var r = document.selection.createRange().duplicate();
        r.moveEnd("character", o.value.length);
        if (r.text === "") {
            return o.value.length;
        } else {
            return o.value.lastIndexOf(r.text);
        }
    } else {
        return o.selectionStart;
    }
}

function populateRecent() {
    chrome.storage.sync.get('emojiInputRecents', function(object) {
        var recentEmojis = [];
        if (object['emojiInputRecents']) {
            recentEmojis = object['emojiInputRecents'];

            document.querySelector('.tab-pane.recent').innerHTML = (emojiPickerHtml(findEmojiByUnifiedArray(recentEmojis), recentEmojis));

            bindEvent('.tab-pane.recent .eq', emojiClick);

            // clear recents link
            if (recentEmojis.length > 0) {
                document.querySelector('.tab-pane.recent').insertAdjacentHTML('beforeend', '<br><a href="javascript:void(0);" id="aClearRecents">clear recents</a>');
                bindEvent('#aClearRecents', function() {
                    var recentEmojis = new Array();
                    chrome.storage.sync.set({
                        'emojiInputRecents': recentEmojis
                    }, function() {
                        populateRecent();
                    });
                });
            } else {
                document.querySelector('.tab-pane.recent').insertAdjacentHTML('beforeend', '<div style="color: #ccc; text-align:center; padding: 50px;">recently used emoji will appear here</div>');
            }
        }
    });
}


function populateCategory() {
    document.querySelectorAll('.tab-content div').forEach(function(el) { el.classList.remove('active'); });

    var myselector = '.tab-content div.' + this.classList;

    var thisCategory = this.getAttribute('data-category');

    document.querySelector(myselector).classList.add('active');

    if (thisCategory === "0") return false;

    var categoryEmojis = findEmojiByCategory(thisCategory);

    categoryEmojis = sortBySortOrder(categoryEmojis);

    document.querySelector(myselector).innerHTML = emojiPickerHtml(categoryEmojis);

    bindEvent(myselector + ' .eq', emojiClick);
}


function emojiPickerHtml(filteredEmojiData, onlyListTheseEmojis) {

    filteredEmojiData = filteredEmojiData || emojisData;
    onlyListTheseEmojis = onlyListTheseEmojis || [];
    var alreadyProcessedEmojis = [];

    var emojis = '';

    var tabindex = 2;
    filteredEmojiData.forEach(function(val, i) {

        if (typeof val == 'undefined') return true;

        if (onlyListTheseEmojis.length == 0 || (onlyListTheseEmojis.indexOf(val.unified) > -1 && alreadyProcessedEmojis.indexOf(val.unified) == -1)) {
            var theEmoji = emojiFromUnified(val.unified);
            var strClassnameHasVariations = '';
            var strClassnameVariation = '';

            if (typeof val.skin_variations !== 'undefined' && declutterVariations == true) {
                strClassnameHasVariations = ' hasVariations';
                strClassnameVariation = '  isVariation';
            }

            emojis = emojis + '<a href="#" title="' + val.name + ' ::' + val.short_name + '::" class="eq' + strClassnameHasVariations + '" data-emoji="' + val.unified + '" tabindex="' + tabindex + '">' + theEmoji + '</a> ';
            alreadyProcessedEmojis.push(val.unified);
            tabindex++;
        }

        if (typeof val.skin_variations !== 'undefined') {
            var counter = 1;

            for (var skinval in val.skin_variations) {

                skinval = val.skin_variations[skinval];

                if (onlyListTheseEmojis.length == 0 || (onlyListTheseEmojis.indexOf(skinval.unified) > -1 && alreadyProcessedEmojis.indexOf(skinval.unified) == -1)) {
                    skinEmoji = emojiFromUnified(skinval.unified);
                    emojis = emojis + '<a href="#" title="' + val.name + ' ::' + val.short_name + "_" + (counter) + '::" class="eq' + strClassnameVariation + '" data-emoji="' + skinval.unified + '" tabindex="' + tabindex + '">' + skinEmoji + '</a> ';
                    alreadyProcessedEmojis.push(skinval.unified);
                    tabindex++;
                }
                counter++;
            }

        }

    });

    emojis = emoji.replace_unified(emojis);

    return emojis;

}

function init() {


    bindEvent('.navEmoji a', populateCategory); //:not([value="0"])

    bindEvent('#navEmojiRecent', populateRecent);

    bindEvent('#txtSearch', displayBySearch, "keyup");

    bindEvent('#navEmojiSearch', openSearch);

    bindEvent('#txtCopyBox', function() { this.select(); });

    bindEvent('#aCopy', copyEmoji);

    bindEvent('#optionsLink', openOptions);

    emoji.img_sets = {
        'apple': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_apple_32.png'), 'mask': 1 },
        'google': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_google_32.png'), 'mask': 2 },
        'twitter': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_twitter_32.png'), 'mask': 4 },
        'emojione': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_emojione_32.png'), 'mask': 8 },
        'facebook': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_facebook_32.png'), 'mask': 16 },
        'messenger': { 'path': '/emoji-data/', 'sheet': chrome.extension.getURL('/emoji-data/sheet_messenger_32.png'), 'mask': 32 }
    };


    emoji.use_css_imgs = false;
    emoji.colons_mode = false;
    emoji.text_mode = false;
    emoji.include_title = false;
    emoji.include_text = false;
    emoji.allow_native = false;
    emoji.use_sheet = true;
    emoji.avoid_ms_emoji = true;
    emoji.allow_caps = false;
    emoji.img_suffix = '';
    emoji.supports_css = true;

    chrome.storage.sync.get('emojiInputEmojiStyle', function(object) {
        if (typeof object['emojiInputEmojiStyle'] == 'undefined') {
            emoji.img_set = 'apple';
        } else {
            emoji.img_set = object['emojiInputEmojiStyle'];
        }
    });

    chrome.storage.sync.get('emojiInputDeclutterVariations', function(object) {
        if (object['emojiInputDeclutterVariations'] == false) declutterVariations = false;
    });

    chrome.storage.sync.get('emojiInputAutoInsert', function(object) {
        if (object['emojiInputAutoInsert'] == false) autoInsert = false;
    });

    chrome.storage.sync.get('emojiInputAutoCopy', function(object) {
        if (object['emojiInputAutoCopy'] == true) autoCopy = true;
    });

    chrome.storage.sync.get('emojiInputAutoCloseWindow', function(object) {
        if (object['emojiInputAutoCloseWindow'] == true) autoCloseWindow = true;
    });

    chrome.storage.sync.get('emojiInputHideCopyBox', function(object) {
        if (object['emojiInputHideCopyBox'] == true) {
            document.getElementById('txtCopyBox').style.display = 'none';
            document.getElementById('aCopy').style.display = 'none';
        }
    });

    document.getElementById('navEmojiSearch').click();

    addEmojiDataScript().then(function() {
        var shouldUseSearch = true;
        chrome.tabs.query({ active: true }, function(activeTab) {
            activeTab = activeTab ? activeTab[0] : null;
            if (activeTab)
                chrome.runtime.sendMessage({ action: "get_emocat_for_tab", tabId: activeTab.id }, function(response) {
                    if (typeof response === "string") {
                        const capitalized = response.capitalize(),
                            selector = `#navEmoji${capitalized}`,
                            toClick = document.body.querySelector(selector);
                        if (toClick) {
                            populateCategory.apply(toClick);
                            shouldUseSearch = false;
                        }
                    }
                });
        });
        if (shouldUseSearch) setTimeout(displayBySearch, 50);
    });

    setTimeout(function() {
        addFontAwesome();
        initializeBanners();
        addGoogleAnalytics();
    }, 100);

}

function addEmojiDataScript() {
    var s = document.createElement('script');
    document.body.appendChild(s);
    return new Promise(function(resolve) {
        s.addEventListener("load", resolve);
        s.setAttribute('src', chrome.extension.getURL('emojis.js'));
    });
}

function addGoogleAnalytics() {
    var s = document.createElement('script');
    document.body.appendChild(s);
    s.setAttribute('src', chrome.extension.getURL('eiga.js'));
}

function addFontAwesome() {
    var fileref = document.createElement("link");
    fileref.setAttribute("rel", "stylesheet");
    fileref.setAttribute("type", "text/css");
    fileref.setAttribute("href", chrome.extension.getURL("css/font-awesome.min.css"));
    document.getElementsByTagName("head")[0].appendChild(fileref);
}

function openSearch() {
    var searchMessage = document.getElementById('searchMessage');
    if (searchMessage) searchMessage.parentNode.removeChild(searchMessage);

    document.getElementById('divSearchResults').insertAdjacentHTML('beforeend', '<div id="searchMessage">matching emoji will appear here when searching</div>');
    document.getElementById('txtSearch').focus();

    //displayBySearch();

}

function bindEvent(query, functionName, eventName) {

    eventName = eventName || "click";

    document.querySelectorAll(query).forEach(function(element) {
        element.addEventListener(eventName, functionName)
    });

}

function openOptions() {
    if (chrome.runtime.openOptionsPage) {
        // New way to open options pages, if supported (Chrome 42+).
        chrome.runtime.openOptionsPage();
    } else {
        // Reasonable fallback.
        window.open(chrome.runtime.getURL('options.html'));
    }
}

function openVariations(element) {
    if (element.classList.contains('hasVariations') && element.nextElementSibling.classList.contains('isVariationShown') == false) {

        var nextOne = element.nextElementSibling;

        while (nextOne.classList.contains('isVariation') && nextOne.classList.contains('isVariationShown') == false) {
            nextOne.classList.add('isVariationShown');
            nextOne = nextOne.nextElementSibling;
        }

        return true;
    }
}

function emojiClick() {

    if (openVariations(this) == true) return false;

    var dataEmoji = this.getAttribute('data-emoji');

    addToRecents(dataEmoji);

    dataEmoji = emojiFromUnified(dataEmoji);

    document.getElementById('txtCopyBox').value = document.getElementById('txtCopyBox').value + dataEmoji;

    copyToClipboard(dataEmoji);

    _gaq.push(['_trackEvent', dataEmoji, 'clicked']);

    if (autoInsert == true) {
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { emoji: dataEmoji }, function(response) {});
            chrome.runtime.sendMessage({ log: true, emoji: dataEmoji, site: tabs[0].url, inputMethod: 'popupAutoInsert' })
        });
    } else if (autoCopy == true) {
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function(tabs) {
            chrome.runtime.sendMessage({ log: true, emoji: dataEmoji, site: tabs[0].url, inputMethod: 'popupAutocopy' })
        });
    } else {
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function(tabs) {
            chrome.runtime.sendMessage({ log: true, emoji: dataEmoji, site: tabs[0].url, inputMethod: 'popupClick' })
        });
    }

    if (autoCloseWindow == true) {
        window.close();
    }
}



function copyToClipboard(text) {

    if (autoCopy === false) return false;

    var textArea = document.createElement("textarea");

    //
    // *** This styling is an extra step which is likely not required. ***
    //
    // Why is it here? To ensure:
    // 1. the element is able to have focus and selection.
    // 2. if element was to flash render it has minimal visual impact.
    // 3. less flakyness with selection and copying which **might** occur if
    //    the textarea element is not visible.
    //
    // The likelihood is the element won't even render, not even a flash,
    // so some of these are just precautions. However in IE the element
    // is visible whilst the popup box asking the user for permission for
    // the web page to copy to the clipboard.
    //

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';


    textArea.value = text;

    document.body.appendChild(textArea);

    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);
    } catch (err) {
        console.log('Oops, unable to copy');
    }

    document.body.removeChild(textArea);
}


function copyEmoji() {

    document.getElementById('txtCopyBox').select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? '✓' : '✗';
        document.getElementById('aCopy').textContent = 'Copy ' + msg;
        setTimeout(function() {
            document.getElementById('aCopy').textContent = 'Copy';
            document.getElementById('txtCopyBox').value = '';
        }, 1500);
    } catch (err) {
        alert('Sorry, there was an error copying the emoji');
    }

}


function addToRecents(emojiToAdd) {
    chrome.storage.sync.get('emojiInputRecents', function(object) {
        if (object['emojiInputRecents']) {
            var recentEmojis = object['emojiInputRecents'];
            var index = recentEmojis.indexOf(emojiToAdd);

            if (index > -1) {
                recentEmojis.splice(index, 1);
            }

        } else {
            var recentEmojis = new Array();
        }


        recentEmojis.unshift(emojiToAdd);

        chrome.storage.sync.set({
            'emojiInputRecents': recentEmojis
        }, function() {});

    });

}

function orderCategoriesByCustomHierarchy(category) {
    switch (category) {
        case 'Activities':
            return 3;
            break;
        case 'Flags':
            return 7;
            break;
        case 'Food & Drink':
            return 2;
            break;
        case 'Animals & Nature':
            return 1;
            break;
        case 'Objects':
            return 5;
            break;
        case 'Smileys & People':
            return 0;
            break;
        case 'Travel & Places':
            return 4;
            break;
        case 'Symbols':
            return 6;
            break;

    }
}

function zeroPad(num) {
    return ("0000" + num).substr(-4, 4);
}

function displayBySearch() {

    var searchTerm = document.getElementById('txtSearch').value.toLowerCase();

    var emojiSearchResults = findEmojiByName(searchTerm);

    emojiSearchResults.sort(function(a, b) {
        // get an integer for each category
        var aCategoryNumber = orderCategoriesByCustomHierarchy(a.category);
        var bCategoryNumber = orderCategoriesByCustomHierarchy(b.category);

        // append sort order to category after a decimal point
        var aOrder = parseFloat(aCategoryNumber + '.' + zeroPad(a.sort_order));
        var bOrder = parseFloat(bCategoryNumber + '.' + zeroPad(b.sort_order));

        return aOrder - bOrder;
    });


    document.getElementById('divSearchResults').innerHTML = emojiPickerHtml(emojiSearchResults);

    bindEvent('#divSearchResults .eq', emojiClick);

    if (emojiSearchResults.length === 0) {
        document.getElementById('#divSearchResults').insertAdjacentHTML('beforeend', '<div id="searchMessage">no emoji match your search</div>');
    }

    populateCategory.apply(document.body.querySelector('#navEmojiSearch'));

    // if (searchTerm.length > 0) _gaq.push(['_trackEvent', 'search: ' + searchTerm, 'searched']);

}


function findEmojiByCategory(searchTerm) {
    //searchTerm = searchTerm.toLowerCase();
    return grep(emojisData, function(n, i) {
        var category = n.category || '';
        return category.indexOf(searchTerm) > -1;
    });
}

function findEmojiByUnifiedArray(arrUnified) {
    var retArray = [];

    for (var e = 0; e < arrUnified.length; e++) {

        retArray.push(grep(emojisData, function(n, i) {
            var unified = n.unified || '';

            if (n.skin_variations && n.skin_variations[arrUnified[e]]) {
                return true;
            }

            return unified == arrUnified[e];
        })[0]);

    }

    return retArray;
}


function sortBySortOrder(emojiData) {

    return emojiData.sort(function(a, b) {
        var aOrder = a.sort_order || 999999999999;
        var bOrder = b.sort_order || 999999999999;
        return aOrder - bOrder;
    });

}

function emojiFromUnified(unified) {
    unified = unified || '';
    unified = unified.split('-');

    var elem = document.createElement('p');
    var entities = '';
    var retval;

    for (var i = 0; i < unified.length; i++) {
        entities = entities + '&#x' + unified[i] + ';';
    }

    elem.innerHTML = entities;

    retval = elem.innerHTML;

    elem.remove();

    return retval;
}


function findEmojiByShortNamePrecise(searchTerm) {
    searchTerm = searchTerm || '';
    searchTerm = searchTerm.toLowerCase();
    for (var i = 0; i < emojisData.length; i++) {
        if (emojisData[i].short_name === searchTerm) {
            return emojisData[i];
        }
    }
}

function findEmojiByName(searchTerm) {
    // excludes flag full names - does include flag short names

    searchTerm = searchTerm || '';
    searchTerm = searchTerm.toLowerCase();

    return grep(emojisData, function(n, i) {
        var name = n.name || '';
        var category = n.category || '';
        name = name.toLowerCase();

        var shortnames = n.short_names || [];
        var foundInShortName = false;
        var foundInName = (name.indexOf(searchTerm) > -1);


        for (var j = 0; j < shortnames.length; j++) {
            if (shortnames[j].toLowerCase().indexOf(searchTerm) > -1) foundInShortName = true;
        }

        return (foundInName && (category != "Flags")) || foundInShortName == true;
    });
}

function grep(elems, callback, inv) {
    var ret = [],
        retVal;
    inv = !!inv;

    // Go through the array, only saving the items
    // that pass the validator function
    for (var i = 0, length = elems.length; i < length; i++) {
        retVal = !!callback(elems[i], i);
        if (inv !== retVal) {
            ret.push(elems[i]);
        }
    }

    return ret;
}

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
};