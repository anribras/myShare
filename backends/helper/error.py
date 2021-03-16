from enum import Enum


class ErrorCode(Enum):
    table_insert_error = 1


def derived_error(err=None):
    if err is None:
        return {'status_code': 0, 'status': 'Ok', 'status_message': ''}
    if err in list(ErrorCode.__dict__['_member_map_'].keys()):
            return {'status_code': ErrorCode.__getitem__(err).value,
                'status_message': ErrorCode.__getitem__(err).name,
                'status': 'Fail'
                }
    else:
        return {'status_code': 1,
                'status_message': 'undefined error',
                'status': 'Fail'
                }
