
function load_bookmarks(callback) {
  chrome.bookmarks.getTree(function (results) {
    var bar_bookmarks = results[0].children[0].children;
    var html = ""; 
    for (var i = 0; i < bar_bookmarks.length; i++) {
      var bm = bar_bookmarks[i]; 
      var icon = bm.url ? 'chrome://favicon/'+bm.url : 'icons/bookmark/folder-win.png';
      if (bm.url)
      	if (bm.url.indexOf('javascript:') == 0 )
      		var icon = 'icons/bookmark/js.png'
      	else 
      		var icon = 'chrome://favicon/'+bm.url;
      else 
      	var icon = 'icons/bookmark/folder-win.png';
  		html += "<a href='#' class='bookmark'><img width='16' height='16' src='"+ icon +"' />" + bm.title + "</a>";
    }
    $("#bookmarks-bar").innerHTML = html;
    callback && callback();
  });
}

function display_bookmarks_bar() {
  $("#bookmarks-bar").opacity = 1;
  $("#page").style.margin = '41px';
}