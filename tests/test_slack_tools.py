"""test_slack_tools.py"""
import pytest

from botman.slack_tools import clean


@pytest.mark.parametrize('test, control, description', [
    (
        '<@U0CQ36LUT> uploaded a file: <https://thosebreeders.slack.com/files/U0CQ36LUT/FAFT35ES0/image.png|image.png>',  # noqa
        'https://thosebreeders.slack.com/files/U0CQ36LUT/FAFT35ES0/image.png',
        'failed example upload of file test',
    ),
])
def test_clean(test, control, description):
    """Test that clean does what it is supposed to."""
    assert clean(test) == control, description
