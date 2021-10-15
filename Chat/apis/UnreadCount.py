from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import ChatUser
from Chat.models import Session
from Chat.models import ChatLog

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers


class UnreadCount(View):
    """ 获取用户未读消息数量
    目前仅限单聊
    """
    @method_decorator(check_user_sig)
    def get(self, request):
        # 从headers中获取user_id
        user_id = get_user_id_from_headers(headers=request.headers)

        # 筛选该用户的所有未读信息并统计数量
        unread_count = ChatLog.objects.filter(
            session__chat_users__user_id__contains=user_id,  # 要这个用户参与的会话的
            have_read=False,  # 要未读的
        ).exclude(
            sender__user_id=user_id,  # 不要发送者是当前用户的，也即接收者是当前用户的
        ).count()

        return response_200(
            message='获取成功',
            data={
                'unread_count': unread_count,
            }
        )

