# 聊天相关工具方法

from Chat.models import ChatUser

from utils.custom_reponse import response_404
from utils.custom_reponse import response_200
from utils.user_sig import get_user_id_from_headers
from utils.logger import logger


# 生命周期状态
class State:
    LOGIN_SUCCESS = 'loginSuccess'  # 聊天登录认证成功，可以收发消息了
    LOGOUT_SUCCESS = 'logoutSuccess'  # 聊天登出成功，可以再次登录了
    MESSAGE_RECEIVED = 'onMessageReceived'  # 收到推送的单聊、群聊、群提示、群系统通知的新消息
    MESSAGE_SEND_SUCCESS = 'onMessageSendSuccess'  # 消息发送成功的响应
    ERROR = 'error'  # 收到 SDK 发生错误通知
    KICKED_OUT = 'kickedOut'  # 收到被踢下线通知


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
online_user_dict = {}  # 记录在线的用户字典
logout_device_dict = {}  # 记录还没登录的连接{设备id: 聊天对象}映射关系


def delete_login_device_record(user_id, device_id):
    """ 删除已登录设备记录
    """
    # 取出该用户已登录的设备们
    user_device_dict = online_user_dict.get(user_id)
    if user_device_dict is None:
        # 该用户无已登录设备
        logger.error(f'{user_id} 没有已登录的 {device_id}')
        return False
    # 取出该用户已登录设备们了

    # 找到并删除该用户下的该设备
    if device_id in user_device_dict.keys():
        # 删除该记录
        online_user_dict[user_id].pop(device_id)
        logger.info(f'{user_id} 已登录设备 {device_id} 断开连接')
        # 如果该用户已无已登录设备，就从在线记录中删除该用户
        if online_user_dict[user_id] == {}:
            online_user_dict.pop(user_id)
        return True
    else:
        # 该用户下无登录的该设备
        logger.error(f'{user_id} 没有已登录的 {device_id}')
        return False


def delete_logout_device_record(device_id):
    """ 删除未登录设备记录
    """
    # 找到并删除该设备记录
    if device_id in logout_device_dict.keys():
        # 删除该记录
        logout_device_dict.pop(device_id)
        logger.info(f'{device_id} 断开连接')
        return True
    else:
        # 未登录中无该设备记录
        logger.error(f'{device_id} 无未登录记录')
        return False


