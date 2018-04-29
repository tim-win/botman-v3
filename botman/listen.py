"""Listener command"""
import random
import sqlite3

RESPOND_PERCENT = 30
DB_NAME = '/opt/botman-v3/main.db'


def run(message):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
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
    conn.commit()

    if random.random() < RESPOND_PERCENT / 100.0:
        c = conn.cursor()

        count = c.execute('SELECT COUNT(*) from messages;')
        count = count.fetchone()[0]

        _id = random.randint(0, count-1)

        row = c.execute('''
            SELECT text
            FROM messages
            LIMIT 1
            OFFSET {0};'''.format(_id)).fetchone()

        message.send(row[0])
