from django.db import models
import datetime

from utils.data_converter import datetime_to_str
from utils.data_converter import date_to_str


class ChatUser(models.Model):
    """ 聊天用户
    """
    user_id = models.CharField(unique=True, max_length=128, verbose_name='用户id', help_text='用户id')  # 用户自定义，唯一
    name = models.CharField(null=True, blank=True, max_length=64, verbose_name='姓名', help_text='姓名')
    nickname = models.CharField(null=True, blank=True, max_length=128, verbose_name='昵称', help_text='昵称')
    username = models.CharField(null=True, blank=True, max_length=128, verbose_name='用户名', help_text='用户名')
    gender = models.CharField(null=True, blank=True, max_length=8, verbose_name='性别', help_text='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期', help_text='出生日期')
    id_card_num = models.CharField(null=True, blank=True, max_length=32, verbose_name='身份证号', help_text='身份证号')
    phone = models.CharField(null=True, blank=True, max_length=16, verbose_name='手机号', help_text='手机号')
    email = models.CharField(null=True, blank=True, max_length=128, verbose_name='电子邮箱', help_text='电子邮箱')
    province = models.CharField(null=True, blank=True, max_length=32, verbose_name='省', help_text='省')
    city = models.CharField(null=True, blank=True, max_length=32, verbose_name='市', help_text='市')
    avatar = models.CharField(null=True, blank=True, max_length=128, verbose_name='头像', help_text='头像')
    description = models.TextField(null=True, blank=True, verbose_name='描述', help_text='描述')

    is_disable = models.BooleanField(default=False, verbose_name='是否禁用', help_text='是否禁用')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除', help_text='是否删除')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='最近登录时间', help_text='最近登录时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name_plural = '聊天用户'
        verbose_name = '聊天用户'

    def __str__(self):
        return '{id}-{name}'.format(
            id=self.id,
            name=self.name,
        )

    def out_info(self) -> dict:
        """ 对外信息
        """
        return {
            'user_id': self.user_id,
            'name': self.name,
            'nickname': self.nickname,
            'username': self.username,
            'gender': self.gender,
            'birthday': date_to_str(self.birthday),
            'id_card_num': self.id_card_num,
            'phone': self.phone,
            'email': self.email,
            'province': self.province,
            'city': self.city,
            'avatar': self.avatar,
            'description': self.description,
            'is_disable': self.is_disable,
            'login_time': datetime_to_str(self.login_time),
            'create_time': datetime_to_str(self.create_time),
        }

    def update_login_time(self):
        """ 更新最近登录时间
        """
        self.login_time = datetime.datetime.now()
        self.save()


class SessionTypeOption(models.IntegerChoices):
    """ 聊天会话选项
    """
    SINGLE = 1, '单聊'
    GROUP = 2, '群聊'


class Session(models.Model):
    """ 聊天会话
    """
    name = models.CharField(max_length=128, verbose_name='会话名', help_text='会话名')
    type = models.IntegerField(
        choices=SessionTypeOption.choices,
        verbose_name='会话类型',
        help_text='会话类型',
    )
    chat_users = models.ManyToManyField(ChatUser, verbose_name='会话参与者', help_text='会话参与者')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name_plural = '聊天会话'
        verbose_name = '聊天会话'

    def __str__(self):
        return '{}-{}'.format(
            self.id,
            self.name,
        )

    def out_info(self, self_user_id):
        """ 对外信息
        """
        if self.type == SessionTypeOption.SINGLE:
            # 单聊
            session_info = self.session_info_single(self_user_id=self_user_id)
        elif self.type == SessionTypeOption.GROUP:
            # 群聊
            session_info = self.session_info_group()
        else:
            session_info = {}
        return {
            'session_id': self.id,  # session的id
            'type': self.type,  # session的type
            'name': self.name,  # session的名字
            'session_info': session_info,  # session信息
            'create_time': datetime_to_str(self.create_time),  # session的创建时间
            'unread_count': self.get_unread_count(),  # 未读消息数
            'recently_chat_log': self.get_recently_chat_log(),  # 最近一条消息
        }

    def session_info_single(self, self_user_id):
        """ 单聊的session信息
        单聊的session信息就是对方(ChatUser)的信息
        接收己方的user_id，然后从本session的chat_users中排除掉己方，剩下的那个就是对方
        """
        # TODO 性能待优化 如果两个人是一个人（自己给自己发消息），就取出第一个
        if self.chat_users.first().id == self.chat_users.last().id:
            # 一个人
            another_chat_user = self.chat_users.first()
        else:
            another_chat_user = self.chat_users.exclude(user_id=self_user_id).first()
        return another_chat_user.out_info()

    def session_info_group(self):
        """ TODO 群聊的session信息
        """
        return {}

    def get_unread_count(self) -> int:
        """ 获取未读消息数
        """
        return ChatLog.objects.filter(
            session=self,  # 要session是本session的
            have_read=False,  # 要未读的
        ).count()

    def get_recently_chat_log(self) -> dict:
        """ 最近一条消息
        """
        recently_chat_log = ChatLog.objects.filter(
            session=self,  # 要session是本session的
        ).last()  # 要最后一条
        return recently_chat_log.base_out_info()

    def get_chat_user_info_list(self) -> list:
        """ 获取参与用户信息
        """
        chat_users = ChatUser.objects.filter(
            session=self,  # session要本session
        )
        chat_user_info_list = []
        for chat_user in chat_users:
            chat_user_info_list.append(chat_user.out_info())
        return chat_user_info_list


class ChatLog(models.Model):
    """ 聊天记录
    """
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='single_chat_log_sender', verbose_name='发送者', help_text='发送者')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='聊天会话', help_text='聊天会话')
    have_read = models.BooleanField(default=False, verbose_name='已读', help_text='已读')
    read_time = models.DateTimeField(null=True, blank=True, verbose_name='已读时间', help_text='已读时间')
    content = models.JSONField(verbose_name='内容', help_text='内容')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name_plural = '聊天记录'
        verbose_name = '聊天记录'

    def __str__(self):
        return '{}-{}-{}'.format(
            self.create_time,
            self.sender.name,
            self.session.name,
        )

    def session_add_out_info(self, self_user_id) -> dict:
        """ 附加了session信息的对外信息
        """
        info = self.base_out_info()
        info.update({
            'session': self.session.out_info(self_user_id=self_user_id),
        })
        return info

    def base_out_info(self) -> dict:
        """ 基础对外信息
        由于session中也有聊天记录信息，会导致无限套娃，所以这里单独搞了个基础的，不包含session信息
        """
        return {
            'id': self.id,
            'have_read': self.have_read,
            'read_time': datetime_to_str(self.read_time),
            'content': self.content,
            'sender': self.sender.user_id,
            'create_time': datetime_to_str(self.create_time),
        }



