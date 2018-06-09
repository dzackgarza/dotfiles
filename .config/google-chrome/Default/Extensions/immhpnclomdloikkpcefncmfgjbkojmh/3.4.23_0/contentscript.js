var observer;
var runningReact = 'unknown';
var translateEmojis = true;
var replaceGoogleEmojis = false;
var replaceTwitterEmojis = false;
var insertByTyping = false;
var header_already_added = false;

var gblInput = {
    focusedEl: null,
    strTyped: '',
    shortcodequery: ''
}


// Check if the DOMContentLoaded has already been completed
if (document.readyState === 'complete' || document.readyState !== 'loading') {
    domReady();
} else {
    document.addEventListener('DOMContentLoaded', domReady);
}


var asciiArt = [{
    'code': '::shruggy::',
    'art': '¯\\_(ツ)_/¯'
}, {
    'code': '::tableflip::',
    'art': '(╯°□°）╯︵ ┻━┻)'
}, {
    'code': '::disapproval::',
    'art': 'ಠ_ಠ'
}, {
    'code': '::asciigun::',
    'art': '▄︻̷̿┻̿═━一'
}, {
    'code': '::joint::',
    'art': '<(_̅\\_̅_̅\\_̅_̅_\\̅_̅_\\̅ (ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็)'
}, {
    'code': '::yolo::',
    'art': 'Yᵒᵘ Oᶰˡʸ Lᶤᵛᵉ Oᶰᶜᵉ'
}, {
    'code': '::barbell::',
    'art': '❚█══█❚'
}, {
    'code': '::fuckyou::',
    'art': '┌ಠ_ಠ)┌∩┐ ᶠᶸᶜᵏᵧₒᵤ'
}, {
    'code': '::pingpong::',
    'art': '( •_•)O*¯`·.¸.·´¯`°Q(•_• )'
}, {
    'code': '::kirby::',
    'art': '(つ -‘ _ ‘- )つ'
}, {
    'code': '::asciirose::',
    'art': 'இڿڰۣ-ڰۣ—'
}, {
    'code': '::asciicry::',
    'art': '(இ﹏இ`｡)'
}];



window.emojiInputKeyImitator = window.emojiInputKeyImitator || {
    simulatePasteKeysDown: function simulatePasteKeysDown() {
        this.simulateKeyDown({
            code: "ControlLeft",
            location: KeyboardEvent.DOM_KEY_LOCATION_LEFT,
            keyCode: 17,
            ctrlKey: true
        });
        this.simulateKeyDown({
            code: "KeyV",
            ctrlKey: true,
            keyCode: 86
        });
        this.simulateKeyPress({
            code: "KeyV",
            ctrlKey: true,
            keyCode: 86
        });

    },
    simulatePasteKeysUp: function simulatePasteKeysUp() {
        this.simulateKeyUp({
            key: "KeyV",
            location: KeyboardEvent.DOM_KEY_LOCATION_LEFT,
            ctrlKey: true,
            keyCode: 86
        });
        this.simulateKeyUp({
            key: "ControlLeft",
            location: KeyboardEvent.DOM_KEY_LOCATION_LEFT,
            keyCode: 17
        });
    },

    simulateKeyDown: function simulateKeyDown(KeyboardEventInit) {
        var activeElement = document.activeElement;
        var keyboardEvent = new KeyboardEvent('keydown', KeyboardEventInit);
        activeElement.dispatchEvent(keyboardEvent);
    },

    simulateKeyUp: function simulateKeyUp(KeyboardEventInit) {
        var activeElement = document.activeElement;
        var keyboardEvent = new KeyboardEvent('keyup', KeyboardEventInit);
        activeElement.dispatchEvent(keyboardEvent);
    },
    simulateKeyPress: function simulateKeyPress(KeyboardEventInit) {
        var activeElement = document.activeElement;
        var keyboardEvent = new KeyboardEvent('keypress', KeyboardEventInit);
        activeElement.dispatchEvent(keyboardEvent);
    }
};
var keySynthesize = window.emojiInputKeyImitator;


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        var emoji = request.emoji;
        var theInput = document.activeElement;
        var oldText;
        var caretPos = 0;

        if (theInput.tagName.toLowerCase() === 'input' || theInput.tagName.toLowerCase() === 'textarea') {
            oldText = theInput.value;
            caretPos = theInput.selectionStart;
        } else {
            oldText = theInput.innerText;
            caretPos = 0;
            if (window.getSelection() && window.getSelection().rangeCount > 0) {
                caretPos = window.getSelection().getRangeAt(0).startOffset;
            }
        }


        var leftText = oldText.substr(0, caretPos);
        var rightText = oldText.substr(caretPos, oldText.length);

        if (runningReact === true) {
            var inputEvent = document.createEvent('TextEvent');
            inputEvent.initTextEvent('textInput', true, true, window, emoji);
            keySynthesize.simulatePasteKeysDown();
            theInput.dispatchEvent(inputEvent);
            keySynthesize.simulatePasteKeysUp();
        } else if (theInput.tagName.toLowerCase() === 'input' || theInput.tagName.toLowerCase() === 'textarea') {
            theInput.value = leftText + emoji + rightText;
            theInput.selectionStart = leftText.length + 1;
            theInput.selectionEnd = leftText.length + 1;
        } else {
            if (theInput.getAttribute('contenteditable') === 'true') {
                insertTextAtCursor(emoji);
            }
        }

    }
);

