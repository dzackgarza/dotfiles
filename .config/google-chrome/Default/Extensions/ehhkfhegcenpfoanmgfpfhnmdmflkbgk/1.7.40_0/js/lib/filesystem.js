// TODO: switch to Chrome API + FileSync
// https://developer.chrome.com/apps/app_storage

function handle_file_select(e, callback) {
  var file = e.target.files[0]; // FileList object

 // Only process image files.
  if (!file.type.match('image.*')) {
    alert("Error: Only image files are allowed for background!")
    return;
  }

  var reader = new FileReader();

  // Closure to capture the file information.
  reader.onload =  function(e) {
    callback && callback(file.name, e.target.result);
  };

  // Read in the image file as a data URL.
  reader.readAsDataURL(file);
}

//byId('files').addEventListener('change', handle_file_select, false);


function toArray(list) {
  return Array.prototype.slice.call(list || [], 0);
}

function extract_extension(filename) {
  return filename.split(".").pop();
}

function extract_filename(path) {
  return path.split('/').pop().split('?')[0];
}

function dataURItoBlob(dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
    var array = []
    for(var i = 0; i < byteString.length; i++) {
        array.push(byteString.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: mimeString});
}

function read_file(file, callback) {
  var reader = new FileReader();
  reader.onload = function (event) {
    callback(event.target.result);
  };
  reader.readAsDataURL(file);
}

function save_file(filename, dataURI, callback) {
  save_file_blob(filename, dataURItoBlob(dataURI), callback);
}

function save_file_blob(filename, blob, callback) {
  fs.root.getFile(filename, {create: true}, function(fileEntry) {
    fileEntry.createWriter(function(fileWriter) {
      fileWriter.onwriteend = function(e) {
        callback && callback(fileEntry.toURL());
      };
      fileWriter.write(blob);
    }, error_handler);
  }, error_handler);
}

function remove_file(filename, callback) {
  fs.root.getFile(filename, {create: false}, function(fileEntry) {
    fileEntry.remove(function() {
      callback && callback();
    }, error_handler);
  }, error_handler);
}

var list_files = function(callback) {
  var entries = [];
  var reader = fs.root.createReader();
  function read_entries() {
    reader.readEntries(function (results) {
      if (!results.length) {
        callback(entries.sort());
      } else {
        entries = entries.concat(toArray(results));
        read_entries();
      }
    }, error_handler);
  }
  read_entries();
}

function error_handler(e) {
  console.log(e);
}

function imageURLToBlob(source, callback) {
  var oReq = new XMLHttpRequest();
  oReq.open("GET", source, true);
  oReq.responseType = "blob";
  oReq.onload = function(oEvent) {
    callback && callback(oReq.response);
  };
  oReq.send();
}


/*
window.onload = function () {
  //imageURLToBlob('/img/backgrounds/01.jpg');
  imageURLToBlob('/img/bg.png');
}
*/

/*
var error_handler = (function () {
  /*var codes = ['Unknown Error'];
  for (var err_msg in FileError) {
    var err_code = FileError[err_msg];
    if ('number' == typeof err_code && 
        err_msg.indexOf('ERR') > -1) {
      codes[err_code] = err_msg;
    }
  }
  return function (e) {
    console.log(codes[e.code||0]);
  }
})();
*/

// init PERSISTENT file system
var fs;
function on_init_file_system(filesystem) { fs = filesystem; }
window.requestFileSystem || (window.requestFileSystem = window.webkitRequestFileSystem);
window.requestFileSystem(window.PERSISTENT, 50*1024*1024, on_init_file_system, error_handler);

// size of the ext: URL.revokeObjectURL?
