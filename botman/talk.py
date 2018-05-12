"""Talking stuff."""
import random

from botman.db_mgmt import fetch_counts
from botman.markov import choose_ngram
from botman.db_mgmt import fetch_settings
from botman.db_mgmt import ensure_settings_table


def generate_chain():
    counts = fetch_counts('')

    chain = [choose_ngram(counts)]
    while chain[-1]:
        counts = fetch_counts(chain[-1])
        chain.append(choose_ngram(counts))

    # Get rid of unsightly empty string
    chain.pop(-1)

    return ' '.join(chain)


def run(message, infrequent=True):
    """All things to do when talking."""

    if infrequent:
        ensure_settings_table()
        freq = float(fetch_settings('frequency', '10'))
        if random.random() > 1 / freq:
            return

    message.send(generate_chain())