function insertTextAtCursor(text) {
    var sel, range, html;
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            range = sel.getRangeAt(0);
            range.deleteContents();
            range.insertNode(document.createTextNode(text));
        }
    } else if (document.selection && document.selection.createRange) {
        document.selection.createRange().text = text;
    }
}

function addStyleSheet() {
    if (header_already_added === true) {
        return;
    }

    var x = document.getElementsByTagName("link");
    var i = 0;

    for (i; i < x.length; i++) {
        if (x[i].href === chrome.extension.getURL("css/emoji.css")) {
            header_already_added = true;
        }
    }

    if (header_already_added === false) {
        var fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", chrome.extension.getURL("css/emoji.css"));
        document.getElementsByTagName("head")[0].appendChild(fileref);
    }
}

function trackEvent(emojiString, eventString) {

    chrome.runtime.sendMessage({
        emoji: emojiString,
        site: location.hostname,
        eventtype: eventString,
        url: location.href
    }, function(response) {
        return response;
    });
}

function isElement(obj) {
    return obj instanceof HTMLElement;
}

/**
 * Get all of an element's parent elements up the DOM tree
 * @param  {Node}   elem     The element
 * @param  {String} selector Selector to match against [optional]
 * @return {Array}           The parent elements
 */
var getParents = function(elem, selector) {

    // Element.matches() polyfill
    if (!Element.prototype.matches) {
        Element.prototype.matches =
            Element.prototype.matchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector ||
            Element.prototype.oMatchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            function(s) {
                var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                    i = matches.length;
                while (--i >= 0 && matches.item(i) !== this) {}
                return i > -1;
            };
    }

    // Setup parents array
    var parents = [];

    // Get matching parent elements
    for (; elem && elem !== document; elem = elem.parentNode) {

        // Add matching parents to array
        if (selector) {
            if (elem.matches(selector)) {
                parents.push(elem);
            }
        } else {
            parents.push(elem);
        }

    }

    return parents;

};

