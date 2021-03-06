from django.urls import path

from Chat.apis.CreateChatUser import CreateChatUser
from Chat.apis.ChatUserInfo import ChatUserInfo
from Chat.apis.GetUserSig import GetUserSig
from Chat.apis.ChatLogInfo import ChatLogInfo
from Chat.apis.CreateSession import CreateSession
from Chat.apis.SessionInfo import SessionInfo
from Chat.apis.GetChatOnlineInfo import GetChatOnlineInfo
from Chat.apis.ChangeChatUserInfo import ChangeChatUserInfo
from Chat.apis.MarkAsRead import SingleChatMarkAsRead
from Chat.apis.UnreadCount import UnreadCount
from Chat.apis.ChatLogin import ChatLogin
from Chat.apis.ChatLogout import ChatLogout
from Chat.apis.SearchSession import SearchSession
from Chat.apis.MassMessage import MassMessage
from Chat.apis.SystemMessage import SystemMessage

app_name = 'Chat'

urlpatterns = [
    # 创建用户
    path('create-chat-user/', CreateChatUser.as_view(), name='create_chat_user'),
    # 用户信息
    path('chat-user-info/', ChatUserInfo.as_view(), name='chat_user_info'),
    # 获取user_sig
    path('get-user-sig/', GetUserSig.as_view(), name='get_user_sig'),
    # 聊天记录
    path('chat-log-info/', ChatLogInfo.as_view(), name='chat_log_info'),
    # 创建会话
    path('create-session/', CreateSession.as_view(), name='create_session'),
    # 会话信息
    path('session-info/', SessionInfo.as_view(), name='session_info'),
    # 获取聊天在线信息（目前仅调试用）
    path('get-chat-online-info/', GetChatOnlineInfo.as_view(), name='get_chat_online_info'),
    # 更改用户信息
    path('change-chat-user-info/', ChangeChatUserInfo.as_view(), name='change_chat_user_info'),
    # 单聊标记为已读
    path('single-chat-mark-as-read/', SingleChatMarkAsRead.as_view(), name='single_chat_mark_as_read'),
    # 获取用户未读消息数量
    path('unread-count/', UnreadCount.as_view(), name='unread_count'),
    # 聊天登录
    path('chat-login/', ChatLogin.as_view(), name='chat_login'),
    # 聊天登出
    path('chat-logout/', ChatLogout.as_view(), name='chat_logout'),
    # 搜索会话
    path('search-session/', SearchSession.as_view(), name='search_session'),
    # 群发消息
    path('mass-message/', MassMessage.as_view(), name='mass_message'),
    # 系统消息
    path('system-message/', SystemMessage.as_view(), name='system_message'),
]
