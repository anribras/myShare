from enum import Enum


class ErrorCode(Enum):
    ok = 0
    table_insert_error = 0x1001
    data_null = 0x1002


def derived_error(item):
    return {
        'status': {
            'code': ErrorCode[item.name].value,
            'message': ErrorCode[item.name].name,
        }
    }
