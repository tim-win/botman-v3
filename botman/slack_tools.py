"""slack_tools"""
import re


def clean(text):
    images = re.compile("'@.* uploaded a file\: \<(.*)\|.*\>'")
    match = re.match(images, text)
    if match:
        return re.match.group(1)
