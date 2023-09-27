from src.model.operation import Operation


def parse_operation(operation_value: str) -> Operation:
    """
    Parse the operation value to an operation.

    :param operation_value: The operation value.
    :return: The parsed operation.
    """
    if operation_value == 'list':
        return Operation.LIST
    elif operation_value == 'tag':
        return Operation.TAG
    elif operation_value == 'import':
        return Operation.IMPORT
    elif operation_value == 'export':
        return Operation.EXPORT
    else:
        raise ValueError(f'Invalid operation: {operation_value}')
