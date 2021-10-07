from django.contrib import admin

from Chat.models import ChatUser
from Chat.models import Session
from Chat.models import ChatLog


@admin.register(ChatUser)
class ChatUserInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'name',
        'is_disable',
        'is_delete',
        'login_time',
        'create_time',
    )


@admin.register(Session)
class SessionInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'create_time',
    )


@admin.register(ChatLog)
class ChatLogInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'get_sender_user_id',
        'have_read',
        'read_time',
        'create_time',
    )

    def get_sender_user_id(self, obj):
        return obj.sender.user_id
