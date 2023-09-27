import argparse

from src.helper import filter_helper, operation_helper, tag_helper, file_helper
from src.factory.service_factory import ServiceFactory
from src.model.arguments import Arguments


def parse_args() -> Arguments:
    """
    Parse the command line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', type=str)
    parser.add_argument('--service', type=str, default='')
    parser.add_argument('--filter', action='append')
    parser.add_argument('--tag', action='append')
    parser.add_argument('--file', type=str, default='')
    parser.add_argument('--export-tag', action='append')
    args = parser.parse_args()

    filter_params = args.filter if args.filter else []
    tag_params = args.tag if args.tag else []
    export_tags = args.export_tag if args.export_tag else []

    operation = operation_helper.parse_operation(args.operation)
    service = ServiceFactory().get_service(args.service) if args.service else None
    filters = filter_helper.parse_filters(filter_params)
    tags = tag_helper.parse_tags(tag_params)
    file_path = args.file

    for tag in export_tags:
        tag_helper.validate_tag_key(tag)

    if args.file:
        file_helper.validate_file_path(file_path)

    return Arguments(
        operation=operation,
        service=service,
        filters=filters,
        tags=tags,
        file_path=file_path,
        export_tags=export_tags
    )
