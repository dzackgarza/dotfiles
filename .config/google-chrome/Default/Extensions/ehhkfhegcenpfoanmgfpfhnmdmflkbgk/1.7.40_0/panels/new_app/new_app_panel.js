
var blankSrc = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
//var url = 'nemzetisport.hu'
//var url = 'github.com'
//var url = 'yahoo.com'

// TODO: remove images when removing the app

//processSite(url);
$('input[type=range]').prop('disabled', true);

window.onfocus = function (e) { 
  if (e.target == window)
    $('#url').focus(); 
}

$('#url').change(searchForIcon);
$('#url').on('input', onInput);
$('#imageURL').change(onImageURLChange);
$('#user-app-submit').on('click', saveApp);
$(document).change(clearInvalids);
$('input').on('focus', clearInvalids);

function clearInvalids() {
  $('.invalid').removeClass('invalid');
}

var bg = chrome.extension.getBackgroundPage();

var currentApp = {}; // isn't the same as background page {App} objects
var currentIconFileName; // 
//var currentIconBorderRadius;
var appBeforeEdits; // used in editing mode only

function saveApp() {
  var name = $('#name').val().trim();
  var cropbox = $('.cropimage').data('cropbox');

  if (!cropbox)        return $('#imgWrapper').addClass('invalid');
  if (!name)           return $('#name').addClass('invalid');
  if (!currentApp.url) return $('#url').addClass('invalid');

  (appBeforeEdits) ? saveEditedApp(name, cropbox) : saveNewApp(name, cropbox);
}

function saveNewApp(name, cropbox) {
  saveAppIcon(cropbox, function (savedFilename) { 
    var icons = [{ size: 128, url: savedFilename }];
    var borderRadiusPx = $('#imgWrapper').css('border-radius');
    icons[0].borderRadius = parseInt(borderRadiusPx, 10) || (void 0);
    bg.add_user_app(name, currentApp.url, icons);
  });
}

function saveEditedApp(name, cropbox) {
  function finishSaving(iconURL) {
    var icons = [{ size: 128, url: iconURL }];
    var borderRadiusPx = $('#imgWrapper').css('border-radius');
    icons[0].borderRadius = parseInt(borderRadiusPx, 10) || (void 0);
    bg.edit_user_app(appBeforeEdits.id, name, currentApp.url, icons);
  }
  var newImage = $('#imageURL').val() || $('#imageFile').val();
  if (newImage != appBeforeEdits.icons[0].url)
    saveAppIcon(cropbox, finishSaving);
  else 
    finishSaving(appBeforeEdits.icons[0].url);
}

function saveAppIcon(cropbox, callback) {
  var dataURI = cropbox.getDataURL();
  window.currentIconFileName = window.currentIconFileName.split('.').slice(0, -1) + '.png';
  window.currentIconFileName = randomToken() + '_' + window.currentIconFileName;
  save_file(window.currentIconFileName, dataURI, callback);
}

window.addEventListener('message', function (event) {
  if ('startEditingApp' == event.data.name) {
    startEditingApp(event.data.app);
  }
});

function startEditingApp(app) {
  appBeforeEdits = Object.assign({}, app);
  currentApp.url = app.appLaunchUrl;
  document.body.classList.add('page-edit-app');
  $('#name').val(app.name);
  $('#url').val(app.appLaunchUrl);
  if (app.icons[0]) {
    $('#imageURL').val(app.icons[0].url);
    downloadAndApplyImageWithURL(app.icons[0].url, function () {
      $('#roundedCorner').val(app.icons[0].borderRadius||0);
      $('#roundedCorner').trigger('input');
    });
  }
  $('input[type=range]').prop('disabled', false);
  //$('#url').off('change', searchForIcon);
}

function searchForIcon() {
  //$('input[type=range]').attr('disabled', true);
  var url = $('#url').val().trim();
  if (!url) return;
  if (url.indexOf('.') == -1 && url.indexOf('localhost') == -1) return;

  if (!/^https?:/i.test(url)) url = "http://" + url; 

  currentApp.url = url;

  if (appBeforeEdits) return; // editing mode
  
  processSite(url, function (img) { });
}

