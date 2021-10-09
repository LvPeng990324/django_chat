from channels.generic.websocket import JsonWebsocketConsumer
from django_redis import get_redis_connection
import time

from Chat.models import ChatUser
from Chat.models import ChatLog
from Chat.models import Session

from utils.logger import logger
from utils.session import get_or_create_single_session_by_user_ids
from utils.session import get_session_by_session_id

online_user_dict = {}  # 记录在线的用户字典


# 生命周期状态
class State:
    SDK_READY = 'sdkStateReady'  # 通道已建立,可以发送消息了
    MESSAGE_RECEIVED = 'onMessageReceived'  # 收到推送的单聊、群聊、群提示、群系统通知的新消息
    MESSAGE_SEND_SUCCESS = 'onMessageSendSuccess'  # 消息发送成功的响应
    ERROR = 'error'  # 收到 SDK 发生错误通知
    KICKED_OUT = 'kickedOut'  # 收到被踢下线通知


class ChatConsumer(JsonWebsocketConsumer):
    """ 聊天
    TODO 多端有待支持，记录在线用户的字典的value应该改为一个列表，内容是这个用户的每个端的对象，收到消息时遍历发送
    """
    def connect(self):
        """ 连接建立
        """
        # 获取连接认证信息
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # 获取user_id
        user_sig = self.scope['url_route']['kwargs']['user_sig']  # 获取user_sig

        # 认证检查
        if not self.check_chat_user_auth(user_sig):
            # 认证失败，关闭连接
            logger.warning('{} chat认证失败'.format(self.user_id))
            self.close(code=4003)
        # 认证通过
        # 记录聊天用户对象
        try:
            self.chat_user_db = ChatUser.objects.get(user_id=self.user_id)
        except ChatUser.DoesNotExist:
            # 没取到该用户
            self.close(code=4004)
        # 记录到该聊天用户对象了

        # 建立连接
        self.accept()
        # 记录在线
        online_user_dict[self.user_id] = self
        # 更新登录时间
        self.chat_user_db.update_login_time()

        # 返回通道建立状态
        # self.send_json(content={
        #     'type': State.SDK_READY,  # 通道已建立
        # })

    def disconnect(self, code):
        """ 连接断开
        """
        # 发送下线通知
        self.send_json(content={
            'type': State.KICKED_OUT,  # 下线通知
        })
        # 从连接中删除
        if self.user_id in online_user_dict:
            online_user_dict.pop(self.user_id)

    def receive_json(self, content, **kwargs):
        """ 收到前端来的消息
        """
        # 取出接收消息的session_id
        receiver_session_id = content.get('to_session')  # 取出接收消息的session_id

        # 取出这个session
        receiver_session = get_session_by_session_id(session_id=receiver_session_id)

        # 保存聊天记录
        new_chat_log = self.save_message(sender=self.chat_user_db, session=receiver_session, content=content.get('content'))

        # 给此session中在线的chat_user发消息
        to_chat_user_id_list = list(receiver_session.chat_users.exclude(self.chat_user_db).values_list('user_id', flat=True))  # 获取除了自己的用户user_id列表
        # 遍历这些用户，给在线的发消息
        for to_chat_user_id in to_chat_user_id_list:
            if to_chat_user_id in online_user_dict:
                # 此用户在线，发消息
                online_user_dict.get(to_chat_user_id).send_json(content={
                    'type': State.MESSAGE_RECEIVED,  # 收到消息
                    'chat_log': new_chat_log.session_add_out_info(self_user_id=to_chat_user_id),  # 消息info
                })
            else:
                # 此用户不在线，暂时不采取动作
                pass
        # 给发送者发送成功响应
        self.send_json(content={
            'type': State.MESSAGE_SEND_SUCCESS,  # 消息发送成功
            'chat_log': new_chat_log.session_add_out_info(self_user_id=self.user_id),  # 消息info
        })

    def save_message(self, sender: ChatUser, session: Session, content: str):
        """ TODO 保存聊天记录
        供以上方法调用
        """
        new_chat_log = ChatLog.objects.create(
            sender=sender,
            session=session,
            content=content,
        )
        return new_chat_log

    def check_chat_user_auth(self, user_sig: str):
        """ 检查用户认证信息
        用于连接建立的信息检查，通过返回True，不通过False
        """
        redis_cli = get_redis_connection('userSig')
        return redis_cli.get(user_sig) == self.user_id.encode('utf8')
