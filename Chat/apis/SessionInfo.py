from django.views import View
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from Chat.models import Session

from utils.custom_reponse import response_200
from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers


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
        page_size = request.GET.get('page_size', 10)
        page_num = request.GET.get('page_num', 1)
        total = request.GET.get('total')  # 只要给了就是不分页

        # 获取这个人的会话们
        sessions = Session.objects.filter(
            chat_users__user_id__contains=user_id,
        ).order_by('-recently_active_time')  # 根据最近活跃时间排序

        # 判断是否给了total
        if not total:
            # 加入分页
            num_of_sessions = sessions.count()  # 统计session总数
            sessions_paged = Paginator(sessions, page_size)
            sessions = sessions_paged.page(page_num)  # 取出第page_num页
            num_of_pages = sessions_paged.num_pages  # 获取一共有多少页
        else:
            # 不分页，不操作，补充变量完整
            num_of_sessions = None
            num_of_pages = None

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
                'num_of_pages': num_of_pages,  # 一共多少页
            }
        )