var searchInputTimer;
function onInput() {
  //if (iconSiteRequest) iconSiteRequest.abort();
  //iconSiteRequest = null;
  //clearTimeout(searchInputTimer);
  //searchInputTimer = setTimeout(searchForIcon, 2000);
}

var iconSiteRequest;

// buzzfeed error
function processSite(url, callback) {

  var originalURL = url;
  window.currentRequestURL = url;
  
  startLoadingIndicator();

  //if (iconSiteRequest) iconSiteRequest.abort();

  
  /*iconSiteRequest = ajax({
    url: url,
    beforeSend: function () {  }, // loader.show();
    success: onSuccess,
    error: onError
  });*/

  iconSiteRequest = ajax(url, onSuccess, onError, onProgress);

  function onSuccess(result, requestURL) {
    if (requestURL != window.currentRequestURL) return;
    currentApp.url = requestURL; // after redirects: result.responseURL; 
    var parser = new DOMParser();
    var doc = parser.parseFromString(result.responseText, "text/html");
    processSiteName(doc);
    processImage(doc, originFromURL(result.responseURL), callback);
    // try/catch
  }

  function onError(result, requestURL) {
    // AJAX ashould automatically  follow redirects, but just in case
    if (requestURL != window.currentRequestURL) return; // originalURL?
    if (requestURL.indexOf('www') == -1) {
      console.log('trying www');
      var parts = requestURL.split('://');
      var wwwurl = parts[0] + '://www.' + parts[1]; 
      window.currentRequestURL = wwwurl;
      iconSiteRequest = ajax(wwwurl, onSuccess, onError, onProgress);
    } else {
      //debugger;
      // TODO: error message
      onIconError();
    }
  }

  // only for images though
  function onProgress(e) {
  var percent = (e.loaded / e.total) * 100;  
    $('#icon-progress').css('width', percent + '%');
  }
}

function onIconError() {
  removeImage();
  $('.cropimage').prop('src', 'about:blank'); // blankSrc
  stopLoadingIndicator();
}

function removeImage() {
  $('#imageURL').val('');
  $('#imgWrapper').removeClass('loading');
  $('#loadingSite').fadeOut(300);
  $('.cropimage').css('opacity', 1);
  $('.cropimage').off('load');
  $('.cropimage').off('error');
  $('.cropimage').prop('src', blankSrc); // blankSrc
}


function processImage(doc, baseURL, callback) {
    /*
    var color, colorResults = getMetaTags(doc, msColorTags);
    if (colorResults.length) {
        color = colorResults[0];
    }
    */
    $('#imageFile').val('');

    //var imgs = getMetaTags(doc, msImageTags);
    var imageURLs = getFavicons(doc);

    imageURLs = imageURLs.map(function (imageURL) {
      return absoluteURL(imageURL, baseURL);
    });

    if (!imageURLs.length) {
      onIconError();
      return;
    }

    downloadAndApplyFirstGoodImageFromURLs(imageURLs);
}

function onImageURLChange() {
  downloadAndApplyImageWithURL($('#imageURL').val());
}

function downloadAndApplyImageWithURL(imageURL, callback) {
  downloadAndApplyFirstGoodImageFromURLs([imageURL], callback);
}