function showEmoji(nodes) {

    // if (window.location.hostname.indexOf('.messenger.com') > -1) {

    //     var searchText = "Could not display";
    //     for (var i = 0; i < nodes.length; i++) {
    //         if (nodes[i].textContent.indexOf(searchText) > -1) {
    //             window.location.href = window.location.href;
    //             break;
    //         }
    //     }

    // }

    stopObserver();

    if (nodes.length == 0) {
        startObserver();
        return false;
    }

    var googleReplaced = replaceGoogleEmojiWithTextEmoji();
    var twitterReplaced = replaceTwitterEmojiWithTextEmoji();

    if (googleReplaced == true) { //|| twitterReplaced.length > 0
        showEmoji(filterNodes());
        return false;
    }

    Array.from(nodes).forEach(function(node) {

        if (isElement(node)) {
            if (node.getAttribute('contenteditable') == 'true') return true;
            if (node.getAttribute('contenteditable') == 'plaintext-only') return true;

        }

        if (node.textContent.trim().length < 1) return true;


        var nodeParents = getParents(node);

        // check if inside contenteditable div
        for (var p = 0; p < nodeParents.length; p++) {
            if (isElement(nodeParents[p]) && nodeParents[p].getAttribute('contenteditable') == 'true') return true;
        }

        var textToCheck = node.textContent.replace(/&amp;/g, '&').replace(/&/g, '&amp;');
        var modifiedText = textToCheck;
        var emojiExist = false;

        if (modifiedText.length > 0) {
            modifiedText = emoji.replace_unified(modifiedText);
            if (modifiedText != textToCheck) emojiExist = true;
        }

        if (emojiExist === true) {

            var element = node.parentElement;

            for (var p = 1; p < nodeParents.length; p++) {
                if (element == undefined || !isElement(element)) element = nodeParents[p];
            }

            if (element) {
                var html = element.innerHTML;
                if (html.toLowerCase().indexOf('document.write') === -1) {
                    html = html.replace(/”/g, '&rdquo;');
                    var replace = html.replace(textToCheck.replace(/\xa0/g, '&nbsp;').replace(/”/g, '&rdquo;'), modifiedText);
                    element.innerHTML = replace;
                }
            }


        }

    });

    if (twitterReplaced.length > 0) showEmoji(filterNodes());

    startObserver();

}

function filterNodes(nodies) {

    nodies = nodies || textNodesUnder(document.body);

    var retArray = [];

    for (var i = 0; i < nodies.length; i++) {

        if (nodies[i].nodeType === 3) {
            retArray.push(nodies[i]);
        } else {

            var textNodes = textNodesUnder(nodies[i]);

            for (var j = 0; j < textNodes.length; j++) {
                retArray.push(textNodes[j]);
            }

        }
    }

    return retArray;
}

function on_mutation(mutations) {
    var i = 0;
    var added = [];
    var mutation;

    for (i; i < mutations.length; i++) {
        mutation = mutations[i];
        added.push(...mutation.addedNodes);
    }

    showEmoji(filterNodes(added));
}


function stopObserver() {
    if (observer) observer.disconnect();
}

function startObserver() {
    if (observer) observer.disconnect();
    var config = {
        childList: true,
        characterData: true,
        subtree: true
    };
    observer = new WebKitMutationObserver(on_mutation);
    observer.observe(document.body, config);
}



function domReady() {
    checkForReact();
    var whitelistActive = false;
    var parts = location.hostname.toLowerCase().split('.');
    var subdomain = parts.shift();
    var domain = parts.join('.');


    chrome.storage.sync.get('emojiInputWhitelist', function(object) {
        var whitelisted = false;

        if (object['emojiInputWhitelist']) {
            var WhitelistSites = object['emojiInputWhitelist'].split(',');

            WhitelistSites.forEach(function(site) {
                // alert('"' + site + '"');
                if (site.trim().length > 0) whitelistActive = true;

                if (location.hostname.toLowerCase() === site || domain == site) {
                    whitelisted = true;
                }
            });
        }

        if (whitelistActive == true && whitelisted == false) {
            return false;
        }

        chrome.storage.sync.get('emojiInputBlacklist', function(object) {
            var blacklisted = false;

            if (object['emojiInputBlacklist']) {
                var BlacklistSites = object['emojiInputBlacklist'].split(',');
                BlacklistSites.forEach(function(site) {
                    if (location.hostname.toLowerCase() === site || domain == site) {
                        blacklisted = true;
                        return false;
                    } //TODO: grey out smiley button 
                });
            }

            if (!blacklisted) {

                chrome.storage.sync.get('emojiInputTranslateEmojis', function(object) {
                    if (object['emojiInputTranslateEmojis'] !== false) {
                        translateEmojis = true;
                    } else if (object['emojiInputTranslateEmojis'] === false) {
                        translateEmojis = false;
                    }

                    chrome.storage.sync.get('emojiInputReplaceGoogleEmojis', function(object) {
                        if (object['emojiInputReplaceGoogleEmojis'] !== false) {
                            replaceGoogleEmojis = true;
                        }

                        chrome.storage.sync.get('emojiInputReplaceTwitterEmojis', function(object) {
                            if (object['emojiInputReplaceTwitterEmojis'] !== false) {
                                replaceTwitterEmojis = true;
                            }

                            chrome.storage.sync.get('emojiInputInsertByTyping', function(object) {
                                if (object['emojiInputInsertByTyping'] !== false) {
                                    insertByTyping = true;
                                }

                                init();

                            });
                        });
                    });
                });

            }

        });
    });

    if (checkIsExtensionWebsite() === true) injectDivFromExtension();

}

