from django.views import View
from django.core.paginator import Paginator

from Chat.models import ChatLog

from utils.custom_reponse import response_200


class ChatLogInfo(View):
    """ 聊天记录
    """
    def get(self, request):
        """ 获取聊天记录
        """
        # 获取信息
        # user_id = request.GET.get('user_id')
        session_id = request.GET.get('session_id')
        # 分页信息
        page_size = request.GET.get('page_size', 10)
        page_num = request.GET.get('page_num', 1)
        total = request.GET.get('total')  # 给了内容就不分页，直接给所有

        # 获取这些聊天记录
        chat_logs = ChatLog.objects.filter(
            session_id=session_id,
        ).order_by('-create_time')  # 按照创建时间逆序排序

        # 判断是否给了total
        if not total:
            # 加入分页
            num_of_chat_logs = chat_logs.count()  # 统计此session的聊天记录总数
            chat_logs_paged = Paginator(chat_logs, page_size)
            chat_logs = chat_logs_paged.page(page_num).object_list  # 取出第page_num页
            num_of_pages = chat_logs_paged.num_pages  # 获取一共多少页
        else:
            # 不分页，不操作，补充变量完整
            num_of_chat_logs = None
            num_of_pages = None

        # 打包聊天记录
        chat_log_info_list = []
        for chat_log in chat_logs:
            chat_log_info_list.append(chat_log.base_out_info())

        # 返回响应
        return response_200(
            message='获取成功',
            data={
                'num_of_chat_logs': num_of_chat_logs,  # 此会话的聊天记录总数
                'chat_log_info_list': chat_log_info_list,  # 聊天记录信息列表
                'num_of_pages': num_of_pages,  # 一共多少页
            }
        )