function downloadAndApplyFirstGoodImageFromURLs(imageURLs, callback) {

    (function cropboxifyWithFailover(imageURLs) {
      var imageURL = imageURLs[0];
      var options = { width: 128, height: 128, maxZoom:2 };
      cropboxify(imageURL, options, function onSuccess() {
        cropboxifySuccess(imageURL);
      }, function onError() {
        var remainingURLs = imageURLs.slice(1);
        if (remainingURLs.length) 
          cropboxifyWithFailover(remainingURLs);
        else
          onIconError();
      });
    })(imageURLs);

    function cropboxifySuccess(imageURL) {

      window.currentIconFileName = extract_filename(imageURL);
      if (!window.currentIconFileName || 
          window.currentIconFileName.indexOf('.') == -1) {
        window.currentIconFileName = randomToken() + '.png';
      }

      stopLoadingIndicator();

      $("#imageURL").val(imageURL);

      var link = $('<a>').prop('href', imageURL).text(imageURL);
      $('#new-app-debug').append(link).append('<br>');

      callback && callback();

      var img = document.createElement("img");
      img.onload = function () {
          $('body').append(img);
          cb2 && cb2(img);
          /*resizeImage(img, function (resizedImage) {
              var imageEl = $('<img>').prop('src', resizedImage.src);
              ///$('body').append(imageEl);

              //setTileImagem(data, color);
              carregouImagem = true;
          });*/
      };    
      //img.src = imageURL;

    }

}

function startLoadingIndicator() {
  $('#imgWrapper').addClass('loading');
  $('#loadingSite').fadeIn(300);
  $('.cropimage').on('load', null);
  $('.cropimage').css('opacity', 0.4);
}

function stopLoadingIndicator() {
  $('#imgWrapper').removeClass('loading');
  $('#loadingSite').fadeOut(300);
  $('.cropimage').css('opacity', 1);
}

function absoluteURL(url, baseURL) {
  if (/^https?:/i.test(url)) return url;
  url = url.replace(/^[\/]*/, ''); // started with / or //
  baseURL = baseURL.replace(/[\/]$/, '');
  return baseURL + '/' + url;
}


function originFromURL(url) {
  originFromURL.dummy.href = url;
  return originFromURL.dummy.origin;
}

originFromURL.dummy = document.createElement('a');


// last icon?
// sizes: any | 50x50 | 25x25,120x120 (any is svg)
// case sensitivity!
//  rel="apple-touch-icon-precomposed" media="(resolution: 326dpi)"  
// <link rel="logo" type="image/svg" href="https://f.vimeocdn.com/logo.svg">
// <link rel="icon" sizes="any" mask href="//instagramstatic-a.akamaihd.net/bluebar/ae189c4/images/ico/favicon.svg">
var titleAttributeValues  = ['name', 'og:title', 'og:site_name', 'application-name']; 
// og vs apple-touch-icon
var imageAttributeValues = ['fluid-icon', 'apple-touch-icon-precomposed', 'apple-touch-icon',
                            'og:image', 'image', 'image_src', 'icon', 'shortcut icon'];
var msImageAttributeValues = ['msapplication-tileimage']; 
var colorAttributeValues = ['msapplication-tilecolor', 'msapplication-navbutton-color',
                            'theme-color'];


function getMetaTags(doc, values) {
    //  http-equiv or name -> content
    var elems = doc.querySelectorAll('meta,link');
    var attrKeys = ['rel', 'property', 'type', 'name', 'http-equiv', 'itemprop'];
    var valuesLookup = arrayToLookup(values, 1); // {rel:1, property:1, ...} 
    var returnObject = {}; // {rel:['', ''], property:[''], ...} 
    [].forEach.call(elems, function (el) { 
        for (var i = 0; i < attrKeys.length; i++) {
            var attrKey   = attrKeys[i]; // rel
            var attrValue = (el.getAttribute(attrKey)||'').toLowerCase(); // icon
            if (!valuesLookup[attrValue]) 
                continue;
            var item = { 
                attribute: attrValue,
                content:  el.getAttribute('content') || el.getAttribute('href'),
                sizes: el.sizes,
                type:  el.type
            };
            //if (!el.getAttribute('href') && el.href) debugger;
            //if (!el.getAttribute('content') && el.content) debugger;
            returnObject[attrValue] = returnObject[attrValue] || [];
            returnObject[attrValue].push(item);
            break;
        }
    });
    return returnObject; // { 'icon' => [{}, {}, ...], 'shortcut icon' => ... }
}

