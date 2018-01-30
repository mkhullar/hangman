from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, session
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from hangman.extensions import cache
from hangman.forms import LoginForm, LogonForm
from hangman.models import db, User, Dictionary, Stats
import time

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return redirect(url_for(".login"))


@main.route("/logon", methods=["GET", "POST"])
def logon():
    form = LogonForm()
    if form.validate_on_submit():
        return redirect(request.args.get("next") or url_for(".login"))
    return render_template("logon.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    """ Login the user and set the session variable of username """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)
        session['username'] = form.username.data
        flash("Hi, " + form.username.data + " Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".hangman"))
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    """ Logout of the application and remove the session data """
    logout_user()
    if is_logged_in():
        session.pop('username')
    flash("You have been logged out.", "success")
    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200


@main.route('/hangman', methods=["GET", "POST"])
@login_required
def hangman():
    """ If a user comes back after a while return the state to the previous state """
    games = Stats.query.filter_by(user=session['username']).all()
    guess = '_*_*_*_*_'
    win = 0
    loss = 0
    attempt_left = 10
    for game in games:
        if game.win == 'Game On':
            guess = game.attempt
            attempt_left = game.attempt_left
        if game.win == 'Won':
            win += 1
        if game.win == 'Lost':
            loss += 1
    return render_template("index.html", attempt=guess, won=win, lost=loss, attempt_left=attempt_left)


@main.route('/start', methods=["GET", "POST"])
@login_required
def start():
    """ check if the user is logged in """
    if not is_logged_in():
        return redirect(url_for(".login"))
    else:
        """ Mark previous game as Incomplete and start a new Game """
        finish_games()
        full_word = get_random()
        attempt_word = ''.join(['_ '] * len(full_word[0].word)).strip().replace(' ', '*')
        db.session.add(Stats(session['username'], attempt_word, full_word[0].word, 10, 'Game On', time.time()))
        db.session.commit()
        return jsonify(word=attempt_word)


@main.route('/checkWord', methods=["GET", "POST"])
@login_required
def check_word():
    """ check for the character if it is present in the original word """
    character = request.args.get('w').upper()
    attempt_left = request.args.get('attempt_left').upper()
    games = Stats.query.filter_by(user=session['username']).filter_by(win='Game On').all()
    if len(games) > 0:
        game = games[0]
        guess_word = game.attempt.strip().split('*')
        result = 'Incorrect'
        for index in [i for i, ch in enumerate(game.word) if ch == character]:
            guess_word[index] = character
            result = 'Correct'

        db.session.query(Stats).filter_by(user=session['username']). \
            filter_by(win='Game On').update({'attempt': '*'.join(guess_word)})
        db.session.commit()

        if '_' not in guess_word:
            db.session.query(Stats).filter_by(user=session['username']). \
                filter_by(win='Game On').update({'win': 'Won'})
            db.session.commit()
            return jsonify(word=' '.join(guess_word), result='Won')

        if result == 'Incorrect':
            db.session.query(Stats).filter_by(user=session['username']). \
                filter_by(win='Game On').update({'attempt_left': int(attempt_left) - 1})
            db.session.commit()
            attempt_left = str(int(attempt_left) - 1)
        return jsonify(word=' '.join(guess_word), result=result, attempt_left=attempt_left)
    return redirect(request.args.get("next") or url_for(".start"))


@main.route('/lost', methods=["GET", "POST"])
@login_required
def lost():
    """ Mark the current game as lost """
    db.session.query(Stats).filter_by(user=session['username']). \
        filter_by(win='Game On').update({'win': 'Lost'})
    db.session.commit()
    return jsonify(restart=True)


@main.route('/stats', methods=["GET", "POST"])
@login_required
def stats():
    """ Get the detailed Statistics about win, lose and incomplete games """
    games = Stats.query.filter_by(user=session['username']).all()
    game_list = list()
    for game in games:
        if game.win == "Game On":
            continue
        game_list.append({"user": game.user, "attempt": game.attempt.strip(), "word": game.word, "win": game.win})
    return render_template("stats.html", games=game_list)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_random():
    """ Get a random word from the database of dictionary """
    return Dictionary.query.options(load_only('word')).offset(
        func.floor(
            func.random() *
            db.session.query(func.count(Dictionary.word))
        )
    ).limit(1).all()


def is_logged_in():
    """ check if the user is logged in """
    return 'username' in session


def finish_games():
    """ Mark the previous game as Incomplete to start a new game """
    db.session.query(Stats).filter_by(user=session['username']). \
        filter_by(win='Game On').update({'win': 'Incomplete'})
    db.session.commit()
