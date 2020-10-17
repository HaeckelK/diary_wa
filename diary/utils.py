import calendar
import datetime


def all_days_in_month(year: int, month: int):
    num_days = calendar.monthrange(year, month)[1]
    month_text = f"{month:02d}"
    year_text = f"{year:04d}"
    dates = [year_text + month_text + f"{day:02d}" for day in range(1, num_days+1)]
    return dates


def last_n_days(n):
    today = datetime.datetime.now()
    days = []
    for i in range(n):
        delta = datetime.timedelta(days=i)
        a = today - delta
        days.append(a.strftime("%Y%m%d"))
    return days


def today(date_format='%Y%m%d', string=False):
    date = datetime.datetime.today()
    if string is False:
        return date
    return date.strftime(date_format)


def datestamp(date_format='%Y%m%d'):
    return today(date_format, string=True)
