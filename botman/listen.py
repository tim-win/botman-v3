"""Listener command"""
from botman.db_mgmt import record_message
from botman.db_mgmt import ensure_messages_table
from botman.db_mgmt import ensure_ngrams_table
from botman.db_mgmt import add_gram
from botman.markov import normalize

DB_NAME = '/opt/botman-v3/main.db'


def run(message):
    ensure_messages_table()

    text = record_message(message)

    ensure_ngrams_table()
    ngrams = normalize(text)
    for ngram in ngrams:
        add_gram(ngram, ngrams[ngram])
