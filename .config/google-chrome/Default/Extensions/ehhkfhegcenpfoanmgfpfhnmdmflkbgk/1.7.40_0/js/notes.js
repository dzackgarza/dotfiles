
//
// Notes
//

(function(){

var timer;

if (stored.notes1) {
  var note1 = stored.notes1.split("%%");
  byId("qnote-title").innerHTML = note1[0];
  byId("qnote-text").innerHTML  = note1[1];
}

byId('qnote').oninput = function() {
    clearTimeout(timer);
    timer = setTimeout(function(){
      stored.notes1 = byId("qnote-title").innerHTML + "%%" +  byId("qnote-text").innerHTML;
    }, 50);
}

})();
