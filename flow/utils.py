import calendar
import datetime
from constants import DATETIME

DATETIME_STRING_FORMAT = DATETIME.DATETIME_STR_FORMAT

def convert_datetime_unix(dt):
    try:
        utc_time = calendar.timegm(dt.utctimetuple())
        return utc_time, None
    except Exception as errmsg:
        return None, str(errmsg)

def convert_unix_datetime(un, format=DATETIME_STRING_FORMAT):
    try:
        return datetime.datetime.utcfromtimestamp(un).strftime(format)
    except Exception as errmsg:
        return None, str(errmsg)

def read_csv_table(csv_content, delimiter=",", header_line=0):
    try:
        headers = csv_content[header_line].split(delimiter)
        table_data = []
        for line in csv_content[header_line + 1:]:
            row_dict = {}
            columns = line.split(delimiter)
            for idx, cell in enumerate(columns):
                row_dict[headers[idx].strip()] = cell.strip()
            table_data.append(row_dict)
        return table_data, None
    except Exception as errmsg:
        return None, str(errmsg)

def convert_datetime_str(dt, format=DATETIME_STRING_FORMAT):
    try:
        datetime_str = dt.strftime(format)
        return datetime_str, None
    except Exception as errmsg:
        return None, str(errmsg)

def convert_str_datetime(dt_str, format=DATETIME_STRING_FORMAT):
    try:
        dt_obj = datetime.datetime.strptime(dt_str, format)
        return dt_obj, None
    except Exception as errmsg:
        return None, str(errmsg)


def secs_to_timestamp(secs):
    try:
        return datetime.timedelta(seconds=int(secs))
    except Exception as errmsg:
        return None, str(errmsg)
