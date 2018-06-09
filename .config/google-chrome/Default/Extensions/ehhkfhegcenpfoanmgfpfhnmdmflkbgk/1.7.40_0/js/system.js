(function () {

var previousCpuInfo;

function updateCpuUsage(callback) {
  chrome.system.cpu.getInfo(function(cpuInfo) {
  	var cores = [];
  	var sum = 0;
    for (var i = 0; i < cpuInfo.numOfProcessors; i++) {
      var usage = cpuInfo.processors[i].usage;
      var percent = 0;
      if (previousCpuInfo) {
        var oldUsage = previousCpuInfo.processors[i].usage;
        var nowSum = usage.kernel + usage.user;
        var oldSum = oldUsage.kernel + oldUsage.user
        percent = Math.floor((nowSum - oldSum) / (usage.total - oldUsage.total) * 100);
      } 
      else {
        percent = Math.floor((usage.kernel + usage.user) / usage.total * 100);
      }
      sum += percent;
      cores.push(percent);
    }
    previousCpuInfo = cpuInfo;
    callback(sum/cores.length);
  });
}

function updateMemoryUsage(callback) {
  chrome.system.memory.getInfo(function(memoryInfo) {
    var usedMemory = 100 - Math.round(memoryInfo.availableCapacity / memoryInfo.capacity * 100);
    if ('function' == typeof callback) 
      callback(usedMemory);
  });
};

// keep memory usage in check
localStorage.system_last_reload = +new Date;

var MINUTES = 60*1000;
var HOURS   = 60*MINUTES;

if (chrome.system && chrome.system.memory)
setInterval(function () {
  updateMemoryUsage(function (usedMemory) {

    if (usedMemory < 75 && elapsedSinceLastReload() < 4*HOURS) 
      return;

    if (localStorage.FB_index_is_building == "true") 
      return;

    if (chrome.extension.getViews({ type: "tab" }).length)
      return;

    if (elapsedSinceLastReload() < 30*MINUTES)  // matters only if (memory > 75)
      return;

    // finally :)
    sendReloadEvent('system', function () {
      chrome.runtime.reload();
    });
  });
}, 1*MINUTES);

function elapsedSinceLastReload() {
  return +new Date - (localStorage.system_last_reload || 0);
}

})()