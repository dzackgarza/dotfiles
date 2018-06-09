
//
// Custom Cursor (based on http://jsfiddle.net/dandv/aFPA7/)
//

(function () {

// The properties that we copy into a mirrored div.
// Note that some browsers, such as Firefox,
// do not concatenate properties, i.e. padding-top, bottom etc. -> padding,
// so we have to do every single property specifically.
var properties = [
  'boxSizing',
  ///'width',  TAKEN OUT BECAUSE WE USE 1 LINE TEXTAREA ONLY!!!
  // on Chrome and IE, exclude the scrollbar, so the mirror div wraps exactly as the textarea does
  'height',
  'overflowX',
  'overflowY',  // copy the scrollbar for IE

  'borderTopWidth',
  'borderRightWidth',
  'borderBottomWidth',
  'borderLeftWidth',

  'paddingTop',
  'paddingRight',
  'paddingBottom',
  'paddingLeft',

  // https://developer.mozilla.org/en-US/docs/Web/CSS/font
  'fontStyle',
  'fontVariant',
  'fontWeight',
  'fontStretch',
  'fontSize',
  'lineHeight',
  'fontFamily',

  'textAlign',
  'textTransform',
  'textIndent',
  'textDecoration',  // might not make a difference, but better be safe

  'letterSpacing',
  'wordSpacing'
];

//window.showMirrorDiv  = true;
var isFirefox = !(window.mozInnerScreenX == null);
var mirrorDiv, computed, style;

///////////////////////////////////

// Chrome bug reporting <input> scroll values when zoomed in/out
// Note: doing it lazyly to avoice forced relayout
var zoomCompensation = function () {
  var cachedValue = (function () {
    function isInt(n) { return n % 1 === 0; }
    var a = document.createElement('input');
    a.style.cssText = 'width:1px !important;font-family:arial,helvetica,sans-serif !important;font-size:20px !important;';
    a.value = 'a';
    document.body.appendChild(a);
    a.scrollLeft = 999*999*999;
    var scrollLeft = a.scrollLeft;
    document.body.removeChild(a);
    if (!scrollLeft || isInt(scrollLeft)) return 1;
    else return window.devicePixelRatio || 1;
  })();
  zoomCompensation = function () { return cachedValue; };
  return cachedValue;
}

///////////////////////////////////

// there can be only 1 cursor in the document
var cursor = document.createElement('div');

// these are for use by the ourside world
function hideCursor() {
  cursor.style.display = 'none';
  stopBlinking();
}
function showCursor() {
  cursor.style.display = 'block';
  startBlinking();
}
// these are for inner use
function maybeShowCursor() {
  //cursor.style.visibility = 'visible';
  startBlinking();
}
function maybeHideCursor() {
  //cursor.style.visibility = 'hidden';
  stopBlinking();
}

function addCursorToElement(element) {

  if (typeof element == 'string')
    element = document.querySelector(element);
  if (!element) return;

  var color = getComputedStyle(element).getPropertyValue('color');
  var fontSize = getComputedStyle(element).getPropertyValue('font-size');

  element.style.color = 'transparent';
  element.style.textShadow = '0 0 0 ' + color;

  cursor.style.position = 'fixed'; // border doesn't have hairline zoom bug
  cursor.style.borderLeft = '2px solid rgb(0, 109, 254)';
  cursor.style.fontSize = fontSize;
  cursor.style.height = '1.3em';
  cursor.style.marginTop = '-0.25em';
  cursor.style.marginLeft = '-1px';
  cursor.style.width = 1/window.devicePixelRatio + 'px'; // 1.99
  cursor.style.width = 0 + 'px'; // 1.99
  cursor.style.zIndex = 1000;
  cursor.style.cssText += '; left:0; top:0;';

  //cursor.style.marginLeft = cursor.style.width;
  cursor.className = 'cursor';
  document.body.appendChild(cursor);

  startBlinking();

  if (element == document.activeElement)
    update(); // inital coordinates when starting out focused

  (document.activeElement == element) ? maybeShowCursor() : maybeHideCursor();

  var events = [ 'input', 'keyup', 'keydown', 'click', 'scroll', 'change', 'focus']; // focus
  events.forEach(function (event) {
    element.addEventListener(event, update);
  });


  element.addEventListener('mousedown', function () {
    maybeHideCursor();
    element.addEventListener('mousemove', mousemove);
  });
  element.addEventListener('mouseup', function (e) {
    element.removeEventListener('mousemove', mousemove);
    //setTimeout(update, 1);
  });
  function mousemove() {
    if (element.selectionEnd !== element.selectionStart)  {
      maybeHideCursor();
      element.removeEventListener('mousemove', mousemove);
    }
  }

  window.addEventListener('resize', update);
  element.addEventListener('blur', hideCursor);

  //var zoomLevel = window.devicePixelRatio;

  function update(e) {

    //console.log(e && e.type || '?');

    // wait for scroll
    if (e && e.type == 'input' && element.scrollLeft)
      return true;

    if (element != document.activeElement) {
      maybeHideCursor();
      return true;
    } 

    // arrow keys require faster reaction than keyup
    if (e && e.type == 'keydown') {
      if (e.keyCode >= 37 && e.keyCode <= 40 && !e.defaultPrevented)  {
        // selection is not up to date yet, 
        // but with a short delay it will be
        setTimeout(update, 1);
      }
      return true;
    }

    if (e && e.type == 'focus') {
      // special case of showing without starting to blink
      // because position is not correct just yet
      cursor.style.display = 'block';
      cursor.style.visibility = 'hidden';
      //showCursor();
      // but with a short delay it will be
      setTimeout(update, 1);
      return true;
    }

    if (element.selectionEnd !== element.selectionStart) 
      maybeHideCursor();
    else 
      maybeShowCursor();

    // #00B2FF
    var selection = element.selectionEnd;
    var caretPosition = getCaretCoordinates(element, selection);
    var elementPosition = element.getBoundingClientRect();

    //console.log('(top, left) = (%s, %s)', caretPosition.top, caretPosition.left);
    var cursorTop = elementPosition.top + // element.offsetTop
      - element.scrollTop * zoomCompensation()
      + caretPosition.top
      + 'px';
    var cursorLeft = elementPosition.left + // element.offsetLeft
      - element.scrollLeft * zoomCompensation()
      + caretPosition.left
      + 'px';

    cursor.style.webkitTransform = 'translate('+ cursorLeft +', '+ cursorTop +')';
  }
} 


var blinkInterval;
function startBlinking() {
  clearInterval(blinkInterval);
  var flag = true;
  cursor.style.visibility = 'visible';
  blinkInterval = setInterval(function tick() {
      flag = !flag;
      cursor.style.visibility = flag ? 'visible' : 'hidden';
  }, 600);
}

function stopBlinking() {
  clearInterval(blinkInterval);
  cursor.style.visibility = 'hidden';
}

// Event handling
addListener('show', showCursor);
addListener('hide', hideCursor);

function addListener(name, fn) {
  window.addEventListener('cursor.' + name, fn);
}
function publish(name) {
  window.dispatchEvent(new Event('cursor.' + name));
}

//.nocursor { color : transparent; text-shadow : 0 0 0 #000; }
// causes high CPU on Chrome Mac
/*var keyframes =  '@keyframes "blink" { '+
                  '  from, to { visibility:hidden; } '+
                  '  50% { visibility:visible; } } '; // 
keyframes += keyframes.replace('@key', '@-webkit-key');

var css = '.blinking { animation: 1s blink step-end infinite; }' + 
          keyframes;

var cssEl = document.createElement('style');
cssEl.textContent = css;
document.body.appendChild(cssEl);
*/

//////////////////////////////////////////////////


function getCaretCoordinates(element, position) {

  // mirrored div
  mirrorDiv = document.getElementById(element.nodeName + '--mirror-div');
  if (!mirrorDiv) {
    mirrorDiv = document.createElement('div');
    mirrorDiv.id = element.nodeName + '--mirror-div';
    document.body.appendChild(mirrorDiv);
  }

  // batch all layout reads here
  style = mirrorDiv.style;
  computed = getComputedStyle(element);
  var borderTop  = parseInt(computed['borderTopWidth'], 10);
  var borderLeft = parseInt(computed['borderLeftWidth'], 10);
  var elementOffsetTop = element.offsetTop;

  // default textarea styles
  style.whiteSpace = 'pre-wrap';
  if (element.nodeName !== 'INPUT')
    style.wordWrap = 'break-word';  // only for textarea-s

  // position off-screen
  style.position = 'absolute';  // required to return coordinates properly
  style.top = elementOffsetTop + borderTop + 'px';
  style.left = '-9999px';//element.offsetLeft + element.offsetWidth + 30 + 'px';
  style.visibility = window.showMirrorDiv ? 'visible' : 'hidden';  // not 'display: none' because we want rendering

  // transfer the element's properties to the div
  properties.forEach(function (prop) {
    style[prop] = computed[prop];
  });

  if (isFirefox) {
    style.width = parseInt(computed.width) - 2 + 'px'  // Firefox adds 2 pixels to the padding - https://bugzilla.mozilla.org/show_bug.cgi?id=753662
    // Firefox lies about the overflow property for textareas: https://bugzilla.mozilla.org/show_bug.cgi?id=984275
    if (element.scrollHeight > parseInt(computed.height))
      style.overflowY = 'scroll';
  } else {
    style.overflow = 'hidden';  // for Chrome to not render a scrollbar; IE keeps overflowY = 'scroll'
  }  

  mirrorDiv.textContent = element.value.substring(0, position);

  var left, top;

  if (element.nodeName === 'INPUT') {
    // the second special handling for input type="text" vs textarea: spaces need to be replaced with non-breaking spaces - http://stackoverflow.com/a/13402035/1269037
    mirrorDiv.textContent = mirrorDiv.textContent.replace(/\s/g, "\u00a0");
    // input element scrolls to the right if overflowing
    if (mirrorDiv.scrollWidth > mirrorDiv.offsetWidth) {
      mirrorDiv.scrollLeft = 999*999*999;
      //left = mirrorDiv.offsetWidth + borderLeft;
    }
  }

  var span = document.createElement('span');
  // Wrapping must be replicated *exactly*, including when a long word gets
  // onto the next line, with whitespace at the end of the line before (#7).
  // The  *only* reliable way to do that is to copy the *entire* rest of the
  // textarea's content into the <span> created at the caret position.
  // for inputs, just '.' would be enough, but why bother?
  span.textContent = element.value.substring(position) || '.';  // || because a completely empty faux span doesn't render at all
  span.style.backgroundColor = "lightgrey";
  mirrorDiv.appendChild(span);

  var coordinates = {
    top: span.offsetTop + borderTop, //- mirrorDiv.scrollTop,
    left: (span.offsetLeft + borderLeft) //- mirrorDiv.scrollLeft
  };
  return coordinates;
}

window.addCursorToElement = addCursorToElement;
window.getCaretCoordinates = getCaretCoordinates;
window.hideCursor = hideCursor;
window.showCursor = showCursor;

if (!settings.search_bar) return;

function init_cursors() {
  ['input[type="text"],input[type="url"]'].forEach(addCursorToElement);
}

if (/interactive|complete/.test(document.readyState)) {
  requestAnimationFrame(init_cursors);
} else {
  window.addEventListener('DOMContentLoaded', function () {
    requestAnimationFrame(init_cursors);
    //addCursorToElement(byId('search-input'));
  });
}

})();
