from datetime import timedelta

from django import template
import datetime

from django.utils.timesince import timesince

register = template.Library()


@register.filter
def div(value, div):
    return format(round(round((value / div) / 1000000, 8) * 1000000, 2), ',').rstrip('0').rstrip('.')


@register.filter
def div_no_decimal(value, div):
    return format(round(round((float(value) / div) / 1000000, 8) * 1000000, 0), ',').rstrip('0').rstrip('.')


@register.filter
def number_stringify(value):
    return format(value, ',d')


@register.filter
def news_date_format(date):
    InputDateFormat = "%Y-%m-%d"
    OutputDateFormat = "%A, %d, %B, %y"
    date = datetime.datetime.strptime(date, InputDateFormat)
    date = datetime.datetime.strftime(date, OutputDateFormat)
    return date


@register.filter
def to_percent_format(value):
    value = "%.2f" % round(value * 100, 2)
    return str(value) + '%'


@register.filter
def financial_table_ve_css(value):
    if value < 0:
        return 'fr-table-text-red'
    else:
        return 'fr-table-text-info'


@register.filter
def date_formatter(string):
    try:
        year, month, date = str(string).split('-')
        month_year = month + '/' + year
        return month_year
    except:
        return string


@register.filter
def float_to_string(value):
    try:
        return int(value)
    except:
        return value


@register.filter
def timestamp_to_time(timestamp):
    return datetime.date.fromtimestamp(int(timestamp))


@register.filter
def time_to_naturaltime(value):
    now_date = datetime.datetime.now().date()
    try:
        difference = now_date - value
        if difference <= timedelta(hours=24):
            return 'less than 1 day'
        return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
    except:
        return value


