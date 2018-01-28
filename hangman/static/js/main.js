var used = [];

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
    });
}

function lost() {
    alert("You Lost the game let's play again");
    $.ajax('/lost').done(function(data) {
        $('#lost').text((parseInt($('#lost').text())+1).toString());
        start();
    });
}

