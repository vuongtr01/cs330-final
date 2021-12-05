import sqlite3

import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv

def get_db():
    db = getattr(g, 'db', None)

    if db is None:
        db = g.db = sqlite3.connect(current_app.config['DATABASE'])
        db.execute("PRAGMA foreign_keys = ON;")

    db.row_factory = make_dicts

    return db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def make_dicts(cursor, row):
    """convert the retrieved data into dictionary with key is column name"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    """Run a query"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with open(current_app.config["CSVFILE"]) as f:
        reader = csv.reader(f)
        books = list(reader)[1:1001]

        for line in books:
            query_db(
                "INSERT INTO books (title, author, publication_year, publisher, img_url) VALUES(:title, :author, :publication_year, :publisher, :img_url)",
                {
                    "title": line[1],
                    "author": line[2],
                    "publication_year": line[3],
                    "publisher": line[4],
                    "img_url": line[6]
                }
                )
        db.commit()


# define a command line called init-db that calls the init_db_command function
# init_db_command function creates a database
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
