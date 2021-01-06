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


def fetch_conversation(channel, max_messages=100, threshold=60*60*12):
    """Get the latest `max_messages` messages from a channel.

    message : slack message object lol
    max_messages : int
        This is the maximum number of resposes in a conversation to include
    threshold : int
        time threshold in seconds before a message is deemed outside of the
        conversation window
    """

    with SQLiteConn() as c:
        # fetch
        cursor = c.execute('''
            SELECT *
            FROM messages
            WHERE channel = ?
            ORDER BY ts DESC
            LIMIT ?;''',
            (
                channel,
                max_messages
            )
        )

        # Then check results against threshold
        records = []
        current = None
        for item in cursor:
            if current is None:
                current = item[1]
                records.append(item)
                continue
            if current - item[1] > threshold:
                break

            current = item[1]
            records.append(item)

    # return convo in chronolical order
    return reversed(records)


def get_channel_messages(channel):
    messages = []
    with SQLiteConn() as c:
        cursor = c.execute('''
            SELECT * from messages
            WHERE channel = ?;''', (channel,))
        for i in cursor:
            messages.append(i)
    return messages


def fetch_channel_names():
    channels = set()
    with SQLiteConn() as c:
        cursor = c.execute('''
           SELECT channel FROM messages
           ORDER BY channel;''')
        for channel in cursor:
            channels.add(channel[0])
    return sorted(list(channels))


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


def ensure_settings_table():
    with SQLiteConn() as c:

        c.execute(
            '''CREATE TABLE IF NOT EXISTS
            settings
            (
             key text,
             value text,
             CONSTRAINT key_pk PRIMARY KEY (key))
             '''
        )


def fetch_setting(key, default=None):
    with SQLiteConn() as c:
        row = c.execute('''
            SELECT value
            FROM settings
            WHERE key = ?;''', (key,)).fetchone()

        if row:
            return json.loads(row[0])
    return default


def set_setting(key, value):
    with SQLiteConn() as c:
        c.execute(
            'INSERT or REPLACE INTO settings (key, value) VALUES (?, ?)',
            (key, value)
        )
