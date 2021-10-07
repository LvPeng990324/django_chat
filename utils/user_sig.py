from django.core import signing
import random
from django_redis import get_redis_connection

from utils.custom_reponse import response_403


def gen_user_sig(user_id):
    """ 生成user_sig
    """
    # 将user_id封装进去，并加入随机数进行混淆，使用django自带的signing进行加密
    user_sig_raw = {
        'random_head': random.randint(1, 100),
        'user_id': user_id,
        'random_footer': random.randint(1, 100),
    }
    user_sig = signing.dumps(user_sig_raw)
    return user_sig


def get_user_id_from_user_sig(user_sig):
    """ 从user_sig中获取user_id
    """
    user_sig_raw = signing.loads(user_sig)
    user_id = user_sig_raw.get('user_id')
    return user_id


def get_user_id_from_headers(headers: dict):
    """ 从headers中获取user_id
    """
    user_sig = headers.get('UserSig')
    user_id = get_user_id_from_user_sig(user_sig=user_sig)
    return user_id


def check_user_sig(func):
    """ 检查user_sig
    """
    def wrapper(request, *args, **kwargs):
        # 获取userToken，在headers里叫Authorization
        user_sig_received = request.headers.get('UserSig', '')
        # 验证user_sig有效性
        redis_cli = get_redis_connection('userSig')
        if not redis_cli.get(user_sig_received):
            # 验证不通过，返回403状态码，message为登录已过期
            return response_403(
                message='user_sig无效',
            )
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper

