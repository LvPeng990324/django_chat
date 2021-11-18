from django.views import View

from Chat.models import ChatUser
from Chat.models import ChatLog

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.session import get_or_create_single_session_by_user_ids
from utils.logger import logger
from utils.chatting import send_to_user_by_user_id
from utils.chatting import State


class MassMessage(View):
    """ 群发消息
    """
    def post(self, request):
        """ 群发消息
        传消息发送者user_id和接收者user_id列表以及要发的文本内容
        """
        # 获取信息
        send_user_id = request.POST.get('send_user_id')
        receive_user_id_list = request.POST.getlist('receive_user_id_list')
        to_send_text = request.POST.get('to_send_text')

        # 取出发送者
        try:
            sender = ChatUser.objects.get(user_id=send_user_id, is_delete=False)
        except ChatUser.DoesNotExist:
            # 未取到发送者
            error_message = f'群发消息未取到发送者 {send_user_id}'
            logger.error(error_message)
            return response_404(
                message=error_message,
            )
        # 取出接收者们
        receivers = ChatUser.objects.filter(
            user_id__in=receive_user_id_list,
            is_delete=False,
        )

        # 遍历接收者id列表
        for receiver in receivers:

            # 获取发送者与该接收者的会话session
            session = get_or_create_single_session_by_user_ids(user_id_list=[send_user_id, receiver.user_id])
            # 保存聊天记录
            new_chat_log = ChatLog.objects.create(
                sender=sender,
                session=session,
                content={  # 这里的格式是根据前端读取解析的数据格式来的
                    'text': to_send_text,
                    'type': 'text',
                },
            )
            # 给接收者发送消息
            send_to_user_by_user_id(
                user_id=receiver.user_id,
                content={
                    'type': State.MESSAGE_RECEIVED,  # 收到消息
                    'chat_log': new_chat_log.session_add_out_info(self_user_id=receiver.user_id),
                },
            )
            # 给发送者成功消息
            send_to_user_by_user_id(
                user_id=sender.user_id,
                content={
                    'type': State.MESSAGE_SEND_SUCCESS,  # 消息发送成功
                    'chat_log': new_chat_log.session_add_out_info(self_user_id=sender.user_id),
                },
            )

        # 返回成功响应
        return response_200(
            message='发送成功',
            data={
                'message': 'ok',
            }
        )

