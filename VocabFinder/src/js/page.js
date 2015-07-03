$(document).on('change', '.btn-file :file', function() {
  var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$(document).ready( function() {
  $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
    var input = $(this).parents('.input-group').find(':text');
    if(input.length) {
        input.val(label);
    }
  });

  var isValid = false;
  var clicked = false;

  var validate = function() {
    var isValid = true;
    var $numInput = $('#numInput');
    var $urlInput = $('#urlInput');
    var $fileInput = $('input[readonly]');
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
});