from django.views import View
from django.utils.decorators import method_decorator

from Chat.models import ChatUser

from utils.custom_reponse import response_200
from utils.custom_reponse import response_404
from utils.user_sig import check_user_sig
from utils.user_sig import get_user_id_from_headers
from utils.logger import logger


class ChangeChatUserInfo(View):
    """ 更改用户信息
    按需更改，如果字段是None就不改，否则就直接替换给过来的值
    """
    @method_decorator(check_user_sig)
    def post(self, request):
        # 获取信息
        change_name = request.POST.get('name')
        change_nickname = request.POST.get('nickname')
        change_username = request.POST.get('username')
        change_gender = request.POST.get('gender')
        change_birthday = request.POST.get('birthday')
        change_id_card_num = request.POST.get('id_card_num')
        change_phone = request.POST.get('phone')
        change_email = request.POST.get('email')
        change_province = request.POST.get('province')
        change_city = request.POST.get('city')
        change_avatar = request.POST.get('avatar')
        change_description = request.POST.get('description')
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

        # 按需更改
        if change_name is not None:
            chat_user.name = change_name
        if change_nickname is not None:
            chat_user.nickname = change_nickname
        if change_username is not None:
            chat_user.username = change_username
        if change_gender is not None:
            chat_user.gender = change_gender
        if change_birthday is not None:
            chat_user.birthday = change_birthday
        if change_id_card_num is not None:
            chat_user.id_card_num = change_id_card_num
        if change_phone is not None:
            chat_user.phone = change_phone
        if change_email is not None:
            chat_user.email = change_email
        if change_province is not None:
            chat_user.province = change_province
        if change_city is not None:
            chat_user.city = change_city
        if change_avatar is not None:
            chat_user.avatar = change_avatar
        if change_description is not None:
            chat_user.description = change_description

        chat_user.save()

        # 记录日志
        logger.info(f'更改了 {user_id} 的信息')

        # 返回成功回应
        return response_200(
            message='更改成功',
            data={
                'chat_user': chat_user.out_info(),
            }
        )



