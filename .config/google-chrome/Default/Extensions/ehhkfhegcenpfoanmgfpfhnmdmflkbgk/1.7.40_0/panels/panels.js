(function () {

//
// New User App
//

var panel;

function prepare_new_app_panel() {
  if (panel) return panel;
  panel = document.createElement('iframe');
  panel.src = '/panels/new_app/new_app_panel.html';
  panel.id = 'new-app-panel';
  panel.className = 'hidden';
  document.body.appendChild(panel);
  return panel;
}

function show_new_app_panel(callback) {
  prepare_new_app_panel();
  panel.style.webkitAnimation = '';
  //clearTimeout(hide_new_app_panel.timer);
  setTimeout(function () {
    panel.focus();
    panel.className = '';
    window.on('click', hide_new_app_panel);
    if ('function' == typeof callback) callback(panel);
  }, 10)
}

function hide_new_app_panel() {
  var panel_to_remove = panel;
  if (!panel_to_remove) return;
  panel = null;
  panel_to_remove.className = 'hidden';
  stopAndRemoveAnimation(panel_to_remove);
  hide_new_app_panel.timer = setTimeout(function () {
    document.body.removeChild(panel_to_remove);
  }, 1000);
  window.off('click', hide_new_app_panel);
}

byId('add-app-button').on('click', show_new_app_panel);
byId('add-app-button').on('mouseenter', loadPanelsCSS);
byId('add-app-button').on('mouseenter', bindNextTick(prepare_new_app_panel));
window.show_new_app_panel = show_new_app_panel;

//
// Change background
//

function prepare_background_settings_panel() {
  var el = document.createElement('iframe');
  el.src = '/panels/background/background_panel.html';
  el.id = 'background-setting-panel';
  el.className = 'hidden';
  document.body.appendChild(el);
  return el;
}

function show_background_settings_panel() {
  var el = byId('background-setting-panel') ||
           prepare_background_settings_panel();
  clearTimeout(hide_background_settings_panel.timer);
  el.style.webkitAnimation = '';
  //el.onload = el.focus.bind(el);
  setTimeout(function () {
    el.focus();
    el.className = '';
    window.on('click', hide_background_settings_panel);
  }, 10)
}

function hide_background_settings_panel() {
  var el = byId('background-setting-panel');
  if (!el) return;
  el.className = 'hidden';
  stopAndRemoveAnimation(el);
  hide_background_settings_panel.timer = setTimeout(function () {
    document.body.removeChild(el);
  }, 1000);
  window.off('click', hide_background_settings_panel);
}

byId('background-button').on('click',     show_background_settings_panel);
byId('background-button').on('mouseenter', loadPanelsCSS);
byId('background-button').on('mouseenter', bindNextTick(prepare_background_settings_panel));

window.on('message', function () {
  if ('setBackgroundStyle' == event.data.name) {
    settings.background_style = event.data.content;
    change_background_style();
    save_options();
  }
  if ('setBackgroundImage' == event.data.name) { 
    settings.background_image = event.data.content;
    change_background();
    save_options();
    /*// we temporarily set the user selected image to show him a preview
    settings.background_image = event.data.content;
    change_background(true);
    // but save_new_background does the saving and corrects the settings
    bg.save_new_background(event.data.content);*/
  }
});


window.hide_new_app_panel = hide_new_app_panel;
window.hide_background_settings_panel = hide_background_settings_panel;


//
// New User App
//

function prepare_speech_panel() {
  var el = document.createElement('iframe');
  el.src = '/panels/speech/speech_panel.html';
  el.id = 'speech-panel';
  el.className = 'hidden';
  document.body.appendChild(el);
  return el;
}

function show_speech_panel() {
  var el = byId('speech-panel') || prepare_speech_panel();
  clearTimeout(hide_speech_panel.timer);
  setTimeout(function () {
    el.focus();
    el.className = '';
    window.on('click', hide_speech_panel);
  }, 10)
}

function hide_speech_panel() {
  var el = byId('speech-panel');
  if (!el) return;
  el.className = 'hidden';
  document.body.removeChild(el);
  window.off('click', hide_speech_panel);
}

window.on('message', function () {
  if ('speechSearchEnded' == event.data.name) {
    hide_speech_panel();
    byId('search-input').value = event.data.content;
    byId('search-button').click();
  } 
  else if ('speechClose' == event.data.name) {
    hide_speech_panel();
  }
});

//byId('microphone-button').onmouseenter = bindNextTick(prepare_speech_panel);
byId('microphone-button').on('mousedown', prepare_speech_panel);
byId('microphone-button').on('click', show_speech_panel);
byId('microphone-button').on('mouseenter', loadPanelsCSS);


//
// Animation
//

function stopAndRemoveAnimation(el) {
  var trafo = getComputedStyle(el, null).webkitTransform;
  el.style.webkitTransform = trafo;
  el.style.webkitAnimation = 'none';
  setTimeout(function () {
    el.style.webkitTransform = '';
  }, 1)
}


var frames = [
  ['0', 110.00000000000001],
  ['30', -2.571428571428564],
  ['35', -2.295238095238097],
  ['40', 0],
  ['45', 1.2571428571428577],
  ['50', 1.2190476190476199],
  ['55', 0],
  ['60', -0.7509523809524043],
  ['65', -0.51904761904763],
  ['70', 0],
  ['75', 0.459523809523815],
  ['80', 0.2547619047618964],
  ['85', 0],
  ['90', -0.2723809523809593],
  ['95', -0.1623809523809593],
  ['100', 0]
];

var hwAccel = ' translateZ(0)';

function startAnimation(el, xy, allDuration) {
  var myFrames = frames.slice(); // static copy

  var previousFrame;

  // every other keyframe
  function onKeyFrame() {
    currentFrame = myFrames.shift();

    if (previousFrame) {
      var duration = allDuration * (currentFrame[0]-previousFrame[0]) / 100;
      el.style.webkitTransition = '-webkit-transform '+ duration +'ms'; // ease-in-out
    } else {
      el.style.webkitTransition = ''; 
    }

    el.style.webkitTransform = 'translate(' + currentFrame[1] + '%, 0%)' + hwAccel;

    var nextFrame = myFrames[0];
    if (nextFrame) {
      var delay = allDuration * (nextFrame[0]-currentFrame[0]) / 100;
      setTimeout(onKeyFrame, delay);
    }

    previousFrame = currentFrame;
  }

  onKeyFrame();
}

function loadPanelsCSS() {
  if (byId('panels-css')) return;
  var css  = document.createElement('link');
  css.id   = 'panels-css';
  css.rel  = 'stylesheet';
  css.type = 'text/css';
  css.href = 'css/panels.css';
  document.head.appendChild(css);
}
window.loadPanelsCSS = loadPanelsCSS;

})();