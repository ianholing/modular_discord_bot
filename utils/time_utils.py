import time
import datetime

# time variables
import config

def get_today():
    return (datetime.date.today().strftime('%Y%m%d'))

def get_yesterday():
    return ((datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d'))

def is_final_day():
    return datetime.date.today().weekday() == config.RESET_DAY_OFFSET

def get_thisweek():
    today = datetime.date.today()
    offset = -today.weekday()+config.RESET_DAY_OFFSET
    if today.weekday() < config.RESET_DAY_OFFSET:
        offset = offset-7
    return ((today + datetime.timedelta(days=offset)).strftime('%Y%m%d'))

def get_prevweek():
    today = datetime.date.today()
    offset = -today.weekday()+config.RESET_DAY_OFFSET
    if today.weekday() < config.RESET_DAY_OFFSET:
        offset = offset-7
    return ((today + datetime.timedelta(days=offset-7)).strftime('%Y%m%d'))

def get_time_left():
    return (config.RESET_HOUR - time.gmtime().tm_hour) % 24

def is_weekend():
    return (datetime.datetime.today().weekday() >= 5)

def seconds_to(hour, minute):
    now = datetime.datetime.now()
    target = datetime.datetime(*now.timetuple()[0:3], hour=hour, minute=minute)

    if target < now:  # if the target is before now, add one day
        target += datetime.timedelta(days=1)

    diff = target - now
    return diff.seconds