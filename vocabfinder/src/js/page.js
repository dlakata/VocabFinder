$(document).ready( function() {

  $('.word_row').on('click', function() {
    var _this = $(this);
    var word = _this.find('.word').text();
    $('.modal-title').text(word);

    var $context = $('#context');
    $context.html('<b>Context: </b>Looking...');
    $.getJSON('/get_context', {
        word: word
    }, function(data) {
      var text = $context.html().replace('Looking...', data.result);
      $context.html(text);
    });

    var $definition = $('#definition');
    $.getJSON('/get_definitions', {
      word : word
    }, function(data) {
      var text = '<br>';
      $(data).each(function(i, def) {
        var num = parseInt(i, 10) + 1;
        text += '<b>'+ num + '</b> ' + $(def).prop('text') + '<br>';
      });
      if (text !== '') {
        $definition.html('<b>Definitions:</b> ' + text);
      }
    });

    var $etymology = $('#etymology');
    $.getJSON('/get_etymology', {
      word: word
    }, function(data) {
      var text = $($.parseXML(data[0])).text();
      if (text !== '') {
        $etymology.html('<b>Etymology:</b> ' + text);
      }
    });

    var $pronunciation = $('#pronunciation');
    $.getJSON('/get_pronunciation', {
      word: word
    }, function(data) {
      var text = $(data).first().prop('fileUrl');
      if (text !== '') {
        $pronunciation.html('<b>Pronunciation:</b> ' + '<a href="' + text + '">Audio</a>');
      }
    });
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