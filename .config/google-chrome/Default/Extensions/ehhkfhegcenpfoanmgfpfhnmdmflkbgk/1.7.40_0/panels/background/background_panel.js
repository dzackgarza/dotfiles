
// Copyright (c) 2015 Balázs Galambosi 
// @galambalazs, galambalazs@yahoo.co.uk

var kImageBorder = 5;
var kImageVerticalMargin = 8; // one side

var isFrame = (top !== self);

// not an iframe
if (!isFrame) {
  $('body').css('background', '#222');
  var windowHeight = window.innerHeight;
} else {
  var windowHeight = parent.innerHeight;
}

var kImageHeight = Math.min(window.innerHeight - 80, 160);
var kImageWidth  = kImageHeight * 2;
//var kImageWidth  = 16 * (kImageHeight / 10);

var css = document.createElement('style');
css.textContent = mstc(
  '#image-slider-content div { ' +
    'width:{{0}}px; height:{{1}}px }' + 
  '#image-slider-content img { ' + 
    'width:{{0}}px; height:{{1}}px }' + 
  '#image-slider { height:{{2}}px }' + 
  '::-webkit-scrollbar { ' +
    'width:{{3}}px; height:{{3}}px }',
  [kImageWidth, kImageHeight, 
  kImageHeight + 20, kImageHeight > 100 ? 20 : 16]);
document.body.appendChild(css);
//if (windowHeight > 900) {
//  $('body').css('zoom', '1.25');
//}

//
// Build page
//

//01.jpg - 51.jpg
var html = '';
var count = 52;
for (var i = 1; i <= count; i++) {
  var filename = paddedNumber(i) + '.jpg';
  html += mstc('<div><img src="/img/backgrounds/thumbs/{{0}}"></div>', [filename]);
}

var sliderWidth = count * (kImageWidth + 2*kImageVerticalMargin 
                                       + 2*kImageBorder);
$("#image-slider-content").html(html);
$("#image-slider-content").width(sliderWidth);

$("#image-slider-content div").on("click", function () {
  var $newSelected = $(this);
  $("#image-slider-content .selected").removeClass('selected');
  $newSelected .addClass('selected');

  var image = $newSelected.find('img').prop('src').replace('thumbs/', '');
  parent.postMessage({name: 'setBackgroundStyle', content: 'stretch'}, '*');
  parent.postMessage({name: 'setBackgroundImage', content: image},  '*');
});

var content = $("#image-slider-content")[0];
var wrapper = $("#image-slider")[0];


//
// General scrolling
//

