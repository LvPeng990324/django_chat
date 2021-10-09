# 数据转换器工具
import datetime
from typing import Text
from django_chat.settings import DEPLOY_DOMAIN


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


def get_media_url(file_url):
    """ 获取文件访问URL方法
    将传来的路径直接拼接部署域名
    """
    return DEPLOY_DOMAIN + file_url
