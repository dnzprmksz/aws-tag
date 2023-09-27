import re
from typing import List

from src.model.tag import Tag


def parse_tags(tag_params: List[str]) -> List[Tag]:
    """
    Parse the tags from the command line arguments.

    :param tag_params: List of tag arguments.
    :return: List of tags.
    """
    parsed_tags = []

    for tag_param in tag_params:
        __validate(tag_param)
        key, value = tag_param.split('=')
        tag = Tag(key=str(key), value=str(value))
        parsed_tags.append(tag)

    return parsed_tags


def validate_tag_key(tag_key: str) -> None:
    """
    Validate the tag key.

    :param tag_key: Tag key to validate.
    """
    valid_chars = r'a-zA-Z0-9.:\-_'
    valid_chars_regex = re.compile(f'^[{valid_chars}]+$')

    if not valid_chars_regex.match(tag_key):
        raise ValueError(f'Invalid tag key: {tag_key}')


def __validate(tag_param: str) -> None:
    """
    Validate the tag.

    :param tag_param: Tag to validate.
    """
    valid_chars = r'a-zA-Z0-9.:\-_='
    valid_chars_regex = re.compile(f'^[{valid_chars}]+$')

    if not valid_chars_regex.match(tag_param):
        raise ValueError(f'Invalid tag: {tag_param}')

    if tag_param.count('=') != 1:
        raise ValueError(f'Invalid tag: {tag_param}. Must contain exactly one "=".')
