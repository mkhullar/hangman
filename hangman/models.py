from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    word = db.Column(db.String(), primary_key=True)

    def __init__(self, word):
        self.word = word


class Stats(db.Model):
    __tablename__ = 'stats'
    user = db.Column(db.String(), nullable=False)
    attempt = db.Column(db.String(), nullable=False)
    word = db.Column(db.String(), nullable=False)
    attempt_left = db.Column(db.Integer(), nullable=False)
    win = db.Column(db.String(), nullable=False)
    timestamp_ms = db.Column(db.BigInteger(), index=True, primary_key=True)

    def __init__(self, user, attempt, word, attempt_left, win, timestamp_ms):
        self.user = user
        self.attempt = attempt
        self.word = word
        self.attempt_left = attempt_left
        self.win = win
        self.timestamp_ms = timestamp_ms
