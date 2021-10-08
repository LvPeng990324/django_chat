from django.views import View

from Chat.models import ChatUser

from utils.logger import logger
from utils.custom_reponse import response_200
from utils.custom_reponse import response_400


class CreateChatUser(View):
    """ 创建用户
    这个应该不用做user_sig验证，毕竟还没有创建ChatUser
    """
    def post(self, request):
        # 获取信息
        add_user_id = request.POST.get('user_id')
        add_name = request.POST.get('name')
        add_nickname = request.POST.get('nickname')
        add_username = request.POST.get('username')
        add_gender = request.POST.get('gender')
        add_birthday = request.POST.get('birthday')
        add_id_card_num = request.POST.get('id_card_num')
        add_phone = request.POST.get('phone')
        add_email = request.POST.get('email')
        add_province = request.POST.get('province')
        add_city = request.POST.get('city')
        add_avatar = request.POST.get('avatar')
        add_description = request.POST.get('description')

        # 非空检查
        if not add_user_id:
            return response_400(
                message='user_id不能为空',
            )

        # 创建用户
        new_chat_user = ChatUser.objects.create(
            user_id=add_user_id,
            name=add_name,
            nickname=add_nickname,
            username=add_username,
            gender=add_gender,
            birthday=add_birthday,
            id_card_num=add_id_card_num,
            phone=add_phone,
            email=add_email,
            province=add_province,
            city=add_city,
            avatar=add_avatar,
            description=add_description,
        )

        # 记录日志
        logger.success('{} 用户创建'.format(new_chat_user))

        # 返回用户信息
        return response_200(
            message='创建成功',
            data={
                'chat_user': new_chat_user.out_info(),
            },
        )


