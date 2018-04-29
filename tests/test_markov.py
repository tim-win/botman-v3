import pytest

from botman.markov import fits
from botman.markov import generate_indicies


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
