import pytest

from botman.markov import choose_ngram
from botman.markov import fits
from botman.markov import generate_indicies
from botman.markov import normalize


@pytest.mark.parametrize('test, control, description', [
    (
        ({'very': 1, 'very good': 1, 'very good robot.': 1}, lambda: 0.25),
        'very',
        'Failed to pick first ngram'
    ),
    (
        ({'very': 1, 'very good': 1, 'very good robot.': 1}, lambda: 0.5),
        'very good',
        'Failed to pick second ngram'
    ),
    (
        ({'very': 1, 'very good': 1, 'very good robot.': 1}, lambda: 0.75),
        'very good robot.',
        'Failed to pick third ngram'
    ),
    (
        ({'very': 1, 'very good': 99}, lambda: 0.009),
        'very',
        'Failed to pick minority ngram'
    ),
    (
        ({'very': 1, 'very good': 99}, lambda: 0.02),
        'very good',
        'Failed to pick low-end majority ngram'
    ),
    (
        ({'very': 1, 'very good': 99}, lambda: 0.99),
        'very good',
        'Failed to pick high-end majority ngram'
    ),
    ])
def test_choose_ngram(test, control, description):
    assert choose_ngram(*test) == control, description


@pytest.mark.parametrize('test, control, description', [
    (
        (0, 6, 2, 2),
        True,
        'Did not correctly fit 2x 2-grams into index 0 of a six word list'
    ),
    (
        (3, 6, 2, 2),
        False,
        'Somehow fit 2x 2-grams into index 3 of a six word list'
    ),
    (
        (0, 2, 1, 1),
        True,
        'Did not correctly fit 2x 1-grams into index 0 of a two word list'
    ),
    (
        (1, 17, 8, 8),
        True,
        'Did not correctly fit 2x 8-grams into index 1 of seventeen words'
    ),
    (
        (2, 17, 8, 8),
        False,
        'Somehow fit 2x 8-grams into index 2 of seventeen words'
    ),
    (
        (
            2,
            len(
                ['1', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10', '11', '12']),
            1, 8),
        True,
        'Did not fit 9-words worth of grams into index 2 of twelve words'
    ),
    (
        (
            2,
            len(
                ['1', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10', '11']),
            1,
            8),
        True,
        'Failed to fit 9-words worth of grams into index 2 of eleven words'
    ),
    (
        (
            2,
            len(
                ['1', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10']),
            1,
            8),
        False,
        'Somehow fit 9-words worth of grams into index 2 of ten words'
    ),
    (
        (
            3,
            len(
                ['1', '2']),
            1,
            1),
        False,
        'Somehow fit 2 1-grams into a 2 word list at an illogical index'
    ),
    (
        (
            0,
            len(
                ['1', '2']),
            2,
            0),
        True,
        'Failed to fit 0 length 2nd gram'
    ),
    ])
def test_fits(test, control, description):
    """Tests fits.

    Assert that given a starting index, a word list length, and n and m for
    n-gram and m-gram sizes, both one n-gram and one m-gram can fit in the
    remaining words."""

    assert fits(*test) == control, description


@pytest.mark.parametrize('test, control, description', [
    (
        (0, 1, 1),
        (0, 1, 1, 2),
        'Failed basic case- 2x 1-grams at position 0',
    ),
    (
        (12, 3, 5),
        (12, 15, 15, 20),
        'Failed vaguely involved case- 2x grams at position 12',
    ),

])
def test_generate_indicies(test, control, description):
    assert generate_indicies(*test) == control, description


@pytest.mark.parametrize('test, control, description', [
    (
        'i am a very good robot.',
        {
            '': {'i': 1, 'i am': 1, 'i am a': 1, 'i am a very': 1},
            'i': {'am': 1, 'am a': 1, 'am a very': 1, 'am a very good': 1},
            'i am': {
                'a': 1, 'a very': 1,
                'a very good': 1, 'a very good robot.': 1},
            'i am a': {'very': 1, 'very good': 1, 'very good robot.': 1},
            'i am a very': {'good': 1, 'good robot.': 1},
            'am': {
                'a': 1, 'a very': 1,
                'a very good': 1, 'a very good robot.': 1},
            'am a': {'very': 1, 'very good': 1, 'very good robot.': 1},
            'am a very': {'good': 1, 'good robot.': 1},
            'am a very good': {'robot.': 1},
            'a': {'very': 1, 'very good': 1, 'very good robot.': 1},
            'a very': {'good': 1, 'good robot.': 1},
            'a very good': {'robot.': 1},
            'a very good robot.': {'': 1},
            'very': {'good': 1, 'good robot.': 1},
            'very good': {'robot.': 1},
            'very good robot.': {'': 1},
            'good': {'robot.': 1},
            'good robot.': {'': 1},
            'robot.': {'': 1},
        },
        'manually written out basic case failed, bucko'
    ),
    (
        'a a a',
        {
            '': {'a': 1, 'a a': 1, 'a a a': 1},
            'a': {'a': 2, 'a a': 1, '': 1},
            'a a': {'a': 1, '': 1},
            'a a a': {'': 1}
        },
        'simple case of duplicate occurences failed'
    )
])
def test_normalize(test, control, description):
    assert normalize(test) == control, description
