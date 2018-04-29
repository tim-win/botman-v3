#!/usr/bin/env python
"""Botman-v3.

Fully featured chatbot.
"""
import random
import sqlite3
import sys

from slackbot.bot import Bot
from slackbot.bot import listen_to, respond_to

RESPOND_PERCENT = 100
DB_NAME = 'example.db'


@listen_to('.*')
def lol(message):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS
        messages
        (ts integer,
         source_team text,
         user text,
         type text,
         channel text,
         text text)'''
    )
    c.execute(
        'INSERT INTO messages VALUES ?',
        ([
            message.body['ts'],
            message.body['source_team'],
            message.body['user'],
            message.body['type'],
            message.body['channel'],
            message.body['text'],
            ],))

    if random.random() < RESPOND_PERCENT / 100.0:
        message.send('Saved that comment to disk')


@respond_to('.*')
def catch_direct_cmds(message):
    return lol(message)


def main(args):

    bot = Bot()
    bot.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
