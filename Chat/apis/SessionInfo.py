from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import Session
from Chat.models import ChatUser

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.logger import logger


class SessionInfo(View):
    """ 会话信息
    """
    @method_decorator(check_user_sig)
    def get(self, request):
        """ 获取当前用户的会话信息列表
        """
        # 从headers中取出user_id
        user_id = get_user_id_from_headers(headers=request.headers)
        # 获取分页信息
        offset = int(request.GET.get('offset', 0))  # 偏移量
        length = int(request.GET.get('length', 10))  # 获取长度
        total = request.GET.get('total')  # 只要给了就是不分页

        # 取出当前用户
        try:
            chat_user = ChatUser.objects.get(user_id=user_id)
        except ChatUser.DoesNotExist:
            # 未取到该用户
            logger.error(f'用户 {user_id} 未找到')
            return response_404(
                message='用户未找到',
            )
        # 取出该用户了

        # 获取这个人的会话们
        sessions = Session.objects.filter(
            chat_users=chat_user,
        ).order_by('-recently_active_time')  # 根据最近活跃时间排序

        num_of_sessions = sessions.count()  # 统计session总数

        # 判断是否给了total
        if total != 'total':
            sessions = sessions[offset: offset+length]  # 取出这一段
        else:
            # 不分页，不操作
            pass

        # 打包session信息
        session_info_list = []
        for session in sessions:
            session_info_list.append(session.out_info(self_user_id=user_id))

        # 返回响应
        return response_200(
            message='获取成功',
            data={
                'num_of_sessions': num_of_sessions,  # session总数
                'session_info_list': session_info_list,  # session信息列表
            }
        )


