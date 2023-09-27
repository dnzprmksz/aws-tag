import re
from typing import List

from src.model.filter import Filter


def parse_filters(filter_params: List[str]) -> List[Filter]:
    """
    Parse the filters from the command line arguments.

    :param filter_params: List of filter arguments.
    :return: List of filters.
    """
    parsed_filters = []

    for filter_param in filter_params:
        filter = __validate_parse_single_filter(filter_param)
        parsed_filters.append(filter)

    return parsed_filters


def get_name_prefix_filter_value(filters: List[Filter], default: str = '') -> str:
    """
    Get the name prefix filter value from the list of filters.

    :param filters: List of filters.
    :param default: Default value to return if no name prefix filter is found.
    :return: Name prefix filter value.
    """
    name_prefix_filter_value = next(
        (filter.value for filter in filters if filter.key == '@name' and filter.operator == '^'),
        default
    )

    return name_prefix_filter_value


def get_exact_name_filter_value(filters: List[Filter], default: str = '') -> str:
    """
    Get the exact name filter value from the list of filters.

    :param filters: List of filters.
    :param default: Default value to return if no exact name filter is found.
    :return: Exact name filter value.
    """
    exact_name_filter_value = next(
        (filter.value for filter in filters if filter.key == '@name' and filter.operator == '='),
        default
    )

    return exact_name_filter_value


def __validate_parse_single_filter(filter_param: str) -> Filter:
    """
    Validate and parse a single filter.

    :param filter_param: Filter to validate and parse.
    :return: Filter.
    """
    valid_chars = r'a-zA-Z0-9.:-_=!~\^\$(\-\-)*'
    valid_chars_regex = re.compile(f'^[{valid_chars}]+$')

    if not valid_chars_regex.match(filter_param):
        raise ValueError(f'Invalid filter param: {filter_param}')

    operator = __parse_operator(filter_param)
    split = filter_param.split(operator)
    key = split[0]

    if operator == '--':
        value = ''
    else:
        value = split[1]

    filter = Filter(key, value, operator)

    return filter


def __parse_operator(filter_param: str) -> str:
    """
    Parse the operator from the filter.

    :param filter_param: Filter to parse.
    :return: Operator.
    """
    operators = [
        '!=', '=',
        '!~', '~',
        '!^', '^',
        '!$', '$',
        '--'
    ]

    found_operators = []

    for operator in operators:
        if operator in filter_param:
            found_operators.append(operator)
            filter_param = filter_param.replace(operator, '')

    if len(found_operators) == 1:
        return found_operators[0]
    else:
        raise ValueError(f'Invalid filter param: {filter_param}. '
                         f'Must contain exactly one operator, but found {len(found_operators)}.')