function getFavicons(doc) {
    var valuesHash = getMetaTags(doc, imageAttributeValues);
    var iconsOrdered = [];
    for (var i = 0; i < imageAttributeValues.length; i++) {
        var attrValue = imageAttributeValues[i];
        var item = valuesHash[attrValue];
        if (!item || !item.length) 
            continue;
        else if (item[0].sizes)
            iconsOrdered.push(getBiggestIcon(item).content);
        else
            iconsOrdered.push(item[0].content);
    }
    return iconsOrdered;
}

function getBiggestIcon(items) {
    items.sort(sortImagesBySize);
    return items[0];
}

// image_src && og:image better on IMDB, buzzfeed it's TOO big
// Paypal.com
// cinemacity: vertical align center
// e.g.: instagram.com
// stackoverflow -> FREEZE!
// og bigger: foxnews.com
var testItems = [ {id:4, sizes:['any']}, {id:2, sizes:['500x1000']}, 
       {id:3, sizes:['1x1000']}, {id:1, sizes:['1000x1000']} ];

function sortImagesBySize(a, b) {
   if (a.sizes[0] == 'any' || !a.sizes[0]) // counts as smallest
       return 1;
   if (b.sizes[0] == 'any' || !b.sizes[0]) // counts as smallest
       return -1;
   var aParts = a.sizes[0].split('x');
   var bParts = b.sizes[0].split('x');
   return bParts[0]*bParts[1] - aParts[0]*aParts[1];
}

function processSiteName(doc) {
  var newSiteName = getSiteName(doc) || '';
  var currentValue = $('#name').val().trim();
  if (newSiteName && !currentValue)
    $('#name').val(newSiteName);
}

function getSiteName(doc) {
  var tags = getMetaTags(doc, titleAttributeValues);
  if (!tags.length) return;
  var names = Object.keys(tags).map(function (tag) {
    return tags[tag][0].content;
  });
  names.sort(function (a, b) {
    a.length - b.length
  });
  return names[0];
}

// svg + color, twitter.com
function getSiteColor(doc) {
}

function arrayToLookup(arr, val) {
    if ('undefined' == typeof val) 
        val = 1;
    var hash = {};
    arr.forEach(function (key) {
        hash[key] = val;
    });
    return hash;
}


//
// Upload local file
//

// save on every change
function on_change(e) {
  // background image settings
  if (e.target.type && e.target.type == "file") {
    handle_file_select(e, function (filename, dataURI) {
      window.currentIconFileName = filename;
      var options = { width: 128, height: 128 };
      cropboxify(dataURI, options, function onSuccess() {
        $("#imageURL").val('');
      }, onIconError);
    });
  }
}

document.addEventListener("change", on_change, true);


//
// Helpers
//

function ajax(url, onSuccess, onError, onProgress) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    //console.log('' + xmlhttp.readyState + ' - ' + xmlhttp.status + ' - ' + url);
    if (XMLHttpRequest.DONE == xmlhttp.readyState) {
      xmlhttp.onreadystatechange = null;
      if (xmlhttp.status == 200)
        onSuccess(xmlhttp, url);
      else 
        onError(xmlhttp, url);
    }
  }
  xmlhttp.onprogress = onProgress;
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
  return xmlhttp;
}

function randomToken() {
  return Math.random().toString(36).substr(2) + 
         Math.random().toString(36).substr(2);
}

//
// Resize Image
//

function resizeImage(img, callback) {
    var canvas = document.createElement("canvas");
 
    var MAX_WIDTH  = 128;
    var MAX_HEIGHT = 128;
    var width = img.width;
    var height = img.height;

    if (width > height) {
        if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
        }
    } else {
        if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
        }
    }

    canvas.width = width;
    canvas.height = height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, width, height);

    var imgProcessada = new Image();

    imgProcessada.onload = function () {
        callback(imgProcessada, img);
    }

    imgProcessada.src = canvas.toDataURL("image/png");
}






