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

online_user_dict = {}  # 记录在线的用户字典
# 数据结构设计，支持同一用户多端在线收发消息：
# designing_online_user_dict = {
#     'user_id1': {  # 记录某一用户
#         'device_id1': '[ChatConsumer_1]',  # 记录这个用户的在线设备，value是ChatConsumer的实例
#         'device_id2': '[ChatConsumer_2]',
#     },
#     'user_id2': {
#         'device_id1': '[ChatConsumer_1]',
#     },
# }


# 生命周期状态
class State:
    SDK_READY = 'sdkStateReady'  # 通道已建立,可以发送消息了
    MESSAGE_RECEIVED = 'onMessageReceived'  # 收到推送的单聊、群聊、群提示、群系统通知的新消息
    MESSAGE_SEND_SUCCESS = 'onMessageSendSuccess'  # 消息发送成功的响应
    ERROR = 'error'  # 收到 SDK 发生错误通知
    KICKED_OUT = 'kickedOut'  # 收到被踢下线通知


class ChatConsumer(JsonWebsocketConsumer):
    """ 聊天
    """
    def connect(self):
        """ 连接建立
        """
        # 获取连接认证信息
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # 获取user_id
        user_sig = self.scope['url_route']['kwargs']['user_sig']  # 获取user_sig
        self.device_id = gen_device_id()  # 记录随机生成的设备id

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
        # 判断这个账户是否有在线记录
        if self.user_id not in online_user_dict.keys():
            # 没有在线记录，创建一个空记录
            online_user_dict[self.user_id] = {}  # 这里面之后用来放这个账户下的在线设备们
        # 记录当前设备在线
        online_user_dict[self.user_id][self.device_id] = self

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
        # 从连接中删除当前设备
        if self.user_id in online_user_dict:  # 检查当前用户在线状态
            if self.device_id in online_user_dict[self.user_id]:  # 检查当前设备在线状态
                online_user_dict[self.user_id].pop(self.device_id)  # 删除当前设备
            # 如果没有设备了，就把这个用户的在线状态记录删掉
            if not online_user_dict[self.user_id]:
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

    def check_chat_user_auth(self, user_sig: str):
        """ 检查用户认证信息
        用于连接建立的信息检查，通过返回True，不通过False
        """
        redis_cli = get_redis_connection('userSig')
        return redis_cli.get(user_sig) == self.user_id.encode('utf8')


def gen_device_id() -> str:
    """ 生成设备id方法
    8位长度的随机大小写字母加数字组成的字符串
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=8))

