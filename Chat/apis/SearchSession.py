from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import Session
from Chat.models import SessionTypeOption
from Chat.models import ChatUser

from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.custom_reponse import response_200
from utils.custom_reponse import response_404


class SearchSession(View):
    """ 搜素会话
    """
    @method_decorator(check_user_sig)
    def get(self, request):
        """ 搜索会话信息
        单聊：搜索对面name
        群聊：搜索session的name
        一次返回两个list

        默认给各前五条信息，给了total才给所有
        """
        # 获取信息
        search_text = request.GET.get('search_text')
        total = request.GET.get('total')

        # 从headers中获取当前用户的user_id
        user_id = get_user_id_from_headers(headers=request.headers)

        # 取出此用户的会话们
        sessions = Session.objects.filter(
            chat_users__user_id__contains=user_id,
        ).order_by('-recently_active_time')  # 根据最近活跃时间排序

        # 搜索单聊
        single_chat_sessions = sessions.filter(
            type=SessionTypeOption.SINGLE,  # 要单聊
            chat_users__name__contains=search_text,  # 要参与用户name包含搜索字段的，这样会有个问题，就是自己的name也会被算上
        )

        # 搜索群聊
        group_chat_sessions = sessions.filter(
            type=SessionTypeOption.GROUP,  # 要群聊
            name__contains=search_text,  # 要群聊session的name包含搜索字段的
        )

        # 判断是否给了total，没给就限制前5个
        if total != 'total':
            single_chat_sessions = single_chat_sessions[:5]
            group_chat_sessions = group_chat_sessions[:5]

        # 打包单聊session信息
        single_chat_session_info_list = []
        for single_chat_session in single_chat_sessions:
            single_chat_session_info_list.append(single_chat_session.out_info(self_user_id=user_id))
        # 打包群聊session信息
        group_chat_session_info_list = []
        for group_chat_session in group_chat_sessions:
            group_chat_session_info_list.append(group_chat_session.out_info(self_user_id=user_id))

        # 返回响应
        return response_200(
            message='获取成功',
            data={
                'single_chat_session_info_list': single_chat_session_info_list,
                'group_chat_session_info_list': group_chat_session_info_list,
            }
        )

