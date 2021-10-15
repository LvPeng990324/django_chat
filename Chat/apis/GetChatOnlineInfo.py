from django.views import View
import sys

from Chat.websockets.Chat import online_user_dict

from utils.custom_reponse import response_200


class GetChatOnlineInfo(View):
    """ 获取聊天在线信息（目前仅调试用）
    """
    def get(self, request):
        return response_200(
            message='获取成功',
            data={
                'dict_memory_used': sys.getsizeof(online_user_dict),  # 变量占用内存，单位字节
                'online_user_dict': str(online_user_dict),
            }
        )


