from src.core.app import list_operation, tag_operation, export_operation, import_operation
from src.helper import argument_helper
from src.model.operation import Operation


def main():
    """
    Main entry point.
    """
    args = argument_helper.parse_args()

    if args.operation == Operation.LIST:
        assert args.service, 'You must provide a service using --service flag'
        list_operation.list_resources(args.service, args.filters)

    if args.operation == Operation.TAG:
        assert args.service, 'You must provide a service using --service flag'
        assert args.tags, 'You must provide at least one tag using --tag flag'
        tag_operation.tag_resources(args.service, args.filters, args.tags)

    if args.operation == Operation.EXPORT:
        assert args.service, 'You must provide a service using --service flag'
        assert args.file_path, 'You must provide a file path using --file flag'
        export_operation.export_tags(args.service, args.filters, args.file_path, args.export_tags)

    if args.operation == Operation.IMPORT:
        assert args.file_path, 'You must provide a file path using --file flag'
        import_operation.import_tags(args.file_path)


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(str(error))
    except AssertionError as error:
        print(str(error))
    except Exception as error:
        print('Terminating the program due to an unexpected error!\n' + str(error))
        raise error
