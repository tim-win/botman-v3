"""markov.py"""
import random

N = 4


def generate_chain():
    chain = []

    while True:
        pass


def choose_ngram(counts, function=random.random):
    """Choose next ngram based on a function.

    Parameters
    ----------
    counts : dict
        Key > value pairs where keys are ngrams and values are integer counts
        they have been seen as

    function : callable
        A function that takes no arguments and returns a number between 0 and
        1. Defaults to random.random.

    Returns
    -------
    str: an ngram
    """
    total = sum([val for val in counts.values()])
    magic_number = function() * total

    running = 0
    for item in sorted(counts.items()):
        running += item[1]
        if running > magic_number:
            return item[0]


def normalize(string):
    """Turn into a dict of grams.

    Example input:
        'i am a very good robot.'

    gram output (assuming N == 4):
        {
            'i': {'am': 1, 'am a': 1, 'am a very': 1, 'am a very good': 1},
            'i am': {'a': 1, 'a very': 1, 'a very good': 1, 'very good robot.': 1,},
            'i am a': {'very': 1, 'very good': 1, 'very good robot.': 1,},
            'i am a very': {'good': 1, 'good robot.': 1,},
            'am': {'a': 1, 'a very': 1, 'a very good': 1, 'a very good robot.': 1,},
            'am a': {'very': 1, 'very good': 1, 'very good robot.': 1,},
            'am a very': {'good': 1, 'good robot.': 1,},
            'am a very good': {'robot.': 1,},
            'a': {'very': 1, 'very good': 1, 'very good robot.': 1,},
            'a very': {'good': 1, 'good robot.': 1,},
            'a very good': {'robot.': 1,},
            'a very good robot.': {'': 1,},
            'very': {'good': 1, 'good robot.': 1,},
            'very good': {'robot.': 1,},
            'very good robot.': {'': 1,},
            'good': {'robot.': 1,},
            'good robot.': {'': 1,},
            'robot.': {'': 1,},
        }
    """  # noqa
    words = string.split()
    count = len(words)

    grams = {}

    for gram_size in range(1, N + 1):
        for second_gram_size in range(0, N + 1):
            for index in range(count):
                # First, make sure everything fits
                if not fits(index, count, gram_size, second_gram_size):
                    continue

                # Only run 0 length second grams at end of input
                if not second_gram_size and fits(index, count, gram_size, 1):
                    continue

                g1_start, g1_end, g2_start, g2_end = generate_indicies(
                    index, gram_size, second_gram_size)

                first_gram = ' '.join(words[g1_start:g1_end])
                second_gram = ' '.join(words[g2_start:g2_end])

                grams[first_gram] = grams.get(first_gram, {})

                grams[first_gram][second_gram] = grams[first_gram].get(
                    second_gram, 0) + 1
    return grams


def fits(index, count, gram_one, gram_two):
    """Determine if both grams fit in the line at/after the stated index.

    For instance, you are generating markov probabilities for 2-grams to be
    followed by other 2-grams. You can imagine the following word list being
    iterated over with different index points:

    words = ['i', 'am', 'a', 'very' 'good', 'robot']

    At index 0, the first 2-gram is 'i am', and the second 2-gram is 'a very',
    and everything fits, so 'fits(0, 6, 2, 2)' should return True. However, at
    index 3, the first tw ogram is 'very good', and the second two gram
    doesn't fit, (the only word left is 'robot'), so it `fits(3, 6, 2, 2)`
    should return False.

    Parameters
    ----------
    index : integer
        start index

    count : integer
        length of the word list being tested

    gram_one : integer
        length of first gram

    gram_two : integer
        length of second gram

    Returns
    -------
    bool : true if everything fits
    """
    return index + gram_one + gram_two - 1 < count


def generate_indicies(index, gram_one, gram_two):
    """Determine the stant and end indicies of two sequential n-grams.

    Parameters
    ----------
    index : int
        starting index

    gram_one : int
        length of first gram

    gram_two : int
        length of second gram

    Returns
    -------
    tuple(int, int, int, int) : returns g1_start, g1_end, g1_start, g2_end
    """

    g1_start = index
    g1_end = index + gram_one
    g2_start = g1_end
    g2_end = g2_start + gram_two

    return g1_start, g1_end, g2_start, g2_end
