"""Talking stuff."""
from botman.db_mgmt import fetch_counts
from botman.markov import choose_ngram


def generate_chain():
    counts = fetch_counts('')

    chain = [choose_ngram(counts)]
    while chain[-1]:
        counts = fetch_counts(chain[-1])
        chain.append(choose_ngram(counts))

    return ' '.join(chain)


def run(message):
    """All things to do when talking."""
    message.send(generate_chain())
