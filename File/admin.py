from django.contrib import admin

from File.models import ChatFile


@admin.register(ChatFile)
class ChatFileInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'md5',
        'file',
        'create_time',
    )