(function (el) { 

var absScrollMax = content.scrollWidth - wrapper.offsetWidth;

// internal relative scrolling (so the scrollbar still works)
var relAccumulatedScroll = 0; 

// delta:  one time thing
// target: accumulated deltas
var lastScroll = Date.now();
var options = {};
options.accelerationDelta = 50;
options.accelerationMax   = 5;
var EASING = 0.09;
var easingDirty = false;


//
// Wheel scrolling
//

//el.onwheel = function (e) {
window.onwheel = function (e) {

  // higi precision scrolling Y -> turn it into X scrolling
  if (Math.abs(e.wheelDeltaY) != 100 && Math.abs(e.wheelDeltaY) != 120 && 
      e.wheelDeltaX == 0) {
    el.scrollLeft -= e.wheelDeltaY;
    return;
  }

  // wheelDelta is inverted
  var delta = -e.wheelDelta || -e.wheelDeltaX || -e.wheelDeltaY;
  if (Math.abs(delta) != 100 && Math.abs(delta) != 120) {
    return true; // leave high quality scrolling devices alone
  } 

  //disableHover();

  delta = delta > 0 ? 240 : -240;
  e.preventDefault();

  // acceleration
  var now = Date.now();
  var elapsed = now - lastScroll;
  if (elapsed < options.accelerationDelta) {
      var factor = (1 + (50 / elapsed)) / 2;
      if (factor > 1) {
          factor = Math.min(factor, options.accelerationMax);
          delta *= factor;
      }
  }
  lastScroll = Date.now();


  if (relAccumulatedScroll > 0 && delta < 0 ||
      relAccumulatedScroll < 0 && delta > 0) {
    //relAccumulatedScroll = 0;
  }

  easingDirty = true;
  //if (lastEasing == EASING) lastEasing = EASING / 2;
  var lastDeltaEstimate = relAccumulatedScroll * lastEasing;
  lastEasing = lastDeltaEstimate / (relAccumulatedScroll + delta);

  collect.push('wheel');

  relAccumulatedScroll += delta;

  if (!pendingFrame)
    pendingFrame = requestAnimationFrame(onFrame);
}


//
// Keyboard scrolling
//

var keydownTimer;

window.onkeydown = function (e) {
  if (e.keyCode != 37 && e.keyCode != 39) return true;
  if (keydownTimer) return true;
  keydownTimer = setInterval(onKeydownInterval, 20);
  onKeydownInterval();
  function onKeydownInterval() {
    // 37: left, 39: right
    var delta = (e.keyCode == 39) ? 10 : -10;
    if (relAccumulatedScroll > 0 && delta < 0 ||
        relAccumulatedScroll < 0 && delta > 0) {
      relAccumulatedScroll = 0;
    }
    relAccumulatedScroll += delta;
    if (!pendingFrame)
      pendingFrame = requestAnimationFrame(onFrame);
  }
}

window.onkeyup = function (e) {
  if (e.keyCode != 37 && e.keyCode != 39) return true;
  clearInterval(keydownTimer);
  keydownTimer = null;
}


//
// Scrolling render
//

var pendingFrame;
var lastEasing = 0;
var lastFrame;
var lastDelta;
var frameBudget = 1000/60;

function onFrame() {
  pendingFrame = null;

  lastFrame || (lastFrame = Date.now());
  var now = Date.now();
  var frameDelta = now - lastFrame;
  lastFrame = now;

  var absCurrentScroll = el.scrollLeft;

  // bounds check (0, absScrollMax)
  var absTargetScroll = absCurrentScroll + relAccumulatedScroll;
  absTargetScroll = Math.max(Math.min(absTargetScroll, absScrollMax), 0);

  var absReaminingScroll = absTargetScroll - absCurrentScroll;

  /*if (easingDirty && !isApproachingBounds) {
    //if (lastEasing == EASING) lastEasing = EASING / 2; // crude alt. but looks ok
    var lastDeltaEstimate =  (relAccumulatedScroll-) * lastEasing;
    lastEasing = lastDeltaEstimate / relAccumulatedScroll;
    //lastEasing = lastDelta / relAccumulatedScroll;
  }
  easingDirty = false;
  */

  // final scroll event (tiny portion to go)
  if (Math.abs(absReaminingScroll) < 1) { // 0.01
    var currentDelta = absReaminingScroll; 
  // easing phase, still going
  } else {
    var isApproachingBounds = (!absTargetScroll || absTargetScroll == absScrollMax);
    var currentEasing = lastEasing + (EASING/15) * (frameDelta/frameBudget);
    currentEasing = isApproachingBounds ? EASING : Math.min(currentEasing, EASING);
    lastEasing = currentEasing;
    var currentDelta = absReaminingScroll * currentEasing;
  }

  // accumulated delta gets bounds checked this way as well
  relAccumulatedScroll = absReaminingScroll - currentDelta;

  // Chrome doesn't handle fractures that well,  so we keep
  // the accumulation as FLOAT and the actual scroll as INT
  currentDelta = Math.round(currentDelta);

  if (Math.abs(currentDelta) > 0.1) {
    pendingFrame = requestAnimationFrame(onFrame);
  } else {
    relAccumulatedScroll = 0;
    //enableHover();
  }

  if (currentDelta == 0) {
    lastEasing = 0;
    return;
  }

  var absNewScroll = absCurrentScroll + currentDelta;

  //collect.push(currentDelta);
  lastDelta = currentDelta;

  el.scrollLeft = absNewScroll;
}

var collect = [];

})($("#image-slider")[0]);

//
// Helpers
//

function paddedNumber(n) {
  return (n < 10 ? '0' : '') + n;
}

function mstc(a,b){
  return(a+'').replace(/\{\{([^{}]+)}}/g,
    function(c,d){
      return d in(b||{})?(/^f/.test(typeof b[d])?b[d]():b[d]):c
    })
}

var hoverMask = document.createElement('div');
hoverMask.style.cssText = 'position: fixed;top:0; bottom:0;'+
                          'width:100%; height:100%; z-index:100;';
hoverMask.onmousedown = function (e) {
  enableHover();
  setTimeout(disableHover, 1000)
}

var isHoverEnabled = true;
function disableHover(el) {
  if (isHoverEnabled)
    document.body.appendChild(hoverMask);
  isHoverEnabled = false;
}

function enableHover(el) {
  if (!isHoverEnabled)
    document.body.removeChild(hoverMask);
  isHoverEnabled = true;
}

//
// Debug
//

/*

var scrolls = [];
var imageSlider = $("#image-slider")[0];
$("#image-slider").on('scroll', function () {
  scrolls.push(imageSlider.scrollLeft);
});

setInterval(function () {
  if (!scrolls.length) return;
  var deltas = [];
  for (var i = 1; i < scrolls.length; i++)
    deltas.push(scrolls[i] - scrolls[i-1]);
  console.log(deltas.join('\n'));
  scrolls = [];
}, 1000);

*/