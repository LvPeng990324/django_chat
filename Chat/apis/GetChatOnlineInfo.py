from django.views import View
import sys

from utils.chatting import online_user_dict
from utils.chatting import logout_device_dict

from utils.custom_reponse import response_200


class GetChatOnlineInfo(View):
    """ 获取聊天在线信息（目前仅调试用）
    """
    def get(self, request):
        return response_200(
            message='获取成功',
            data={
                # 变量占用内存，单位字节
                'online_user_dict_memory_used': sys.getsizeof(online_user_dict),
                'logout_device_dict_memory_used': sys.getsizeof(logout_device_dict),

                'online_user_dict': str(online_user_dict),
                'logout_device_dict': str(logout_device_dict),
            }
        )


