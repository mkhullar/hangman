# Hangman
[![Play Hangman](https://cdn4.iconfinder.com/data/icons/trap/500/Trap_15-128.png)](http://18.219.29.191/logon)

## Rules
Hangman is a word guessing game.
* When the game is started, the player is represented with an empty field for
  each letter in the word.
* When the player guesses a letter correctly, each field that represents that
  letter is filled with the letter.
* When the player guesses a letter incorrectly, a piece of a gallow with a
  hanging man is drawn.
* After 10 incorrect guesses, the game is over and the player lost. Thus,
  there should be 10 different states of the gallow to be drawn.
* If all fields are filled with their letter before 10 incorrect guesses, the
  player has won the game.

## Technical 
* Server/client based with the client being the browser
* Business logic executed on the server (so nobody can cheat)
* Allow for keeping simple statistics (games won/lost)
* Game is self-contained
* Game must scale to millions of users (discussion)
* Game State is maintained for the next time a user logs in.
