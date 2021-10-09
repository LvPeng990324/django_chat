from django.urls import path

from File.views.UploadChatFile import UploadChatFile

app_name = 'File'

urlpatterns = [
    path('upload-chat-file/', UploadChatFile.as_view(), name='upload_chat_file'),
]
