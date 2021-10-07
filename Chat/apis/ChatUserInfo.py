from django.views import View

from Chat.models import ChatUser

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404


class ChatUserInfo(View):
    """ 用户信息
    通过user_id获取用户
    """
    def get(self, request):
        """ 通过user_id来获取用户信息
        """
        user_id = request.GET.get('user_id')

        # 取出该用户
        try:
            chat_user = ChatUser.objects.get(user_id=user_id)
        except ChatUser.DoesNotExist:
            # 未取到该用户，返回404
            return response_404(message='未取到该用户')
        # 取到该用户了

        # 返回用户信息
        return response_200(
            message='获取成功',
            data={
                'chat_user': chat_user.out_info(),
            },
        )


