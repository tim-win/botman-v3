"""Talking stuff."""
import random
import time
import json
import requests

from botman.context import compile_context
from botman.db_mgmt import fetch_counts
from botman.markov import choose_ngram
from botman.settings import fetch_typed_setting



def generate_chain():
    counts = fetch_counts('')

    chain = [choose_ngram(counts)]
    while chain[-1]:
        counts = fetch_counts(chain[-1])
        chain.append(choose_ngram(counts))

    # Get rid of unsightly empty string
    chain.pop(-1)

    return ' '.join(chain)


def run(message, infrequent=True, immediate=False):
    """All things to do when talking."""
    print('INFO: Running talk handler')

    if infrequent:

        freq = fetch_typed_setting('frequency')

        if random.random() > 1 / freq:
            return

    if not immediate:

        max_delay = fetch_typed_setting('delay')
        delay = max_delay * random.random()
        print('Delaying response by {0}'.format(delay))

        time.sleep(delay)

    context = compile_context(message.body['channel'])

    text = requests.post('http://workhorse:8080/generate', json={'context': context}).text

    print('Raw response text:', text)

    response = json.loads(text)['response']

    message.send(response)
