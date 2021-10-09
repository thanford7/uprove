from datetime import date, datetime, time
from enum import Enum
from typing import Union, Optional

FORMAT_DATE = '%m-%d-%Y'
FORMAT_TIME = '%H:%M:%S'
FORMAT_DATETIME = f'{FORMAT_DATE} {FORMAT_TIME}'


class FormatType(Enum):
    DATE = 'date'
    TIME = 'time'
    DATETIME = 'datetime'


UNSUPPORTED_FORMAT_CONVERSION = (
    (date, FormatType.TIME),
    (time, FormatType.DATE),
    (time, FormatType.DATETIME)
)

FORMAT_LOOKUP = {
    FormatType.DATE: FORMAT_DATE,
    FormatType.TIME: FORMAT_TIME,
    FormatType.DATETIME: FORMAT_DATETIME,
    date: FORMAT_DATE,
    time: FORMAT_TIME,
    datetime: FORMAT_DATETIME
}


def serializeDatetime(val: Union[date, time, datetime, None], formatAs: Optional[FormatType] = None, allowNone: Optional[bool] = False):
    """Get a string value from a date, time, or datetime object
    """
    if val is None:
        if allowNone:
            return None
        else:
            raise ValueError('Datetime value cannot be None')

    objectType = type(val)
    if formatAs and (objectType, formatAs) in UNSUPPORTED_FORMAT_CONVERSION:
        raise ValueError(f'Can\'t convert {val} to a {formatAs.value}')

    formatString = FORMAT_LOOKUP.get(formatAs) or FORMAT_LOOKUP.get(objectType)

    return val.strftime(formatString)
