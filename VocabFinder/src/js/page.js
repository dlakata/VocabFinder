$(document).ready( function() {

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

  $('#saved-message').text("These are all the vocab lists you've made while logged in.");

  var saveMessage = function() {
    $('#saved-message').text('Your changes were saved!');
    setTimeout(function(){
      $('#saved-message').text("These are all the vocab lists you've made while logged in.");
    }, 2000);
  }

  $('[type="checkbox"]').on('click', function() {
    var _this = $(this);
    $.getJSON('/change_visibility', {
      id: _this.data('vocab-id')
    });
    saveMessage();
  });

  $('.close').on('click', function() {
    var _this = $(this);
    $.getJSON('/delete_vocab_set', {
      id: _this.data('vocab-id')
    });
    _this.parent().parent().remove();
    if ($('.close').length === 0) {
      location.reload();
    }
    saveMessage();
  });

  $('.difficulty-level').on('change', function() {
    var _this = $(this);
    $.getJSON('/change_difficulty', {
      id: _this.data('vocab-id'),
      difficulty: _this.val()
    });
    saveMessage();
  });

  $('.num-words').on('change', function() {
    var _this = $(this);
    $.getJSON('/change_num_words', {
      id: _this.data('vocab-id'),
      num_words: _this.val()
    });
    saveMessage();
  });
});