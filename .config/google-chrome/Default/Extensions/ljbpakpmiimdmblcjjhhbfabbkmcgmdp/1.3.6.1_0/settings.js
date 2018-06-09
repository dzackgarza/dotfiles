var ownBitmap, storedCanvas = document.createElement("canvas"), ownIconSelected = !1;
function resetDefaultPrefs() {
  window.localStorage.buttonSettings = JSON.stringify({addToMnu:!1, blockDownloads:!1});
  var a = JSON.parse(window.localStorage.buttonSettings);
  document.getElementById("addToMnu").checked = a.addToMnu;
  document.getElementById("blockDownloads").checked = a.blockDownloads;
  a.yellowIcon = !1;
  document.getElementById("yellowIcon").checked = !1;
  a.greenIcon = !1;
  document.getElementById("greenIcon").checked = !1;
  a.purpleIcon = !1;
  document.getElementById("purpleIcon").checked = !1;
  a.redIcon = !1;
  document.getElementById("redIcon").checked;
  a.beigeIcon = !1;
  document.getElementById("beigeIcon").checked = !1;
  a.defaultIcon = !0;
  document.getElementById("defaultIcon").checked = !0;
  saveSettings();
}
function saveSettings() {
  var a = JSON.parse(window.localStorage.buttonSettings);
  a.addToMnu = document.getElementById("addToMnu").checked;
  a.blockDownloads = document.getElementById("blockDownloads").checked;
  a.yellowIcon = document.getElementById("yellowIcon").checked;
  a.greenIcon = document.getElementById("greenIcon").checked;
  a.purpleIcon = document.getElementById("purpleIcon").checked;
  a.redIcon = document.getElementById("redIcon").checked;
  a.beigeIcon = document.getElementById("beigeIcon").checked;
  a.defaultIcon = document.getElementById("defaultIcon").checked;
  a.ownIcon = document.getElementById("ownIcon").checked;
  a.ownIcon && ownIconSelected && (a.storedCanvas = storedCanvas.toDataURL("image/png"));
  a.yellowIcon ? chrome.browserAction.setIcon({path:"yellow.png"}) : a.greenIcon ? chrome.browserAction.setIcon({path:"green.png"}) : a.purpleIcon ? chrome.browserAction.setIcon({path:"purple.png"}) : a.redIcon ? chrome.browserAction.setIcon({path:"red.png"}) : a.beigeIcon ? chrome.browserAction.setIcon({path:"beige.png"}) : a.ownIcon && null != a.storedCanvas ? chrome.browserAction.setIcon({imageData:ownBitmap}) : chrome.browserAction.setIcon({path:"icon.png"});
  document.getElementById("labelError").style.display = "none";
  window.localStorage.buttonSettings = JSON.stringify(a);
  chrome.extension.getBackgroundPage().startOrRefresh();
}
window.onload = function() {
  var a = JSON.parse(window.localStorage.buttonSettings);
  document.getElementById("addToMnu").checked = a.addToMnu;
  document.getElementById("blockDownloads").checked = a.blockDownloads;
  document.getElementById("addToMnu").onclick = function() {
    saveSettings();
  };
  document.getElementById("blockDownloads").onclick = function() {
    saveSettings();
  };
  document.getElementById("restoreDefaults").onclick = function() {
    resetDefaultPrefs();
  };
  document.getElementById("yellowIcon").checked = a.yellowIcon;
  document.getElementById("greenIcon").checked = a.greenIcon;
  document.getElementById("purpleIcon").checked = a.purpleIcon;
  document.getElementById("redIcon").checked = a.redIcon;
  document.getElementById("beigeIcon").checked = a.beigeIcon;
  document.getElementById("defaultIcon").checked = a.defaultIcon;
  document.getElementById("ownIcon").checked = a.ownIcon;
  a.yellowIcon || a.greenIcon || a.blueIcon || a.redIcon || a.beigeIcon || a.purpleIcon || a.defaultIcon || a.ownIcon || (document.getElementById("defaultIcon").checked = !0);
  document.getElementById("yellowIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("greenIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("purpleIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("redIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("beigeIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("defaultIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("ownIcon").onclick = function() {
    saveSettings();
  };
  document.getElementById("errorMessage").innerHTML = "";
  if (null != a.storedCanvas) {
    var b = new Image;
    b.onload = function() {
      var e = document.createElement("canvas");
      e.width = b.width;
      e.height = b.height;
      var d = e.getContext("2d");
      d.drawImage(b, 0, 0);
      d = d.getImageData(0, 0, 19, 19);
      if (19 < b.width || 19 < b.width) {
        document.getElementById("errorMessage").innerHTML = "Image is " + b.width + "x" + b.height + " pixels. Only the top/left 19x19 pixels are used!";
      }
      a.ownIcon && chrome.browserAction.setIcon({imageData:d});
      ownBitmap = d;
      storedCanvas = e;
    };
    b.setAttribute("src", a.storedCanvas);
    document.getElementById("destination").appendChild(b);
  }
  document.getElementById("upload-file").addEventListener("change", function() {
    var a = document.getElementById("destination");
    a.innerHTML = "";
    var b = this.files[0];
    if (-1 != b.type.indexOf("image")) {
      var f = new FileReader;
      f.onload = function(b) {
        var c = new Image;
        c.onload = function() {
          var a = document.createElement("canvas");
          a.width = c.width;
          a.height = c.height;
          var b = a.getContext("2d");
          b.drawImage(c, 0, 0);
          b = b.getImageData(0, 0, 19, 19);
          document.getElementById("errorMessage").innerHTML = "";
          if (19 < c.width || 19 < c.width) {
            document.getElementById("errorMessage").innerHTML = "Image is " + c.width + "x" + c.height + " pixels. Only the top/left 19x19 pixels are used!";
          }
          ownBitmap = b;
          storedCanvas = a;
          saveSettings();
        };
        c.src = b.target.result;
        a.appendChild(c);
      };
      f.readAsDataURL(b);
      ownIconSelected = document.getElementById("ownIcon").checked = !0;
    } else {
      a.innerHTML = "Wrong File...", document.getElementById("errorMessage").innerHTML = "";
    }
  });
};