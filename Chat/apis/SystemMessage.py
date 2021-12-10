from django.views import View
import json

from Chat.models import ChatUser
from Chat.models import ChatLog

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.session import get_or_create_single_session_by_user_ids
from utils.logger import logger
from utils.chatting import send_to_user_by_user_id
from utils.chatting import State


# 系统通知作为聊天系统的user_id
system_user_id = '000002'


class SystemMessage(View):
    """ 系统消息
    """
    def post(self, request):
        """ 系统消息
        发送者是系统，一个固定的用户，接收者是user_id列表或者所有用户
        """
        # 获取信息
        receive_user_id_list = request.POST.getlist('receive_user_id_list')
        send_all_user = request.POST.get('send_all_user')  # 是否发送所有用户，给字符串total就是发送所有用户，就可以不用给上面那个list
        to_send_content = json.loads(request.POST.get('to_send_content'))

        # 取出系统通知用户
        try:
            system_user = ChatUser.objects.get(id=system_user_id)
        except ChatUser.DoesNotExist:
            # 未取到系统通知用户
            error_message = f'未取到系统通知用户 {system_user_id}'
            logger.error(error_message)
            return response_404(
                message=error_message,
            )
        # 取到系统通知用户了

        # 取出接收者们
        # 判断是否给了发送所有用户标志
        if send_all_user == 'total':
            # 发送所有聊天用户，系统预留用户除外
            receivers = ChatUser.objects.exclude(
                user_id__in=['000001', '000002'],  # 排除掉系统预留用户们
            )
        else:
            # 发送指定用户
            receivers = ChatUser.objects.filter(
                user_id__in=receive_user_id_list,
            )
        # 取出接收者们了

        # 遍历接收者们
        for receiver in receivers:
            # 获取发送者与接收者的会话session
            session = get_or_create_single_session_by_user_ids(user_id_list=[system_user_id, receiver.user_id])
            # 保存聊天记录
            new_chat_log = ChatLog.objects.create(
                sender=system_user,
                session=session,
                content=to_send_content,
            )
            # 给接收者发消息
            send_to_user_by_user_id(
                user_id=receiver.user_id,
                content={
                    'type': State.MESSAGE_RECEIVED,  # 收到消息
                    'chat_log': new_chat_log.session_add_out_info(self_user_id=receiver.user_id),
                },
            )

        # 返回成功响应
        return response_200(
            message='发送成功',
            data={
                'message': 'ok',
            },
        )



