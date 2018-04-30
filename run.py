#!/usr/bin/env python
"""Botman-v3.

Fully featured chatbot.
"""
from importlib import reload
import random
import sys

from slackbot.bot import Bot
from slackbot.bot import listen_to, respond_to

from botman import listen
from botman import talk
from botman.db_mgmt import debug_ngrams

RESPOND_PERCENT = 100
DB_NAME = '/opt/botman-v3/main.db'


@listen_to('.*')
def hear(message):
    print(message.body['text'])
    reload(listen)
    reload(talk)
    listen.run(message)
    if random.random() < 1/100.0:
        talk.run(message)
    # message.send('ok, prove this works at all')


@respond_to('debug')
def debug_reply(message):
    print(debug_ngrams())
    message.send('Check the logs.')


@respond_to('.*')
def catch_direct_cmds(message):
    talk.run(message)


def main(args):

    bot = Bot()
    bot.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
