from channels.generic.websocket import JsonWebsocketConsumer
from django_redis import get_redis_connection
import time
import string
import random

from Chat.models import ChatUser
from Chat.models import ChatLog
from Chat.models import Session

from utils.logger import logger
from utils.session import get_or_create_single_session_by_user_ids
from utils.session import get_session_by_session_id
from utils.chatting import State
from utils.chatting import online_user_dict
from utils.chatting import logout_device_dict
from utils.chatting import delete_login_device_record
from utils.chatting import delete_logout_device_record


class ChatConsumer(JsonWebsocketConsumer):
    """ 聊天
    先建立连接再进行用户登录
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_id = gen_device_id()  # 记录随机生成的设备id
        self.state = State.LOGOUT_SUCCESS  # 默认状态是已登出
        self.user_id = None  # 记录user_id
        self.chat_user_db = None  # 记录聊天用户的数据库对象

    def connect(self):
        """ 连接建立
        """
        # 建立连接
        self.accept()
        # 记录该未登录连接
        logout_device_dict[self.device_id] = self
        # 返回device_id
        self.send_json(content={
            'type': 'deviceNo',
            'device_id': self.device_id,
        })
        # 记录日志
        logger.info(f'{self.device_id} 已连接')

    def disconnect(self, code):
        """ 连接断开
        """
        # 发送断开通知
        self.send_json(content={
            'type': State.KICKED_OUT,  # 断开通知
        })
        # 判断当前连接状态，根据是否登录来进行动作
        if self.state == State.LOGIN_SUCCESS:
            # 已登录
            # 从已登录记录中删除
            delete_login_device_record(user_id=self.user_id, device_id=self.device_id)
        elif self.state == State.LOGOUT_SUCCESS:
            # 未登录
            # 从未登录记录中删除
            delete_logout_device_record(device_id=self.device_id)
        else:
            # 一般不会这样
            logger.error(f'{self.device_id} 断开连接时状态未知：{self.state}')

    def receive_json(self, content, **kwargs):
        """ 收到前端来的消息
        """
        # 判断状态，如果不是已登录就不给发
        if self.state != State.LOGIN_SUCCESS:
            # 不是已登录，不给发
            self.send_json(content={
                'message': '当前未登录',
            })

        # 取出接收消息的session_id
        receiver_session_id = content.get('to_session')  # 取出接收消息的session_id

        # 取出这个session
        receiver_session = get_session_by_session_id(session_id=receiver_session_id)

        # 保存聊天记录
        new_chat_log = self.save_message(sender=self.chat_user_db, session=receiver_session, content=content.get('content'))

        # 给此session中在线的chat_user发消息
        to_chat_user_id_list = list(receiver_session.chat_users.exclude(user_id=self.user_id).values_list('user_id', flat=True))  # 获取除了自己的用户user_id列表
        # 遍历这些用户，给在线的发消息
        for to_chat_user_id in to_chat_user_id_list:
            if to_chat_user_id in online_user_dict:
                # 此用户在线，给他在线的所有设备发消息
                for receiver_device_id, receiver_device in online_user_dict[to_chat_user_id].items():
                    receiver_device.send_json(content={
                        'type': State.MESSAGE_RECEIVED,  # 收到消息
                        'chat_log': new_chat_log.session_add_out_info(self_user_id=to_chat_user_id),  # 消息info
                    })
            else:
                # 此用户不在线，暂时不采取动作
                pass
        # 给发送者在线设备们发送成功响应
        for self_device_id, self_device in online_user_dict[self.user_id].items():
            self_device.send_json(content={
                'type': State.MESSAGE_SEND_SUCCESS,  # 消息发送成功
                'chat_log': new_chat_log.session_add_out_info(self_user_id=self.user_id),  # 消息info
            })

    def save_message(self, sender: ChatUser, session: Session, content: str):
        """ 保存聊天记录
        供以上方法调用
        """
        new_chat_log = ChatLog.objects.create(
            sender=sender,
            session=session,
            content=content,
        )
        return new_chat_log


def gen_device_id() -> str:
    """ 生成设备id方法
    8位长度的随机大小写字母加数字组成的字符串
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=8))

