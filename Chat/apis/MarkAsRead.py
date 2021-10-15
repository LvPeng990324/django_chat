from django.views import View
from django.utils.decorators import method_decorator
import datetime

from Chat.models import ChatLog
from Chat.models import ChatUser
from Chat.models import Session
from Chat.models import SessionTypeOption

from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.logger import logger


class SingleChatMarkAsRead(View):
    """ 单聊标记为已读
    待确认：如果一个人的一个会话未读消息太多了，他只加载了最近的几条，那么之前的那些未读消息要不要改已读，
          但是，如果只标记了部分已读的话，那么就会出现点击进入一个会话页面再退出的话，这个会话列表项还会有未读的红点提示
          先这么做吧，如果后面有问题要改动，再考虑其他办法
    目前是会将这个会话中接收方是当前用户的所有消息全标记为已读
    """
    @method_decorator(check_user_sig)
    def post(self, request):
        # 获取session_id
        session_id = request.POST.get('session_id')
        # 从headers中获取user_id
        user_id = get_user_id_from_headers(headers=request.headers)
        # 取出该用户
        try:
            chat_user = ChatUser.objects.get(user_id=user_id)
        except ChatUser.DoesNotExist:
            # 未取到该用户
            return response_404(
                message='未取到该用户',
            )
        # 取到该用户了

        # 取出这个用户参与的该session
        try:
            session = Session.objects.get(
                id=session_id,  # 要这个id的session
                type=SessionTypeOption.SINGLE,  # 要单聊的
                chat_users__user_id__contains=user_id,  # 要这个用户参与的
            )
        except Session.DoesNotExist:
            # 未取到符合条件的，session不存在或者该用户未参与
            return response_404(
                message='session不存在或该用户未参与该会话',
            )
        # 取到session了

        # 将这个session中当前用户的所有未读消息标记为已读
        to_mark_chat_logs = ChatLog.objects.filter(
            session=session,  # 要这个session的
            have_read=False,  # 要未读的
        ).exclude(
            sender=chat_user,  # 不要发送者是当前用户的，也即接收者是当前用户的
        )
        # 标记为已读并记录已读时间
        to_mark_chat_logs.update(
            have_read=True,  # 标记已读
            read_time=datetime.datetime.now(),  # 记录当前时间为已读时间
        )

        # 记录已读条数
        marked_count = to_mark_chat_logs.count()

        # 记录日志
        logger.info(f'{user_id} 已读 {session_id} 会话的 {marked_count} 条信息')

        # 返回成功响应
        return response_200(
            message='标记成功',
            data={
                'marked_count': marked_count,  # 已读条数
            }
        )



