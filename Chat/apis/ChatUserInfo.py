from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import ChatUser

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.user_sig import check_user_sig


class ChatUserInfo(View):
    """ 用户信息
    通过user_id获取用户
    """
    @method_decorator(check_user_sig)
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


