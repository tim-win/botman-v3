"""Simple settings configuration."""
from importlib import reload
import re
from textwrap import dedent

from botman.db_mgmt import ensure_settings_table
from botman.db_mgmt import set_setting
from botman.db_mgmt import fetch_setting
from botman.db_mgmt import debug_ngrams
from botman import talk

SAVE_SETTINGS_RE = re.compile(r'^save (\w+) (\w+)$')
SHOW_SETTINGS_RE = re.compile(r'^show (\w+)$')

SCHEMA = {
    'frequency': {
        'type': float,
        'default': 20.0,
        'description': dedent('''
            Botman picks a number
            between 0 and 1, and if that number
            is greater than `1 / <frequency>`,
            he will generate nonsense.
            '''),
        'max': 10000,
        'min': 1
    },
    'delay': {
        'type': float,
        'default': 20.0,
        'description': dedent('''
            Botman includes an arbitrary,
            random delay before replying in
            normal conversation, to help
            make it feel more natural.
            '''),
        'max': 999,
        'min': 0
    }
}


def fetch_typed_setting(key):
    """Ensure correct type."""
    schema = SCHEMA.get(key, None)
    cast = schema['type']
    default = schema['default']

    # Minimum and Maximum are not required
    minimum = schema.get('min')
    maximum = schema.get('max')

    value = fetch_setting(key, default)

    if minimum and maximum:
        if value < minimum or value > maximum:
            print('Setting for {0} out of bounds, returning default'.format(
                key))
            return default

    return cast(value)


def debug_reply(message):
    print(debug_ngrams())
    message.send('Check the logs.')


def validate_name(key):
    """Ensure the name is good."""
    if key not in SCHEMA:
        return False
    return True


def validate_type(key, value):
    """Ensure the type works out."""
    try:
        schema = SCHEMA.get(key)
        cast = schema['type']
        cast(value)
        return True
    except ValueError:
        return False
    return None


def save_settings(message):
    match = re.match(SAVE_SETTINGS_RE, message.body['text'])

    key, value = match.group(1), match.group(2)

    if not validate_name(key):
        message.send(
            'I don\'t like the key name "{0}". Try another'.format(key))
        return

    if not validate_type(key, value):
        message.send('Value "{1}" for key {0} is of invalid type.'.format(
            key, value))
        return

    set_setting(key, value)

    message.send('I saved setting {0} as value {1}'.format(key, value))


def show_settings(message):
    match = re.match(SHOW_SETTINGS_RE, message.body['text'])
    key = match.group(1)

    if not validate_name(key):
        message.send('"{0}" is a valid setting name. ')
        return

    value = fetch_setting(key)
    message.send('Setting "{0}" is set to "{1}"'.format(key, value))


def run(message):
    ensure_settings_table()

    print('Running settings handler')

    if re.match(SAVE_SETTINGS_RE, message.body['text']):
        save_settings(message)

    elif re.match(SHOW_SETTINGS_RE, message.body['text']):
        show_settings(message)

    else:
        reload(talk)
        talk.run(message, infrequent=False, immediate=True)