function init() {

    if (insertByTyping == true) {
        document.addEventListener('keyup', function(e) {
            inputEmojiByTyping(e);
        }, true);
    }

    if (translateEmojis == true) {
        addStyleSheet();
        showEmoji(textNodesUnder(document.body));
    }

}



function selectAllAndReplace(newText) {
    var selection = window.getSelection();
    var range = document.createRange();
    range.selectNodeContents(gblInput.focusedEl);
    selection.removeAllRanges();
    selection.addRange(range);

    setTimeout(function() {
        var inputEvent = document.createEvent('TextEvent');
        inputEvent.initTextEvent('textInput', true, true, window, newText);
        keySynthesize.simulatePasteKeysDown();
        gblInput.focusedEl.dispatchEvent(inputEvent);
        keySynthesize.simulatePasteKeysUp();
    }, 50);
}


function saveSelection() {
    var range = window.getSelection().getRangeAt(0);
    var preSelectionRange = range.cloneRange();
    preSelectionRange.selectNodeContents(gblInput.focusedEl);
    preSelectionRange.setEnd(range.startContainer, range.startOffset);
    var start = preSelectionRange.toString().length;

    return {
        start: start,
        end: start + range.toString().length
    };
};

function restoreSelection(savedSel) {
    var containerEl = gblInput.focusedEl;

    // google voice has an issue with refocusing the field - but somehow it works when restoreSelection function doesn't run
    if (containerEl.hasAttribute("gv-focus-when")) {
        return false;
    } 

    var charIndex = 0,
        range = document.createRange();
    range.setStart(containerEl, 0);
    range.collapse(true);
    var nodeStack = [containerEl],
        node, foundStart = false,
        stop = false;

    while (!stop && (node = nodeStack.pop())) {
        if (node.nodeType == 3) {
            var nextCharIndex = charIndex + node.length;
            if (!foundStart && savedSel.start >= charIndex && savedSel.start <= nextCharIndex) {
                range.setStart(node, savedSel.start - charIndex);
                foundStart = true;
            }
            if (foundStart && savedSel.end >= charIndex && savedSel.end <= nextCharIndex) {
                range.setEnd(node, savedSel.end - charIndex);
                stop = true;
            }
            charIndex = nextCharIndex;
        } else {
            var i = node.childNodes.length;
            while (i--) {
                nodeStack.push(node.childNodes[i]);
            }
        }
    }

    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}



function setEnd(el) {
    if (el.value) {
        el.setSelectionRange(el.value.length, el.value.length);
    } else {
        var range, selection;

        range = document.createRange(); //Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(el); //Select the entire contents of the element with the range
        range.collapse(false); //collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection(); //get the selection object (allows you to change selection)
        selection.removeAllRanges(); //remove any selections already made
        selection.addRange(range); //make the range you have just created the visible selection
    }

}

function getOffset(el) {
    const box = el.getBoundingClientRect();

    return {
        top: box.top + window.pageYOffset - document.documentElement.clientTop,
        left: box.left + window.pageXOffset - document.documentElement.clientLeft
    }
}


function createEmojiAutoComplete(focusedEl) {

    var emojiAutoComplete = document.getElementById('emojiAutoComplete');


    if (!emojiAutoComplete) {

        var focusedOffset = getOffset(focusedEl);

        addStyleSheet();

        emojiAutoComplete = document.createElement('div');
        emojiAutoComplete.id = 'emojiAutoComplete';
        emojiAutoComplete.class = 'emojiAutoComplete'
        emojiAutoComplete.style.cssText = 'left:' + focusedOffset.left + 'px;top:' + (focusedOffset.top + focusedEl.offsetHeight) + 'px;width:' + (focusedEl.offsetWidth - 10) + 'px;display:block;position:absolute;z-index:99999999;';
        document.body.appendChild(emojiAutoComplete);
    }


    // remove all child nodes from autocomplete
    while (emojiAutoComplete.firstChild) {
        emojiAutoComplete.removeChild(emojiAutoComplete.firstChild);
    }


    return emojiAutoComplete;

}

