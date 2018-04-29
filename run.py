#!/usr/bin/env python
"""Botman-v3.

Fully featured chatbot.
"""
from importlib import reload
import sys

from slackbot.bot import Bot
from slackbot.bot import listen_to, respond_to

from botman import listen

RESPOND_PERCENT = 100
DB_NAME = '/opt/botman-v3/main.db'


@listen_to('.*')
def lol(message):
    reload(listen)
    try:
        return listen.run(message)
    except Exception as e:
        message.send(e)


@respond_to('.*')
def catch_direct_cmds(message):
    return lol(message)


def main(args):

    bot = Bot()
    bot.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
