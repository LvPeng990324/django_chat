from django.views import View
import time
from django_redis import get_redis_connection
from django.core import signing
import random

from utils.custom_reponse import response_200
from utils.custom_reponse import response_403

from utils.get_md5 import get_md5
from utils.user_sig import gen_user_sig


userSigExpireTime = 500  # TODO user_sig过期时间，5秒，这里先设置为500，方便调试


class GetUserSig(View):
    """ 获取user_sig
    user_sig是用于登录聊天websocket接口的密钥，与user_id一一对应来验证
    也当作请求Token进行HTTP接口请求验证，可从中提取到ChatUser的user_id
    """
    def post(self, request):
        """ 通过自定规则生成的token来验证请求是否有效
        token生成规则：md5({user_id})
        """
        user_id = request.POST.get('user_id')
        token = request.POST.get('token')

        # 按照规则生成token
        token_raw = user_id
        token_correct = get_md5(data=token_raw)

        # 验证token
        if token != token_correct:
            # token不匹配，返回403
            return response_403(message='验证失败')
        # 验证通过了

        # 生成user_sig
        user_sig = gen_user_sig(user_id=user_id)

        # 记录user_id和user_sig对应关系在redis中
        redis_cli = get_redis_connection('userSig')
        redis_cli.setex(user_sig, userSigExpireTime, user_id)

        # 返回给前端
        return response_200(
            message='获取成功',
            data={
                'user_sig': user_sig,
            },
        )