function positionEmojiAutoComplete() {
    // position autocomplete div

    var emojiAutoComplete = document.getElementById('emojiAutoComplete');
    var focusedOffset = getOffset(gblInput.focusedEl);
    var windowScrollTop = (document.documentElement && document.documentElement.scrollTop) || document.body.scrollTop;
    var emojiAutoCompleteTop = (focusedOffset.top + gblInput.focusedEl.offsetHeight);
    var spaceAbove = (focusedOffset.top - windowScrollTop);
    var spaceBelow = (window.innerHeight - (focusedOffset.top - windowScrollTop));
    if (spaceAbove > spaceBelow) {
        emojiAutoCompleteTop = (focusedOffset.top - emojiAutoComplete.offsetHeight);
    }
    emojiAutoComplete.style.top = emojiAutoCompleteTop + 'px';

    emojiAutoComplete.style.height = 'auto';
    emojiAutoComplete.style.overflow = 'auto';
    if (emojiAutoComplete.offsetHeight > window.innerHeight) {
        emojiAutoComplete.style.height = (window.innerHeight - 200) + 'px';
        emojiAutoComplete.style.overflow = 'scroll';
    }

}

function populateEmojiAutoComplete() {
    // find all matching emoji and put them in the autocomplete
    findEmojiByName(gblInput.shortcodequery).forEach(function(val, i) {
        var spanShortcode = autoCompleteItem(val);
        emojiAutoComplete.appendChild(spanShortcode);

        if (typeof val.skin_variations !== 'undefined') {
            var iteration = 1;
            for (var skin in val.skin_variations) {

                skin = val.skin_variations[skin];

                var spanShortcode = autoCompleteItem(val, skin, iteration);
                emojiAutoComplete.appendChild(spanShortcode);

                iteration++;
            }
        }
    });
}

function isPrintableCharacter(e) {
    var keycode = e.keyCode;

    //if (e.keyCode == '9' || e.keyCode == '10' || e.keyCode == '16') return false;

    var valid =
        (keycode > 47 && keycode < 58) || // number keys
        keycode == 32 || keycode == 13 || // spacebar & return key(s) (if you want to allow carriage returns)
        (keycode > 64 && keycode < 91) || // letter keys
        (keycode > 95 && keycode < 112) || // numpad keys
        (keycode > 185 && keycode < 193) || // ;=,-./` (in order)
        (keycode > 218 && keycode < 223); // [\]' (in order)

    return valid;
}


function inputEmojiByTyping(e) {

    if (isPrintableCharacter(e) == false && e.which != 8) return false;

    // reset global variable at the "beginning" of each keystroke
    gblInput.focusedEl = null;
    gblInput.strTyped = '';
    gblInput.shortcodequery = '';

    // populate the global variable
    gblInput.focusedEl = e.target;
    gblInput.strTyped = gblInput.focusedEl.innerText;



    // check if the focused element is something that can be typed into
    if (typeof gblInput.focusedEl == 'undefined' || gblInput.focusedEl == null) return false;
    if (gblInput.focusedEl && gblInput.focusedEl.tagName && gblInput.focusedEl.tagName.toLowerCase() != 'input' && gblInput.focusedEl.tagName.toLowerCase() != 'textarea' && (gblInput.focusedEl.hasAttribute("contentEditable") && gblInput.focusedEl.getAttribute("contentEditable").toLowerCase() != "true")) return false;



    if (gblInput.strTyped.length === 0) gblInput.strTyped = gblInput.focusedEl.value;
    if (typeof gblInput.strTyped == 'undefined' || gblInput.strTyped.length === 0) gblInput.strTyped = '';

    var strTypedLower = gblInput.strTyped.toLowerCase();
    var arrTypedEmojiSplit = gblInput.strTyped.split(/::/);

    if (arrTypedEmojiSplit.length < 2) {
        destroyAutoCompleteDiv();
        return false;
    }


    if (arrTypedEmojiSplit.length === 2) {

        if (arrTypedEmojiSplit[1].length > 1) {

            emojiAutoComplete = createEmojiAutoComplete(gblInput.focusedEl);

            gblInput.shortcodequery = arrTypedEmojiSplit[1].toLowerCase();

            // handle spaces to attempt inserting within existing text
            if (gblInput.shortcodequery.indexOf(' ') > -1 || gblInput.shortcodequery.indexOf('\n') > -1) {
                gblInput.shortcodequery = gblInput.shortcodequery.replace(/\n/g, ' ').split(' ')[0]
            }

            populateEmojiAutoComplete(arrTypedEmojiSplit);

            positionEmojiAutoComplete();

            if (emojiAutoComplete.hasChildNodes() === false) destroyAutoCompleteDiv();

            // event listener for tab autocompletion
            gblInput.focusedEl.removeEventListener('keydown', checkTabOnAutocomplete);
            gblInput.focusedEl.addEventListener('keydown', checkTabOnAutocomplete);


        } else {
            destroyAutoCompleteDiv();
        }


    }

    replaceShortcodeQueryInString(arrTypedEmojiSplit);

    replaceAsciiArt(gblInput.focusedEl, gblInput.strTyped);

}


