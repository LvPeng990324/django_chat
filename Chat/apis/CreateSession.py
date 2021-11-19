from django.views import View
from django.utils.decorators import method_decorator
import json

from Chat.models import Session
from Chat.models import SessionTypeOption
from Chat.models import ChatUser

from utils.custom_reponse import response_200
from utils.custom_reponse import response_400
from utils.custom_reponse import response_404
from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.chatting import send_to_user_by_user_id
from utils.chatting import State


class CreateSession(View):
    """ 创建会话
    """
    @method_decorator(check_user_sig)
    def post(self, request):
        """ 创建会话
        """
        name = request.POST.get('name')  # 会话名，可重复，不可空
        session_type = request.POST.get('type')  # 会话类型，单选：1单聊、2群聊
        chat_user_id_list = json.loads(request.POST.get('chat_user_id_list'))  # 会话参与者的user_id列表
        self_user_id = get_user_id_from_headers(headers=request.headers)

        print(request.POST)
        print(type(chat_user_id_list), chat_user_id_list)

        # 转换会话类型
        if session_type not in [1, '1', 2, '2']:
            # 格式有误
            return response_400(
                message='会话类型格式有误，只能为1或者2，int或者str',
            )
        session_type = SessionTypeOption(int(session_type))

        # 判断是否存在这个单聊session
        # 规则是chat_users一样就是
        if session_type in [1, '1']:
            # 单聊，进行重复判断
            session_exists = Session.objects.filter(
                type=SessionTypeOption.SINGLE,  # 要单聊地
                chat_users__user_id=chat_user_id_list[0],  # 要包含第一个
            ).filter(
                chat_users__user_id=chat_user_id_list[1],  # 要包含第二个
            )
            if session_exists.exists():
                # 已存在
                session_exists = session_exists.first()
                return response_200(
                    message='已存在，不需创建',
                    data={
                        'session': session_exists.out_info(self_user_id=self_user_id),
                    },
                )

        # 取出这些参与者用户
        chat_user_list = []
        for chat_user_id in chat_user_id_list:
            try:
                chat_user = ChatUser.objects.get(user_id=chat_user_id)
            except ChatUser.DoesNotExist:
                # 未取到当前用户
                return response_404(
                    message='未取到user_id为 {} 的用户'.format(chat_user_id),
                )
            # 记录下来
            chat_user_list.append(chat_user)
        # 取到这些参与者用户了

        # 创建会话
        new_session = Session.objects.create(
            name=name,
            type=session_type,
        )
        new_session.chat_users.add(*chat_user_list)  # 添加参与者

        # 遍历新会话的参与者们，给他们的在线设备发送会话更新生命周期
        for chat_user_id in chat_user_id_list:
            send_to_user_by_user_id(
                user_id=chat_user_id,
                content={
                    'type': State.CONVERSATION_CREATED,  # 会话创建
                    'session': new_session.out_info(self_user_id=self_user_id),
                },
            )

        # 返回成功信息
        return response_200(
            message='创建成功',
            data={},  # 这里不需要数据
        )



