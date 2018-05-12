import json
import random
import sqlite3

DB_NAME = '/opt/botman-v3/main.db'


class SQLiteConn(object):
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME, timeout=30)
        return self.conn.cursor()

    def __exit__(self, *args):
        self.conn.commit()
        self.conn.close()


def ensure_messages_table():
    with SQLiteConn() as c:
        c.execute(
            '''CREATE TABLE IF NOT EXISTS
            messages
            (
             text text,
             ts integer,
             user text,
             type text,
             channel text,
             source_team text)'''
        )


def record_message(message):
    with SQLiteConn() as c:
        c.execute(
            'INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)',
            (
                message.body['text'],
                message.body['ts'],
                message.body['user'],
                message.body['type'],
                message.body['channel'],
                message.body.get('source_team', 'None'),
            ))
    return message.body['text']


def fetch_counts(ngram):
    counts = {}

    ensure_ngrams_table()

    with SQLiteConn() as c:
        row = c.execute('''
            SELECT counts
            FROM ngrams
            WHERE ngram = ?;''', (ngram,)).fetchone()

        if row:
            counts = json.loads(row[0])

    return counts


def set_counts(ngram, counts):
    ensure_ngrams_table()
    with SQLiteConn() as c:
        c.execute(
            'INSERT OR REPLACE INTO ngrams VALUES (?, ?)',
            (ngram, json.dumps(counts))
        )

    return ngram, counts


def ensure_ngrams_table():
    with SQLiteConn() as c:

        c.execute(
            '''CREATE TABLE IF NOT EXISTS
            ngrams
            (
             ngram text,
             counts text,
             CONSTRAINT ngrams_pk PRIMARY KEY (ngram))
             '''
        )


def add_gram(ngram, counts):
    ensure_ngrams_table()

    with SQLiteConn() as c:

        existing = fetch_counts(ngram)

        for key in counts:
            existing[key] = existing.get(key, 0) + counts[key]

        c.execute(
            'INSERT or REPLACE INTO ngrams (ngram, counts) VALUES (?, ?)',
            (ngram, json.dumps(existing))
        )

    return existing


def retrieve_random_message():
    with SQLiteConn() as c:

        count = c.execute('SELECT COUNT(*) from messages;')
        count = count.fetchone()[0]

        _id = random.randint(0, count-1)

        row = c.execute('''
            SELECT text
            FROM messages
            LIMIT 1
            OFFSET {0};'''.format(_id)).fetchone()

        rando = row[0]

    return rando


def debug_ngrams():
    outp = []
    with SQLiteConn() as c:
        rows = c.execute('SELECT * from ngrams;')
        for row in rows:
            outp.append(row)

    return json.dumps(outp, indent=4)
