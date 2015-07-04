$(document).ready( function() {

  var isValid = false;
  var clicked = false;

  var validate = function() {
    var isValid = true;
    var $numInput = $('#numInput');
    var $urlInput = $('#urlInput');
    var $fileInput = $('input[type="file"]');
    var $textInput = $('#textInput');
    if (!$numInput.val()) {
      $numInput.parent().addClass('has-error');
      isValid = false;
      return isValid;
    } else {
      $numInput.parent().removeClass('has-error');
    }

    if (!$urlInput.val()) {
      $urlInput.parent().addClass('has-error');
      isValid = false;
    } else {
      $urlInput.parent().removeClass('has-error');
      isValid = true;
      return isValid;
    }

    if (!$fileInput.val()) {
      $fileInput.parent().addClass('has-error');
      isValid = false;
    } else {
      $fileInput.parent().removeClass('has-error');
      isValid = true;
      return isValid;
    }

    if (!$textInput.val()) {
      $textInput.parent().addClass('has-error');
      isValid = false;
    } else {
      $textInput.parent().removeClass('has-error');
      isValid = true;
      return isValid;
    }

    return isValid;
  }

  $('input').on('change', function() {
    if (clicked) {
      isValid = validate();
    }
  });

  $('#analyze').on('click', function(e) {
    clicked = true;
    isValid = validate();
    if (!isValid) {
      e.preventDefault();
    }
  });

  $('.word_row').on('click', function() {
    var _this = $(this);
    var $context_row = _this.next();
    var $context = $context_row.find('.context');
    if ($context_row.is(':visible')) {
      $context_row.hide('fast');
    } else {
      $context_row.show('fast');
    }
    if ($context.text() === '') {
      $context.html('<b>Context: </b>Looking...');
      $.getJSON('/get_context', {
          word: _this.find('.word').text()
      }, function(data) {
        var text = $context.html().replace('Looking...', data.result);
        $context.html(text);
      });
    }
  });
});