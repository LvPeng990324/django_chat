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


class ChatLogin(View):
    """ 聊天登录
    聊天系统是先建立ws连接然后手动登录的
    """
    @method_decorator(check_user_sig)
    def post(self, request):
        """ 登录
        """
        # 从headers中获取user_id
        user_id = get_user_id_from_headers(headers=request.headers)

        # 获取设备id
        device_id = request.POST.get('device_id')

        # 从未登录连接设备中取出该设备（聊天对象）
        if device_id in logout_device_dict.keys():
            # 从未登录记录中弹出该设备
            chat_device = logout_device_dict.pop(device_id)
        else:
            # 未取到该设备
            return response_404(
                message='未取到该设备',
            )
        # 取出设备了

        # 取出该用户
        try:
            chat_user = ChatUser.objects.get(user_id=user_id)
        except ChatUser.DoesNotExist:
            # 未取到该用户
            return response_404(
                message='未找到该用户',
            )

        # 记录到在线用户中
        # 判断这个账户是否有在线记录
        if user_id not in online_user_dict.keys():
            # 没有在线记录，创建一个空记录
            online_user_dict[user_id] = {}  # 这里面之后用来放这个账户下的在线设备们
        # 记录当前设备在线
        online_user_dict[user_id][device_id] = chat_device
        # 记录用户信息到该设备（聊天对象）中
        chat_device.user_id = user_id
        chat_device.state = State.LOGIN_SUCCESS
        chat_device.chat_user_db = chat_user

        # 更新登录时间
        chat_user.update_login_time()

        # 记录日志
        logger.info(f'{user_id} 已登录为 {device_id}')

        # 返回登录成功
        return response_200(
            message='登录成功',
            data={
                'type': State.LOGIN_SUCCESS,  # 登录成功
            }
        )

