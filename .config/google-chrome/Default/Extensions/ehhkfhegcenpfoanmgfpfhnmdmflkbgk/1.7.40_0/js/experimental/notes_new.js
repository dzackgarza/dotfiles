
//
// Notes
//

(function(){

var timer;

show_note(get_legacy_local_note());

if (chrome.storage.sync)
chrome.storage.sync.get('qnote', function (result) {
  if (result.qnote) show_note(result.qnote);
});

function show_note(note1) {
  note1 = note1.split("%%");
  byId("qnote-title").innerHTML = note1[0]; 
  byId("qnote-text").innerHTML  = note1[1];
}

function save_current_note() {
  stored.notes1 = byId("qnote-title").innerHTML + "%%" + byId("qnote-text").innerHTML;
  if (chrome.storage.sync)
    chrome.storage.sync.set({ 'qnote': stored.notes1 });
}

byId('qnote').oninput = function() {
    clearTimeout(timer);
    timer = setTimeout(save_current_note, 500);
}

byId('qnote').onchange = function() {
    clearTimeout(timer);
    save_current_note();
}

if (chrome.storage.sync)
chrome.storage.onChanged.addListener(function(changes, namespace) {
  Object.keys(changes).forEach(function (key) {
    var storageChange = changes[key];
    console.log('Storage key "%s" in namespace "%s" changed. ' +
                'Old value was "%s", new value is "%s".',
                key,
                namespace,
                storageChange.oldValue,
                storageChange.newValue);
  })
});

function get_legacy_local_note() {
  return stored.notes1;
}

})();
