
//
// Draggable
//

// (c) 2012 Balázs Galambosi

// kell több items []
// drag oldal váltás lapozáskor
// ordered i,i,i,i;i,i,i,,,;
// átrendezés lapok között
// méretezés általánosítása
// új temp. oldal grab-kor

(function(){

window.requestAnimationFrame = window.requestAnimationFrame || 
                               window.webkitRequestAnimationFrame;

var item_width, item_height, rows, cols, root, root_width, root_height,
    items, target, ghost, drag_item_x, drag_item_y, store_timer,
    target_index, page, dots;
var margin = 10;
var page_margin = 100;
var page_width = 740;
var items_per_page = 20;
var cols = 5;
var rows = 4;
var mouse_is_moving = false;

function init() {

  root = byId('apps-pages-list');
  page = byId('page');
  dots = byId('apps-dots');

  dots.on("mouseover", dots_action);

  // use a static copy of item list
  // but make sure to keep it up to date when using ghost item
  items = [].slice.call($('.test-item', root));

  if (!stored.icons_order)
    calculate_order();

  calculate_grid(); // !!stored.app_html_webstore

  // resize event may change icon size (but not the structure)
  last_window_width = window.innerWidth;
  window.on("resize", onresize);

  // scroll event handlers
  root.on('mousewheel', onscroll);
  document.on("keydown", onkeydown);

  // show new item on install (last page)
  if (window.location.hash == "#last") {
    window.location.hash = "";
    setTimeout(go_last_page, 500);
  } else if (window.location.hash.indexOf("#page=") != -1) {
    var pageToGo = window.location.hash.split('=')[1];
    window.location.hash = "";
    setTimeout(function () { switch_page(pageToGo); }, 500);
  }

  // append as many handler "dots" as pages
  refresh_dots();

  // possible drag start
  root.onmousedown = function(e) {
    // only need left mouse button
    if (e.button != 0) return;
    var target = e.target;
    // var item = e.target.closest('.test-item'); to drag not just by img, but problems
    // it was a click on an icon
    if (target.nodeName == 'IMG'|| /^cal/.test(target.id)) {
      // don't want the image to be dragged by Chrome
      e.preventDefault();
      // select the item containing the icon
      var item = target.parentNode.parentNode;
      // save mouse offset on item
      drag_item_x = e.offsetX;
      drag_item_y = e.offsetY;
      // drag starts on the first mousemove
      item.onmousemove = function(e) {
        // micro movements are still clicks
        if (distance(drag_item_x, drag_item_y, e.offsetX, e.offsetY) < 10)
          return;
        // clean up
        item.onmousemove = null;
        // find out the items index
        var index = get_cell_index_at(e.pageX, e.pageY);
        // start dragging
        grab(index, e);
        // stop 'app launch' from happening
        // when the item is released
        item.onclick = function(e){
          item.onclick = null;
          e.stopPropagation();
        }
      }
      // if there's a click wo movement
      // it's a simple app launch event
      item.onclick = function(e) {
        item.onclick = null;
        item.onmousemove = null;
      }
    }
  }
}

function refresh_dots() {
  // append as many handler "dots" as pages
  var dots_count = $('span', dots).length;
  for (var i = get_page_count() - dots_count; i--;) {
    dots.insertAdjacentHTML("beforeend", "<span></span>");
  }
  dots.style.visibility =  (get_page_count() == 1) ? "hidden" : "";
}

function distance(x1, y1, x2, y2) {
  return Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

function calculate_order() {
  var arr = [];
  for (var i = 0; i < items.length; i++) {
    arr.push(items[i].id);
  }
  stored.icons_order = JSON.stringify(arr);
}

/// TODO: only recalc. if things have changed
function calculate_grid(cached) {

  // delay if we were too fast and not everything's been painted yet
  if (!window.innerWidth) {
    setTimeout(function() {
      calculate_grid(cached);
    }, 10);
    return;
  }

  root_width  = root.clientWidth;
  root_height = root.clientHeight;
  item_width  = root.firstElementChild.clientWidth;
  item_height = root.firstElementChild.clientHeight;

  //cols = Math.floor(root_width / (item_width + 2 * margin));
  //rows = Math.ceil(items.length / cols);

  if (cached) return;

  // calculate absolute positions
  for (var i = items.length; i--;) {
    var pos = get_cell_pos(i);
    var item = items[i];
    //item.style.position = 'absolute';
    setPos(item, pos.left, pos.top);
    cache_set_app_html(item, item.outerHTML);
  }
}

var resize_timer;
var last_window_width;

function onresize(e) {
  ///console.log(window.innerWidth  + " x " + window.innerHeight);
  if (window.innerWidth == last_window_width) return;
  last_window_width = window.innerWidth;
  clearTimeout(resize_timer);
  resize_timer = setTimeout(calculate_grid, 200);
}


/**
 * Drag start.
 */
function grab(index, e) {

  ///if (index == -1) return;
  ////console.log("grab " + index + " : " + e.pageX + " , "  + e.pageY); ////
  mouse_is_moving = true;

  target = items[index];
  target_index = index;

  root.classList.remove('animated');

  // make a ghost copy for replacement
  ghost = target.cloneNode(true);
  ghost.style.visibility = 'hidden';

  // this event is initialized by the
  // first mousemove after mousedown
  // so we call mousemove for coordinates
  save_mouse_coordinates(e);
  update();

  // replace dragged item with a blank 'ghost'
  // replace in DOM
  root.replaceChild(ghost, target);
  // replace in static list
  items[index] = ghost;

  //target.style.left = ghost.offsetLeft + 'px';
  //target.style.top  = ghost.offsetTop  + 'px';

  // target item is removed from the list while dragging
  target.classList.add('dragged');
  page.appendChild(target);

  var next_move;
  var timer;
  var pager_timer;
  var container_offset = root.parentNode.parentNode.offsetLeft;
  var mouse_x, mouse_y;

  /**
   * Do as little work on mouse move as we can
   */
  function save_mouse_coordinates(e) {
    mouse_x = e.pageX;
    mouse_y = e.pageY;
    // stop default dragging action
    e.preventDefault();
  }

  /**
   * Updates the dragged item (vsync)
   */
  function update() {

    if (!mouse_is_moving) return;

    // update dragged item coordinates
    setPos(target,
          (mouse_x - drag_item_x - margin),
          (mouse_y - drag_item_y - margin))

    // refresh list order after some delay
    //clearTimeout(timer);
    if (!timer) {
      timer = setTimeout(function() {
        timer = null;
        if (!pager_timer) {
          var center_x = mouse_x - container_offset - drag_item_x + item_width / 2;
          if (center_x < 10 || center_x > 730) {
              pager_timer = setTimeout(function(){
                if (center_x < 10 && current_page != 0) {
                  go_previous_page();
                }
                else if (center_x > 730) {
                  go_next_page();
                }
                pager_timer = null;
              }, 500);
          }
        }
        // new index is where the mouse if pointing at
        var new_index = get_cell_index_at(mouse_x, mouse_y);
        //if (new_index != -1) {
          // do the reordering
          move(new_index, index);
          index = new_index;
        //}
      }, 30);
    }

    // go on while the mouse is still moving
    if (mouse_is_moving) requestAnimationFrame(update);
  }

  function mouseup(e) {
    // clean up
    mouse_is_moving = false;
    save_mouse_coordinates(e);
    update();
    clearTimeout(timer);
    document.off('mouseup', mouseup);
    mouse_overlay.style.display = "none";
    mouse_overlay.off('mousemove', save_mouse_coordinates);
    release(e);
  }

  var mouse_overlay = byId("mouse-move-overlay");
  mouse_overlay.style.display = "block";

  document.on('mouseup', mouseup);
  mouse_overlay.on('mousemove', save_mouse_coordinates);

  // start the dragging animation
  requestAnimationFrame(update);
}

/**
 * Drag end.
 */
function release(e) {

  ////console.log("release" + " : " + e.pageX + " , "  + e.pageY); ////

  // make return animation faster
  //target.style.webkitTransitionDuration = ".15s, .10s, .15s, .15s";
  target.style.webkitTransition = "left .15s ease-out, top .15s ease-out";

  // do the reordering
  var index = get_cell_index_at(e.pageX, e.pageY);

  // move everybody into their new place
  move(index, target_index);

  // change from on-screen position to in-list-element positions
  var root_pos = root.getBoundingClientRect();
  //target.style.left = e.pageX - root_pos.left + "px";
  //target.style.top  = e.pageY - root_pos.top  + "px";

  // send target to ghost's destination
  // (works even if ghost was still moving)
  setPos(target, root_pos.left + getLeft(ghost), root_pos.top + getTop(ghost));
  target.classList.remove('dragged');

  // after the animation ended
  target.on("webkitTransitionEnd", transitionEnd);

  function transitionEnd(e){

    if (!/left|right/i.test(e.propertyName)) return;

    target.off("webkitTransitionEnd", transitionEnd);

    target.style.webkitTransition = ""; // webkitTransitionDuration

    setPos(target, getLeft(ghost), getTop(ghost));
    //target.classList.remove('dragged');

    // replace back in DOM
    root.replaceChild(target, ghost);
    // replace back in static list
    items[index] = target;


    // store icons order and cache htmls
    var list = [];
    for (var i = 0; i < items.length; i++) {
      list.push(items[i].id);
      cache_set_app_html(items[i], items[i].outerHTML);
    }
    stored.icons_order = list.join(",");
    // clean up
    target = ghost = null;
  }


}

function get_cell_index_at(pageX, pageY) {
  // TODO: ignore coords out of the target zone
  //...

  // convert to in-element positions
  var root_pos = root.parentNode.getBoundingClientRect();
  var x = pageX - root_pos.left;
  var y = pageY - root_pos.top;

  // calculate cell position in grid
  var row = Math.floor(y / (item_height + 2 * margin))
  var col = Math.floor(x / (item_width  + 2 * margin));

  // ignore negative values
  col = Math.max(col, 0);
  row = Math.max(row, 0);

  var index = row * cols + col + (current_page * rows * cols);

  return Math.min(index, items.length - 1);///index < items.length ? index : -1;///Math.min(index, items.length - 1);///
}

function get_cell_pos(index) {
  var row = Math.floor(index / cols) % rows; // 0-1-2-3
  var col = index % cols;
  var page_index = Math.floor(index / (rows * cols));

  var top  = row * item_height + (2 * row) * margin;
  var left = col * item_width  + (2 * col) * margin + page_index * (page_width + page_margin);

  return {left: left, top: top};
}

function move(new_index, old_index) {

  if (new_index == old_index || new_index < 0) return;

  ////console.log("move : " + old_index + " -> " + new_index ); ////

  target_index = new_index;

  /// TODO: don't issue reorderings in parallel?
  /// cancel last one maybe?

  root.classList.remove('animated');

  var new_items = [];

  // create new list of items
  // (exact copy at first)
  for (var i = items.length; i--;) {
    new_items[i] = items[i];
  }

  // shift items to fill blank space
  // 2 possible directions
  var temp = new_items[old_index];

  if (new_index - old_index > 0) {
    for (var i = new_index; i > old_index; i--) {
      new_items[i-1] = items[i];
    }
  }
  else {
    for (var i = new_index; i < old_index; i++) {
      new_items[i+1] = items[i];
    }
  }

  new_items[new_index] = temp;

  root.classList.add('animated');

  // calculate new positions
  for (var i = new_items.length; i--;) {
    var pos = get_cell_pos(i);
    new_items[i].style.position = 'absolute';
    setPos(new_items[i], pos.left, pos.top);
  }

  items = new_items;
}


var current_page = 0;
var dots_timer;

function get_current_page() {
  return current_page;
}

function go_next_page() {
  if (current_page >= get_page_count() - 1) return;
  switch_page(current_page + 1);
}

function go_previous_page() {
  if (current_page <= 0) return;
  switch_page(current_page - 1);
}

function go_last_page() {
  switch_page(get_page_count() - 1);
}

function get_page_count() {
  return Math.floor((items.length - 1) / (cols * rows)) + 1;
}

function switch_page(index) {
  if (current_page == index) return;
  current_page = index;
  var pages = byId('apps-pages-list'), style = pages.style;
  //style.webkitTransform = "translateX(" + (-current_page * 840) + 'px)';
  style.webkitTransform = "translate3d(" + (-current_page * 840) + 'px,0,0)';

  clearTimeout(dots_timer);
  dots_timer = setTimeout(function() {
    $('.active-dot', dots)[0].className = "";
    dots.children[current_page].className = 'active-dot';
  }, 300);
}

function dots_action(e) {
  if (e.target.nodeName != 'SPAN') return;
  var cnt = 0;
  var el = e.target;
  while ((el = el.previousSibling)) {
    cnt++;
  }
  switch_page(cnt);
}

var is_scrolling = false;

function onscroll(e) {
  ///console.log(e.wheelDeltaX)
  e.preventDefault();
  var delta = e.wheelDeltaX || e.wheelDeltaY;
  if (!is_scrolling && delta) {
    (delta < 0) ? go_next_page() : go_previous_page();
    is_scrolling = true;
    setTimeout(function() {
      is_scrolling = false;
    }, Math.abs(delta) == 120 ? 300 : 1000);
    // FIXED: add delay because mac os x continues scrolling for a long time
  }
}

function onkeydown(e) {
  if (!is_scrolling && e.target == document.body) {
    if (e.keyCode == 37)
      go_previous_page();
    if (e.keyCode == 39)
      go_next_page();
    is_scrolling = true;
    setTimeout(function() {
      is_scrolling = false;
    }, 300);
  }
}

function reset() {
  calculate_order();
  calculate_grid();
}

function add_new_app_html_beforeend(html) {
  root.insertAdjacentHTML("beforeend", html);
  var el = root.lastChild;
  var pos = get_cell_pos(items.length);
  setPos(el, pos.left, pos.top);
  items.push(root.lastChild);
  refresh_dots();
}

function add_new_app_html_afterbegin(html) {
  root.insertAdjacentHTML("afterbegin", html);
  var el = root.firstChild;
  var pos = get_cell_pos(0);
  setPos(el, pos.left, pos.top);
  items.unshift(el);
  refresh_dots();
  reset();
}

function replace_app_html(oldEl, replacementHtml) {
  var index = items.indexOf(oldEl);
  if (index == -1) return;
  var pos = get_cell_pos(index);
  var newEl = document.createElement('div');
  newEl.innerHTML = replacementHtml;
  newEl = newEl.firstChild;
  items[index] = newEl;
  setPos(newEl, pos.left, pos.top);
  oldEl.parentNode.replaceChild(newEl, oldEl);
}

function add_new_app_html(html) {
  add_new_app_html_beforeend(html);
}

// Data attributes are nice but expandos are still the fastest (50-100x)
// http://jsperf.com/dataset-vs-setattribute-vs-expando
function setPos(el, left, top) {
  el.left = left;
  el.top = top;
  el.style.left = left + 'px';
  el.style.top = top + 'px';
  //el.style.webkitTransform = 'translate(' + left +  'px, ' + top + 'px)';
}

function getLeft(el) {
  return el.left || (el.left = parseInt(el.style.left, 10));
}

function getTop(el) {
  return el.top  || (el.top = parseInt(el.style.top, 10));
}

function getPos(el) {
  return { left: el.dataset.left, top: el.dataset.top };
}

window.draggable_init = init;
window.get_cell_pos = get_cell_pos;
window.get_cell_index_at = get_cell_index_at;
window.get_current_page = get_current_page;
window.go_last_page = go_last_page;
window.go_next_page = go_next_page;
window.go_previous_page = go_previous_page;
window.add_new_app_html = add_new_app_html;
window.replace_app_html = replace_app_html;

// somebody already called us
if (window.draggable_should_init_async) {
  window.draggable_init();
}

})();