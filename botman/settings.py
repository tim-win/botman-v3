"""Simple settings configuration."""
from importlib import reload
import re

from botman.db_mgmt import ensure_settings_table
from botman.db_mgmt import set_setting
from botman.db_mgmt import debug_ngrams
from botman import talk

SET_SETTINGS_RE = re.compile(r'^set (\w+) (\w+)$')


def debug_reply(message):
    print(debug_ngrams())
    message.send('Check the logs.')


def save_settings(message):
    match = re.match(SET_SETTINGS_RE, message)

    key, value = match.group(1), match.group(2)

    set_setting(key, value)

    message.s


def run(message):
    ensure_settings_table()

    if re.match(SET_SETTINGS_RE, message.body['text']):
        save_settings(message)

    else:
        reload(talk)

        # do not run in thread,
        # settings.run is already in its own thread.
        talk.run(message)
