from django.db import models

from utils.data_converter import datetime_to_str
from utils.data_converter import get_media_url


class ChatFile(models.Model):
    """ 聊天文件
    """
    md5 = models.CharField(max_length=32, verbose_name='文件md5', help_text='文件md5')
    file = models.FileField(upload_to='media/chat_file', verbose_name='聊天文件', help_text='聊天文件')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name_plural = '聊天文件'
        verbose_name = '聊天文件'

    def __str__(self):
        return '{}-{}'.format(
            self.id,
            self.file.name,
        )

    def out_info(self):
        """ 对外信息
        """
        return {
            'id': self.id,
            'md5': self.md5,
            'create_time': datetime_to_str(self.create_time),
            'url': get_media_url(self.file.url),
        }

