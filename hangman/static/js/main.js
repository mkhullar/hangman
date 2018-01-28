var used = [];
var canvas = $('#hangman-playground');
var context = canvas[0].getContext("2d");


function init_hangman() {
    var done = parseInt($('#attempts').text());
    for(var i = 9;i >=done; i--){
        draw_hanging_man(i);
    }
}

window.onload = init_hangman;

function checkWord() {

    var val = $('#guess').val();
    if(used.includes(val)){
        $('#guess').val('');
        alert("Alphabet Already Used");
        return;
    }
    if($('#word').val()== ''){
        start();
        return
    }
    used.push(val);
    var filter =  'w='+val+'&attempt_left='+parseInt($('#attempts').text());
    $.ajax('/checkWord?'+filter).done(function(data) {
        $('#guess').val('');
        $('#word').val(data['word']);
        if(data['result'] === 'Won'){
            alert("Congratulations!! You Won the Game let's play again");
            $('#won').text((parseInt($('#won').text())+1).toString());
            start();
            return
        }

        if(data['result'] === 'Incorrect'){
            //draw_hangman();
            $('#attempts').text(data['attempt_left'].toString());
        }
        draw_hanging_man(parseInt($('#attempts').text()));

        if($('#attempts').text() === '0'){
            lost();
            }

    });

}

function start() {
    used = [];
    $('#attempts').text('10');
     $.ajax('/start').done(function(data) {
        $('#guess').val('');
        $('#word').val(data['word']);
        canvas = $('#hangman-playground');
        context = canvas[0].getContext('2d');
        context.clearRect(0, 0, canvas[0].width, canvas[0].height);
    });
}

function lost() {
    alert("You Lost the game let's play again");
    $.ajax('/lost').done(function(data) {
        $('#lost').text((parseInt($('#lost').text())+1).toString());
        start();
    });
}


function draw_hanging_man(attempt_left){
    if(attempt_left === 9){
      context.beginPath();
      context.lineWidth = 7;
      context.moveTo(0, 250);
      context.lineTo(100, 250);
      context.strokeStyle = '#000000';
      context.stroke();
    } else if (attempt_left === 8){
      context.beginPath();
      context.lineWidth = 7;
      context.moveTo(50, 250);
      context.lineTo(50,25);
      context.stroke();
    } else if (attempt_left === 7){
      context.beginPath();
      context.lineWidth = 7;
      context.moveTo(50, 25);
      context.lineTo(200,25);
      context.stroke();
    } else if(attempt_left === 6){
      context.beginPath();
      context.lineWidth = 7;
      context.moveTo(200, 25);
      context.lineTo(200,50);
      context.stroke();
    } else if(attempt_left === 5){
      context.beginPath();
      context.lineWidth = 7;
      context.arc(200, 75, 25, 2 * Math.PI, 0);
      context.stroke();
   } else if(attempt_left === 4){
      context.beginPath();
     context.lineWidth = 7;
      context.moveTo(200,100);
      context.lineTo(200,150);
      context.stroke();
   } else if(attempt_left === 3){
      context.beginPath();
     context.lineWidth = 7;
      context.moveTo(200,150);
      context.lineTo(150,200);
      context.stroke();
   } else if(attempt_left === 2){
      context.beginPath();
     context.lineWidth = 7;
      context.moveTo(200,150);
      context.lineTo(250,200);
      context.stroke();
   } else if(attempt_left === 1){
      context.beginPath();
     context.lineWidth = 7;
      context.moveTo(200,125);
      context.lineTo(250,175);
      context.stroke();
   } else if(attempt_left === 0){
      context.beginPath();
      context.lineWidth = 7;
      context.moveTo(200,125);
      context.lineTo(150,175);
      context.stroke();
   }
  }