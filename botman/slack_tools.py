"""slack_tools"""
import re


def clean(text):
    images = re.compile(r"\<@.*\> (uploaded|mentioned) a file\: \<(.*)\|.*\>")
    match = re.match(images, text)
    if match:
        return match.group(2)
    return text