function destroyAutoCompleteDiv() {
    var emojiAutoComplete = document.getElementById('emojiAutoComplete');
    if (emojiAutoComplete) emojiAutoComplete.parentNode.removeChild(emojiAutoComplete);

    gblInput.focusedEl.removeEventListener('keydown', checkTabOnAutocomplete);
    gblInput.focusedEl.removeEventListener('keydown', checkEnterOnAutoComplete);
    gblInput.focusedEl.removeEventListener('keydown', checkEscapeOnAutoComplete);
}

function checkTabOnAutocomplete(e) {
    // start listening for tab
    // after tab is pressed start listening for enter or esc
    // if either is pressed unbind event
    // unbind event after inserting emoji or destroying shortcut hint
    if (e.keyCode == 9) {

        if (!document.getElementById('emojiAutoComplete')) return false;

        var element = document.getElementById('emojiAutoComplete').querySelector('.emojiHighlighted');

        if (!element) {
            element = document.getElementById('emojiAutoComplete').querySelector('.spanShortCode');
            element.classList.add('emojiHighlighted');
        } else {

            var elementToHighlight = element;
            var shortCodes = document.getElementById('emojiAutoComplete').querySelectorAll('.spanShortCode');

            if (!e.shiftKey) {
                // if there's no next one, use the first one
                elementToHighlight = element.nextElementSibling || shortCodes[0];
            } else {
                // if there's no previous one, use the last one
                elementToHighlight = element.previousElementSibling || shortCodes[shortCodes.length - 1];;
            }

            element.classList.remove('emojiHighlighted');
            elementToHighlight.classList.add('emojiHighlighted');
        }


        gblInput.focusedEl.removeEventListener('keydown', checkEscapeOnAutoComplete);
        gblInput.focusedEl.addEventListener('keydown', checkEscapeOnAutoComplete);

        gblInput.focusedEl.removeEventListener('keydown', checkEnterOnAutoComplete);
        gblInput.focusedEl.addEventListener('keydown', checkEnterOnAutoComplete);

        e.preventDefault();
        return false;
    }
}

function checkClickOnAutoComplete() {
    gblInput.focusedEl.focus();
    checkEnterOnAutoComplete({ keyCode: 13 }, true);
}

function checkEnterOnAutoComplete(e, fake) {

    fake = fake || false;

    if (e.keyCode == 13) {

        if (fake == false) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
        }

        var strTyped = gblInput.strTyped;
        var focusedEl = gblInput.focusedEl;
        var shortcodequery = gblInput.shortcodequery;

        var shortcutcode = document.getElementById('emojiAutoComplete').querySelector('.emojiHighlighted span[data-unified]').getAttribute('data-unified');
        var replacement = emojiFromUnified(shortcutcode);

        strTyped = strTyped.replace('::' + shortcodequery, replacement);

        gblInput.strTyped = strTyped;
        gblInput.focusedEl = focusedEl;
        gblInput.shortcodequery = shortcodequery;
        replaceShortCodeQueryInTextBox(replacement, '');

        destroyAutoCompleteDiv();

        return false;
    }
}

