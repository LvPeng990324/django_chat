from django.views import View
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from Chat.models import ChatLog

from utils.custom_reponse import response_200
from utils.user_sig import check_user_sig


class ChatLogInfo(View):
    """ 聊天记录
    """
    @method_decorator(check_user_sig)
    def get(self, request):
        """ 获取聊天记录
        TODO 这里考虑要不要验证下要请求的session是否包含当前用户，防止利用接口查看别人聊天记录问题
        """
        # 获取信息
        session_id = request.GET.get('session_id')
        # 分页信息
        offset = request.GET.get('offset', 0)  # 偏移量
        length = request.GET.get('length', 10)  # 获取长度
        total = request.GET.get('total')  # 给了内容就不分页，直接给所有

        # 获取这些聊天记录
        chat_logs = ChatLog.objects.filter(
            session_id=session_id,
        ).order_by('-create_time')  # 按照创建时间逆序排序

        num_of_chat_logs = chat_logs.count()  # 统计此session的聊天记录总数

        # 判断是否给了total
        if not total:
            chat_logs = chat_logs[offset: offset+length]  # 取这一段
        else:
            # 给所有
            pass

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
            }
        )




