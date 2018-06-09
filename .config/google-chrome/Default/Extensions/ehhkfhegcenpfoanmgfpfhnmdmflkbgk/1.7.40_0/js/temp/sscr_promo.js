(function () {

show();

function show() {
  var el = document.createElement('div');
  el.id = 'sscr-promo';
  el.className = 'helpful-message clickable';
  el.innerHTML = 'SmoothScroll';
  el.innerHTML = '<img src="img/promo/smoothscroll.png" ' + 
                 '     width="20" style="display: inline-block; ' +
                 '                       position: relative; top: 4px;"> ' + 
                 el.innerHTML;
  el.style.cursor = 'pointer';
  el.style.right = '-146px';
  el.onclick = onClick;
  byId('search-form').appendChild(el);
}

function hide() {
  var el = byId('sscr-promo');
  if (el) el.parentNode.removeChild(el);
}

function onClick() {
  //hide();
  stored.SS_promo_clicked = 'true';
  stored.SS_promo_click_date = Date.now();
  window.location = "https://www.smoothscroll.net/mac/?ext-home";
}

})();