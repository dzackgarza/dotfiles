
//
// Recently closed
//

/*
6 Tabs
show tab titles in link title attr.
open new window with tabs
last tab selected
var recent_tab_src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2hpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozMUJCMTE0RjEwMjA2ODExODIyQUI0Q0UzM0EzRUU5RSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo1NjA2NTZCMEM0ODcxMUUxQUZBQ0M1NjBBMzY5NzYxRCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1NjA2NTZBRkM0ODcxMUUxQUZBQ0M1NjBBMzY5NzYxRCIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M2IChNYWNpbnRvc2gpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6NkE3RkQ0RTQyNjIwNjgxMThBNkRBQTQ1MzA5MjkxNzIiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MzFCQjExNEYxMDIwNjgxMTgyMkFCNENFMzNBM0VFOUUiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7Km3O2AAAAOElEQVQ4y2M4ceLEYSD+TyY+zECBZjCGG4AOQGLPnj1DwTgNwAWIMQSvAYTAqAGjBgwuAyjJzkcAtmTCw0j9ScUAAAAASUVORK5CYII=";
*/

(function(){

var opened = false;

byId('recently-closed-button').onmouseenter = function () {
  if (byId('recently-closed-css')) return;
  var css  = document.createElement('link');
  css.id   = 'recently-closed-css';
  css.rel  = 'stylesheet';
  css.type = 'text/css';
  css.href = 'css/recently_closed.css'
  document.head.appendChild(css);
}

byId('recently-closed-button').onclick = function() {
  var box = byId('recently-closed-box');
  var list = byId('recently-closed-list');
  if (opened) {
    close();
  }
  else {
    document.on("click", close);
    box.style.display = 'none';

    var html = "";
    var closedTabIdMax = stored['SU_closedTabIdInc'] - 1;

    if (closedTabIdMax >= 0) {
      for (var i = 0; i < 10; i++) {
        var id = closedTabIdMax - i;
        var tab = stored['SU_closedTab:' + id];
        if (!tab) continue;
        try { 
          tab = JSON.parse(tab); 
          html += '<a href="'+ tab.url +'" target="_blank">' + 
                    '<img src="chrome://favicon/'+ tab.url +'">'+ 
                    escapeHtml(tab.title) +
                  '</a>';
        } catch (e) {
          logError(new Error('ERROR: recently closed has invalid JSON: '));
        }
      }
      byId('recently-closed-clear-button').style.display = '';
    } else {
      html = "<div style='padding:20px 40px'>List is empty. Only the tabs closed <b>after</b> installing this extension will appear here.</div>";
      byId('recently-closed-clear-button').style.display = 'none';
    }

    list.innerHTML = html;

    var width = box.offsetWidth;

    box.style.webkitTransition = "none";
    //list.style.right = (-width) + "px"; // 
    //list.style.webkitTransform = "translateX("+ width +"px)";
    box.style.display = 'block';
    box.classList.add('minimized');

    setTimeout(function(){
      box.style.webkitTransition = "";
      //list.style.right =  "0px";
      box.classList.remove('minimized');
    }, 1)
    
    box.on("webkitTransitionEnd", function transitionEnd(e) {
      box.off("webkitTransitionEnd", transitionEnd);
      opened = true;
    });
  }

 function close(e) {
    if (!opened) return;

    document.off("click", close);

    //box.style.right =  -width + "px";
    //box.style.webkitTransform = "translateX("+ width +"px)";
    box.classList.add('minimized');

    box.on("webkitTransitionEnd", function transitionEnd(e) {
      box.off("webkitTransitionEnd", transitionEnd);
      box.style.display = 'none';  
      opened = false;
    });

    if (e.target && e.target.id == 'recently-closed-clear-button')
      clear();
  }
}

function clear() {
  var closedTabIdMax = stored['SU_closedTabIdInc'] - 1;
  for (var i = 0; i < 30; i++) {
    var id = closedTabIdMax - i;
    delete stored['SU_closedTab:' + id];
  }
  stored['SU_closedTabIdInc'] = 0;
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

})();