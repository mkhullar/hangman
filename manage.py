#!/usr/bin/env python

import os

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean
from hangman import create_app
from hangman.models import db, User
import pandas as pd

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('HANGMAN_ENV', 'dev')
app = create_app('hangman.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """
    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """
    db.create_all()
    db.session.add(User('admin', 'hangman'))
    db.session.commit()
    conn = db.session.connection().connection
    cur = conn.cursor()
    df1 = pd.read_csv('dictionary.csv')
    word_list = df1['Word'].tolist()
    final_words = list()
    for index in range(len(word_list)):
        if pd.isnull(word_list[index]):
            continue
        if len(word_list[index]) == 5 or len(word_list[index]) == 6:
            final_words.append(word_list[index])
    del word_list
    df = pd.DataFrame(final_words)
    df.to_csv('dictionary1.csv', index=False)

    dictionary_sql = """
                   COPY dictionary FROM stdin WITH CSV HEADER
                   DELIMITER as ','
                   """
    with open('dictionary1.csv', 'r') as f:
        cur.copy_expert(sql=dictionary_sql, file=f)
        conn.commit()
        cur.close()
    db.session.commit()


if __name__ == "__main__":
    manager.run()
