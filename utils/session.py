# 聊天会话相关方法
from django.db.models import Q
from typing import Optional

from Chat.models import ChatUser
from Chat.models import Session
from Chat.models import SessionTypeOption


def get_single_session_by_user_ids(user_id_list: [ChatUser.user_id]):
    """ 通过user_id获取单聊session
    找到了就返回session，没找到就返回None
    """
    # 判断给定的user_id_list是不是长度为2，不是的话直接返回None
    if len(user_id_list) != 2:
        return None

    # 先筛选第一个用户所有的单聊，再筛选包含第二个用户的
    try:
        session = Session.objects.filter(
            type=SessionTypeOption.SINGLE,  # 要是单聊的
            chat_users__user_id__contains=user_id_list[0]  # 要包含第一个用户的
        ).get(
            chat_users__user_id__contains=user_id_list[1]  # 再筛选包含第二个用户的
        )
    except Session.DoesNotExist:
        # 未找到，返回None
        return None

    return session


def get_or_create_single_session_by_user_ids(user_id_list: [ChatUser.user_id]) -> Session:
    """ 通过user_id获取或创建单聊session
    找到了就返回session，没找到就创建并返回新的session
    """
    # 判断是否找到
    session = get_single_session_by_user_ids(user_id_list=user_id_list)
    if session is not None:
        # 找到了，直接返回
        return session
    # 没找到，创建新的单聊会话
    new_session = Session.objects.create(
        name='未命名单聊',
        type=SessionTypeOption.SINGLE,
    )
    for user_id in user_id_list:  # 添加会话参与者
        new_session.chat_users.add(ChatUser.objects.get(user_id=user_id))
    # 返回新创建的session
    return new_session



