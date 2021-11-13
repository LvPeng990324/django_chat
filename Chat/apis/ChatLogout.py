from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import ChatUser

from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.logger import logger
from utils.chatting import logout_device_dict
from utils.chatting import online_user_dict
from utils.chatting import State


class ChatLogout(View):
    """ 聊天登出
    聊天系统是可以不断开连接手动登出再登录的
    """
    @method_decorator(check_user_sig)
    def post(self, request):
        """ 登出
        """
        # headers中获取user_id
        user_id = get_user_id_from_headers(headers=request.headers)

        # 获取设备id
        device_id = request.POST.get('device_id')

        # 取出该用户已登录设备们
        user_device_dict = online_user_dict.get(user_id)
        if user_device_dict is None:
            # 该用户无已登录设备
            return response_404(
                message='该用户无已登录设备',
            )
        # 取出该用户已登录设备们了

        # 取出该设备
        chat_device = user_device_dict.get(device_id)
        if chat_device is None:
            # 该用户下无该设备登录记录
            return response_404(
                message='该用户下无该设备登录记录',
            )
        # 取到该设备了

        # 记录该设备到未登录记录中
        logout_device_dict[device_id] = chat_device

        # 清空用户登录信息
        chat_device.user_id = None
        chat_device.state = State.LOGOUT_SUCCESS
        chat_device.chat_user_db = None

        # 记录日志
        logger.info(f'{user_id} 已登出 {device_id}')

        # ws发送登出成功生命周期
        chat_device.send_json(content={
            'type': State.LOGOUT_SUCCESS,  # 登出成功
        })

        # 返回登出成功
        return response_200(
            message='登出成功',
            data={
                'type': State.LOGOUT_SUCCESS,  # 登出成功
            }
        )
