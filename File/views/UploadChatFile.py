from django.views import View
from django.utils.decorators import method_decorator

from File.models import ChatFile

from utils.custom_reponse import response_200
from utils.custom_reponse import response_400
from utils.user_sig import check_user_sig
from utils.get_md5 import get_file_md5


class UploadChatFile(View):
    """ 上传聊天文件
    """
    # @method_decorator(check_user_sig)
    def post(self, request):
        """ 上传聊天文件
        """
        upload_file = request.FILES.get('file')

        # 文件筛选检查
        # 文件大小限制，限制20M以内
        file_size = upload_file.size / (1024*1024)  # 文件大小(M)
        if file_size > 20:
            # 大小超限，返回403
            return response_400(
                message='文件大小超限，20M以内',
            )

        # 计算文件md5
        file_md5 = get_file_md5(data=upload_file)

        # 记录文件信息并保存文件
        new_chat_file = ChatFile.objects.create(
            md5=file_md5,
            file=upload_file,
        )

        # 返回成功响应
        return response_200(
            message='上传成功',
            data={
                'chat_file': new_chat_file.out_info(),  # 新文件对外信息
            }
        )


