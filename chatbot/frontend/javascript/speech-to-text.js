 $(document).ready(function(){
  if (!('webkitSpeechRecognition' in window)) {
    upgrade();
  } else {

    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    speaking = true;

    recognition.onstart = function() {
      console.log('INFO: Voice module started!')
    };

    recognition.onerror = function(event) {
      alert('Error')
    };

    recognition.onend = function() {
      console.log('INFO: Voice module stopped!')
    };

    recognition.onresult = function(event) {
      $('.question-here').text(event.results[0][0].transcript);
      if(event.results[0].isFinal){
        $('.question-here').text(event.results[0][0].transcript);
        $('.mic-stop').click();
      }
    };
  }

  $('.mic-trigger').on('click', function(e){      
    recognition.start();
  });

  $('.mic-stop').on('click', function(e){
    recognition.stop();
    $('#question').val($('.question-here').text());
    $('.question-here').text('');
    $('.bot-form').submit();
  });
});