
function cropboxify(imageURL, options, onSuccess, onError) {

  var image = $( '.cropimage' ),
      results = image.next('.results' ),
      download = $('.download').find('a');

  var cropbox = $('.cropimage').data('cropbox');
  cropbox && cropbox.remove();

  var first = true;
  var cropimage, borderRadius = 0;

  removeListeners();
  $('.cropimage' ).on('load', initcrobox);
  $('.cropimage' ).on('error', onErrorInternal);
  $('.cropimage' ).prop('src', imageURL);   

  function initcrobox() {
    options.showControls = 'never';
    $('input[type=range]').attr('disabled', false);
    image
      .cropbox(options, null)
      .on('cropbox', function( event, results, img ) {
        if (first) {
          $('#zoom').attr('min', img.minPercent);
          $('#zoom').val(img.percent);
          if (img.minPercent == 1) {
            $('#zoom').attr('disabled', true);
          }
          update();
          first = false;
        }

        //download.attr('href', img.getDataURL());
        //$('.preview').prop('src', img.getDataURL())
      });
      removeListeners();
      onSuccess && onSuccess();
  }

  $('#zoom').on('input', function () {
    var cropbox = $('.cropimage').data('cropbox');
    cropbox && cropbox.zoom(this.value)
    $('#zoomText').val(this.value*100 >> 0);
    update();
  });
  $('#roundedCorner').on('input', function () {
    borderRadius = this.value;
    update();
  });

  function update() {
    window.requestAnimationFrame(function () {
      var cropimage = $('.cropimage').data('cropbox');
      cropimage && cropimage.update();
      $('#imgWrapper').css('border-radius', borderRadius + 'px');
    });
  }

  function onErrorInternal() {
    removeListeners();
    onError && onError();
  }
  function removeListeners() {
    $('.cropimage' ).off('load');
    $('.cropimage' ).off('error');
  }
}