function checkEscapeOnAutoComplete(e) {
    if (e.keyCode == 27) destroyAutoCompleteDiv();
}

function replaceShortcodeQueryInString(arrTypedEmojiSplit) {
    var originalText = gblInput.strTyped;
    // replace string of ::wave:: or ::wave_1:: with correct emoji symbol in typed text
    if (arrTypedEmojiSplit.length > 2) {
        if (arrTypedEmojiSplit[1].length > 0) {

            gblInput.shortcodequery = arrTypedEmojiSplit[1].toLowerCase();

            var last2characters = gblInput.shortcodequery.substr(gblInput.shortcodequery.length - 2);
            var variantId = 0;
            var variantString = '';

            if (last2characters.indexOf('_') === 0) {
                variantId = parseInt(last2characters.replace('_', ''));
                variantString = last2characters;
            }

            var preciseEmoji = findEmojiByShortNamePrecise(gblInput.shortcodequery.replace(variantString, ''));

            if (typeof preciseEmoji !== 'undefined') {
                if (variantId > 0 && variantId < 6) {

                    var iteration = 0;
                    var skinUnified = '';

                    for (var skin in preciseEmoji.skin_variations) {
                        skin = preciseEmoji.skin_variations[skin];
                        iteration++;
                        if (variantId == iteration) skinUnified = skin.unified;
                    }

                    var replacement = emojiFromUnified(skinUnified);

                } else {
                    var replacement = emojiFromUnified(preciseEmoji.unified);
                }

                gblInput.strTyped = gblInput.strTyped.replace('::' + gblInput.shortcodequery + '::', replacement);

                //safety check to prevent ::randomnoise:: from breaking sites
                if (gblInput.strTyped == originalText) return false;

                replaceShortCodeQueryInTextBox(replacement, '::');



                destroyAutoCompleteDiv();


            }
        }
    }
}


function replaceShortCodeQueryInTextBox(replacement, trailing) {

    var newCaretPosition = saveSelection();
    newCaretPosition.start = (newCaretPosition.start - (2 + gblInput.shortcodequery.length + trailing.length)) + replacement.length;
    newCaretPosition.end = (newCaretPosition.end - (2 + gblInput.shortcodequery.length + trailing.length)) + replacement.length;

    if (runningReact === true) {
        selectAllAndReplace(gblInput.strTyped);

        setTimeout(function() {
            restoreSelection(newCaretPosition);
        }, 120);

    } else if (gblInput.focusedEl.getAttribute('contenteditable') == 'true') {

        // handle contenteditable divs - like gmail emails
        gblInput.focusedEl.innerHTML = gblInput.focusedEl.innerHTML.replace('::' + gblInput.shortcodequery + trailing, replacement);
        restoreSelection(newCaretPosition);

    } else {

        if (gblInput.focusedEl.value) {
            gblInput.focusedEl.value = gblInput.strTyped;
        } else {
            gblInput.focusedEl.textContent = gblInput.strTyped;
        }

        restoreSelection(newCaretPosition);

    }

    chrome.runtime.sendMessage({ log: true, emoji: replacement, inputMethod: 'inputByTyping' })
}


function replaceAsciiArt(focusedEl, strTyped) {
    // ascii art replacement
    for (var i = 0; i < asciiArt.length; i++) {
        if (strTyped.indexOf(asciiArt[i].code) > -1) {
            strTyped = strTyped.replace(asciiArt[i].code, asciiArt[i].art);
            if (focusedEl.value) {
                focusedEl.value = strTyped;
            } else {
                focusedEl.textContent = strTyped;
            }
            setEnd(focusedEl);

            trackEvent(asciiArt[i].code, 'ASCIIart');
        }
    }
}

