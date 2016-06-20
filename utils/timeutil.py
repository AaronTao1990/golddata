import time
from datetime import datetime
import random

def str_to_seconds(time_s, format_s='%Y-%m-%d %H:%M:%S'):
    struct_t = time.strptime(time_s, format_s)
    return int(time.mktime(struct_t))

def str_to_mcroseconds(time_s, format_s='%Y-%m-%d %H:%M:%S'):
    struct_t = datetime.strptime(time_s, format_s)
    return time.mktime(struct_t.timetuple()) * 1000 + struct_t.microsecond / 1000

def microseconds_format(time_ms, format_s='%Y-%m-%d %H:%M:%S'):
    struct_t = datetime.fromtimestamp(time_ms/1000)
    return time.mktime(struct_t.timetuple()) * 1000 + struct_t.microsecond / 1000

def seconds_format(time_s, format_s='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(time_s).strftime(format_s)

def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def random_date_since(start_date):
    seconds = str_to_seconds(start_date)
    return seconds_format(seconds + random.randint(0, int(time.time()) - seconds))

if __name__ == '__main__':
    #print long(str_to_mcroseconds('2015-12-12 12:12:12'))
    #print long(str_to_seconds('2015-12-12 12:12:12'))
    #print random_date_since('2016-02-20 00:00:00')
    print seconds_format(1456124856)
