#!/usr/bin/env python
"""Botman-v3.

Fully featured chatbot.

"""
from importlib import reload
import sys
from threading import Thread

from slackbot.bot import Bot
from slackbot.bot import listen_to, respond_to

from botman import listen
from botman import talk
from botman import settings

RESPOND_PERCENT = 100
DB_NAME = '/opt/botman-v3/main.db'


@listen_to('.*')
def hear(message):
    print(message.body['text'])
    reload(listen)
    reload(talk)

    listen_thread = Thread(target=listen.run, args=(message,))
    talk_thread = Thread(target=talk.run, args=(message,))

    listen_thread.start()
    talk_thread.start()


@respond_to('.*')
def catch_direct_cmds(message):
    settings_thread = Thread(target=settings.run, args=(message,))
    settings_thread.run()


def main(args):

    bot = Bot()
    bot.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
