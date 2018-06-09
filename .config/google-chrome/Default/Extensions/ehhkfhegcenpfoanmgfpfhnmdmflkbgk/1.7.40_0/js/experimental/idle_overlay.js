
//
// Idle Overlay
//
/*
var active = true;
var last_action = +new Date;
var overlay_opacity = 0;
var overlay;

document.onmousemove = function() {
  last_action = +new Date;
  if (overlay_opacity == 1) {
    overlay || (overlay = document.getElementsByClassName('overlay')[0]);
    overlay.style.opacity = overlay_opacity = 0;
    setTimeout(function(){
      overlay.style.display = "none";
    }, 550);
  }
}

setInterval(function(){
  overlay || (overlay = document.getElementsByClassName('overlay')[0]);
  if (+new Date - last_action > 30000 && overlay.style.opacity == 0) {
    overlay.style.opacity = overlay_opacity = 0;
    overlay.style.display = "block";
    setTimeout(function(){
      overlay.style.opacity = overlay_opacity = 1;
    }, 1000);
  }
}, 1000); 
*/