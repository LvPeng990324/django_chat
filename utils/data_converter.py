# 数据转换器工具
import datetime
from typing import Text


def date_to_str(date: datetime.date) -> Text:
    """ 日期转字符串方法
    格式：YYYY-MM-DD
    """
    if not date:
        return date
    return date.strftime('%Y-%m-%d')


def datetime_to_str(time: datetime.datetime) -> Text:
    """ 时间转字符串方法
    格式：YYYY-MM-DD hh:mm:ss
    """
    if not time:
        return time
    return time.strftime('%Y-%m-%d %H:%M:%S')