function replaceGoogleEmojiWithTextEmoji() {

    if (location.hostname.indexOf('.google.com') === -1) return false;
    if (replaceGoogleEmojis !== true) return false;

    var googleEmojiReplaced = false;

    document.querySelectorAll('[data-emo]').forEach(function(element) {

        var emojichar = element.getAttribute('data-emo');
        var nodeModified = false;

        if (element.nextSibling) {
            if (element.nextSibling.nodeType == 3) {
                element.nextSibling.nodeValue = emojichar + element.nextSibling.nodeValue;
                googleEmojiReplaced = true;
                nodeModified = true;
            }
        }

        if (element.previousSibling && nodeModified == false) {
            if (element.previousSibling.nodeType == 3) {
                element.previousSibling.nodeValue = element.previousSibling.nodeValue + emojichar;
                googleEmojiReplaced = true;
                nodeModified = true;
            }
        }

        if (nodeModified == false) {
            var t = document.createTextNode(emojichar);
            element.parentNode.insertBefore(t, element);
            googleEmojiReplaced = true;
            nodeModified = true;
        }

        element.parentNode.removeChild(element);

    });

    return googleEmojiReplaced;
}

function replaceTwitterEmojiWithTextEmoji() {

    var twitterEmojiReplaced = [];

    if (location.hostname !== 'twitter.com' && location.hostname.indexOf('.twitter.com') === -1) return twitterEmojiReplaced;
    if (replaceTwitterEmojis !== true) return twitterEmojiReplaced;

    document.querySelectorAll('img.Emoji').forEach(function(element) {

        var emojichar = element.getAttribute('alt');

        var t = document.createTextNode(emojichar);
        element.parentNode.insertBefore(t, element);
        twitterEmojiReplaced.push(t);
        nodeModified = true;

        element.parentNode.removeChild(element);

    });

    return twitterEmojiReplaced;
}

function checkForReact() {

    if (window.location.hostname.indexOf('.messenger.com') > -1 || window.location.hostname.indexOf('facebook.com') > -1) {
        runningReact = true;
        return true;
    }

    if (runningReact = 'unknown') {
        setTimeout(checkForReact, 5000);
    }

    var selector = '[data-reactroot], [data-reactid]';
    runningReact = !!document.querySelector(selector);

}


function textNodesUnder(el) {
    if (!el.nodeType) {
        return [];
    }

    var n, a = [],
        walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
    while (n = walk.nextNode()) a.push(n);
    return a;
}


function checkIsExtensionWebsite() {
    var webstoreLink = document.querySelector('link[rel="chrome-webstore-item"]');
    if (webstoreLink && webstoreLink.getAttribute('href') === 'https://chrome.google.com/webstore/detail/immhpnclomdloikkpcefncmfgjbkojmh') {
        return true;
    } else {
        return false;
    }
}

function injectDivFromExtension() {
    var injectedDivFromExtension = document.createElement('div');
    injectedDivFromExtension.setAttribute('id', 'injectedDivFromExtension');
    document.body.appendChild(injectedDivFromExtension);
}


function autoCompleteItem(val, variant, variationIteration) {
    var spanShortcode = document.createElement('span');
    var spanShortcodeText = document.createElement('span');

    spanShortcode.setAttribute('class', 'spanShortCode');

    if (variant) {
        spanShortcode.innerHTML = emoji.replace_unified(emojiFromUnified(variant.unified));
        spanShortcodeText.setAttribute('data-unified', variant.unified);
        spanShortcodeText.innerText = '::' + val.short_name + '_' + variationIteration + '::';
    } else {
        spanShortcode.innerHTML = emoji.replace_colons(':' + val.short_name + ':');
        spanShortcodeText.setAttribute('data-unified', val.unified);
        spanShortcodeText.innerText = '::' + val.short_name + '::';
    }

    spanShortcode.appendChild(spanShortcodeText);

    spanShortcode.addEventListener('mouseenter', function() {
        var alreadyHighlighted = document.getElementById('emojiAutoComplete').querySelector('.emojiHighlighted');
        if (alreadyHighlighted) alreadyHighlighted.classList.remove('emojiHighlighted');
        spanShortcode.classList.add('emojiHighlighted');
    })

    spanShortcode.addEventListener('mouseleave', function() {
        spanShortcode.classList.remove('emojiHighlighted');
    })

    spanShortcode.addEventListener('click', checkClickOnAutoComplete);

    return spanShortcode;
}